from dataclasses import dataclass
from dotenv import load_dotenv
from openai_backendtools import *
import time
import os
import datetime

load_dotenv()

# Global variables
# https://platform.openai.com/docs/assistants/tools/file-search/supported-files#supported-files
default_filetypes_accepted_by_vector_stores = ["c", "cpp", "cs", "css", "doc", "docx", "go", "html", "java", "js", "json", "md", "pdf", "php", "pptx", "py", "rb", "sh", "tex", "ts", "txt"]

default_assistant_instruction = """You are a helpful assistant that can search through files to answer questions about their content.

When referencing documents in the vector store, add a "Sources" section at the end of the answer. In this section, list the document name and the referenced page numbers. Like this: "[FILENAME] (page 93 - [user_topic])" or "[FILENAME] (pages 21, 45 - [user_topic])" or "[FILENAME] (pages 21 - 25, [user_topic])" Note: [user_topic] is the main topic of the citation (less than 6 words)
"""

# ----------------------------------------------------- START: Tests ----------------------------------------------------------

@dataclass
class VectorStoreFiles:
  vector_store: any
  files: any
  files_metadata: any
  files_data: any

def collect_files_from_folder_path(folder_path, include_subfolders=True, include_file_types=["*"]):
  """
  Recursively collect files from folder_path and return file information.
  
  Args:
    folder_path: Path to the folder to collect files from
    include_subfolders: Whether to include files from subdirectories (default: True)
    include_filetypes: List of file extensions to include (e.g., ["txt", "pdf", "docx"]) or ["*"] for all files (default: ["*"])
  
  Returns:
    tuple: (files, files_metadata, files_data) where:
      - files: list of file paths
      - files_metadata: dict with file metadata for upload (key=file_path)
      - files_data: dict with file data not for upload (key=file_path)
  """
  files = []; files_metadata = {}; files_data = {}
  
  # normalize folder path
  folder_path = os.path.abspath(folder_path) 
  if not os.path.exists(folder_path):
    raise Exception(f"File '{folder_path}' does not exist.")
  
  # Normalize file types for comparison (remove dots and convert to lowercase)
  normalized_filetypes = []
  include_all_files = "*" in include_file_types
  if not include_all_files:
    for filetype in include_file_types:
      normalized_type = filetype.lower().lstrip('.')
      normalized_filetypes.append(normalized_type)
  
  # Recursively walk through all subdirectories
  for root, dirs, filenames in os.walk(folder_path):
    # If include_subfolders is False, only process the root directory
    if not include_subfolders and root != folder_path: continue
      
    for filename in filenames:
      file_path = os.path.join(root, filename)
      if os.path.isfile(file_path):
        try:
          # Get file type from extension (handles multiple dots in filename)
          file_type = filename.split('.')[-1].lower() if '.' in filename else ''
          
          # Check if file type should be included
          if not include_all_files and file_type not in normalized_filetypes: continue
            
          # Extract year from file's last modification date
          mod_timestamp = os.path.getmtime(file_path)
          last_modified = datetime.datetime.fromtimestamp(mod_timestamp).strftime('%Y-%m-%d')
          file_size = os.path.getsize(file_path)
          # Store file source path and metadata
          files.append(file_path)
          files_metadata[file_path] = { 'source': file_path, 'filename': filename, 'file_type': file_type }
          files_data[file_path] = { 'file_size': file_size, 'last_modified': last_modified}
        except (PermissionError, OSError) as e:
          # Skip files that can't be accessed (lock files, permission issues, etc.)
          print(f"  Skipping inaccessible file: {filename}")
          continue
  
  return files, files_metadata, files_data


