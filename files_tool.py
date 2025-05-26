import os
import re
import openai
import datetime
import time
import json
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
load_dotenv()

# ----------------------------------------------------- START: Utilities ------------------------------------------------------
def create_openai_client():
  api_key = os.environ.get('OPENAI_API_KEY')
  return openai.OpenAI(api_key=api_key)

# Create an Azure OpenAI client using either managed identity or API key authentication.
def create_azure_openai_client(use_key_authentication=False):
  endpoint = os.environ.get('AZURE_OPENAI_ENDPOINT')
  api_version = os.environ.get('AZURE_OPENAI_API_VERSION')
  
  if use_key_authentication:
    # Use API key authentication
    api_key = os.environ.get('AZURE_OPENAI_API_KEY')
    # Create client with API key
    return openai.AzureOpenAI(
      api_version=api_version,
      azure_endpoint=endpoint,
      api_key=api_key
    )
  else:
    # Use managed identity or service principal authentication (whatever is configured in the environment variables)
    cred = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(cred, "https://cognitiveservices.azure.com/.default")
    # Create client with token provider
    return openai.AzureOpenAI( api_version=api_version, azure_endpoint=endpoint, azure_ad_token_provider=token_provider )

# Format a file size in bytes into a human-readable string
def format_filesize(num_bytes):
  if not num_bytes: return ''
  for unit in ['B','KB','MB','GB','TB']:
    if num_bytes < 1024: return f"{num_bytes:.2f} {unit}"
    num_bytes /= 1024
  return f"{num_bytes:.2f} PB"

# Format timestamp into a human-readable string (RFC3339 with ' ' instead of 'T')
def format_timestamp(ts):
  return ('' if not ts else datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))

def get_all_assistant_vector_store_ids(client):
  all_assistants = get_all_assistants(client)
  all_assistant_vector_store_ids = [get_assistant_vector_store(a) for a in all_assistants]
  return all_assistant_vector_store_ids

def get_files_used_by_assistant_vector_stores(client):
  # Get all assistants and their vector stores
  all_assistant_vector_store_ids = get_all_assistant_vector_store_ids(client)
  all_vector_stores = get_all_vector_stores(client)
  # Remove those that returned None
  all_assistant_vector_store_ids = [vs for vs in all_assistant_vector_store_ids if vs]
  # Remove duplicates
  all_assistant_vector_store_ids = list(set(all_assistant_vector_store_ids))
  
  # Dictionary to store unique files to avoid duplicates
  all_files = []
  processed_file_ids = set()
  
  # For each vector store used by assistants
  for vector_store_id in all_assistant_vector_store_ids:
    # Find the vector store object
    vector_store = next((vs for vs in all_vector_stores if vs.id == vector_store_id), None)
    vector_store_name = getattr(vector_store, 'name', None)
      
    # Get all files in this vector store
    vector_store_files = get_vector_store_files(client, vector_store)
    
    # Filter out failed and cancelled files, and add  new ones to our collection
    for file in vector_store_files:
      file_status = getattr(file, 'status', None)
      if file_status in ['failed', 'cancelled']: continue
      if (getattr(file, 'id', None) and file.id not in processed_file_ids):
        setattr(file, 'vector_store_id', vector_store_id)
        setattr(file, 'vector_store_name', vector_store_name)
        all_files.append(file)
        processed_file_ids.add(file.id)
  
  # Add index attribute to all files
  for idx, file in enumerate(all_files):
    setattr(file, 'index', idx)

  return all_files

def get_files_used_by_vector_stores(client):
  # Get all vector stores
  all_vector_stores = get_all_vector_stores(client)
  
  # Dictionary to store unique files to avoid duplicates
  all_files = []
  processed_file_ids = set()
  
  # For each vector store used by assistants
  for vector_store in all_vector_stores:
    # Get all files in this vector store
    vector_store_files = get_vector_store_files(client, vector_store)
    vector_store_name = getattr(vector_store, 'name', None)
    vector_store_id = getattr(vector_store, 'id', None)
    
    # Filter out failed and cancelled files, and add others to our collection
    for file in vector_store_files:
      file_status = getattr(file, 'status', None)
      if file_status in ['failed', 'cancelled']: continue
      if file.id not in processed_file_ids:
        setattr(file, 'vector_store_id', vector_store_id)
        setattr(file, 'vector_store_name', vector_store_name)
        all_files.append(file)
        processed_file_ids.add(file.id)
      else:
        # Here we add the vector store ID and name to the existing file's attributes. These files are used in multiple vector stores.
        existing_file = next((f for f in all_files if f.id == file.id), None)
        if not existing_file: continue
        existing_vector_store_id = getattr(existing_file, 'vector_store_id', None)
        existing_vector_store_name = getattr(existing_file, 'vector_store_name', None)
        existing_vector_store_id = (existing_vector_store_id + f", {vector_store_id}") if existing_vector_store_id else vector_store_id
        existing_vector_store_name = (existing_vector_store_name + f", {vector_store_name}") if existing_vector_store_name else vector_store_name
        setattr(existing_file, 'vector_store_id', existing_vector_store_id)
        setattr(existing_file, 'vector_store_name', existing_vector_store_name)
  
  return all_files

# ----------------------------------------------------- END: Utilities --------------------------------------------------------

