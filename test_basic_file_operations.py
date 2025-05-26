from dotenv import load_dotenv
from openai_backendtools import *

load_dotenv()

# ----------------------------------------------------- START: Tests ----------------------------------------------------------
def test_basic_file_operations(client, file_path):
  function_name = 'Basic file operations (upload, vector stores, delete)'
  start_time = log_function_header(function_name)

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

  log_function_footer(function_name, start_time)
# ----------------------------------------------------- END: Tests ------------------------------------------------------------

# ----------------------------------------------------- START: Main -----------------------------------------------------------
if __name__ == '__main__':

  openai_service_type = os.getenv("OPENAI_SERVICE_TYPE", "openai")
  azure_openai_use_key_authentication = os.getenv("AZURE_OPENAI_USE_KEY_AUTHENTICATION", "false").lower() in ['true']

  if openai_service_type == "openai":
    client = create_openai_client()
  elif openai_service_type == "azure_openai":
    client = create_azure_openai_client(azure_openai_use_key_authentication)

  test_basic_file_operations(client, "./RAGFiles/Batch01/Publications1.md")

  exit()

# ----------------------------------------------------- END: Main -------------------------------------------------------------