def build_test_vector_store_by_adding_collected_files(client, vector_store, files, files_metadata, files_data, log_headers=True) -> VectorStoreFiles:
  function_name = 'Update test vector store from collected files'
  start_time = log_function_header(function_name) if log_headers else datetime.datetime.now()

  # Upload RAG files
  max_retries = 1
  attempt = 0
  files_to_upload = files.copy()
  failed_files = []
  do_not_retry_files = []

  while attempt < max_retries:
    if attempt > 0:
      # Filter out non-retryable files and prepare for retry
      files_to_upload = [f for f in failed_files if f not in do_not_retry_files]
      if not files_to_upload:
        break
      failed_files = []
      print(f"\n  Retry attempt {attempt + 1} / {max_retries} for uploading {len(files_to_upload)} files...")
    else:
      print(f"  Uploading {len(files_to_upload)} files...")
    for idx, file_path in enumerate(files_to_upload, 1):
      # Step 1: Upload file, but only if not already uploaded
      file_id = files_data[file_path].get('file_id') if files_data[file_path] else None
      if not file_id:
        try:
          with open(file_path, 'rb') as f:
            try:
              vector_store_file = client.files.create(file=f, purpose="assistants")
              if vector_store_file.id:
                status = f"OK: Upload"
                files_data[file_path]['file_id'] = vector_store_file.id
              else:
                status = f"FAIL: Upload"
                failed_files.append(file_path)
            except Exception as e:
              status = f"FAIL: Upload '{file_path}' - {str(e)}"
              failed_files.append(file_path)
        except (PermissionError, OSError) as e:
          # Skip files that can't be opened (lock files, permission issues, etc.)
          status = f"SKIPPED: Cannot access file - {os.path.basename(file_path)}"
          # Don't add to failed_files since this is expected for inaccessible files
      else:
        status = f"OK: Upload (skipped)"

      # Step 2: Add file to vector store
      file_id = files_data[file_path].get('file_id') if files_data[file_path] else None
      if file_id:
        try:
          metadata = files_metadata[file_path]
          retVal = client.vector_stores.files.create(vector_store_id=vector_store.id, file_id=file_id, attributes=metadata)
          status += f", OK: Add to vector store ID={file_id} '{file_path}'"
        except Exception as e:
          # Error code: 400 - File type not supported; Error = 'unsupported_file'; do not retry
          if e.status_code == 400 and e.code == 'unsupported_file':
            do_not_retry_files.append(file_path)
          status += f", FAIL: Add to vector store ID={file_id} '{file_path}' - {str(e)}"
          failed_files.append(file_path)
      print(f"    [ {idx} / {len(files_to_upload)} ] {status}")

    # Try to delete files globally that are marked as not retryable
    for file_path in do_not_retry_files:
      file_id = files_data[file_path].get('file_id') if files_data[file_path] else None
      if file_id:
        try: client.files.delete(file_id=file_id)
        except Exception as e: pass
    
    # Ensure all files in the vector store are of status 'completed'
    # Otherwise delete them from vector store and add them to failed files
    print(f"  Verifying all vector store files are 'completed'...")
    
    # Calculate max wait time and max status checks:
    # for < 11 files -> 10 checks with 3 secs; for > 10 files -> 15 checks with 10 secs; for > 100 files -> 20 checks with 20 secs
    max_status_checks, wait_time = (10, 3) if len(files_to_upload) < 11 else (15, 10) if len(files_to_upload) <= 100 else (20, 20)
    # Exception: if HTML files are uploaded, adjust wait parameters based on HTML file count and size
    # Reason: Large HTML files take much longer to process
    html_files = [f for f in files_to_upload if f.lower().endswith('.html')]
    if html_files:
        html_count = len(html_files)
        total_size_mb = sum(os.path.getsize(f) / (1024 * 1024) for f in html_files)
        # Adjust max checks based on file count and size: at least number of HTML files, plus extra time for larger files
        max_status_checks = max(max_status_checks, html_count + int(total_size_mb / 5))  # Add 1 check per 5MB
        wait_time = max(wait_time, 10)  # Ensure at least 10 seconds wait for HTML files

    status_check = 0; in_progress_files_count=0
    while status_check < max_status_checks:
      temp_vector_store = client.vector_stores.retrieve(vector_store.id)
      in_progress_files_count = temp_vector_store.file_counts.in_progress
      if in_progress_files_count == 0: break
      print(f"    Waiting {wait_time} seconds ( {status_check + 1} / {max_status_checks} ) for {in_progress_files_count} files to complete...")
      time.sleep(wait_time)
      status_check += 1

    vector_store_files = get_vector_store_files(client, vector_store)
    for vector_store_file in vector_store_files:
      if vector_store_file.status != 'completed' and vector_store_file.status != 'in_progress':
        file_id = vector_store_file.id
        file_status = getattr(vector_store_file,"status","[UNKNOWN]")
        error_msg = "UNKNOWN" if vector_store_file.last_error is None else vector_store_file.last_error.message
        # Find file data by searching through files_data
        file_path = None; file_size = None
        for path, data in files_data.items():
            if data.get('file_id') == file_id:
              file_path = path; file_size = data.get('file_size');
              break        
        print(f"    WARNING: '{error_msg}' - status: '{file_status}', id: {file_id}, file_path: '{file_path}', size: {format_filesize(file_size)}.")
        # delete file from vector store
        client.vector_stores.files.delete(vector_store_id=vector_store.id, file_id=file_id)

        if file_path:
          failed_files.append(file_path)
          
    attempt += 1

  # Remove failed files from files data
  if len(failed_files) > 0:
    print(f"  WARNING: {len(failed_files)} files could not be added to vector store. Deleting them...")
    for idx, file_path in enumerate(failed_files, 1):
      file_id = files_data[file_path].get('file_id') if files_data[file_path] else None
      print(f"    [ {idx} / {len(failed_files)} ] ID={file_id} '{file_path}'")    
      # Delete file from vector store and from global file storage
      if file_id:
        try: client.vector_stores.files.delete(vector_store_id=vector_store.id, file_id=file_id)
        except Exception as e: pass
        try: client.files.delete(file_id=file_id)
        except Exception as e: pass
      del files_data[file_path]
      del files_metadata[file_path]
      del files[files.index(file_path)]

  log_function_footer(function_name, start_time)
  return VectorStoreFiles(vector_store, files, files_metadata, files_data)

