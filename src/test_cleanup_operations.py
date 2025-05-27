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


# ----------------------------------------------------- END: Main -------------------------------------------------------------
