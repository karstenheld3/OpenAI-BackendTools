import os
import datetime
import time
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
import openai

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

def log_function_header(name):
  start_time = datetime.datetime.now()
  print(f"[{start_time.strftime('%Y-%m-%d %H:%M:%S')}] START: {name}...")
  return start_time

def log_function_footer(name, start_time):
  end_time = datetime.datetime.now()
  secs = (end_time - start_time).total_seconds()
  if secs < 1: total_time = f"{int(secs * 1000)} ms"
  else:
    parts = [(int(secs // 3600), 'hour'), (int((secs % 3600) // 60), 'min'), (int(secs % 60), 'sec')]
    total_time = ', '.join(f"{val} {unit}{'s' if val != 1 else ''}" for val, unit in parts if val > 0)
  print(f"[{end_time.strftime('%Y-%m-%d %H:%M:%S')}] END: {name} ({total_time}).")

def get_all_assistant_vector_store_ids(client):
  all_assistants = get_all_assistants(client)
  all_assistant_vector_store_ids = [get_assistant_vector_store_id(client, a) for a in all_assistants]
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
    
    # Filter out failed and cancelled files, and add new ones to our collection
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

def get_all_files_used_by_vector_stores(client):
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

# Utility function to remove temperature parameter for reasoning models that don't support it
# When reasoning model is used, it will add the reasoning effort if specified
def remove_temperature_from_request_params_for_reasoning_models(request_params, model_name, reasoning_effort=None):
  if (model_name.startswith('o') or model_name.startswith('gpt-5')) and 'temperature' in request_params:
    del request_params['temperature']
  
  # Add reasoning parameter for reasoning models if reasoning_effort is specified
  if reasoning_effort and reasoning_effort in ["minimal", "low", "medium", "high"]:
    if model_name.startswith('o') or model_name.startswith('gpt-5'):
      # For 'o' models, 'minimal' is invalid and will be mapped to 'low'
      if model_name.startswith('o') and reasoning_effort == "minimal": request_params["reasoning"] = {"effort": "low"}
      else: request_params["reasoning"] = {"effort": reasoning_effort}

# ----------------------------------------------------- END: Utilities --------------------------------------------------------

# ----------------------------------------------------- START: Files ----------------------------------------------------------
# Gets all files from Azure OpenAI with pagination handling.
# Adds a zero-based 'index' attribute to each file.
def get_all_files(client):
  first_page = client.files.list()
  has_more = hasattr(first_page, 'has_more') and first_page.has_more
  
  # If only one page, add 'index' and return
  if not has_more:
    for idx, file in enumerate(first_page.data): setattr(file, 'index', idx)
    return first_page.data
  
  # Initialize collection with first page data
  all_files = list(first_page.data)
  total_files = len(all_files)
  
  # Continue fetching pages while there are more results
  current_page = first_page
  while has_more:
    last_id = current_page.data[-1].id if current_page.data else None    
    if not last_id: break
    next_page = client.files.list(after=last_id)
    all_files.extend(next_page.data)
    total_files += len(next_page.data)
    current_page = next_page
    has_more = hasattr(next_page, 'has_more') and next_page.has_more
  
  # Add index attribute to all files
  for idx, file in enumerate(all_files): setattr(file, 'index', idx)
    
  return all_files

# Format a list of files into a table
def truncate_row_data(row_data, max_widths, except_indices=[0,1]):
  truncated_data = []
  for i, cell in enumerate(row_data):
    cell_str = str(cell)
    if len(cell_str) > max_widths[i] and (not i in except_indices):  # Don't truncate row numbers or index
      cell_str = cell_str[:max_widths[i]-3] + '...'
    truncated_data.append(cell_str)
  return truncated_data

def format_files_table(file_list):
  # Check if input object is raw API response and if yes, extract list of items
  # file_list: either SyncCursorPage[FileObject] or list of FileObject
  files = getattr(file_list, 'data', None)
  if files is None: files = file_list  # fallback if just a list
  if not files or len(files) == 0: return '(No files found)'
  
  # Define headers and max column widths
  headers = ['Index', 'ID', 'Filename', 'Size', 'Created', 'Status', 'Purpose']
  max_widths = [6, 40, 40, 10, 19, 12, 15]  # Maximum width for each column

  append_vector_store_column = (getattr(files[0], 'vector_store_id', None) != None)
  if append_vector_store_column:
    headers.append('Vector Store')
    max_widths.append(40)
  
  attributes = getattr(files[0], 'attributes', {})
  append_metadata_column = isinstance(attributes, dict) and len(attributes) > 0
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
      if isinstance(attributes, dict):
        row_data.append(len(attributes))
      else:
        row_data.append('')  

    # Truncate cells and update column widths
    row_data = truncate_row_data(row_data, max_widths)
    for i, cell_str in enumerate(row_data):
      col_widths[i] = min(max(col_widths[i], len(cell_str)), max_widths[i])
    
    rows.append(row_data)
  
  # Build table as string
  lines = []
  header_line = ' | '.join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
  sep_line = ' | '.join('-'*col_widths[i] for i in range(len(headers)))
  lines.append(header_line)
  lines.append(sep_line)
  
  for row in rows:
    lines.append(' | '.join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)))
  
  return '\n'.join(lines)

# Deletes a list of files
def delete_files(client, files):
  for file in files:
    file_id = getattr(file, 'id', None)
    if not file_id: continue
    filename = getattr(file, 'filename', None)
    print(f"Deleting file ID={file_id} '{filename}'...")
    try: client.files.delete(file_id)
    except Exception as e: print(f"  WARNING: Failed to delete file file_id={file_id} '{filename}'. The file is probably already deleted in the global file storage.")

# Deletes a list of file IDs
def delete_file_ids(client, file_ids):
  for file_id in file_ids:
    print(f"Deleting file ID={file_id}...")
    try: client.files.delete(file_id)
    except Exception as e: print(f"  WARNING: Failed to delete file file_id={file_id}. The file is probably already deleted in the global file storage.")

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

def get_assistant_vector_store_id(client, assistant):
  if isinstance(assistant, str):
    # if it's a name, retrieve the assistant
    assistants = get_all_assistants(client)
    for temp_assistant in assistants:
      if temp_assistant.name == assistant:
        assistant = temp_assistant
        break

  if not assistant:
    raise ValueError(f"Assistant '{assistant}' not found")

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
      vector_store_id = get_assistant_vector_store_id(client, assistant)
      setattr(assistant, 'vector_store_id', vector_store_id)
    return first_page.data
  
  # Initialize collection with first page data
  all_assistants = list(first_page.data)
  total_assistants = len(all_assistants)
  
  # Continue fetching pages while there are more results
  current_page = first_page
  while has_more:
    last_id = current_page.data[-1].id if current_page.data else None    
    if not last_id: break
    next_page = client.beta.assistants.list(after=last_id)
    all_assistants.extend(next_page.data)
    total_assistants += len(next_page.data)
    current_page = next_page
    has_more = hasattr(next_page, 'has_more') and next_page.has_more
  
  # Add 'index' attribute and extract vector store ID for all assistants
  for idx, assistant in enumerate(all_assistants):
    setattr(assistant, 'index', idx)
    # Extract and set vector store ID
    vector_store_id = get_assistant_vector_store_id(client, assistant)
    setattr(assistant, 'vector_store_id', vector_store_id)
    
  return all_assistants

# Delete an assistant by name
def delete_assistant_by_name(client, name):
  assistants = get_all_assistants(client)
  assistant = next((a for a in assistants if a.name == name), None)
  if not assistant:
    print(f"  Assistant '{name}' not found.")
    return

  print(f"  Deleting assistant '{name}'...")
  client.beta.assistants.delete(assistant.id)

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
    
    # Truncate cells and update column widths
    row_data = truncate_row_data(row_data, max_widths)
    for i, cell_str in enumerate(row_data):
      col_widths[i] = min(max(col_widths[i], len(cell_str)), max_widths[i])
    
    rows.append(row_data)
  
  # Build table as string
  lines = []
  header_line = ' | '.join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
  sep_line = ' | '.join('-'*col_widths[i] for i in range(len(headers)))
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
    for idx, vector_store in enumerate(first_page.data): setattr(vector_store, 'index', idx)
    return first_page.data
  
  # Initialize collection with first page data
  all_vector_stores = list(first_page.data)
  total_vector_stores = len(all_vector_stores)
  
  # Continue fetching pages while there are more results
  current_page = first_page
  while has_more:
    last_id = current_page.data[-1].id if current_page.data else None    
    if not last_id: break
    next_page = client.vector_stores.list(after=last_id)
    all_vector_stores.extend(next_page.data)
    total_vector_stores += len(next_page.data)
    current_page = next_page
    has_more = hasattr(next_page, 'has_more') and next_page.has_more
  
  # Add index attribute to all vector stores
  for idx, vector_store in enumerate(all_vector_stores): setattr(vector_store, 'index', idx)
    
  return all_vector_stores

def get_vector_store_by_name(client, vector_store_name):
  vector_stores = get_all_vector_stores(client)
  for vector_store in vector_stores:
    if vector_store.name == vector_store_name:
      return vector_store
  return None

def get_vector_store_by_id(client, vector_store_id):
  vector_stores = get_all_vector_stores(client)
  for vector_store in vector_stores:
    if vector_store.id == vector_store_id:
      return vector_store
  return None

def get_vector_store_files(client, vector_store):
  if isinstance(vector_store, str):
    # if it's a name or ID, retrieve the vector store
    vector_stores = get_all_vector_stores(client)
    for temp_vs in vector_stores:
      if temp_vs.name == vector_store or temp_vs.id == vector_store:
        vector_store = temp_vs
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
def get_vector_store_file_metrics(client, vector_store):
  metrics = { "total": 0, "failed": 0, "cancelled": 0, "in_progress": 0, "completed": 0 }

  if isinstance(vector_store, str):
    vector_stores = get_all_vector_stores(client)
    for vs in vector_stores:
      if vs.name == vector_store or vs.id == vector_store:
        vector_store = vs
        break

  if not vector_store:
    raise ValueError(f"Vector store '{vector_store}' not found")

  if hasattr(vector_store, 'file_counts'):
    file_counts = vector_store.file_counts
    for key in metrics:
      metrics[key] = getattr(file_counts, key, 0)

  return metrics

# Format a list of vector stores into a table
def format_vector_stores_table(client, vector_store_list):
  # Check if input object is raw API response and if yes, extract list of items
  # vector_store_list: SyncCursorPage[VectorStoreObject] or list of VectorStoreObject
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
    metrics = get_vector_store_file_metrics(client, item)
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
    
    # Truncate cells and update column widths
    row_data = truncate_row_data(row_data, max_widths)
    for i, cell_str in enumerate(row_data):
      col_widths[i] = min(max(col_widths[i], len(cell_str)), max_widths[i])
    
    rows.append(row_data)
  
  # Build table as string
  lines = []
  header_line = ' | '.join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
  sep_line = ' | '.join('-'*col_widths[i] for i in range(len(headers)))
  lines.append(header_line)
  lines.append(sep_line)
  
  for row in rows:
    lines.append(' | '.join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)))
  
  return '\n'.join(lines)

