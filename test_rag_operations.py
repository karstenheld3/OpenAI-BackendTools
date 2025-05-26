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


def create_test_vector_store_with_files(client, vector_store_name, folder_path):
  function_name = 'Create test vector store with files'
  start_time = log_function_header(function_name)

  # Load RAG files and store
  # file source paths in list 'files' 
  # metadata to be uploaded in dict 'files_metadata' with key=file_path
  # metadata to not be uploaded in dict 'files_data' with key=file_path
  files = []; files_metadata = {}; files_data = {}; 
  if not os.path.exists(folder_path):
    raise Exception(f"File '{folder_path}' does not exist.")
  else:
    for filename in os.listdir(folder_path):
      file_path = os.path.join(folder_path, filename)
      if os.path.isfile(file_path):
        # Extract year from file's last modification date
        mod_timestamp = os.path.getmtime(file_path)
        file_year = str(datetime.datetime.fromtimestamp(mod_timestamp).year)
        file_last_modified_date = datetime.datetime.fromtimestamp(mod_timestamp).strftime('%Y-%m-%d')
        # Get file type from extension (handles multiple dots in filename)
        file_type = filename.split('.')[-1] if '.' in filename else ''
        file_size = os.path.getsize(file_path)
        # Store file source path and metadata
        files.append(file_path)
        files_metadata[file_path] = { 'source': file_path, 'filename': filename, 'file_year': file_year, 'file_type': file_type }
        files_data[file_path] = { 'file_size': file_size, 'file_last_modified_date': file_last_modified_date }
  
  # Upload RAG files
  total_files = len(files)
  print(f"  Uploading {total_files} files...")
  for idx, file_path in enumerate(files, 1):
    with open(file_path, 'rb') as f:
      file = client.files.create(file=f, purpose="assistants")
    status = "OK" if file.id else "FAIL"
    print(f"    [ {idx} / {total_files} ] {status}: ID={file.id} '{file_path}'")
    files_data[file_path]['file_id'] = file.id

  # Create vector store
  print(f"  Creating vector store '{vector_store_name}'...")
  vs = client.vector_stores.create(name=vector_store_name)
  print(f"    OK. ID={vs.id}") if vs.id else print("  FAIL.")

  # Add files to vector store
  failed_files = []
  print(f"  Adding files to vector store '{vector_store_name}'...")
  for idx, file_path in enumerate(files, 1):
    file_id = files_data[file_path]['file_id']
    try:
      client.vector_stores.files.create(vector_store_id=vs.id, file_id=file_id)
      print(f"    [ {idx} / {total_files} ] OK: ID={file_id} '{file_path}'")
    except Exception as e:
      print(f"    [ {idx} / {total_files} ] FAIL: '{file_path}' - {str(e)}")
      # add this file to failed files
      failed_files.append(file_path)
  
  # Remove failed files from files data
  for file_path in failed_files:
    del files_data[file_path]
    del files_metadata[file_path]
    del files[files.index(file_path)]
    total_files -= 1

  log_function_footer(function_name, start_time)
  return TestVectorStoreWithFiles(vs, files, files_metadata, files_data)

