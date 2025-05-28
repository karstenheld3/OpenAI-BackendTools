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
  # delete_vector_stores_not_used_by_assistants(client, datetime.datetime.now() - datetime.timedelta(days=10))

  # Run this after you have deleted vector stores to remove unused files
  # delete_failed_and_unused_files(client)

  # delete_vector_store_by_name(client, "test_vector_store", True)

  # client.vector_stores.delete("vs_67b0ca3da1fc819186fc791943fce1a3")

  # delete_assistant_by_name(client, "test_assistant")
  
  # client.beta.assistants.delete("asst_bImGzB7olqLzO177ydqvRQNE")

# ----------------------------------------------------- END: Main -------------------------------------------------------------
