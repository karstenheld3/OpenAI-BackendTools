from dataclasses import dataclass
from dotenv import load_dotenv
from openai_backendtools import *
from test_rag_operations import *
import time
import json
import os
import datetime

load_dotenv()

metadata_extraction_prompt_template = """
## Task
Extract the following tags for the uploaded document and return them as JSON.

Example answer format:
{
  "title": "<document_title>"
  ,"description": "<document_description>"
  ,"doc_type": "<document_type>"
  ,"doc_language": "<document_language>"s
  ,"doc_author": "<document_author>"
  ,"doc_year": "<document_doc_year>"
  ,"doc_start_date": "<document_doc_start_date>"
  ,"doc_end_date": "<document_doc_end_date>"
}

Here is some information about the file:
- filename: '<filename>'
- last_modified: <last_modified>
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
If the date can't be extracted, use the year from the last_modified.
Return an answer in exactly 4 characters.
Examples: '1981', '2022', '2022'

### doc_start_date
If the document contains data that spans multiple years, return oldest date referenced in the document.
If its a report, return the report start date.
If month or day are unknown, use month = 01, day = 01.
Return an answer in exactly 10 characters as ISO-Date or an empty string.
Examples: '1981-01-01', '2022-09-01', '2022-12-31', ''

### doc_end_date
What is the document's data or reporting end date? If the date can't be extracted, use the last_modified.
Return an answer in exactly 10 characters as ISO-Date.
If month or day are unknown, use month = 12, day = last day of the month.
Examples: '1981-01-12', '2022-09-30', '2022-12-31'
"""

# ----------------------------------------------------- START: Tests ----------------------------------------------------------

# Re-add files with metadata to vector store because there is no other way to update the file attributes as of 2025-05-28
def re_add_files_with_metadata_to_vector_store(client,test_vector_store_with_files ):
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
      print(f"    [ {idx} / {len(test_vector_store_with_files.files)} ] OK: ID={file_id} with {file_metadata_count} attributes '{file_path}'")
    except Exception as e:
      print(f"    [ {idx} / {len(test_vector_store_with_files.files)} ] FAIL: '{file_path}' - {str(e)}")

  # make sure all files in the vector store have status 'processed' and delete those that don't
  print(f"  Ensuring all files in the vector store have status='completed'...")
  files = get_vector_store_files(client, test_vector_store_with_files.vector_store)
  for file in files:
    if file.status != 'completed':
      print(f"    Deleting file '{file.id}' with status '{file.status}'")
      client.vector_stores.files.delete( vector_store_id=test_vector_store_with_files.vector_store.id, file_id=file.id )

# Extract metadata from files in vector store using responses API and add it to the vector store
def extract_and_add_metadata_to_vector_store_using_responses_api(client, test_vector_store_with_files, metadata_extraction_prompt_template, openai_model_name, logExtractedMetadata=False):
  function_name = 'Extract and add metadata to vector store using responses API'
  start_time = log_function_header(function_name)

  # We use a temporary vector store that ónly contains 1 file at a time because we can't specify the file_id in the file_search tool

  # Create temporary vector store for metadata extraction
  temp_vector_store = client.vector_stores.create(name="temp_vector_store", expires_after={ "anchor": "last_active_at", "days": 1})

  # Extract metadata for each file
  print(f"  Extracting metadata for {len(test_vector_store_with_files.files)} files...")
  for idx, file_path in enumerate(test_vector_store_with_files.files, 1):
    file_id = test_vector_store_with_files.files_data[file_path]['file_id']
    last_modified = test_vector_store_with_files.files_data[file_path]['last_modified']
    source = test_vector_store_with_files.files_metadata[file_path]['source']
    filename = test_vector_store_with_files.files_metadata[file_path]['filename']

    # Add file to temporary vector store
    client.vector_stores.files.create(vector_store_id=temp_vector_store.id, file_id=file_id) 

    prompt = metadata_extraction_prompt_template.replace("<filename>", filename).replace("<last_modified>", last_modified).replace("<source>", source)

    print(f"    [ {idx} / {len(test_vector_store_with_files.files)} ] Extracting metadata for '{file_path}'...")

    # Extract metadata from files in vector store using responses API and add it to the vector store
    response = retry_on_openai_errors(lambda: client.responses.create(
      model=openai_model_name
      ,input=prompt
      ,tools=[
        {
          "type": "file_search"
          ,"vector_store_ids": [temp_vector_store.id]
          ,"max_num_results": 50
        }
      ]
    ), indentation=6)
    extracted_metadata_string = response.output_text
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
    
    # Remove file from temporary vector store
    client.vector_stores.files.delete(file_id=file_id, vector_store_id=temp_vector_store.id)

  # Delete temporary vector store
  client.vector_stores.delete(temp_vector_store.id)

  re_add_files_with_metadata_to_vector_store(client,test_vector_store_with_files)
  
  log_function_footer(function_name, start_time)