def create_test_vector_store_from_collected_files(client, vector_store_name, files, files_metadata, files_data, log_headers=True, chunk_size=800, chunk_overlap=400) -> VectorStoreFiles:
  function_name = 'Create test vector store from collected files'
  start_time = log_function_header(function_name) if log_headers else datetime.datetime.now()

  # Create vector store with chunking strategy
  print(f"  Creating vector store '{vector_store_name}' with chunk_size={chunk_size}, chunk_overlap={chunk_overlap}...")
  chunking_strategy = {
    "type": "static",
    "static": {
      "max_chunk_size_tokens": chunk_size,
      "chunk_overlap_tokens": chunk_overlap
    }
  }
  vector_store = client.vector_stores.create(name=vector_store_name, chunking_strategy=chunking_strategy)
  print(f"    OK. ID={vector_store.id}") if vector_store.id else print("  FAIL.")

  vector_store_with_files = build_test_vector_store_by_adding_collected_files(client, vector_store, files, files_metadata, files_data, False)

  if log_headers: log_function_footer(function_name, start_time)
  return vector_store_with_files

# Creates a vector store and uploads files from the given folder recursively
def create_test_vector_store_from_folder_path(client, vector_store_name, folder_path, include_subfolders=True, include_file_types=["*"], chunk_size=800, chunk_overlap=400) -> VectorStoreFiles:
  function_name = 'Create test vector store from folder path'
  start_time = log_function_header(function_name)
  files, files_metadata, files_data = collect_files_from_folder_path(folder_path, include_subfolders=include_subfolders, include_file_types=include_file_types)
  test_vector_store_with_files = create_test_vector_store_from_collected_files(client, vector_store_name, files, files_metadata, files_data, False, chunk_size, chunk_overlap)
  log_function_footer(function_name, start_time)
  return test_vector_store_with_files