def extract_and_add_metadata_to_vector_store(client, test_vector_store_with_files, logExtractedMetadata=False):
  function_name = 'Extract and add metadata to vector store'
  start_time = log_function_header(function_name)

  prompt_template = """
  ## Task
  Extract the following tags for the uploaded document and return them as JSON.

  Example answer format:
  {
    "title": "<document_title>"
    ,"description": "<document_description>"
    ,"doc_type": "<document_type>"
    ,"doc_language": "<document_language>"
    ,"doc_author": "<document_author>"
    ,"doc_year": "<document_doc_year>"
    ,"doc_start_date": "<document_doc_start_date>"
    ,"doc_end_date": "<document_doc_end_date>"
  }

  Here is some information about the file:
  - filename: '<filename>'
  - file_last_modified_date: <file_last_modified_date>
  - source: '<source>'

  **Rules**:
  - Return the requested value as plain text. No additional explanantion, description, or thoughts. No surrounding quotes. No markdown formatting.
  - If the information cannot be extracted or the information type is not applicable, use an empty value.
  - Supress citations in the returned text (Incorrect: 'ABC 【29:0†source】', correct: 'ABC').
  - Translate all non-english texts to english. **IMPORTANT:** Use only latin characters (Incorrect: 'ČEZ', Correct 'CEZ'). Avoid all-caps texts (convert them to standard spelling).

  ### title
  What is the document's title?
  Return an answer with less than 256 characters.
  If the document is a about an organization, company, or person, insert the name at the start if it's not explicitly mentioned in the title.
  For companies, spell the names without the legal form suffix ('Siemens' instead of 'Siemens AG', 'Edison' instead of 'Edison S.p.A.').
  If the document does not have a title, try to extract the title from the filename.

  ### description
  What is the document's description?
  Return an answer with less than 256 characters. Don't replicate the documents title.
  Example: 'Insights on world demographics since the 1950s. Focus on Africa and Asia.'

  ### doc_type
  What is the document's type? Use semantic analysis to determine the type.
  Return an answer with less than 30 characters.
  Examples: 'Financial report', ''Market research', 'Invoice', 'Letter', 'Memo', 'Minutes', 'Newsletter', 'Press release', 'Report', 'Speech', 'Survey', 'White paper'

  ### doc_language
  What is the document's language? Return only one language.
  Examples: 'German', 'English', 'Arabic', 'Chinese'

  ### doc_author
  Who is the author of the document? Search on the first few pages. If there are many authors, return a comma-separated list (see examples).
  Return an answer with less than 256 characters.
  Examples: 'Microsoft', 'Greenpeace', 'John Doe', 'M. Zhang, F. Xi'.

  ### doc_year
  What is the year that the document covers? If the document covers multiple years, return the most recent year.
  If the date can't be extracted, use the year from the file_last_modified_date.
  Return an answer in exactly 4 characters.
  Examples: '1981', '2022', '2022'

  ### doc_start_date
  What is the document's data or reporting start date? If the date can't be extracted, return an empty string.
  Return an answer in exactly 10 characters as ISO-Date or an empty string.
  Examples: '1981-01-01', '2022-09-01', '2022-12-31', ''

  ### doc_end_date
  What is the document's data or reporting end date? If the date can't be extracted, use the file_last_modified_date.
  Return an answer in exactly 10 characters as ISO-Date.
  Examples: '1981-01-01', '2022-09-01', '2022-12-31'
  """
  
  # Create assistant for metadata extraction
  assistant = client.beta.assistants.create(
    name="test_assistant",
    instructions="You are a metadata extraction assistant, returning extracted tags from documents as JSON.",
    model="gpt-4o-mini",
    tools=[{"type": "file_search"}],
    tool_resources={"file_search": {"vector_store_ids": [test_vector_store_with_files.vector_store.id]}},
  )
  
  # Extract metadata for each file
  total_files = len(test_vector_store_with_files.files)
  print(f"  Extracting metadata for {total_files} files...")
  for idx, file_path in enumerate(test_vector_store_with_files.files, 1):
    file_id = test_vector_store_with_files.files_data[file_path]['file_id']
    file_last_modified_date = test_vector_store_with_files.files_data[file_path]['file_last_modified_date']
    source = test_vector_store_with_files.files_metadata[file_path]['source']
    filename = test_vector_store_with_files.files_metadata[file_path]['filename']

    print(f"    [ {idx} / {total_files} ] Extracting metadata for '{file_path}'...")

    prompt = prompt_template.replace("<filename>", filename).replace("<file_last_modified_date>", file_last_modified_date).replace("<source>", source)
    
    # Run the assistant on the thread with retries
    max_attempts = 5
    attempt = 1
    while attempt <= max_attempts:
      try:
        # Create a thread for metadata extraction
        thread = client.beta.threads.create()
        
        # Create message with file content and metadata
        client.beta.threads.messages.create(
          thread_id=thread.id,
          role="user",
          content=prompt,
          attachments=[{ "file_id": file_id, "tools": [{"type": "file_search"}] }]
        )
        run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)
        
        # Wait for the run to complete
        while True:
          run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
          if run_status.status == 'completed':
            break
          elif run_status.status == 'failed':
            # delete thread
            client.beta.threads.delete(thread_id=thread.id)
            raise Exception(f"Run failed: {run_status.last_error.message if hasattr(run_status, 'last_error') else 'Unknown error'}")
          time.sleep(1)
        
        # If we get here, the run completed successfully
        break
        
      except Exception as e:
        if attempt == max_attempts:
          raise Exception(f"Assistant run failed after {max_attempts} attempts: {str(e)}")
        print(f"      Attempt {attempt} / {max_attempts} failed, retrying...")
        attempt += 1
        time.sleep(10)  # Wait before retry
    
    # Get the assistant's response
    messages = client.beta.threads.messages.list( thread_id=thread.id )
    
    # Get the latest assistant message
    assistant_message = next(msg for msg in messages if msg.role == 'assistant')
    extracted_metadata_string = assistant_message.content[0].text.value
    # remove ```json and ```
    extracted_metadata_string = extracted_metadata_string.replace("```json", "").replace("```", "")
    if logExtractedMetadata:
      print("-"*140)
      print(f"{extracted_metadata_string}")
      print("-"*140)
    try:
      extracted_metadata = json.loads(extracted_metadata_string)
      test_vector_store_with_files.files_metadata[file_path].update(extracted_metadata)
      # Get non-empty values from metadata
      non_empty_values = [value for value in extracted_metadata.values() if value]
      print(f"      OK: {len(non_empty_values)} of {len(extracted_metadata.keys())} values extracted for file '{file_path}'")
    except:
      print(f"      FAIL: Metadata extraction returned invalid JSON for file '{file_path}'")
      continue

    # delete thread
    client.beta.threads.delete(thread.id)

  # Delete assistant
  client.beta.assistants.delete(assistant.id)

  # Add extracted metadata to files in vector store
  print(f"  Re-adding files to vector store with metadata...")
  for idx, file_path in enumerate(test_vector_store_with_files.files, 1):
    file_id = test_vector_store_with_files.files_data[file_path]['file_id']
    file_metadata = test_vector_store_with_files.files_metadata[file_path]
    # calculate metadata tags - count total fields
    file_metadata_count = len(file_metadata.keys())

    try:
      # first remove the file from the vector store
      client.vector_stores.files.delete( vector_store_id=test_vector_store_with_files.vector_store.id, file_id=file_id )
      # then add the file back with the updated metadata
      client.vector_stores.files.create( vector_store_id=test_vector_store_with_files.vector_store.id, file_id=file_id, attributes=file_metadata )
      print(f"    [ {idx} / {total_files} ] OK: ID={file_id} with {file_metadata_count} attributes '{file_path}'")
    except Exception as e:
      print(f"    [ {idx} / {total_files} ] FAIL: '{file_path}' - {str(e)}")

  # make sure all files in the vector store have status 'processed' and delete those that don't
  print(f"  Ensuring all files in the vector store have status='completed'...")
  files = get_vector_store_files(client, test_vector_store_with_files.vector_store)
  for file in files:
    if file.status != 'completed':
      print(f"    Deleting file '{file.id}' with status '{file.status}'")
      client.vector_stores.files.delete( vector_store_id=test_vector_store_with_files.vector_store.id, file_id=file.id )
  
  log_function_footer(function_name, start_time)