# Extract metadata from files in vector store using assistants API and add it to the vector store
def extract_and_add_metadata_to_vector_store_using_asssistants_api(client, test_vector_store_with_files, metadata_extraction_prompt_template, openai_model_name, logExtractedMetadata=False):
  function_name = 'Extract and add metadata to vector store'
  start_time = log_function_header(function_name)

  # We use a temporary vector store that ónly contains 1 file at a time to avoid the automatic creation of unnecessary vector stores 

  # Create temporary vector store for metadata extraction
  temp_vector_store = client.vector_stores.create(name="temp_vector_store", expires_after={ "anchor": "last_active_at", "days": 1})
 
  # Create assistant for metadata extraction
  assistant = client.beta.assistants.create(
    name="test_assistant"
    ,instructions="You are a metadata extraction assistant, returning extracted tags from documents as JSON."
    ,model=openai_model_name
    ,tools=[{"type": "file_search"}]
    ,tool_resources={"file_search": {"vector_store_ids": [temp_vector_store.id]}}
  )
  
  # Extract metadata for each file
  print(f"  Extracting metadata for {len(test_vector_store_with_files.files)} files...")
  for idx, file_path in enumerate(test_vector_store_with_files.files, 1):
    file_id = test_vector_store_with_files.files_data[file_path]['file_id']
    last_modified = test_vector_store_with_files.files_data[file_path]['last_modified']
    source = test_vector_store_with_files.files_metadata[file_path]['source']
    filename = test_vector_store_with_files.files_metadata[file_path]['filename']

    print(f"    [ {idx} / {len(test_vector_store_with_files.files)} ] Extracting metadata for '{file_path}'...")

    # Add file to temporary vector store
    client.vector_stores.files.create(vector_store_id=temp_vector_store.id, file_id=file_id) 

    prompt = metadata_extraction_prompt_template.replace("<filename>", filename).replace("<last_modified>", last_modified).replace("<source>", source)
    
    # Run the assistant on the thread with retries
    max_attempts = 5; attempt = 1
    while attempt <= max_attempts:
      try:
        # Create a thread for metadata extraction
        thread = client.beta.threads.create()
        
        # Create message with file content and metadata
        # We don't use attachments as shown below because that would create a new vector store with an empty name for each file processed.
        # ,attachments=[{ "file_id": file_id, "tools": [{"type": "file_search"}] }]
        client.beta.threads.messages.create(
          thread_id=thread.id
          ,role="user"
          ,content=prompt
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

    # Remove file from temporary vector store
    client.vector_stores.files.delete(file_id=file_id, vector_store_id=temp_vector_store.id)

    # delete thread
    client.beta.threads.delete(thread.id)

  # Delete assistant
  client.beta.assistants.delete(assistant.id)

  # Delete temporary vector store
  client.vector_stores.delete(temp_vector_store.id)

  re_add_files_with_metadata_to_vector_store(client,test_vector_store_with_files)
  
  log_function_footer(function_name, start_time)


def test_file_search_functionalities(client, vector_store_id, params):
  function_name = 'File search functionalities (RAG search, filter, rewrite query)'
  start_time = log_function_header(function_name)

  # Search for files using query
  # https://cookbook.openai.com/examples/file_search_responses#standalone-vector-search

  query = params.search_query_1; score_threshold = 0.3; max_num_results = 10
  print(f"  Testing query search (score_threshold={str(score_threshold)}, max_num_results={max_num_results}): {query}")
  search_results = retry_on_openai_errors(lambda: client.vector_stores.search(
    vector_store_id=vector_store_id,
    query=query,
    ranking_options={"ranker": "auto", "score_threshold": score_threshold},
    max_num_results=max_num_results
  ), indentation=4)
  # sort by score
  search_results.data.sort(key=lambda x: x.score, reverse=True)
  print(f"    {len(search_results.data)} search results")
  table = ("    " + format_search_results_table(search_results.data)).replace("\n","\n    ")
  print(table)

  # Search for files using filter
  # https://platform.openai.com/docs/guides/tools-file-search#metadata-filtering
  query = params.search_query_2
  filters = params.search_query_2_filters
  print("  " + "-"*140)
  print(f"  Testing filtered query search (filter: {filters['key']}='{filters['value']}', score_threshold={str(score_threshold)}, max_num_results={max_num_results}): {query}")

  search_results = retry_on_openai_errors(lambda: client.vector_stores.search(
    vector_store_id=vector_store_id,
    query=query,
    ranking_options={"ranker": "auto", "score_threshold": score_threshold},
    max_num_results=max_num_results,
    filters=filters
  ), indentation=4)
  print(f"    {len(search_results.data)} search results")
  table = ("    " + format_search_results_table(search_results.data)).replace("\n","\n    ")
  print(table)

  # Search for files using rewrite-query
  # https://platform.openai.com/docs/guides/retrieval#query-rewriting
  query = params.search_query_3_with_query_rewrite; score_threshold = 0.3; max_num_results = 10
  print("  " + "-"*140)
  print(f"  Testing rewrite query search (score_threshold={str(score_threshold)}, max_num_results={max_num_results}): {query}")
  search_results = retry_on_openai_errors(lambda: client.vector_stores.search(
    vector_store_id=vector_store_id,
    query=query,
    rewrite_query=True,
    ranking_options={"ranker": "auto", "score_threshold": score_threshold},
    max_num_results=max_num_results
  ), indentation=4)

  print(f"    {len(search_results.data)} search results")
  rewritten_search_query = search_results.model_extra['search_query'][0]
  print(f"    Rewritten query: {rewritten_search_query}")

  table = ("    " + format_search_results_table(search_results.data)).replace("\n","\n    ")
  print(table)
  log_function_footer(function_name, start_time)

# ----------------------------------------------------- END: Tests ------------------------------------------------------------


# ----------------------------------------------------- START: Main -----------------------------------------------------------

if __name__ == '__main__':
  openai_service_type = os.getenv("OPENAI_SERVICE_TYPE", "openai")
  azure_openai_use_key_authentication = os.getenv("AZURE_OPENAI_USE_KEY_AUTHENTICATION", "false").lower() in ['true']
  openai_model_name = os.getenv("AZURE_OPENAI_MODEL_DEPLOYMENT_NAME", "gpt-4o-mini")

  if openai_service_type == "openai":
    client = create_openai_client()
  elif openai_service_type == "azure_openai":
    client = create_azure_openai_client(azure_openai_use_key_authentication)

  @dataclass
  class SearchParams: vector_store_name: str; folder_path: str; search_query_1: str; search_query_2: str; search_query_2_filters: dict; search_query_3_with_query_rewrite: str

  params = SearchParams(
    vector_store_name="test_vector_store"
    ,folder_path="./RAGFiles/Batch01"
    ,search_query_1="Who is Arilena Drovik?"
    ,search_query_2="Who is Arilena Drovik?"
    ,search_query_2_filters = { "key": "file_type", "type": "eq", "value": "md" }
    ,search_query_3_with_query_rewrite="All files from year 2015."
  )
  
  # Step 1: Create vector store by uploading files
  test_vector_store_with_files = create_test_vector_store_from_folder_path(client,params.vector_store_name, params.folder_path)

  # Step 2: Extract metadata from files and re-add files with more metadata to the vector store
  extract_and_add_metadata_to_vector_store_using_asssistants_api(client, test_vector_store_with_files, metadata_extraction_prompt_template, openai_model_name, True)
  # extract_and_add_metadata_to_vector_store_using_responses_api(client, test_vector_store_with_files, metadata_extraction_prompt_template, openai_model_name, True)

  print("\n")

  files = get_vector_store_files(client, test_vector_store_with_files.vector_store)
  print(f"{len(files)} files in vector store:")
  print("-"*140)
  print(format_file_attributes_table(files))

  print("\n")

  # Step 3: Test file search functionalities
  test_file_search_functionalities(client, test_vector_store_with_files.vector_store.id, params)

  print("-"*140)

  # Step 4: Delete vector store including all files
  delete_vector_store_by_name(client, params.vector_store_name, True)

# ----------------------------------------------------- END: Main -------------------------------------------------------------
