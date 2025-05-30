import os
import datetime
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
  parts = [(int(secs // 3600), 'hour'), (int((secs % 3600) // 60), 'min'), (int(secs % 60), 'sec')]
  total_time = ', '.join(f"{val} {unit}{'s' if val != 1 else ''}" for val, unit in parts if val > 0)
  print(f"[{end_time.strftime('%Y-%m-%d %H:%M:%S')}] END: {name} ({total_time}).")

def get_all_assistant_vector_store_ids(client):
  all_assistants = get_all_assistants(client)
  all_assistant_vector_store_ids = [get_assistant_vector_store_id(a) for a in all_assistants]
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
def truncate_row_data(row_data, max_widths, except_indices=[0,1]):
  truncated_data = []
  for i, cell in enumerate(row_data):
    cell_str = str(cell)
    if len(cell_str) > max_widths[i] and (not i in except_indices):  # Don't truncate row numbers or index
      cell_str = cell_str[:max_widths[i]-3] + '...'
    truncated_data.append(cell_str)
  return truncated_data

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

def get_assistant_vector_store_id(assistant):
  if isinstance(assistant, str):
    # if it's a name, retrieve the assistant
    assistants = get_all_assistants(client)
    for ast in assistants:
      if ast.name == assistant:
        assistant = ast
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
      vector_store_id = get_assistant_vector_store_id(assistant)
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
    vector_store_id = get_assistant_vector_store_id(assistant)
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
    for vector_store in vector_stores:
      if vector_store.name == vector_store or vector_store.id == vector_store:
        vector_store = vector_store
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

  if isinstance(vector_store, str):
    # if it's a name, retrieve the vector store
    vector_stores = get_all_vector_stores(client)
    for vector_store in vector_stores:
      if vector_store.name == vector_store:
        vector_store = vector_store
        break

  if not vector_store:
    raise ValueError(f"Vector store '{vector_store}' not found")

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
  
# ----------------------------------------------------- END: Vector stores ----------------------------------------------------

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
def delete_failed_and_unused_files(client):
  function_name = 'Delete failed and unused files'
  start_time = log_function_header(function_name)

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

  log_function_footer(function_name, start_time)

def delete_vector_stores_not_used_by_assistants(client, until_date_created):
  function_name = 'Delete vector stores not used by assistants'
  start_time = log_function_header(function_name)

  all_vector_stores = get_all_vector_stores(client)
  all_assistant_vector_store_ids = get_all_assistant_vector_store_ids(client)
  vector_stores_not_used_by_assistants = [vs for vs in all_vector_stores if vs.id not in all_assistant_vector_store_ids and datetime.datetime.fromtimestamp(vs.created_at) <= until_date_created]

  for vs in vector_stores_not_used_by_assistants:
    print(f"  Deleting vector store ID={vs.id} '{vs.name}' ({format_timestamp(vs.created_at)})...")
    client.vector_stores.delete(vs.id)

  log_function_footer(function_name, start_time)

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
        try: client.files.delete(file_id=file.id)
        except Exception as e:
          print(f"      WARNING: Failed to delete file ID={file.id} ({format_timestamp(file.created_at)}). The file is probably already deleted in the global file storage.")
    client.vector_stores.delete(vs.id)
  else:
    print(f"  Vector store '{name}' not found.")

# ----------------------------------------------------- END: Cleanup ----------------------------------------------------------
