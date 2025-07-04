from dotenv import load_dotenv
from openai_backendtools import *

load_dotenv()

# ----------------------------------------------------- START: Main -----------------------------------------------------------
if __name__ == '__main__':
  openai_service_type = os.getenv("OPENAI_SERVICE_TYPE", "openai")
  azure_openai_use_key_authentication = os.getenv("AZURE_OPENAI_USE_KEY_AUTHENTICATION", "false").lower() in ['true']

  if openai_service_type == "openai":
    client = create_openai_client()
  elif openai_service_type == "azure_openai":
    client = create_azure_openai_client(azure_openai_use_key_authentication)

  # delete_expired_vector_stores(client)

  # delete_duplicate_files_in_vector_stores(client)

  # USE WITH CAUTION! This will delete all non-assistant vector stores older than 10 days. Including those used in current conversations.
  # -------------------------------------------------------------------------------------------------
  # delete_vector_stores_not_used_by_assistants(client, datetime.datetime.now() - datetime.timedelta(days=10))

  # Run this after you have deleted vector stores to remove unused files
  # -------------------------------------------------------------------------------------------------
  # delete_failed_and_unused_files(client)

  # delete_vector_store_by_name(client, "test_vector_store", True)
  # client.vector_stores.delete("vs_67b0ca3da1fc819186fc791943fce1a3")
  # delete_vector_store_by_id(client, "vs_67b0ca3da1fc819186fc791943fce1a3", True)

  # delete_assistant_by_name(client, "test_assistant")
  # client.beta.assistants.delete("asst_bImGzB7olqLzO177ydqvRQNE")

  # USE WITH CAUTION! This will delete all stored files. Including those used in current conversations.
  # -------------------------------------------------------------------------------------------------
  # delete_files(client, get_all_files(client))

  # Example: Find files with specific filename across all vector stores
  # -------------------------------------------------------------------------------------------------
  # filename = "ArilenaDrovikCV.pdf"
  # files_found = find_files_in_all_vector_stores_by_filename(client, [filename])
  # print("-"*140)
  # print(f"{len(files_found)} files found with name '{filename}':")
  # if filename in files_found and files_found[filename]:
  #   for file in files_found[filename]:
  #     for vs in file['vector_stores']:
  #       print(f"  Vector store '{vs['vector_store_name']}' (ID={vs['vector_store_id']}), File ID={file['file_id']}")
  # else:
  #   print("No files found.")
  # print("-"*140)

  # USE WITH CAUTION! This will delete all files with specific filename across all vector stores. 
  # If dry_run is True, it will only show what files would be deleted.
  # If delete_files_in_global_storage is True, it will also delete the files from global storage.
  # -------------------------------------------------------------------------------------------------
  # filenames = ["ArilenaDrovikCV.pdf", "Publications1.md"]
  # files_deleted = delete_files_in_all_vector_stores_by_filename(client, filenames, dry_run=True, delete_files_in_global_storage=True)

  # USE WITH CAUTION! This will delete all files of a specific type in a vector store.
  # If dry_run is True, it will only show what files would be deleted.
  # If delete_files_in_global_storage is True, it will also delete the files from global storage.
  # -------------------------------------------------------------------------------------------------
  # vector_store_id = "vs_1iPc8a1Js8QqAW55Ld4BK1MY"
  # files_deleted = delete_files_in_vector_store_by_file_type(client, vector_store_id, ["pdf","md"], dry_run=True, delete_files_in_global_storage=True)

# ----------------------------------------------------- END: Main -------------------------------------------------------------