# return formatted table of files with attributes: index,  filename, file_size, followed by all attributes in the order they are defined in the file
def list_vector_store_files_with_attributes(client, vector_store_id):
  """Get a formatted table of files in a vector store with their attributes.
  
  Args:
    client: OpenAI client
    vector_store_id: ID or name of the vector store
  
  Returns:
    Formatted table as string showing files and their attributes
  """
  files = get_vector_store_files(client, vector_store_id)
  return format_file_attributes_table(files)

def format_file_attributes_table(vector_store_files):
  if not vector_store_files: return '(No files found)'
  
  # Get all possible attributes from all files
  all_attribute_names = set()
  for file in vector_store_files:
    attributes = getattr(file, 'attributes', {})
    if not attributes: continue
    all_attribute_names.update(attributes.keys())
  
  # Define max widths for each attribute type
  attribute_max_widths = {
    'filename': 30  # Fixed width for filename
  }
  
  # Define headers and max column widths
  headers = ['Index'] + list(all_attribute_names)
  max_widths = [6] + [attribute_max_widths.get(attr, len(attr)) for attr in all_attribute_names]  # Use fixed width for filename, attribute length for others
  
  # Initialize column widths with header lengths, but respect max widths
  col_widths = [min(len(h), max_widths[i]) for i, h in enumerate(headers)]
  
  rows = []
  for idx, item in enumerate(vector_store_files):
    # Prepare row data
    row_data = [
      f"{idx:05d}",
    ]
    
    # Add attributes in the same order as headers
    attributes = getattr(item, 'attributes', {})
    for attr_name in all_attribute_names:
      row_data.append(str(attributes.get(attr_name, '')))
    
    # Truncate cells and update column widths
    row_data = truncate_row_data(row_data, max_widths, [])
    for i, cell_str in enumerate(row_data):
      col_widths[i] = min(max(col_widths[i], len(cell_str)), max_widths[i])
    
    rows.append(row_data)
  
  # Build table as string
  lines = []
  header_line = ' | '.join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
  sep_line = ' | '.join('-'*col_widths[i] for i in range(len(headers)))
  lines.append(header_line)
  lines.append(sep_line)
  
  for row in rows:
    lines.append(' | '.join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)))
  
  return '\n'.join(lines)

