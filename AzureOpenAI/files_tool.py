import os
import openai
import datetime
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
load_dotenv()

# ----------------------------------------------------- START: Utilities ---------------------------------------------------------------
# Create an Azure OpenAI client using either managed identity or API key authentication.
def create_openai_client(use_managed_identity=False):
  endpoint = os.environ.get('AZURE_OPENAI_ENDPOINT')
  api_version = os.environ.get('AZURE_OPENAI_API_VERSION')
  
  if use_managed_identity:
    # Use managed identity (service principal) authentication
    cred = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(cred, "https://cognitiveservices.azure.com/.default")
    
    # Create client with token provider
    return openai.AzureOpenAI( api_version=api_version, azure_endpoint=endpoint, azure_ad_token_provider=token_provider )
  else:
    # Use API key authentication
    api_key = os.environ.get('AZURE_OPENAI_API_KEY')
    
    # Create client with API key
    return openai.AzureOpenAI(
      api_version=api_version,
      azure_endpoint=endpoint,
      api_key=api_key
    )

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

def get_files_used_by_assistants(client):
  # Get all assistants and their vector stores
  all_assistants = get_all_assistants(client)
  all_vector_stores = get_all_vector_stores(client)
  all_assistant_vector_stores = [get_assistant_vector_store(a) for a in all_assistants]
  
  # Dictionary to store unique files to avoid duplicates
  all_files = []
  processed_file_ids = set()
  
  # For each vector store used by assistants
  for vector_store_id in all_assistant_vector_stores:
    if not vector_store_id:
      continue
      
    # Find the vector store object
    vector_store = next((vs for vs in all_vector_stores if vs.id == vector_store_id), None)
    if not vector_store:
      continue
      
    # Get all files in this vector store
    vector_store_files = get_vector_store_files(client, vector_store)
    
    # Filter out failed and cancelled files, and add new ones to our collection
    for file in vector_store_files:
      if (getattr(file, 'id', None) and 
          getattr(file, 'status', '') not in ['failed', 'cancelled'] and
          file.id not in processed_file_ids):
        all_files.append(file)
        processed_file_ids.add(file.id)
  
  return all_files

def get_files_used_by_vector_stores(client):
  # Get all vector stores
  all_vector_stores = get_all_vector_stores(client)
  
  # Dictionary to store unique files to avoid duplicates
  all_files = []
  processed_file_ids = set()
  
  # For each vector store used by assistants
  for vector_store in all_vector_stores:
    if not vector_store:
      continue
      
    # Get all files in this vector store
    vector_store_files = get_vector_store_files(client, vector_store)
    
    # Filter out failed and cancelled files, and add new ones to our collection
    for file in vector_store_files:
      if (getattr(file, 'id', None) and 
          getattr(file, 'status', '') not in ['failed', 'cancelled'] and
          file.id not in processed_file_ids):
        all_files.append(file)
        processed_file_ids.add(file.id)
  
  return all_files

# ----------------------------------------------------- END: Utilities ---------------------------------------------------------------

# ----------------------------------------------------- START: Files -----------------------------------------------------------------
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
  if not files: return '(No files found)'
  
  # Define headers and max column widths
  headers = ['Index', 'ID', 'Filename', 'Size', 'Created', 'Status', 'Purpose']
  max_widths = [6, 40, 40, 10, 19, 12, 15]  # Maximum width for each column
  
  # Initialize column widths with header lengths, but respect max widths
  col_widths = [min(len(h), max_widths[i]) for i, h in enumerate(headers)]
  
  rows = []
  for idx, f in enumerate(files):
    # Prepare row data
    row_data = [
      "..." if not hasattr(f, 'index') else f"{f.index:05d}",
      getattr(f, 'id', '...'),
      getattr(f, 'filename', '...'), 
      format_filesize(getattr(f, 'bytes', None)),
      format_timestamp(getattr(f, 'created_at', None)), 
      getattr(f, 'status', '...'), 
      getattr(f, 'purpose', '...')
    ]
    
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
# ----------------------------------------------------- END: Files -----------------------------------------------------------------