# ----------------------------------------------------- START: Files ----------------------------------------------------------
# Gets all files from Azure OpenAI with pagination handling.
# Adds a zero-based 'index' attribute to each file.
def get_all_files(client):
  first_page = client.files.list()
  has_more = hasattr(first_page, 'has_more') and first_page.has_more
  
  # If only one page, add 'index' and return
  if not has_more:
    for idx, file in enumerate(first_page.data):
      setattr(file, 'index', idx)
    return first_page.data
  
  # Initialize collection with first page data
  all_files = list(first_page.data)
  page_count = 1
  total_files = len(all_files)
  
  # Continue fetching pages while there are more results
  current_page = first_page
  while has_more:
    last_id = current_page.data[-1].id if current_page.data else None    
    if not last_id: break
    next_page = client.files.list(after=last_id)
    page_count += 1
    all_files.extend(next_page.data)
    total_files += len(next_page.data)
    current_page = next_page
    has_more = hasattr(next_page, 'has_more') and next_page.has_more
  
  # Add index attribute to all files
  for idx, file in enumerate(all_files):
    setattr(file, 'index', idx)
    
  return all_files

# Format a list of files into a table
def format_files_table(file_list_page):
  # file_list_page: SyncCursorPage[FileObject] or similar
  files = getattr(file_list_page, 'data', None)
  if files is None: files = file_list_page  # fallback if just a list
  if not files or len(files) == 0: return '(No files found)'
  
  # Define headers and max column widths
  headers = ['Index', 'ID', 'Filename', 'Size', 'Created', 'Status', 'Purpose']
  max_widths = [6, 40, 40, 10, 19, 12, 15]  # Maximum width for each column

  append_vector_store_column = (getattr(files[0], 'vector_store_id', None) != None)
  if append_vector_store_column:
    headers.append('Vector Store')
    max_widths.append(40)
  
  append_metadata_column = (getattr(files[0], 'attributes', None) != None)
  if append_metadata_column:
    headers.append('Attributes')
    max_widths.append(10)
  
  # Initialize column widths with header lengths, but respect max widths
  col_widths = [min(len(h), max_widths[i]) for i, h in enumerate(headers)]
  
  rows = []
  for idx, item in enumerate(files):
    # Prepare row data
    row_data = [
      "..." if not hasattr(item, 'index') else f"{item.index:05d}",
      getattr(item, 'id', '...'),
      getattr(item, 'filename', '...'), 
      format_filesize(getattr(item, 'bytes', None)),
      format_timestamp(getattr(item, 'created_at', None)), 
      getattr(item, 'status', '...'), 
      getattr(item, 'purpose', '...'),
    ]

    if append_vector_store_column: row_data.append(getattr(item, 'vector_store_name', ''))
    if append_metadata_column:
      attributes = getattr(item, 'attributes', '')
      row_data.append(len(attributes))
    
    
    # Truncate cells if they exceed max width
    for i, cell in enumerate(row_data):
      cell_str = str(cell)
      if len(cell_str) > max_widths[i] and i > 1:  # Don't truncate row numbers or index
        if i == 3:  # Filename column - special handling
          # For filenames, keep the extension and truncate the middle
          name_parts = cell_str.split('.')
          if len(name_parts) > 1:
            ext = name_parts[-1]
            base = '.'.join(name_parts[:-1])
            avail_chars = max_widths[i] - len(ext) - 3  # -3 for '...' and '.' before extension
            if avail_chars > 5:  # Only truncate if we can show a reasonable amount
              cell_str = base[:avail_chars] + '...' + '.' + ext
            else:
              cell_str = cell_str[:max_widths[i]-3] + '...'
          else:
            cell_str = cell_str[:max_widths[i]-3] + '...'
        else:  # Other columns
          cell_str = cell_str[:max_widths[i]-3] + '...'
      
      # Update column width if needed, but respect max width
      col_widths[i] = min(max(col_widths[i], len(cell_str)), max_widths[i])
      row_data[i] = cell_str
    
    rows.append(row_data)
  
  # Build table as string
  lines = []
  header_line = ' | '.join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
  sep_line = '-+-'.join('-'*col_widths[i] for i in range(len(headers)))
  lines.append(header_line)
  lines.append(sep_line)
  
  for row in rows:
    lines.append(' | '.join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)))
  
  return '\n'.join(lines)

# Deletes a list of files
def delete_files(client, files):
  for file in files:
    file_id = getattr(file, 'id', None)
    if not id: continue
    filename = getattr(file, 'filename', None)
    print(f"Deleting file ID={file_id} '{filename}'...")
    client.files.delete(file_id)

# Deletes a list of file IDs
def delete_file_ids(client, file_ids):
  for file_id in file_ids:
    print(f"Deleting file ID={file_id}...")
    client.files.delete(file_id)

# returns dictionary with metrics for a list of files
def get_filelist_metrics(files):
  metrics = ["processed","failed","cancelled","frozen","in_progress","completed"]
  
  # Initialize counts for each metric
  counts = {metric: 0 for metric in metrics}
  
  # Count files in each state
  for file in files:
    status = getattr(file, 'status', None)
    if status in counts:
      counts[status] += 1
  
  return counts

# ----------------------------------------------------- END: Files ------------------------------------------------------------

# ----------------------------------------------------- START: Assistants -----------------------------------------------------