# Delete files with 'failed' or 'cancelled' status from both vector store and global storage
def delete_failed_vector_store_files(client, vector_store_id):
  files = get_vector_store_files(client, vector_store_id)
  failed_files = [f for f in files if getattr(f, 'status', None) in ['failed', 'cancelled']]
  for i, file in enumerate(failed_files):
    print(f"[ {i+1} / {len(failed_files)} ] Deleting file ID={file.id} with status='{getattr(file, 'status', '')}'...")
    try: client.vector_stores.files.delete(vector_store_id=vector_store_id, file_id=file.id)
    except Exception as e: print(f"  WARNING: Failed to delete file_id='{file.id}' from vector_store_id='{vector_store_id}'. The file is probably already deleted in the global file storage.")
    try: client.files.delete(file_id=file.id)
    except Exception as e: print(f"  WARNING: Failed to delete file_id='{file.id}' from global file storage.")

def delete_vector_store_files_added_after_date(client, vector_store_id, date, dry_run=False):
  function_name = 'Delete vector store files added after date'
  start_time = log_function_header(function_name)
  
  files = get_vector_store_files(client, vector_store_id)
  timestamp = date.timestamp()
  files_added_after_date = [f for f in files if getattr(f, 'created_at', None) > timestamp]
  for i, file in enumerate(files_added_after_date):
    print(f"[ {i+1} / {len(files_added_after_date)} ] Deleting file ID={file.id} added after '{date}'...")
    if dry_run: continue
    try: client.vector_stores.files.delete(vector_store_id=vector_store_id, file_id=file.id)
    except Exception as e: print(f"  WARNING: Failed to delete file_id='{file.id}' from vector_store_id='{vector_store_id}'. The file is probably already deleted in the global file storage.")
  
  log_function_footer(function_name, start_time)