def test_rag_operations_using_responses_api(client, vector_store_id, openai_model_name, query, truncate_output=True):
  function_name = 'RAG operations using responses API'
  start_time = log_function_header(function_name)

  # Ask question
  print("-"*140)
  print(f"  Test query with 'file_search' tool: {query}")

  request_params = {
    "model": openai_model_name,
    "input": query,
    "tools": [{ "type": "file_search", "vector_store_ids": [vector_store_id] }],
    "temperature": 0
  }
  
  # Remove temperature parameter for reasoning models that don't support it
  remove_temperature_from_request_params_for_reasoning_models(request_params, openai_model_name, reasoning_effort="low")
  
  response = retry_on_openai_errors(lambda: client.responses.create(**request_params), indentation=4)
  model_output = ("\n" + response.output_text) if not truncate_output else truncate_string(response.output_text.replace("\n", " ") ,80)
  print(f"    Response: {model_output}")
  print(f"    status='{response.status}', tool_choice='{response.tool_choice}', input_tokens={response.usage.input_tokens}, output_tokens={response.usage.output_tokens}")
  # search for tool call of type 'file_search_call' in response.output
  response_file_search_tool_call = next((item for item in response.output if item.type == 'file_search_call'), None)
  response_file_search_results = response_file_search_tool_call.results
  if response_file_search_tool_call: print(f"    File search tool call status: '{response_file_search_tool_call.status}', results: {len(response_file_search_results) if response_file_search_results else 'N/A'}")

  print(f"  Test query with 'file_search' tool with 'file_search_call.results': {query}")
  request_params = {
    "model": openai_model_name,
    "input": query,
    "tools": [{ "type": "file_search", "vector_store_ids": [vector_store_id] }],
    "include": ["file_search_call.results"],
    "temperature": 0
  }
  
  # Remove temperature parameter for reasoning models that don't support it
  remove_temperature_from_request_params_for_reasoning_models(request_params, openai_model_name, reasoning_effort="low")
  
  response = retry_on_openai_errors(lambda: client.responses.create(**request_params), indentation=4)
  model_output = ("\n" + response.output_text) if not truncate_output else truncate_string(response.output_text.replace("\n", " ") ,80)
  print(f"    Response: {model_output}")
  print(f"    status='{response.status}', tool_choice='{response.tool_choice}', input_tokens={response.usage.input_tokens}, output_tokens={response.usage.output_tokens}")
  # search for tool call of type 'file_search_call' in response.output
  response_file_search_tool_call = next((item for item in response.output if item.type == 'file_search_call'), None)
  response_file_search_results = response_file_search_tool_call.results
  if response_file_search_tool_call: print(f"    File search tool call status: '{response_file_search_tool_call.status}', results: {len(response_file_search_results) if response_file_search_results else 'N/A'}")
  lines = format_search_results_table(response_file_search_results)
  print("    " + lines.replace("\n","\n    "))

  log_function_footer(function_name, start_time)

def test_rag_operations_using_assistants_api(client, assistant_id, query, truncate_output=True):
  function_name = 'RAG operations using assistants API'
  start_time = log_function_header(function_name)

  # Ask question
  print("-"*140)
  print(f"  Test query with 'assistant' tool: {query}")

  # Get answer from assistant
  answer = get_assistant_answer(client, assistant_id, query)
  
  # Display the answer
  model_output = ("\n" + answer) if not truncate_output else truncate_string(answer.replace("\n", " "), 80)
  print(f"    Response: {model_output}")

  log_function_footer(function_name, start_time)
  
  return answer