def get_assistant_vector_store(assistant):
  if hasattr(assistant, 'tool_resources') and assistant.tool_resources:
    file_search = getattr(assistant.tool_resources, 'file_search', None)
    if file_search:
      vector_store_ids = getattr(file_search, 'vector_store_ids', [])
      if vector_store_ids and len(vector_store_ids) > 0:
        return vector_store_ids[0]
  return None

# Adds a zero-based 'index' attribute to each file.
def get_all_assistants(client):
  first_page = client.beta.assistants.list()
  has_more = hasattr(first_page, 'has_more') and first_page.has_more
  
  # If only one page, add 'index' and return
  if not has_more:
    for idx, assistant in enumerate(first_page.data):
      setattr(assistant, 'index', idx)
      # Extract and set vector store ID
      vector_store_id = get_assistant_vector_store(assistant)
      setattr(assistant, 'vector_store_id', vector_store_id)
    return first_page.data
  
  # Initialize collection with first page data
  all_assistants = list(first_page.data)
  page_count = 1
  total_assistants = len(all_assistants)
  
  # Continue fetching pages while there are more results
  current_page = first_page
  while has_more:
    last_id = current_page.data[-1].id if current_page.data else None    
    if not last_id: break
    next_page = client.beta.assistants.list(after=last_id)
    page_count += 1
    all_assistants.extend(next_page.data)
    total_assistants += len(next_page.data)
    current_page = next_page
    has_more = hasattr(next_page, 'has_more') and next_page.has_more
  
  # Add 'index' attribute and extract vector store ID for all assistants
  for idx, assistant in enumerate(all_assistants):
    setattr(assistant, 'index', idx)
    # Extract and set vector store ID
    vector_store_id = get_assistant_vector_store(assistant)
    setattr(assistant, 'vector_store_id', vector_store_id)
    
  return all_assistants

# Format a list of assistants into a table
def format_assistants_table(assistant_list):
  # assistant_list: List of Assistant objects
  assistants = getattr(assistant_list, 'data', None)
  if assistants is None: assistants = assistant_list  # fallback if just a list
  if not assistants: return '(No assistants found)'
  
  # Define headers and max column widths
  headers = ['Index', 'ID', 'Name', 'Model', 'Created', 'Vector Store']
  max_widths = [6, 31, 40, 11, 19, 36]  # Maximum width for each column
  
  # Initialize column widths with header lengths, but respect max widths
  col_widths = [min(len(h), max_widths[i]) for i, h in enumerate(headers)]
  
  rows = []
  for idx, item in enumerate(assistants):
    # Prepare row data
    row_data = [
      "..." if not hasattr(item, 'index') else f"{item.index:04d}",
      getattr(item, 'id', '...'),
      "" if not getattr(item, 'name') else getattr(item, 'name'), 
      getattr(item, 'model', '...'),
      format_timestamp(getattr(item, 'created_at', "")), 
      "" if not getattr(item, 'vector_store_id') else getattr(item, 'vector_store_id', "")
    ]
    
    # Truncate cells if they exceed max width
    for i, cell in enumerate(row_data):
      cell_str = str(cell)
      if len(cell_str) > max_widths[i] and i > 1:  # Don't truncate row numbers or index
        cell_str = cell_str[:max_widths[i]-3] + '...'
      
      # Update column width if needed, but respect max width
      col_widths[i] = min(max(col_widths[i], len(cell_str)), max_widths[i])
      row_data[i] = cell_str
    
    rows.append(row_data)
  
  # Build table as string
  lines = []
  header_line = ' | '.join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
  sep_line = '-+-'.join('-'*col_widths[i] for i in range(len(headers)))
  lines.append(header_line)
  lines.append(sep_line)
  
  for row in rows:
    lines.append(' | '.join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)))
  
  return '\n'.join(lines)

# ----------------------------------------------------- END: Assistants -------------------------------------------------------

# ----------------------------------------------------- START: Vector stores --------------------------------------------------

# Gets all vector stores from Azure OpenAI with pagination handling.
# Adds a zero-based 'index' attribute to each vector store.
def get_all_vector_stores(client):
  first_page = client.vector_stores.list()
  has_more = hasattr(first_page, 'has_more') and first_page.has_more
  
  # If only one page, add 'index' and return
  if not has_more:
    for idx, vector_store in enumerate(first_page.data):
      setattr(vector_store, 'index', idx)
    return first_page.data
  
  # Initialize collection with first page data
  all_vector_stores = list(first_page.data)
  page_count = 1
  total_vector_stores = len(all_vector_stores)
  
  # Continue fetching pages while there are more results
  current_page = first_page
  while has_more:
    last_id = current_page.data[-1].id if current_page.data else None    
    if not last_id: break
    next_page = client.vector_stores.list(after=last_id)
    page_count += 1
    all_vector_stores.extend(next_page.data)
    total_vector_stores += len(next_page.data)
    current_page = next_page
    has_more = hasattr(next_page, 'has_more') and next_page.has_more
  
  # Add index attribute to all vector stores
  for idx, vector_store in enumerate(all_vector_stores):
    setattr(vector_store, 'index', idx)
    
  return all_vector_stores