# Replicate files from source and target vector stores by replicating missing files and optionally removing extra files
# Returns: Tuple of (added_file_ids, removed_file_ids, errors) where:
#   - added_file_ids: List of file IDs successfully added to target stores
#   - removed_file_ids: List of file IDs removed from target stores (if remove_target_files_not_in_sources=True)
#   - errors: List of (file_id, error_message) tuples for failed operations
def replicate_vector_store_content(client, source_vector_store_ids, target_vector_store_ids, remove_target_files_not_in_sources=False):
  function_name = 'Replicate vector store content'
  start_time = log_function_header(function_name)

  # check if source_vector_store_ids or target_vector_store_ids is string and if yes, create list with single entry
  if isinstance(source_vector_store_ids, str): source_vector_store_ids = [source_vector_store_ids]
  if isinstance(target_vector_store_ids, str): target_vector_store_ids = [target_vector_store_ids]

  collected_file_ids_and_source_vector_stores = []; added_file_ids = []; removed_file_ids = []; errors = []
  for source_vs_id in source_vector_store_ids:
    source_vs = get_vector_store_by_id(client, source_vs_id)
    if not source_vs: print(f"  WARNING: Source vector store ID={source_vs_id} not found, skipping..."); continue
    source_vs_name = getattr(source_vs, 'name', source_vs_id)
    print(f"  Loading files from source vector store '{source_vs_name}' (ID={source_vs_id})...")
    source_files = get_vector_store_files(client, source_vs_id)
    collected_file_ids_and_source_vector_stores.extend([(f.id, source_vs) for f in source_files])

  for i, target_vs_id in enumerate(target_vector_store_ids):
    target_vs = get_vector_store_by_id(client, target_vs_id)
    if not target_vs: print(f"  WARNING: Target vector store ID={target_vs_id} not found, skipping..."); continue
    target_vs_name = getattr(target_vs, 'name', target_vs_id)
    print(f"  [ {i+1} / {len(target_vector_store_ids)} ] Processing target vector store '{target_vs_name}' (ID={target_vs_id})...")
            
    target_files = get_vector_store_files(client, target_vs_id)
    target_file_ids = [f.id for f in target_files]

    # find out which files are not in target
    file_ids_missing_in_target_vs = [(file_id, source_vs) for (file_id, source_vs) in collected_file_ids_and_source_vector_stores if file_id not in target_file_ids]
    file_ids_in_target_but_not_in_collected_files = [file_id for file_id in target_file_ids if file_id not in [f[0] for f in collected_file_ids_and_source_vector_stores]]
    
    # Build status message
    if len(file_ids_missing_in_target_vs) > 0:
      message = f"Adding {len(file_ids_missing_in_target_vs)} files to '{target_vs_name}' (ID={target_vs_id})"
    else:      
      message = f"Nothing to add"
    if remove_target_files_not_in_sources and len(file_ids_in_target_but_not_in_collected_files) > 0:
      message += f", removing {len(file_ids_in_target_but_not_in_collected_files)} files"
    print(f"    {message}...")

    added_target_file_ids = []; removed_target_file_ids = []; target_errors = []
    # add files to target
    for j, (file_id, source_vs) in enumerate(file_ids_missing_in_target_vs):
      source_vs_name = getattr(source_vs, 'name', source_vs.id)
      print(f"    [ {j+1} / {len(file_ids_missing_in_target_vs)} ] Adding file ID={file_id} from '{source_vs_name}' (ID={source_vs_id}) to '{target_vs_name}' (ID={target_vs_id})...")
      try:
        client.vector_stores.files.create(vector_store_id=target_vs_id, file_id=file_id)
        added_target_file_ids.append((file_id, source_vs))
      except Exception as e:
        print(f"      WARNING: Failed to add file ID={file_id} from '{source_vs_name}'. Error: {str(e)}")
        target_errors.append((file_id, f"FAILED: Add file ID='{file_id}' from '{source_vs_name}' to vector store '{target_vs_name}': {str(e)}"))

    # remove files not in source
    if remove_target_files_not_in_sources and len(file_ids_in_target_but_not_in_collected_files) > 0:
      print(f"   Removing {len(file_ids_in_target_but_not_in_collected_files)} files from target '{target_vs_name}'...")
      for j, file_id in enumerate(file_ids_in_target_but_not_in_collected_files):
        print(f"    [ {j+1} / {len(file_ids_in_target_but_not_in_collected_files)} ] Removing file ID={file_id} from target vector store '{target_vs_name}'...")
        try:
          client.vector_stores.files.delete(vector_store_id=target_vs_id, file_id=file_id)
          removed_target_file_ids.append(file_id)
        except Exception as e:
          print(f"      WARNING: Failed to remove file ID={file_id} from '{target_vs_name}'. Error: {str(e)}")
          target_errors.append((file_id, f"FAILED: Remove file ID='{file_id}' from vector store '{target_vs_name}': {str(e)}"))
    
    # add to return values
    added_file_ids.append(added_target_file_ids)
    removed_file_ids.append(removed_target_file_ids)
    errors.append(target_errors)

  log_function_footer(function_name, start_time)
  return (added_file_ids, removed_file_ids, errors)

# Print replication summary: added files, removed files, and errors
def print_vector_store_replication_summary(target_vector_store_ids, added_file_ids, removed_file_ids, errors):
  for i, target_vs_id in enumerate(target_vector_store_ids):
    print(f"  [ {i+1} / {len(target_vector_store_ids)} ] Vector store ID={target_vs_id}: {len(added_file_ids[i])} files added, {len(removed_file_ids[i])} removed, {len(errors[i])} errors.")
    if errors[i] and len(errors[i]) > 0:
      for j, (file_id, error_msg) in enumerate(errors[i]):
        print(f"      [{j+1}] {error_msg}")


