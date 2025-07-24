from dataclasses import dataclass
from dotenv import load_dotenv
from openai.types import vector_store
from openai_backendtools import *
from test_rag_operations import *
import os

load_dotenv()

# ----------------------------------------------------- START: Main -----------------------------------------------------------

if __name__ == '__main__':
  openai_service_type = os.getenv("OPENAI_SERVICE_TYPE", "openai")
  azure_openai_use_key_authentication = os.getenv("AZURE_OPENAI_USE_KEY_AUTHENTICATION", "false").lower() in ['true']

  if openai_service_type == "openai": client = create_openai_client()
  elif openai_service_type == "azure_openai": client = create_azure_openai_client(azure_openai_use_key_authentication)

  # Step 1: Create source vector stores 1 and 2
  source_1 = create_test_vector_store_from_folder_path(client, "Batch01", "./RAGFiles/Batch01")
  source_2 = create_test_vector_store_from_folder_path(client, "Batch02", "./RAGFiles/Batch02")

  # Step 2: Create target vector store
  target_vector_store_name = "test-vector-store"
  target_vector_store = client.vector_stores.create(name=target_vector_store_name)

  # Step 3: Replicate vector store content from source 1 and 2 to new target vector store
  source_vector_store_ids = [source_1.vector_store.id, source_2.vector_store.id]
  target_vector_store_ids = [target_vector_store.id]
  added_files, removed_files, errors = replicate_vector_store_content(client, source_vector_store_ids, target_vector_store_ids)
  print("-"*140+"\nReplication summary:")
  print_vector_store_replication_summary(target_vector_store_ids, added_files, removed_files, errors)
  print("-"*140)

  # Step 4: Delete vector stores and used files
  delete_vector_store_by_name(client, target_vector_store_name)
  delete_vector_store_by_name(client, source_1.vector_store.name, True)
  delete_vector_store_by_name(client, source_2.vector_store.name, True)
  print("-"*140)

# ----------------------------------------------------- END: Main -------------------------------------------------------------