def get_vector_store_files(client, vector_store):

  if isinstance(vector_store, str):
    # if it's a name, retrieve the vector store
    vector_stores = get_all_vector_stores(client)
    for vs in vector_stores:
      if vs.name == vector_store:
        vector_store = vs
        break

  if not vector_store:
    raise ValueError(f"Vector store '{vector_store}' not found")

  # Get the vector store ID
  vector_store_id = getattr(vector_store, 'id', None)
  vector_store_name = getattr(vector_store, 'name', None)
  if not vector_store_id:
    return []
    
  files_page = client.vector_stores.files.list(vector_store_id=vector_store_id)
  all_files = list(files_page.data)
  
  # Get additional pages if they exist
  has_more = hasattr(files_page, 'has_more') and files_page.has_more
  current_page = files_page
  
  while has_more:
    last_id = current_page.data[-1].id if current_page.data else None
    if not last_id: break
    
    next_page = client.vector_stores.files.list(vector_store_id=vector_store_id, after=last_id)
    all_files.extend(next_page.data)
    current_page = next_page
    has_more = hasattr(next_page, 'has_more') and next_page.has_more
  
  # Add index and vector store attributes to all files
  for idx, file in enumerate(all_files):
    setattr(file, 'index', idx)
    setattr(file, 'vector_store_id', vector_store_id)
    setattr(file, 'vector_store_name', vector_store_name)
  
  return all_files


# Gets the file metrics for a vector store as dictionary with keys: total, failed, cancelled, in_progress, completed
def get_vector_store_file_metrics(vector_store):
  metrics = { "total": 0, "failed": 0, "cancelled": 0, "in_progress": 0, "completed": 0 }
  if hasattr(vector_store, 'file_counts'):
    file_counts = vector_store.file_counts
    for key in metrics:
      metrics[key] = getattr(file_counts, key, 0)
      
  return metrics

# Format a list of vector stores into a table
def format_vector_stores_table(vector_store_list):
  # vector_store_list: SyncCursorPage[VectorStoreObject] or similar
  vector_stores = getattr(vector_store_list, 'data', None)
  if vector_stores is None: vector_stores = vector_store_list  # fallback if just a list
  if not vector_stores: return '(No vector stores found)'
  
  # Define headers and max column widths
  headers = ['Index', 'ID', 'Name','Created', 'Status', 'Size', 'Files (completed, in_progress, failed, cancelled)']
  max_widths = [6, 36, 40, 19, 12, 10, 50]  # Maximum width for each column
  
  # Initialize column widths with header lengths, but respect max widths
  col_widths = [min(len(h), max_widths[i]) for i, h in enumerate(headers)]
  
  rows = []
  for idx, item in enumerate(vector_stores):
    # Prepare row data
    # Get file metrics
    metrics = get_vector_store_file_metrics(item)
    files_str = f"Total: {metrics['total']} (✓ {metrics['completed']}, ⌛ {metrics['in_progress']}, ❌ {metrics['failed']}, ⏹ {metrics['cancelled']})" if metrics['total'] > 0 else '' 
    
    row_data = [
      "..." if not hasattr(item, 'index') else f"{item.index:05d}",
      getattr(item, 'id', '...'),
      "" if not getattr(item, 'name') else getattr(item, 'name'), 
      format_timestamp(getattr(item, 'created_at', None)), 
      getattr(item, 'status', '...'),
      format_filesize(getattr(item, 'usage_bytes', None)),
      files_str
    ]
    
    # Truncate cells if they exceed max width
    for i, cell in enumerate(row_data):
      cell_str = str(cell)
      if len(cell_str) > max_widths[i] and i > 1:  # Don't truncate row numbers or index
        cell_str = cell_str[:max_widths[i]-3] + '...'
      
      # Update column width if needed, but respect max width
      col_widths[i] = min(max(col_widths[i], len(cell_str)), max_widths[i])
      row_data[i] = cell_str
    
    rows.append(row_data)
  
  # Build table as string
  lines = []
  header_line = ' | '.join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
  sep_line = '-+-'.join('-'*col_widths[i] for i in range(len(headers)))
  lines.append(header_line)
  lines.append(sep_line)
  
  for row in rows:
    lines.append(' | '.join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)))
  
  return '\n'.join(lines)

# formats a list of vector store search results 
def format_search_results_table(search_results):
  # search_results: list of search results
  if not search_results: return '(No search results found)'
  
  # Define headers and max column widths
  headers = ['Index', 'File ID', 'Filename', 'Score', 'Content', 'Attributes']
  max_widths = [6, 36, 40, 8, 40, 10]  # Maximum width for each column
  
  # Initialize column widths with header lengths, but respect max widths
  col_widths = [min(len(h), max_widths[i]) for i, h in enumerate(headers)]
  
  # Process each row
  rows = []
  for idx, item in enumerate(search_results):
    content = getattr(item, 'content', '...')
    # Clean content for better readability
    if content and len(content) > 0:
      content = content[0].text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('  ', ' ')
    attributes = getattr(item, 'attributes', {})
    # calculate metadata tags - count total fields that are not empty
    non_empty_values = [value for value in attributes.values() if value]
    attributes_string = f"{len(non_empty_values)} of {len(attributes)}"
    # Prepare row data
    row_data = [
      f"{idx:05d}",
      getattr(item, 'file_id', '...'),
      getattr(item, 'filename', '...'),
      f"{getattr(item, 'score', 0):.2f}",
      content,
      attributes_string
    ]
    
    # Truncate cells if they exceed max width
    for i, cell in enumerate(row_data):
      cell_str = str(cell)
      if len(cell_str) > max_widths[i] and i > 1:  # Don't truncate row numbers or index
        if i == 4:  # Content column - special handling to preserve useful info
          cell_str = cell_str[:max_widths[i]-3] + '...'
        else:
          cell_str = cell_str[:max_widths[i]-3] + '...'
      
      # Update column width if needed, but respect max width
      col_widths[i] = min(max(col_widths[i], len(cell_str)), max_widths[i])
      row_data[i] = cell_str
    
    rows.append(row_data)
  
  # Build table as string
  lines = []
  header_line = ' | '.join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
  sep_line = '-+-'.join('-'*col_widths[i] for i in range(len(headers)))
  lines.append(header_line)
  lines.append(sep_line)
  
  for row in rows:
    lines.append(' | '.join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)))
  
  return '\n'.join(lines)
  