# Returns a dictionary with filename as key and list of results as items
# Key : <filename>
# Value : [
#   { file_id : <file_id>;
#     found_vector_stores: [
#       {vector_store_id : <vector_store_id>; vector_store_name : <vector_store_name>}
#     ]
#   }
def find_files_in_all_vector_stores_by_filename(client, filenames, log_headers=True) -> dict:
  function_name = 'Find files in all vector stores by filename'
  start_time = log_function_header(function_name) if log_headers else datetime.datetime.now()

  # Create filename dict with filename as key and empty list as value. Eliminates duplicate filenames, empty strings.
  search_results = {filename: [] for filename in filenames if filename}

  print(f"  Loading all files...")
  all_files = get_all_files(client)
  # Build dictionaries for fast lookup:
  # all_files_by_id with file.id as key and file as value
  # all_files_by_filename with file.name as key and list of file.id as value
  # found_file_ids = with file.id as key and None as value
  all_files_by_id = {}; all_files_by_filename = {}; found_file_ids = {}
  for global_file in all_files:
    all_files_by_id[global_file.id] = global_file
    if global_file.filename not in all_files_by_filename: all_files_by_filename[global_file.filename] = []
    all_files_by_filename[global_file.filename].append(global_file.id)
    if global_file.filename in search_results: found_file_ids[global_file.id] = None
  
  print(f"  Loading all files used by vector stores...")
  all_vector_store_files = get_all_files_used_by_vector_stores(client)
  for i, vector_store_file in enumerate(all_vector_store_files):
    if vector_store_file.id not in found_file_ids: continue
    global_file = all_files_by_id[vector_store_file.id]
    filename = global_file.filename
    # get comma-separated vector store ids and names from vector store file attributes (added by get_all_files_used_by_vector_stores function) and convert them into arrays
    found_vector_store_ids = [x for x in getattr(vector_store_file, 'vector_store_id', '').split(', ') if x]
    found_vector_store_names = [x for x in getattr(vector_store_file, 'vector_store_name', '').split(', ') if x]
    found_vector_stores = []
    for j, vector_store_id in enumerate(found_vector_store_ids):
      found_vector_stores.append({ 'vector_store_id' : vector_store_id, 'vector_store_name' : found_vector_store_names[j] })

    search_result = { 'file_id' : global_file.id, 'vector_stores' : found_vector_stores }
    search_results[filename].append(search_result)

  if log_headers: log_function_footer(function_name, start_time)
  return search_results

def delete_files_in_all_vector_stores_by_filename(client, filenames, dry_run=False, delete_files_in_global_storage=False):
  function_name = 'Delete files in all vector stores by filename'
  start_time = log_function_header(function_name)
  found_files = find_files_in_all_vector_stores_by_filename(client, filenames, log_headers=False)

  # if filenames is string, make list with single item
  if isinstance(filenames,str): filenames = [filenames]
  
  # calculate found file count (where we have results) and missing file count (where we don't have results)
  found_files_count = len(set(found_files))
  print(f"  {found_files_count} of {len(filenames)} files found.")

  if found_files_count == 0: log_function_footer(function_name, start_time); return found_files

  print(f"  Deleting files from vector stores...")
  for i, (filename, files) in enumerate(found_files.items()):
    print(f"    [ {i+1} / {len(found_files)} ] Removing file '{filename}'...")
    for file in files:
      file_id = file['file_id']
      vector_stores = file['vector_stores']
      for vector_store in vector_stores:
        vector_store_id = vector_store['vector_store_id']
        vector_store_name = vector_store['vector_store_name']
        try:
          print(f"      Deleting file '{filename}' (ID={file_id}) from vector store '{vector_store_name}' (ID={vector_store_id})")
          if dry_run: continue
          client.vector_stores.files.delete(vector_store_id=vector_store_id, file_id=file_id)
          print(f"        OK.")
        except Exception as e:
          print(f"      WARNING: Failed to delete file ID={file_id} from vector store ID={vector_store_id}: {str(e)}")

  if delete_files_in_global_storage:
    print(f"  Deleting files from global storage...")
    for i, (filename, files) in enumerate(found_files.items()):
      print(f"    [ {i+1} / {len(found_files)} ] Deleting file '{filename}' (ID={file_id}) from global storage...")
      for file in files:
        file_id = file['file_id']
        try:
          if dry_run: continue
          client.files.delete(file_id=file_id)
          print(f"      OK.")
        except Exception as e:
          print(f"      WARNING: Failed to delete file ID={file_id} from global storage: {str(e)}")

  log_function_footer(function_name, start_time)
  return found_files

