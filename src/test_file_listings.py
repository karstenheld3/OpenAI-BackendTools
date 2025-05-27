from dotenv import load_dotenv
from openai_backendtools import *

load_dotenv()

# ----------------------------------------------------- START: Main -----------------------------------------------------------

openai_service_type = os.getenv("OPENAI_SERVICE_TYPE", "openai")
azure_openai_use_key_authentication = os.getenv("AZURE_OPENAI_USE_KEY_AUTHENTICATION", "false").lower() in ['true']

if openai_service_type == "openai":
  client = create_openai_client()
elif openai_service_type == "azure_openai":
  client = create_azure_openai_client(azure_openai_use_key_authentication)

# delete_expired_vector_stores(client)

# delete_duplicate_files_in_vector_stores(client)

# USE WITH CAUTION! This will delete all non-assistant vector stores older than 10 days. Including those used in current conversations.
# delete_vector_stores_not_used_by_assistants(client, datetime.datetime.now() - datetime.timedelta(days=10))

# delete_failed_and_unused_files(client)

# Get all files with pagination handling
all_files = get_all_files(client)
metrics = get_filelist_metrics(all_files)
metrics_str = ", ".join([f"{v} {k}" for k, v in metrics.items()])
total_size_in_bytes = sum([f.bytes for f in all_files]) 

# Since console out will trim the output due to max char limit, we will only show the first 25 and last 25 files
if len(all_files) > 50:
  # Create new collection with only the first 25 and the last 25 files, with empty row in the middle
  class EmptyRow: pass
  all_files_trimmed = all_files[:25] + [EmptyRow()] + all_files[-25:]
else:
  all_files_trimmed = all_files

# Display the total files count and the formatted table
print(f"Total files: {len(all_files)} using {format_filesize(total_size_in_bytes)} ({metrics_str}). Showing first 25 and last 25 files.")
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

# ----------------------------------------------------- END: Main -------------------------------------------------------------