# ----------------------------------------------------- END: Vector stores ----------------------------------------------------

# ----------------------------------------------------- START: Assistants ----------------------------------------------------

# Delete an assistant by name
def delete_assistant_by_name(client, name):
  assistants = get_all_assistants(client)
  assistant = next((a for a in assistants if a.name == name), None)
  if not assistant:
    print(f"  Assistant '{name}' not found.")
    return

  print(f"  Deleting assistant '{name}'...")
  client.beta.assistants.delete(assistant.id)

# ----------------------------------------------------- END: Assistants ------------------------------------------------------


# ----------------------------------------------------- START: Cleanup --------------------------------------------------------
# Delete expired vector stores
def delete_expired_vector_stores(client):
  start_time = datetime.datetime.now()
  print(f"[{start_time.strftime('%Y-%m-%d %H:%M:%S')}] START: Delete expired vector stores...")

  vector_stores = get_all_vector_stores(client)
  vector_stores_expired = [v for v in vector_stores if getattr(v, 'status', None) == 'expired']
  if len(vector_stores_expired) == 0: print(" Nothing to delete.")
  
  for vs in vector_stores_expired:
    print(f"  Deleting expired vector store ID={vs.id} '{vs.name}'...")
    client.vector_stores.delete(vs.id)
  
  end_time = datetime.datetime.now(); secs = (end_time - start_time).total_seconds()
  parts = [(int(secs // 3600), 'hour'), (int((secs % 3600) // 60), 'min'), (int(secs % 60), 'sec')]
  total_time = ', '.join(f"{val} {unit}{'s' if val != 1 else ''}" for val, unit in parts if val > 0)
  print(f"[{end_time.strftime('%Y-%m-%d %H:%M:%S')}] END: Delete expired vector stores ({total_time}).")

# Delete duplicate files in vector stores
# This will delete all duplicate filenames in vector stores, keeping only the file with the latest upload time
def delete_duplicate_files_in_vector_stores(client):
  start_time = datetime.datetime.now()
  print(f"[{start_time.strftime('%Y-%m-%d %H:%M:%S')}] START: Delete duplicate files in vector stores...")

  print(f"  Loading all files...")
  all_files_list = get_all_files(client)
  # Convert to hashmap by using id as key
  all_files = {f.id: f for f in all_files_list}

  print(f"  Loading all vector stores...")
  vector_stores = get_all_vector_stores(client)
  for vs in vector_stores:
    print(f"  Loading files for vector store '{vs.name}'...")
    files = get_vector_store_files(client, vs)
    # Sort files so newest files are on top
    files.sort(key=lambda f: f.created_at, reverse=True)
    # Add filenames from all_files to files
    for f in files:
      # If error, use datetime timestamp as filename. Can happen if vector store got new file just after all_files was loaded.
      try: f.filename = all_files[f.id].filename
      except: f.filename = str(datetime.datetime.now().timestamp())

    # Create dictionary with filename as key and list of files as value
    files_by_filename = {}
    for f in files:
      if f.filename not in files_by_filename:
        files_by_filename[f.filename] = []
      files_by_filename[f.filename].append(f)
    
    # Find files with duplicate filenames. Omit first file (the newest), treat others (older files) as duplicates.
    duplicate_files = []
    for filename, files in files_by_filename.items():
      if len(files) > 1:
        duplicate_files.extend(files[1:])

    for file in duplicate_files:
      print(f"    Deleting duplicate file ID={file.id} '{file.filename}' ({format_timestamp(file.created_at)})...")
      client.vector_stores.files.delete(file_id=file.id, vector_store_id=vs.id)

  end_time = datetime.datetime.now(); secs = (end_time - start_time).total_seconds()
  parts = [(int(secs // 3600), 'hour'), (int((secs % 3600) // 60), 'min'), (int(secs % 60), 'sec')]
  total_time = ', '.join(f"{val} {unit}{'s' if val != 1 else ''}" for val, unit in parts if val > 0)
  print(f"[{end_time.strftime('%Y-%m-%d %H:%M:%S')}] END: Delete duplicate files in vector stores ({total_time}).")


# deletes all files with status = 'failed', 'cancelled' and all files with purpose = 'assistants' that are not used by any vector store
def delete_failed_and_unused_files(client):
  start_time = datetime.datetime.now()
  print(f"[{start_time.strftime('%Y-%m-%d %H:%M:%S')}] START: Delete failed and unused files...")

  print(f"  Loading all files...")
  all_files_list = get_all_files(client)
  # Convert to hashmap by using id as key
  all_files = {f.id: f for f in all_files_list}

  # Find files with status = 'failed', 'cancelled'
  files_to_delete = [f for f in all_files.values() if f.status in ['failed', 'cancelled']]

  print(f"  Loading files used by vector stores...")
  files_used_by_vector_stores_list = get_files_used_by_vector_stores(client)
  files_used_by_vector_stores = {f.id: f for f in files_used_by_vector_stores_list}

  # Find files with purpose = 'assistants' that are not used by any vector store
  files_not_used_by_vector_stores = [f for f in all_files.values() if f.purpose == 'assistants' and f.id not in files_used_by_vector_stores]
  files_to_delete.extend(files_not_used_by_vector_stores)

  for file in files_to_delete:
    print(f"    Deleting file ID={file.id} '{file.filename}' ({format_timestamp(file.created_at)})...")
    client.files.delete(file_id=file.id)

  end_time = datetime.datetime.now(); secs = (end_time - start_time).total_seconds()
  parts = [(int(secs // 3600), 'hour'), (int((secs % 3600) // 60), 'min'), (int(secs % 60), 'sec')]
  total_time = ', '.join(f"{val} {unit}{'s' if val != 1 else ''}" for val, unit in parts if val > 0)
  print(f"[{end_time.strftime('%Y-%m-%d %H:%M:%S')}] END: Delete failed and unused files ({total_time}).")

def delete_vector_stores_not_used_by_assistants(client, until_date_created):
  start_time = datetime.datetime.now()
  print(f"[{start_time.strftime('%Y-%m-%d %H:%M:%S')}] START: Delete vector stores not used by assistants...")

  all_vector_stores = get_all_vector_stores(client)
  all_assistant_vector_store_ids = get_all_assistant_vector_store_ids(client)
  vector_stores_not_used_by_assistants = [vs for vs in all_vector_stores if vs.id not in all_assistant_vector_store_ids and vs.created_at <= until_date_created]

  for vs in vector_stores_not_used_by_assistants:
    print(f"  Deleting vector store ID={vs.id} '{vs.name}' ({format_timestamp(vs.created_at)})...")
    client.vector_stores.delete(vs.id)

  end_time = datetime.datetime.now(); secs = (end_time - start_time).total_seconds()
  parts = [(int(secs // 3600), 'hour'), (int((secs % 3600) // 60), 'min'), (int(secs % 60), 'sec')]
  total_time = ', '.join(f"{val} {unit}{'s' if val != 1 else ''}" for val, unit in parts if val > 0)
  print(f"[{end_time.strftime('%Y-%m-%d %H:%M:%S')}] END: Delete vector stores not used by assistants ({total_time}).")

def delete_vector_store_by_name(client, name, delete_files=False):
  vector_stores = get_all_vector_stores(client)
  vs = [vs for vs in vector_stores if vs.name == name]
  if vs:
    vs = vs[0]
    print(f"  Deleting vector store ID={vs.id} '{vs.name}' ({format_timestamp(vs.created_at)})...")
    if delete_files:
      files = get_vector_store_files(client, vs)
      for file in files:
        print(f"    Deleting file ID={file.id} ({format_timestamp(file.created_at)})...")
        client.vector_stores.files.delete(file_id=file.id, vector_store_id=vs.id)
    client.vector_stores.delete(vs.id)
  else:
    print(f"  Vector store '{name}' not found.")

# ----------------------------------------------------- END: Cleanup ----------------------------------------------------------

# ----------------------------------------------------- START: Tests ----------------------------------------------------------
def test_basic_file_functionalities(client, file_path="./RAGFiles/Batch01/Publications1.md"):
  start_time = datetime.datetime.now()
  print(f"[{start_time.strftime('%Y-%m-%d %H:%M:%S')}] START: File functionalities (upload, vector stores, delete)...")

  # Upload a file
  if not os.path.exists(file_path):
    # remove part to move one folder up
    file_path_split = file_path.split("/")
    file_path = "/".join(file_path_split[1:])
  if not os.path.exists(file_path):
    raise Exception(f"File '{file_path}' does not exist.")

  print(f"  Uploading file '{file_path}'...")
  with open(file_path, 'rb') as f:
    file = client.files.create(file=f, purpose="assistants")
  print(f"    OK. ID: {file.id}") if file.id else print("    FAIL.")

  # Create a vector store
  vs_name = "test_vector_store"
  print(f"  Creating vector store '{vs_name}'...")
  vs = client.vector_stores.create(name=vs_name)
  print(f"    OK. ID: {vs.id}") if vs.id else print("    FAIL.")

  # Add file to vector store
  print(f"  Adding file '{file.filename}' to vector store...")
  client.vector_stores.files.create(vector_store_id=vs.id, file_id=file.id)
  print("    OK.")

  # Remove file from vector store
  print(f"  Removing file '{file.filename}' from vector store...")
  client.vector_stores.files.delete(vector_store_id=vs.id, file_id=file.id)
  print("    OK.")

  # Delete vector store
  print(f"  Deleting vector store '{vs_name}'...")
  client.vector_stores.delete(vs.id)
  print("    OK.")

  # Delete file
  print(f"  Deleting file '{file.filename}'...")
  client.files.delete(file_id=file.id)
  print("    OK.")

  end_time = datetime.datetime.now(); secs = (end_time - start_time).total_seconds()
  parts = [(int(secs // 3600), 'hour'), (int((secs % 3600) // 60), 'min'), (int(secs % 60), 'sec')]
  total_time = ', '.join(f"{val} {unit}{'s' if val != 1 else ''}" for val, unit in parts if val > 0)
  print(f"[{end_time.strftime('%Y-%m-%d %H:%M:%S')}] END: File functionalities (upload, vector stores, delete) ({total_time}).")


# 
def test_file_search_functionalities(client, folder_path, logExtractedMetadata=False):
  start_time = datetime.datetime.now()
  print(f"[{start_time.strftime('%Y-%m-%d %H:%M:%S')}] START: File functionalities (upload, vector stores, delete)...")

  # Load RAG files and store metadata in dict (filename, file_year, file_type)
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
  vs_name = "test_vector_store"
  print(f"  Creating vector store '{vs_name}'...")
  vs = client.vector_stores.create(name=vs_name)
  print(f"    OK. ID={vs.id}") if vs.id else print("  FAIL.")

  # Add files to vector store
  failed_files = []
  print(f"  Adding files to vector store '{vs_name}'...")
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
    model="gpt-4o-mini"
  )
  
  # Extract metadata for each file
  total_files = len(files)
  print(f"  Extracting metadata for {total_files} files...")
  for idx, file_path in enumerate(files, 1):
    file_id = files_data[file_path]['file_id']
    file_last_modified_date = files_data[file_path]['file_last_modified_date']
    source = files_metadata[file_path]['source']
    filename = files_metadata[file_path]['filename']

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
        message = client.beta.threads.messages.create(
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
      files_metadata[file_path].update(extracted_metadata)
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
  for idx, file_path in enumerate(files, 1):
    file_id = files_data[file_path]['file_id']
    file_metadata = files_metadata[file_path]
    # calculate metadata tags - count total fields
    file_metadata_count = len(file_metadata.keys())

    try:
      # first remove the file from the vector store
      client.vector_stores.files.delete( vector_store_id=vs.id, file_id=file_id )
      # then add the file back with the updated metadata
      client.vector_stores.files.create( vector_store_id=vs.id, file_id=file_id, attributes=file_metadata )
      print(f"    [ {idx} / {total_files} ] OK: ID={file_id} with {file_metadata_count} attributes '{file_path}'")
    except Exception as e:
      print(f"    [ {idx} / {total_files} ] FAIL: '{file_path}' - {str(e)}")

    # make sure all files in the vector store have status 'processed' and delete those that don't
    print(f"  Ensuring all files in the vector store have status='completed'...")
    files = get_vector_store_files(client, vs)
    for file in files:
      if file.status != 'completed':
        print(f"    Deleting file '{file.id}' with status '{file.status}'")
        client.vector_stores.files.delete( vector_store_id=vs.id, file_id=file.id )

  # Search for files using query
  # https://cookbook.openai.com/examples/file_search_responses#standalone-vector-search

  query = "Who is Arilena Drovik?"; score_threshold = 0.3; max_num_results = 10
  print("-"*140)
  print(f"  Testing query search (score_threshold={str(score_threshold)}, max_num_results={max_num_results}): {query}")
  search_results = client.vector_stores.search(
    vector_store_id=vs.id,
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
    vector_store_id=vs.id,
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
    vector_store_id=vs.id,
    query=query,
    rewrite_query=True,
    ranking_options={"ranker": "auto", "score_threshold": score_threshold},
    max_num_results=max_num_results
  )
  print(f"    {len(search_results.data)} search results")
  table = ("    " + format_search_results_table(search_results.data)).replace("\n","\n    ")
  print(table)

  # Delete vector store
  delete_vector_store_by_name(client, "test_vector_store", delete_files=True)

  end_time = datetime.datetime.now(); secs = (end_time - start_time).total_seconds()
  parts = [(int(secs // 3600), 'hour'), (int((secs % 3600) // 60), 'min'), (int(secs % 60), 'sec')]
  total_time = ', '.join(f"{val} {unit}{'s' if val != 1 else ''}" for val, unit in parts if val > 0)
  print(f"[{end_time.strftime('%Y-%m-%d %H:%M:%S')}] END: File functionalities (upload, vector stores, delete) ({total_time}).")

# ----------------------------------------------------- END: Tests ------------------------------------------------------------

# ----------------------------------------------------- START: Main -----------------------------------------------------------
if __name__ == '__main__':

### START: Configuration
  use_openai_instead_of_azure_open_ai = False
  use_managed_identity = False
### END: Configuration

  openai_service_type = os.getenv("OPENAI_SERVICE_TYPE", "openai")
  azure_openai_use_key_authentication = os.getenv("AZURE_OPENAI_USE_KEY_AUTHENTICATION", "false").lower() in ['true']

  if openai_service_type == "openai":
    client = create_openai_client()
  elif openai_service_type == "azure_openai":
    client = create_azure_openai_client(azure_openai_use_key_authentication)

  # test_basic_file_functionalities(client, "./RAGFiles/Batch01/Publications1.md")

  test_file_search_functionalities(client, "./RAGFiles/Batch01")
  
  exit()

  # delete_expired_vector_stores(client)
  
  # delete_duplicate_files_in_vector_stores(client)

  # USE WITH CAUTION! This will delete all non-assistant vector stores older than 10 days. Including those used in current conversations.
  # delete_vector_stores_not_used_by_assistants(client, datetime.datetime.now() - datetime.timedelta(days=10))

  # delete_failed_and_unused_files(client)
  
  # Get all files with pagination handling
  all_files = get_all_files(client)
  metrics = get_filelist_metrics(all_files)
  metrics_str = ", ".join([f"{v} {k}" for k, v in metrics.items()])
  
  # Since console out will trim the output due to max char limit, we will only show the first 25 and last 25 files
  if len(all_files) > 50:
    # Create new collection with only the first 25 and the last 25 files, with empty row in the middle
    class EmptyRow: pass
    all_files_trimmed = all_files[:25] + [EmptyRow()] + all_files[-25:]
  else:
    all_files_trimmed = all_files

  # Display the total files count and the formatted table
  print(f"Total files: {len(all_files)} ({metrics_str}). Showing first 25 and last 25 files.")
  print("-"*140)
  print(format_files_table(all_files_trimmed))

  print("\n")
  # Display the vector stores total count and the formatted table
  all_vector_stores = get_all_vector_stores(client)
  all_vector_stores_expired = [v for v in all_vector_stores if getattr(v, 'status', None) == 'expired']
  print(f"Total vector stores: {len(all_vector_stores)} ({len(all_vector_stores_expired)} expired)")
  print("-"*140)
  print(format_vector_stores_table(all_vector_stores))

  print("\n")
  # Display the files used by vector stores
  files_used_by_vector_stores = get_files_used_by_vector_stores(client)
  metrics = get_filelist_metrics(files_used_by_vector_stores)
  metrics_str = ", ".join([f"{v} {k}" for k, v in metrics.items()])

  print(f"Total files in vector stores: {len(files_used_by_vector_stores)} ({metrics_str})")
  print("-"*140)
  print(format_files_table(all_files_trimmed))

  print("\n")
  # Display the assistants total count and the formatted table
  all_assistants = get_all_assistants(client)
  print(f"Total assistants: {len(all_assistants)}")
  print("-"*140)
  print(format_assistants_table(all_assistants))

  print("\n")
  # Display the vector stores not used by assistants
  all_assistant_vector_store_ids = get_all_assistant_vector_store_ids(client)
  vector_stores_not_used_by_assistants = [vs for vs in all_vector_stores if vs.id not in all_assistant_vector_store_ids]
  print(f"Total vector stores NOT used by assistants: {len(vector_stores_not_used_by_assistants)}")
  print("-"*140)
  print(format_vector_stores_table(vector_stores_not_used_by_assistants))


  print("\n")
  # filter out all files that do not have purpose = 'assistants' and show files not used in vector stores
  unused_vector_store_files = [f for f in all_files if getattr(f, 'purpose', None) == 'assistants']
  # filter out all files not used by 
  unused_vector_store_files = [f for f in all_files if f.id not in [file.id for file in unused_vector_store_files]]
  # Since console out will trim the output due to max char limit, we will only show the first 25 and last 25 files
  if len(unused_vector_store_files) > 50:
    # Create new collection with only the first 25 and the last 25 files, with empty row in the middle
    class EmptyRow: pass
    unused_vector_store_files_trimmed = unused_vector_store_files[:25] + [EmptyRow()] + unused_vector_store_files[-25:]
  else:
    unused_vector_store_files_trimmed = unused_vector_store_files
  print(f"Total files not used in vector stores: {len(unused_vector_store_files)}")
  print("-"*140)
  print(format_files_table(unused_vector_store_files_trimmed))

  print("\n")
  # Display the files used by assistants
  files_used_by_assistant_vector_stores = get_files_used_by_assistant_vector_stores(client)
  metrics = get_filelist_metrics(files_used_by_assistant_vector_stores)
  metrics_str = ", ".join([f"{v} {k}" for k, v in metrics.items()])

  if len(files_used_by_assistant_vector_stores) > 50:
    # Create new collection with only the first 25 and the last 25 files, with empty row in the middle
    class EmptyRow: pass
    files_used_by_assistant_vector_stores_trimmed = files_used_by_assistant_vector_stores[:25] + [EmptyRow()] + files_used_by_assistant_vector_stores[-25:]
  else:
    files_used_by_assistant_vector_stores_trimmed = files_used_by_assistant_vector_stores
  print(f"Total files used by assistants: {len(files_used_by_assistant_vector_stores)} ({metrics_str})")
  print("-"*140)
  print(format_files_table(files_used_by_assistant_vector_stores_trimmed))

  print("\n")
  files_used_by_assistant_vector_stores_dict = {f.id: f for f in files_used_by_assistant_vector_stores}
  # Find files that are not used by any vector store
  files_not_used_by_assistants = [f for f in all_files if f.id not in files_used_by_vector_stores]
  metrics = get_filelist_metrics(files_not_used_by_assistants)
  metrics_str = ", ".join([f"{v} {k}" for k, v in metrics.items()])

  # Since console out will trim the output due to max char limit, we will only show the first 25 and last 25 files
  if len(files_not_used_by_assistants) > 50:
    # Create new collection with only the first 25 and the last 25 files, with empty row in the middle
    class EmptyRow: pass
    files_not_used_by_assistants_trimmed = files_not_used_by_assistants[:25] + [EmptyRow()] + files_not_used_by_assistants[-25:]
  else:
    files_not_used_by_assistants_trimmed = files_not_used_by_assistants
  print(f"Total files NOT used by assistants: {len(files_not_used_by_assistants)} ({metrics_str})")
  print("-"*140)
  print(format_files_table(files_not_used_by_assistants_trimmed))
  
  print("\n")
  