def delete_files_in_vector_store_by_file_type(client, vector_store_id, file_types, dry_run=False, delete_files_in_global_storage=False):
  function_name = 'Delete files in vector stores by file type'
  start_time = log_function_header(function_name)

  vector_store = get_vector_store_by_id(client,vector_store_id)
  if not vector_store: print(f" Vector store id '{vector_store_id}' not found.")    
  else:
    vector_store_name = vector_store.name
    print(f"  Loading files of vector store '{vector_store_name}' (ID={vector_store_id})...")
    vector_store_files = get_vector_store_files(client, vector_store_id)
    print("  Loading global files...")
    all_files = get_all_files(client)
    all_files_dict = {file.id: file for file in all_files}

    found_files = []
    # run over all files in vector store, get filename and add to found_files if file type matches one of file_types
    for file in vector_store_files:
      # Get the filename from all_files_dict, since this is not stored in vector stores
      if file.id not in all_files_dict: continue
      global_file = all_files_dict[file.id]
      # Check if file matches any of the file types
      if any(global_file.filename.lower().endswith(ft.lower()) for ft in file_types):
        # Add file info to the list
        found_files.append({ 'file_id': file.id, 'filename': global_file.filename, 'created_at': global_file.created_at })

    if len(found_files) == 0: print(f"  No files found. Nothing to delete.")
    else:
      print(f"  Deleting {len(found_files)} files from vector store...")
      for i, item in enumerate(found_files):
        file_id = item['file_id']; filename = item['filename']; created_at = item['created_at']
        print(f"    [ {i+1} / {len(found_files)} ] File '{filename}'...")
        try:
          print(f"      Removing file '{filename}' (ID={file_id}) from vector store '{vector_store_name}' (ID={vector_store_id})...")
          if not dry_run:
            client.vector_stores.files.delete(vector_store_id=vector_store_id, file_id=file_id)
            print(f"        OK.")
        except Exception as e:
          print(f"      WARNING: Failed to delete file ID={file_id} from vector store ID={vector_store_id}: {str(e)}")
        if delete_files_in_global_storage:          
          try:
            print(f"      Deleting file '{filename}' (ID={file_id}) from global files...")
            if not dry_run:
              client.files.delete(file_id=file.id)
              print(f"        OK.")
          except Exception as e:
            print(f"      WARNING: Failed to delete file '{filename}' (ID={file_id}, {format_timestamp(created_at)}). The file is probably already deleted in the global file storage.")

  log_function_footer(function_name, start_time)
  return found_files


def delete_vector_store_by_id(client, vector_store_id, delete_files=False):
  vector_stores = get_all_vector_stores(client)
  vs = [vs for vs in vector_stores if vs.id == vector_store_id]
  if vs:
    vs = vs[0]
    print(f"  Deleting vector store '{vs.name}' (ID={vs.id} , {format_timestamp(vs.created_at)})...")
    if delete_files:
      files = get_vector_store_files(client, vs)
      for i, file in enumerate(files):
        print(f"    [ {i+1} / {len(files)} ] Deleting file ID={file.id} ({format_timestamp(file.created_at)})...")
        try: client.files.delete(file_id=file.id)
        except Exception as e:
          print(f"      WARNING: Failed to delete file ID={file.id} ({format_timestamp(file.created_at)}). The file is probably already deleted in the global file storage.")
    client.vector_stores.delete(vs.id)
  else:
    print(f"  Vector store id='{vector_store_id}' not found.")

def delete_vector_store_by_name(client, name, delete_files=False):
  vector_stores = get_all_vector_stores(client)
  vs = [vs for vs in vector_stores if vs.name == name]
  if vs:
    vs = vs[0]
    print(f"  Deleting vector store '{vs.name}' (ID={vs.id} , {format_timestamp(vs.created_at)})...")
    if delete_files:
      files = get_vector_store_files(client, vs)
      for i, file in enumerate(files):
        print(f"    [ {i+1} / {len(files)} ] Deleting file ID={file.id} ({format_timestamp(file.created_at)})...")
        try: client.files.delete(file_id=file.id)
        except Exception as e:
          print(f"      WARNING: Failed to delete file ID={file.id} ({format_timestamp(file.created_at)}). The file is probably already deleted in the global file storage.")
    client.vector_stores.delete(vs.id)
  else:
    print(f"  Vector store '{name}' not found.")
  
# ----------------------------------------------------- END: Vector stores ----------------------------------------------------


# ----------------------------------------------------- START: Search results -------------------------------------------------

# formats a list of vector store search results 
def format_search_results_table(search_results):
  # search_results: list of search results
  if not search_results: return '(No search results found)'
  
  # Define headers and max column widths
  headers = ['Index', 'File ID', 'Filename', 'Score', 'Attributes', 'Content']
  max_widths = [6, 36, 40, 8, 10, 60]  # Maximum width for each column
  
  # Initialize column widths with header lengths, but respect max widths
  col_widths = [min(len(h), max_widths[i]) for i, h in enumerate(headers)]
  
  # Process each row
  rows = []
  for idx, item in enumerate(search_results):
    # Get content safely, checking for content list first, then falling back to text
    content = '...'
    if hasattr(item, 'content') and item.content and len(item.content) > 0: content = item.content[0].text
    elif hasattr(item, 'text'): content = item.text
    
    # Clean content for better readability
    if content != '...': content = content.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('  ', ' ')
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
      attributes_string,
      content
    ]
    
    # Truncate cells and update column widths
    row_data = truncate_row_data(row_data, max_widths)
    for i, cell_str in enumerate(row_data):
      col_widths[i] = min(max(col_widths[i], len(cell_str)), max_widths[i])
    
    rows.append(row_data)
  
  # Build table as string
  lines = []
  header_line = ' | '.join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
  sep_line = ' | '.join('-'*col_widths[i] for i in range(len(headers)))
  lines.append(header_line)
  lines.append(sep_line)
  
  for row in rows:
    lines.append(' | '.join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)))
  
  return '\n'.join(lines)


# ----------------------------------------------------- END: Search results ---------------------------------------------------

# ----------------------------------------------------- START: Evals ----------------------------------------------------------