def test_file_search_functionalities(client, test_vector_store_with_files):
  function_name = 'File search functionalities (RAG search, filter, rewrite query)'
  start_time = log_function_header(function_name)

  # Search for files using query
  # https://cookbook.openai.com/examples/file_search_responses#standalone-vector-search

  query = "Who is Arilena Drovik?"; score_threshold = 0.3; max_num_results = 10
  print("-"*140)
  print(f"  Testing query search (score_threshold={str(score_threshold)}, max_num_results={max_num_results}): {query}")
  search_results = client.vector_stores.search(
    vector_store_id=test_vector_store_with_files.vector_store.id,
    query=query,
    ranking_options={"ranker": "auto", "score_threshold": score_threshold},
    max_num_results=max_num_results
  )
  # sort by score
  search_results.data.sort(key=lambda x: x.score, reverse=True)
  print(f"    {len(search_results.data)} search results")
  table = ("    " + format_search_results_table(search_results.data)).replace("\n","\n    ")
  print(table)

  # Search for files using filter
  query = "Who is Arilena Drovik?"; score_threshold = 0.3; max_num_results = 10
  filters = { "key": "file_type", "type": "eq", "value": "md" }
  print("-"*140)
  print(f"  Testing filtered query search (filter: {filters['key']}='{filters['value']}', score_threshold={str(score_threshold)}, max_num_results={max_num_results}): {query}")
  search_results = client.vector_stores.search(
    vector_store_id=test_vector_store_with_files.vector_store.id,
    query=query,
    ranking_options={"ranker": "auto", "score_threshold": score_threshold},
    max_num_results=max_num_results,
    filters=filters
  )
  print(f"    {len(search_results.data)} search results")
  table = ("    " + format_search_results_table(search_results.data)).replace("\n","\n    ")
  print(table)

  # Search for files using rewrite-query
  query = "All files with file_type='md'."; score_threshold = 0.3; max_num_results = 10
  print("-"*140)
  print(f"  Testing rewrite query search (score_threshold={str(score_threshold)}, max_num_results={max_num_results}): {query}")
  search_results = client.vector_stores.search(
    vector_store_id=test_vector_store_with_files.vector_store.id,
    query=query,
    rewrite_query=True,
    ranking_options={"ranker": "auto", "score_threshold": score_threshold},
    max_num_results=max_num_results
  )
  print(f"    {len(search_results.data)} search results")
  table = ("    " + format_search_results_table(search_results.data)).replace("\n","\n    ")
  print(table)
  log_function_footer(function_name, start_time)

# ----------------------------------------------------- END: Tests ------------------------------------------------------------

# ----------------------------------------------------- START: Main -----------------------------------------------------------

openai_service_type = os.getenv("OPENAI_SERVICE_TYPE", "openai")
azure_openai_use_key_authentication = os.getenv("AZURE_OPENAI_USE_KEY_AUTHENTICATION", "false").lower() in ['true']

if openai_service_type == "openai":
  client = create_openai_client()
elif openai_service_type == "azure_openai":
  client = create_azure_openai_client(azure_openai_use_key_authentication)

test_vector_store_name = "test_vector_store"

# Part 1: Create vector store by uploading files
test_vector_store_with_files = create_test_vector_store_with_files(client,test_vector_store_name, "./RAGFiles/Batch01")

# Part 2: Extract metadata from files and re-add files with more metadata to the vector store
extract_and_add_metadata_to_vector_store(client, test_vector_store_with_files, False)

# Part 3: Test file search functionalities
test_file_search_functionalities(client, test_vector_store_with_files)

# Part 4: Delete vector store including all files
delete_vector_store_by_name(client, test_vector_store_name, True)

exit()

# ----------------------------------------------------- END: Main -------------------------------------------------------------
