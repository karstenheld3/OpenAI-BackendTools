from dotenv import load_dotenv
from openai_backendtools import *
import time
import json
import os
import datetime

load_dotenv()

# ----------------------------------------------------- START: Tests ----------------------------------------------------------

class TestVectorStoreWithFiles:
  def __init__(self, vector_store, files, files_metadata, files_data):
    self.vector_store = vector_store
    self.files = files
    self.files_metadata = files_metadata
    self.files_data = files_data

# Retries the given function on rate limit errors
def retry_on_openai_errors(fn, indentation=0, retries=5, backoff_seconds=10):
  for attempt in range(retries):
    try:
      return fn()
    except Exception as e:
      # Only retry on rate limit errors
      if not (hasattr(e, 'type') and e.type == 'rate_limit_error'):
        raise e
      if attempt == retries - 1:  # Last attempt
        raise e
      print(f"{' '*indentation}Rate limit reached, retrying in {backoff_seconds} seconds... (attempt {attempt + 2} of {retries})")
      time.sleep(backoff_seconds)

def truncate_string(string, max_length):
  if len(string) > max_length:
    return string[:max_length] + "..."
  return string

def create_test_vector_store_with_files(client, vector_store_name, folder_path):
  function_name = 'Create test vector store with files'
  start_time = log_function_header(function_name)

  # Create vector store
  print(f"  Creating vector store '{vector_store_name}'...")
  vector_store = client.vector_stores.create(name=vector_store_name)
  print(f"    OK. ID={vector_store.id}") if vector_store.id else print("  FAIL.")


  # Load RAG files and store
  # file source paths in list 'files' 
  # metadata to be uploaded in dict 'files_metadata' with key=file_path
  # metadata to not be uploaded in dict 'files_data' with key=file_path
  files = []; files_metadata = {}; files_data = {};
  # normalize folder path
  folder_path = os.path.abspath(folder_path)
  if not os.path.exists(folder_path):
    raise Exception(f"File '{folder_path}' does not exist.")
  else:
    for filename in os.listdir(folder_path):
      file_path = os.path.join(folder_path, filename)
      if os.path.isfile(file_path):
        # Extract year from file's last modification date
        mod_timestamp = os.path.getmtime(file_path)
        file_last_modified_date = datetime.datetime.fromtimestamp(mod_timestamp).strftime('%Y-%m-%d')
        # Get file type from extension (handles multiple dots in filename)
        file_type = filename.split('.')[-1] if '.' in filename else ''
        file_size = os.path.getsize(file_path)
        # Store file source path and metadata
        files.append(file_path)
        files_metadata[file_path] = { 'source': file_path, 'filename': filename, 'file_type': file_type }
        files_data[file_path] = { 'file_size': file_size, 'file_last_modified_date': file_last_modified_date}
  

  # Upload RAG files
  files_to_upload = files.copy(); failed_files = []; do_not_retry_files = []

  print(f"  Uploading {len(files_to_upload)} files...")
  for idx, file_path in enumerate(files_to_upload, 1):
    # Step 1: Upload file, but only if not already uploaded
    file_id = files_data[file_path].get('file_id') if files_data[file_path] else None
    if not file_id:    
      with open(file_path, 'rb') as f:
        try:
          file = client.files.create(file=f, purpose="assistants")
          if file.id:
            status = f"OK: Upload"
            files_data[file_path]['file_id'] = file.id
          else:
            status = f"FAIL: Upload"
            failed_files.append(file_path)
        except Exception as e:
          status = f"FAIL: Upload '{file_path}' - {str(e)}"
          failed_files.append(file_path)

    # Step 2: Add file to vector store
    file_id = files_data[file_path]['file_id']
    if file_id:
      try:
        retVal = client.vector_stores.files.create(vector_store_id=vector_store.id, file_id=file_id)
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
    try: client.files.delete(file_id=files_data[file_path]['file_id'])
    except Exception as e: pass
  
  # Ensure all files in the vector store are of status 'completed'; otherwise add them to failed files
  vector_store_files = get_vector_store_files(client, vector_store)
  for file in vector_store_files:
    if file.status != 'completed':
      file_id = file.id
      # delete file from vector store
      client.vector_stores.files.delete(vector_store_id=vector_store.id, file_id=file_id)
      # find file path from files_data
      file_path = next((path for path, data in files_data.items() if data['file_id'] == file_id), None)
      if file_path:
        failed_files.append(file_path)


  # Remove failed files from files data
  for file_path in failed_files:
    del files_data[file_path]
    del files_metadata[file_path]
    del files[files.index(file_path)]

  log_function_footer(function_name, start_time)
  return TestVectorStoreWithFiles(vector_store, files, files_metadata, files_data)