# Gets all evals from Azure OpenAI with pagination handling.
# Adds a zero-based 'index' attribute to each eval.
def get_all_evals(client):
  first_page = client.evals.list()
  has_more = hasattr(first_page, 'has_more') and first_page.has_more
  
  # If only one page, add 'index' and return
  if not has_more:
    for idx, eval in enumerate(first_page.data): setattr(eval, 'index', idx)
    return first_page.data
  
  # Initialize collection with first page data
  all_evals = list(first_page.data)
  total_evals = len(all_evals)
  
  # Continue fetching pages while there are more results
  current_page = first_page
  while has_more:
    last_id = current_page.data[-1].id if current_page.data else None
    if not last_id: break
    next_page = client.evals.list(after=last_id)
    all_evals.extend(next_page.data)
    total_evals += len(next_page.data)
    current_page = next_page
    has_more = hasattr(next_page, 'has_more') and next_page.has_more
  
  # Add index attribute to all evals
  for idx, eval in enumerate(all_evals): setattr(eval, 'index', idx)
    
  return all_evals

# Creates a table containing 'Name' , 'Data source' (type), 'Tests' (number), 'Test Types' (comma separated), 'Created' (timestamp) 
def format_evals_table(evals_list):
  # Check if input object is raw API response and if yes, extract list of items
  # evals_list: either SyncCursorPage[EvalObject] or list of EvalObject
  evals = getattr(evals_list, 'data', None)
  if evals is None: evals = evals_list  # fallback if just a list
  if not evals: return '(No evals found)'
  
  # Define headers and max column widths
  headers = ['Name', 'ID', 'Data Source', 'Tests', 'Test Types', 'Created']
  max_widths = [60, 40, 20, 8, 50, 19]  # Maximum width for each column
  
  # Initialize column widths with header lengths, but respect max widths
  col_widths = [min(len(h), max_widths[i]) for i, h in enumerate(headers)]
  
  rows = []
  for item in evals:
    # Get test types from testing criteria
    test_types = []
    testing_criteria = getattr(item, 'testing_criteria', [])
    for criterion in testing_criteria:
      test_type = getattr(criterion, 'type', None)
      if test_type and test_type not in test_types:
        test_types.append(test_type)
    
    # Get data source type
    data_source_config = getattr(item, 'data_source_config', {})
    data_source_type = getattr(data_source_config, 'type', '...')
    
    # Prepare row data
    name = getattr(item, 'name', '')
    id = getattr(item, 'id', '')
    if name and len(name) > max_widths[0]:
      name = name[:max_widths[0]-3] + '...'
    
    row_data = [
      name,
      id,
      data_source_type,
      str(len(testing_criteria)),
      ', '.join(test_types) if test_types else '...',
      format_timestamp(getattr(item, 'created_at', ''))
    ]
    
    # Truncate cells and update column widths
    row_data = truncate_row_data(row_data, max_widths)
    for i, cell_str in enumerate(row_data):
      col_widths[i] = min(max(col_widths[i], len(cell_str)), max_widths[i])
    
    rows.append(row_data)
  
  # Build table as string
  lines = []
  header_line = ' | '.join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
  sep_line = ' | '.join('-'*col_widths[i] for i in range(len(headers)))
  lines.append(header_line)
  lines.append(sep_line)
  
  for row in rows:
    lines.append(' | '.join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)))
  
  return '\n'.join(lines)

# Gets all eval runs from Azure OpenAI with pagination handling.
def get_all_eval_runs(client, eval_id):
  runs_page = client.evals.runs.list(eval_id=eval_id)
  all_runs = list(runs_page.data)
  
  # Get additional pages if they exist
  has_more = hasattr(runs_page, 'has_more') and runs_page.has_more
  current_page = runs_page
  
  while has_more:
    last_id = current_page.data[-1].id if current_page.data else None
    if not last_id: break
    
    next_page = client.evals.runs.list(eval_id=eval_id, after=last_id)
    all_runs.extend(next_page.data)
    current_page = next_page
    has_more = hasattr(next_page, 'has_more') and next_page.has_more
  
  # Add index and eval_id attributes to all runs
  for idx, run in enumerate(all_runs):
    setattr(run, 'index', idx)
    setattr(run, 'eval_id', eval_id)
  
  return all_runs

def get_all_eval_run_output_items(client, run_id, eval_id, expected_count=None, max_retries=3):
  import time
  
  for attempt in range(max_retries + 1):
    if attempt > 0:
      print(f"  DEBUG: [Get all eval output items] - Retry attempt {attempt} / {max_retries} for fetching output items")
      time.sleep(2)  # Wait 2 seconds before retry
    
    # Fetch first page
    output_items_page = client.evals.runs.output_items.list(eval_id=eval_id, run_id=run_id)
    all_output_items = list(output_items_page.data)
    
    # Get additional pages if they exist
    has_more = hasattr(output_items_page, 'has_more') and output_items_page.has_more
    current_page = output_items_page
    
    while has_more:
      last_id = current_page.data[-1].id if current_page.data else None
      if not last_id: break
      
      next_page = client.evals.runs.output_items.list(eval_id=eval_id, run_id=run_id, after=last_id)
      all_output_items.extend(next_page.data)
      current_page = next_page
      has_more = hasattr(next_page, 'has_more') and next_page.has_more
    
    # Check if we got the expected number of items
    if expected_count is None or len(all_output_items) == expected_count:
      if attempt > 0:
        print(f"  DEBUG: [Get all eval output items] - Successfully retrieved {len(all_output_items)} items after {attempt} retries")
      return all_output_items
    
    # Log the mismatch
    print(f"  DEBUG: [Get all eval output items] - Attempt {attempt + 1}: Got {len(all_output_items)} items, expected {expected_count}")
    if attempt < max_retries:
      print(f"  DEBUG: [Get all eval output items] - Will retry fetching items in 10 seconds...")
      time.sleep(10)
  
  # If we get here, all retries failed
  print(f"  WARNING: [Get all eval output items] - After {max_retries + 1} attempts, still got {len(all_output_items)} items instead of expected {expected_count}")
  return all_output_items