# retrives the chunks for each file and writes the chunks to console
def test_vector_store_files_content_retrieval(client, vector_store_id):
  function_name = 'File content retrieval from vector store'
  start_time = log_function_header(function_name)
  
  print(f"  Retrieving all files and chunks from vector store '{vector_store_id}'...")
  file_contents = get_all_vector_store_file_contents(client, vector_store_id)
  print(f"    OK: {len(file_contents)} file(s)")
  
  # Display formatted table
  lines = format_vector_store_file_content_table(file_contents)
  print("    " + lines.replace("\n","\n    "))
  
  log_function_footer(function_name, start_time)



# ----------------------------------------------------- END: Tests ------------------------------------------------------------

# ----------------------------------------------------- START: Main -----------------------------------------------------------

if __name__ == '__main__':
  openai_service_type = os.getenv("OPENAI_SERVICE_TYPE", "openai")
  if openai_service_type == "openai":
    openai_model_name = "gpt-5-nano"
    client = create_openai_client()
  elif openai_service_type == "azure_openai":
    openai_model_name = os.getenv("AZURE_OPENAI_MODEL_DEPLOYMENT_NAME", "gpt-4o-mini")
    azure_openai_use_key_authentication = os.getenv("AZURE_OPENAI_USE_KEY_AUTHENTICATION", "false").lower() in ['true']
    client = create_azure_openai_client(azure_openai_use_key_authentication)

  @dataclass
  class RAGParams: vector_store_name: str; folder_path: str; query: str; use_existing_vector_store: bool; create_assistant: bool; truncate_output: bool; chunk_size: int; chunk_overlap: int; create_assistant: bool; assistant_name: str; assistant_instructions: str; assistant_model: str; assistant_temperature: float; delete_vector_store_after_run: bool; delete_assistant_after_run: bool

  params = RAGParams(
    vector_store_name="test_vector_store"
    ,folder_path="./RAGFiles/Batch01"
    ,query="Who is Arilena Drovik?"
    ,use_existing_vector_store=False
    ,truncate_output=True
    ,chunk_size=4096
    ,chunk_overlap=2048
    ,create_assistant=False
    ,assistant_name="Test RAG Assistant"
    ,assistant_instructions=default_assistant_instruction
    ,assistant_model="gpt-4o-mini"
    ,assistant_temperature=0
    ,delete_vector_store_after_run=True
    ,delete_assistant_after_run=True
  )

  # delete_vector_store_by_name(client, params.vector_store_name, True)
  # delete_vector_store_by_id(client, "vs_6922fa4676748191bc426a115ed8e2ab", True)
  # delete_assistant_by_name(client, params.assistant_name)

  # Step 1: Create vector store by uploading files or get existing vector store
  vs = None
  if params.use_existing_vector_store:
    vs = get_vector_store_by_name(client, params.vector_store_name)
  else:
    test_vector_store_with_files = create_test_vector_store_from_folder_path(client, params.vector_store_name, params.folder_path, chunk_size=params.chunk_size, chunk_overlap=params.chunk_overlap)
    vs = test_vector_store_with_files.vector_store
    print(f"Vector store created: '{vs.id}'")

  assistant = None
  if params.create_assistant:
    vs_id = vs.id if vs else ""
    assistant = create_assistant(client, params.assistant_name, params.assistant_instructions, vs_id, params.assistant_model, params.assistant_temperature)
    print(f"Assistant created: '{assistant.id}'")

  # Step 2: Test file RAG functionalities
  test_rag_operations_using_responses_api(client, vs.id, openai_model_name, params.query, params.truncate_output)

  print("-"*140)

  if assistant:
    test_rag_operations_using_assistants_api(client, assistant.id, params.query, params.truncate_output)

  # Step 3: Test file chunk retrieval
  test_vector_store_files_content_retrieval(client, vs.id)
  
  print("-"*140)

  # Step 4: Delete vector store including all files
  if params.delete_vector_store_after_run and vs:
    delete_vector_store_by_id(client, vs.id, True)
  
  # Step 5: Delete assistant
  if params.delete_assistant_after_run and assistant:
    delete_assistant_by_id(client, assistant.id)

# ----------------------------------------------------- END: Main -------------------------------------------------------------