def test_rag_operations_using_responses_api(client, test_vector_store_with_files, openai_model_name):
  function_name = 'RAG operations using responses API'
  start_time = log_function_header(function_name)

  vector_store_id = test_vector_store_with_files.vector_store.id

  # Ask question
  query = "Who is Arilena Drovik?";
  print("-"*140)
  print(f"  Testing query with 'file_search' tool: {query}")

  response = retry_on_openai_errors(lambda: client.responses.create(
    model=openai_model_name
    ,input=query
    ,tools=[{ "type": "file_search", "vector_store_ids": [vector_store_id] }]
  ), indentation=4)
  print(f"    Response: {truncate_string(response.output_text,80)}")
  print(f"    status='{response.status}', tool_choice='{response.tool_choice}', input_tokens={response.usage.input_tokens}, output_tokens={response.usage.output_tokens}")
  # search for tool call of type 'file_search_call' in response.output
  response_file_search_tool_call = next((item for item in response.output if item.type == 'file_search_call'), None)
  if response_file_search_tool_call: print(f"    File search tool call status: '{response_file_search_tool_call.status}'")


  print(f"  Testing query with 'file_search' tool with 'file_search_call.results': {query}")
  response = retry_on_openai_errors(lambda: client.responses.create(
    model=openai_model_name
    ,input=query
    ,tools=[{ "type": "file_search", "vector_store_ids": [vector_store_id] }]
    ,include=["file_search_call.results"]
  ), indentation=4)
  print(f"    Response: {truncate_string(response.output_text,80)}")
  print(f"    status='{response.status}', tool_choice='{response.tool_choice}', input_tokens={response.usage.input_tokens}, output_tokens={response.usage.output_tokens}")
  # search for tool call of type 'file_search_call' in response.output
  response_file_search_tool_call = next((item for item in response.output if item.type == 'file_search_call'), None)
  if response_file_search_tool_call: print(f"    File search tool call status: '{response_file_search_tool_call.status}'")
  # search for 'file_search_call.results' in response.output
  response_file_search_results = response_file_search_tool_call.results
  lines = format_files_table(response_file_search_results)
  print("    " + lines.replace("\n","\n    "))

  log_function_footer(function_name, start_time)


# ----------------------------------------------------- END: Tests ------------------------------------------------------------

# ----------------------------------------------------- START: Main -----------------------------------------------------------

if __name__ == '__main__':
  openai_service_type = os.getenv("OPENAI_SERVICE_TYPE", "openai")
  azure_openai_use_key_authentication = os.getenv("AZURE_OPENAI_USE_KEY_AUTHENTICATION", "false").lower() in ['true']

  if openai_service_type == "openai":
    client = create_openai_client()
  elif openai_service_type == "azure_openai":
    client = create_azure_openai_client(azure_openai_use_key_authentication)


  # In Azure, the model name is the deployment name
  openai_model_name = os.getenv("AZURE_OPENAI_MODEL_DEPLOYMENT_NAME", "gpt-4o-mini")
  test_vector_store_name = "test_vector_store"

  delete_vector_store_by_name(client, test_vector_store_name, True)

  # Step 1: Create vector store by uploading files
  test_vector_store_with_files = create_test_vector_store_with_files(client,test_vector_store_name,"./RAGFiles/Batch02")

  # Step 2: Test file RAG functionalities
  # test_rag_operations_using_responses_api(client, test_vector_store_with_files, openai_model_name)

  print("-"*140)

  # Step 3: Delete vector store including all files
  delete_vector_store_by_name(client, test_vector_store_name, True)

# ----------------------------------------------------- END: Main -------------------------------------------------------------