def delete_all_evals(client, dry_run=False):
  function_name = 'Delete all evals'
  start_time = log_function_header(function_name)

  all_evals = get_all_evals(client)
  for i, eval in enumerate(all_evals):
    print(f"  [ {i+1} / {len(all_evals)} ] Deleting eval '{eval.name}' (ID={eval.id})...")
    if dry_run: continue
    try: client.evals.delete(eval_id=eval.id)
    except Exception as e: print(f"    WARNING: Failed to delete '{eval.name}' (ID={eval.id}). Error: {str(e)}")

  log_function_footer(function_name, start_time)

def delete_eval_by_id(client, eval_id):
  try:
    print(f"  Deleting eval ID={eval_id}...")
    response = client.evals.delete(eval_id=eval_id)
    return response
  except Exception as e:
    print(f"  WARNING: Failed to delete eval ID={eval_id}. Error: {str(e)}")
    return None

def delete_eval_by_name(client, name):
  evals = get_all_evals(client)
  eval_list = [e for e in evals if e.name == name]
  if eval_list:
    eval_obj = eval_list[0]
    print(f"  Deleting eval '{eval_obj.name}' (ID={eval_obj.id}, {format_timestamp(eval_obj.created_at)})...")
    client.evals.delete(eval_obj.id)
  else:
    print(f"  Eval '{name}' not found.")


# ----------------------------------------------------- END: Evals ------------------------------------------------------------


# ----------------------------------------------------- START: Cleanup --------------------------------------------------------
# Delete expired vector stores
def delete_expired_vector_stores(client):
  function_name = 'Delete expired vector stores'
  start_time = log_function_header(function_name)

  vector_stores = get_all_vector_stores(client)
  vector_stores_expired = [v for v in vector_stores if getattr(v, 'status', None) == 'expired']
  if len(vector_stores_expired) == 0: print(" Nothing to delete.")

  for vs in vector_stores_expired:
    print(f"  Deleting expired vector store ID={vs.id} '{vs.name}'...")
    client.vector_stores.delete(vs.id)

  log_function_footer(function_name, start_time)

# Delete duplicate files in vector stores
# This will delete all duplicate filenames in vector stores, keeping only the file with the latest upload time
def delete_duplicate_files_in_vector_stores(client):
  function_name = 'Delete duplicate files in vector stores'
  start_time = log_function_header(function_name)

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

  log_function_footer(function_name, start_time)


# deletes all files with status = 'failed', 'cancelled' and all files with purpose = 'assistants' that are not used by any vector store
def delete_failed_and_unused_files(client, dry_run=False):
  function_name = 'Delete failed and unused files'
  start_time = log_function_header(function_name)

  print(f"  Loading all files...")
  all_files_list = get_all_files(client)
  # Convert to hashmap by using id as key
  all_files = {f.id: f for f in all_files_list}

  # Find files with status = 'failed', 'cancelled'
  files_to_delete = [f for f in all_files.values() if f.status in ['failed', 'cancelled']]

  print(f"  Loading files used by vector stores...")
  files_used_by_vector_stores_list = get_all_files_used_by_vector_stores(client)
  files_used_by_vector_stores = {f.id: f for f in files_used_by_vector_stores_list}

  # Find files with purpose = 'assistants' that are not used by any vector store
  files_not_used_by_vector_stores = [f for f in all_files.values() if f.purpose == 'assistants' and f.id not in files_used_by_vector_stores]
  files_to_delete.extend(files_not_used_by_vector_stores)

  for i, file in enumerate(files_to_delete, 1):
    print(f"    [ {i} / {len(files_to_delete)} ] Deleting file '{file.filename}' (ID={file.id}, {format_timestamp(file.created_at)})...")
    if dry_run: continue
    try:
      client.files.delete(file_id=file.id)
    except Exception as e:
      print(f"  WARNING: Failed to delete file ID={file.id} from global storage: {str(e)}")

  log_function_footer(function_name, start_time)

def delete_vector_stores_not_used_by_assistants(client, until_date_created, dry_run=False):
  function_name = 'Delete vector stores not used by assistants'
  start_time = log_function_header(function_name)

  all_vector_stores = get_all_vector_stores(client)
  all_assistant_vector_store_ids = get_all_assistant_vector_store_ids(client)
  vector_stores_not_used_by_assistants = [vs for vs in all_vector_stores if vs.id not in all_assistant_vector_store_ids and datetime.datetime.fromtimestamp(vs.created_at) <= until_date_created]

  for vs in vector_stores_not_used_by_assistants:
    print(f"  Deleting vector store ID={vs.id} '{vs.name}' ({format_timestamp(vs.created_at)})...")
    if dry_run: continue
    try:
      client.vector_stores.delete(vs.id)
    except Exception as e:
      print(f"  WARNING: Failed to delete vector store ID={vs.id}: {str(e)}")

  log_function_footer(function_name, start_time)


# ----------------------------------------------------- END: Cleanup ----------------------------------------------------------