# ----------------------------------------------------- START: Assistants ----------------------------------------------------------

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
  max_widths = [6, 31, 25, 11, 19, 36]  # Maximum width for each column
  
  # Initialize column widths with header lengths, but respect max widths
  col_widths = [min(len(h), max_widths[i]) for i, h in enumerate(headers)]
  
  rows = []
  for idx, a in enumerate(assistants):
    # Prepare row data
    row_data = [
      "..." if not hasattr(a, 'index') else f"{a.index:04d}",
      getattr(a, 'id', '...'),
      getattr(a, 'name', '...'), 
      getattr(a, 'model', '...'),
      format_timestamp(getattr(a, 'created_at', None)), 
      getattr(a, 'vector_store_id', 'None')
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

# ----------------------------------------------------- END: Assistants ----------------------------------------------------------

# ----------------------------------------------------- START: Vector stores -----------------------------------------------------

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
  # Get the vector store ID
  vector_store_id = getattr(vector_store, 'id', None)
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
  
  return all_files


# Gets the file metrics for a vector store
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
  headers = ['Index', 'ID', 'Name','Created', 'Status', 'Files (completed, in_progress, failed, cancelled)']
  max_widths = [6, 36, 40, 19, 12, 50]  # Maximum width for each column
  
  # Initialize column widths with header lengths, but respect max widths
  col_widths = [min(len(h), max_widths[i]) for i, h in enumerate(headers)]
  
  rows = []
  for idx, vs in enumerate(vector_stores):
    # Prepare row data
    # Get file metrics
    metrics = get_vector_store_file_metrics(vs)
    files_str = f"Total: {metrics['total']} (✓ {metrics['completed']}, ⌛ {metrics['in_progress']}, ❌ {metrics['failed']}, ⏹ {metrics['cancelled']})" if metrics['total'] > 0 else '...' 
    
    row_data = [
      "..." if not hasattr(vs, 'index') else f"{vs.index:05d}",
      getattr(vs, 'id', '...'),
      getattr(vs, 'name', '...'), 
      format_timestamp(getattr(vs, 'created_at', None)), 
      getattr(vs, 'status', '...'),
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
    # Aort files so newest files are on top
    files.sort(key=lambda f: f.created_at, reverse=True)
    # Add filenames from all_files to files
    for f in files:
      # If error, use datetime timestamp as filename. Can happen if vector store got new file just after all_files was loaded.
      try: f.filename = all_files[f.id].filename
      except: f.filename = str(datetime.datetime.now().timestamp())

    # create dictionary with filename as key and list of files as value
    files_by_filename = {}
    for f in files:
      if f.filename not in files_by_filename:
        files_by_filename[f.filename] = []
      files_by_filename[f.filename].append(f)
    
    # find files with duplicate filenames
    duplicate_files = []
    for filename, files in files_by_filename.items():
      if len(files) > 1:
        # Omit first file (the newest), keep all others
        duplicate_files.extend(files[1:])

    for file in duplicate_files:
      print(f"    Deleting duplicate file ID={file.id} '{file.filename}' ({format_timestamp(file.created_at)})...")
      client.vector_stores.files.delete(file_id=file.id, vector_store_id=vs.id)

  end_time = datetime.datetime.now(); secs = (end_time - start_time).total_seconds()
  parts = [(int(secs // 3600), 'hour'), (int((secs % 3600) // 60), 'min'), (int(secs % 60), 'sec')]
  total_time = ', '.join(f"{val} {unit}{'s' if val != 1 else ''}" for val, unit in parts if val > 0)
  print(f"[{end_time.strftime('%Y-%m-%d %H:%M:%S')}] END: Delete duplicate files in vector stores ({total_time}).")

# ----------------------------------------------------- END: Vector stores -----------------------------------------------------

# ----------------------------------------------------- START: Main -----------------------------------------------------
if __name__ == '__main__':
  use_managed_identity = True
  client = create_openai_client(use_managed_identity)

  # delete_expired_vector_stores(client)
  
  # delete_duplicate_files_in_vector_stores(client)
  
  
  # Get all files with pagination handling
  all_files = get_all_files(client)

  # Since console out will trim the output due to max char limit, we will only show the first 25 and last 25 files
  if len(all_files) > 50:
    # Create new collection with only the first 25 and the last 25 files, with empty row in the middle
    class EmptyRow: pass
    all_files_trimmed = all_files[:25] + [EmptyRow()] + all_files[-25:]
  else:
    all_files_trimmed = all_files

  # Display the total files count and the formatted table
  print(f"Total files: {len(all_files)}. Showing first 25 and last 25 files.")
  print("-"*80)
  print(format_files_table(all_files_trimmed))

  print("\n")
  # Display the assistants total count and the formatted table
  all_vector_stores = get_all_vector_stores(client)
  all_vector_stores_expired = [v for v in all_vector_stores if getattr(v, 'status', None) == 'expired']
  print(f"Total vector stores: {len(all_vector_stores)} ({len(all_vector_stores_expired)} expired)")
  print(format_vector_stores_table(all_vector_stores))

  print("\n")
  # Display the files in the first vector store
  vector_store_files = get_vector_store_files(client, all_vector_stores[0])
  print(f"Total files in first vector store '{all_vector_stores[0].name}': {len(vector_store_files)}.")

  print("\n")
  # Display the assistants total count and the formatted table
  all_assistants = get_all_assistants(client)
  print(f"Total assistants: {len(all_assistants)}.")
  print(format_assistants_table(all_assistants))

  print("\n")
  # Display the files used by vector stores
  files_used_by_vector_stores = get_files_used_by_vector_stores(client)
  print(f"Total files in vector stores: {len(files_used_by_vector_stores)}.")

  print("\n")
  # filter out all files that do not have purpose = 'assistants'
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
  print(f"Total files not used in vector stores: {len(unused_vector_store_files)}.")
  print("-"*80)
  print(format_files_table(unused_vector_store_files_trimmed))


  print("\n")
  # Display the files used by assistants
  files_used_by_assistants = get_files_used_by_assistants(client)
  print(f"Total files used by assistants: {len(files_used_by_assistants)}.")

  print("\n")
  # filter out all files that do not have purpose = 'assistants'
  unused_assistant_files = [f for f in all_files if getattr(f, 'purpose', None) == 'assistants']
  # filter out all files not used by 
  unused_assistant_files = [f for f in all_files if f.id not in [file.id for file in files_used_by_assistants]]

  # Since console out will trim the output due to max char limit, we will only show the first 25 and last 25 files
  if len(unused_assistant_files) > 50:
    # Create new collection with only the first 25 and the last 25 files, with empty row in the middle
    class EmptyRow: pass
    unused_assistant_files_trimmed = unused_assistant_files[:25] + [EmptyRow()] + unused_assistant_files[-25:]
  else:
    unused_assistant_files_trimmed = unused_assistant_files
  print(f"Total files not used by assistants: {len(unused_assistant_files)}.")
  print("-"*80)
  print(format_files_table(unused_assistant_files_trimmed))
  
  print("\n")
  
