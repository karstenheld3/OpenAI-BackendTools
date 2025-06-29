from dotenv import load_dotenv
from openai_backendtools import *

load_dotenv()

# ----------------------------------------------------- START: Listings -------------------------------------------------------

# Since console out will trim the output due to max char limit, we will only show the first 25 and last 25 files
def truncate_list_if_too_long(lines):
  if len(lines) > 50:
    # Create new collection with only the first 25 and the last 25 files, with empty row in the middle
    class EmptyRow: pass
    lines = lines[:25] + [EmptyRow()] + lines[-25:]
  return lines

# Display all files with top row showing total count and metrics
def list_all_files(client):
  all_files = get_all_files(client)
  # Get file metrics
  metrics = get_filelist_metrics(all_files)
  metrics_str = ", ".join([f"{v} {k}" for k, v in metrics.items()])
  total_size_in_bytes = sum([f.bytes for f in all_files]) 
  # Display the total files count and the formatted table
  print(f"Total files: {len(all_files)} using {format_filesize(total_size_in_bytes)} ({metrics_str}). Showing first 25 and last 25 files.")
  print("-"*140)
  print(format_files_table(truncate_list_if_too_long(all_files)))
  print("\n")
  return all_files

# Display the vector stores with top row showing total count and expired count
def list_vector_stores(client):
  all_vector_stores = get_all_vector_stores(client)
  all_vector_stores_expired = [v for v in all_vector_stores if getattr(v, 'status', None) == 'expired']
  total_usage_bytes = sum([vs.usage_bytes for vs in all_vector_stores if hasattr(vs, 'usage_bytes')])
  print(f"Total vector stores: {len(all_vector_stores)} ({len(all_vector_stores_expired)} expired, {format_filesize(total_usage_bytes)} total storage)")
  print("-"*140)
  print(format_vector_stores_table(truncate_list_if_too_long(all_vector_stores)))
  print("\n")
  return all_vector_stores
  
# Display the files used by vector stores with top row showing total count and metrics
def list_files_used_by_vector_stores(client):
  files_used_by_vector_stores = get_all_files_used_by_vector_stores(client)
  metrics = get_filelist_metrics(files_used_by_vector_stores)
  metrics_str = ", ".join([f"{v} {k}" for k, v in metrics.items()])
  print(f"Total files in vector stores: {len(files_used_by_vector_stores)} ({metrics_str})")
  print("-"*140)
  print(format_files_table(truncate_list_if_too_long(files_used_by_vector_stores)))
  print("\n") 
  return files_used_by_vector_stores

# Display the assistants with top row showing total count
def list_assistants(client): 
  all_assistants = get_all_assistants(client)
  print(f"Total assistants: {len(all_assistants)}")
  print("-"*140)
  print(format_assistants_table(truncate_list_if_too_long(all_assistants)))
  print("\n")
  return all_assistants

# Display the files not used by vector stores with top row showing total count
def list_files_not_used_by_vector_stores(client, all_files):
  if not all_files: all_files = get_all_files(client)
  # filter out all files that do not have purpose = 'assistants' and show files not used in vector stores
  assistant_files = [f for f in all_files if getattr(f, 'purpose', None) == 'assistants']
  unused_vector_store_files = [f for f in all_files if f.id not in [file.id for file in assistant_files]]
  print(f"Total files NOT used in vector stores: {len(unused_vector_store_files)}")
  print("-"*140)
  print(format_files_table(truncate_list_if_too_long(unused_vector_store_files)))
  print("\n")
  return unused_vector_store_files

# Display the files used by assistants with top row showing total count
def list_files_used_by_assistants(client):
  files_used_by_assistant_vector_stores = get_files_used_by_assistant_vector_stores(client)
  metrics = get_filelist_metrics(files_used_by_assistant_vector_stores)
  metrics_str = ", ".join([f"{v} {k}" for k, v in metrics.items()])
  print(f"Total files used by assistants: {len(files_used_by_assistant_vector_stores)} ({metrics_str})")
  print("-"*140)
  print(format_files_table(truncate_list_if_too_long(files_used_by_assistant_vector_stores)))
  print("\n")
  return files_used_by_assistant_vector_stores

# Display the files not used by assistants with top row showing total count
def list_files_not_used_by_assistants(client, files_used_by_vector_stores):
  if not files_used_by_vector_stores: files_used_by_vector_stores = get_all_files_used_by_vector_stores(client)
  files_not_used_by_assistants = [f for f in all_files if f.id not in files_used_by_vector_stores]
  metrics = get_filelist_metrics(files_not_used_by_assistants)
  metrics_str = ", ".join([f"{v} {k}" for k, v in metrics.items()])
  print(f"Total files NOT used by assistants: {len(files_not_used_by_assistants)} ({metrics_str})")
  print("-"*140)
  print(format_files_table(truncate_list_if_too_long(files_not_used_by_assistants)))
  print("\n")
  return files_not_used_by_assistants
# ----------------------------------------------------- END: Listings ---------------------------------------------------------


# ----------------------------------------------------- START: Main -----------------------------------------------------------

if __name__ == '__main__':
  openai_service_type = os.getenv("OPENAI_SERVICE_TYPE", "openai")
  azure_openai_use_key_authentication = os.getenv("AZURE_OPENAI_USE_KEY_AUTHENTICATION", "false").lower() in ['true']

  if openai_service_type == "openai":
    client = create_openai_client()
  elif openai_service_type == "azure_openai":
    client = create_azure_openai_client(azure_openai_use_key_authentication)

  all_vector_stores = list_vector_stores(client)

  all_assistants = list_assistants(client)

  all_files = list_all_files(client)

  files_used_by_vector_stores = list_files_used_by_vector_stores(client)

  list_files_not_used_by_vector_stores(client, all_files)

  files_used_by_assistants = list_files_used_by_assistants(client)

  list_files_not_used_by_assistants(client, files_used_by_vector_stores)


# ----------------------------------------------------- END: Main -------------------------------------------------------------
