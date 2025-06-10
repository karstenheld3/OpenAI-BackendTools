from dataclasses import dataclass
from dotenv import load_dotenv
from openai_backendtools import *
from test_rag_operations import *
import time
import json
import os
import datetime

load_dotenv()

# ----------------------------------------------------- START: Evals ----------------------------------------------------------

Batch01 = [
  { "item" : { "input": "Who is Arilena Drovik?", "reference": "Arilena Drovik is molecular biologist and geneticist. She is a Professor of Molecular Genetics and principal investigator at the Department of Molecular Biology, Lund University, Sweden. She holds a PhD in Molecular Biology from University of Cambridge, UK."} }
  ,{ "item" : { "input": "What was the title of Arilena Drovik's dissertation?", "reference": "Epigenetic Modulators of Gene Expression in Early Development"} }
  ,{ "item" : { "input": "What was the title of Arilena Drovik's first scientific publication and where and when was it published?", "reference": "The title of Arilena Drovik's first scientific article was 'CRISPR-Cas9: Revolutionizing Genome Editing in Modern Molecular Biology'. It was published by the 'The CRISPR Journal' in 2015."} }
  ,{ "item" : { "input": "With whom did Arilena Drovik collaborate on scientific publications?", "reference":
"""Between 2018 and 2020 Arilena Drovik collaborated with the following researchers:
- L. Fernandez and H.S. Wong on the 2018 article 'CRISPR Screening for Essential Non-Coding Elements'
- R. Novak and other authors on the 2020 article 'Next-Generation CRISPR Tools for Precision Genome Engineering'
"""} }
]

# ----------------------------------------------------- END: Evals ------------------------------------------------------------


# ----------------------------------------------------- START: Tests ----------------------------------------------------------

# Gets all answers for the 'input' in all items using response models and stores them in 'output_text' of each items
def get_answers_from_model_and_return_items(client, vector_store_id, model, items):
  function_name = 'Get answers from model and add in items'
  start_time = log_function_header(function_name)

  for idx, item in enumerate(items, 1):
    input = item['item']['input']
    print(f"    [ {idx} / {len(items)} ] Query: {input}")
    response = retry_on_openai_errors(lambda: client.responses.create(
      model=model
      ,input=input
      ,tools=[{ "type": "file_search", "vector_store_ids": [vector_store_id] }]
      ,temperature=0
    ), indentation=4)
    output_text = response.output_text
    print(f"      Response: {truncate_string(output_text,80)}")
    item['item']['output_text'] = output_text

  log_function_footer(function_name, start_time)
  return items

# ----------------------------------------------------- END: Tests ------------------------------------------------------------


# ----------------------------------------------------- START: Main -----------------------------------------------------------

if __name__ == '__main__':
  openai_service_type = os.getenv("OPENAI_SERVICE_TYPE", "openai")
  azure_openai_use_key_authentication = os.getenv("AZURE_OPENAI_USE_KEY_AUTHENTICATION", "false").lower() in ['true']
  openai_model_name = os.getenv("AZURE_OPENAI_MODEL_DEPLOYMENT_NAME", "gpt-4o-mini")

  if openai_service_type == "openai":
    client = create_openai_client()
  elif openai_service_type == "azure_openai":
    client = create_azure_openai_client(azure_openai_use_key_authentication)

  @dataclass
  class EvalParams: vector_store_name: str; folder_path: str; model: str; items: list

  params = EvalParams(
    vector_store_name="test_vector_store",
    folder_path="./RAGFiles/Batch01",
    model = openai_model_name,
    items = Batch01
  )
  # Step 1: Create vector store by uploading files
  test_vector_store_with_files = create_test_vector_store_with_files(client,params.vector_store_name, params.folder_path)

  # Step 2: Get answers from model and store in items
  params.items = get_answers_from_model_and_return_items(client, test_vector_store_with_files.vector_store.id, params.model, params.items)

  # Step 3: Test eval using graders
  # test_similarity_grader(client, params.items)

  print("-"*140)

  # Step 4: Delete vector store including all files
  delete_vector_store_by_name(client, params.vector_store_name, True)

# ----------------------------------------------------- END: Main -------------------------------------------------------------
