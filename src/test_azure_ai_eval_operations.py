import os
from datetime import datetime
from azure.identity import DefaultAzureCredential
from azure.ai.evaluation._common.onedp import AIProjectClient
from azure.ai.projects import AIProjectClient as ProjectClient
from azure.ai.evaluation._common.onedp.models._models import (Evaluation, InputDataset, EvaluatorConfiguration)
from azure.ai.projects.models._patch_evaluations import EvaluatorIds
from azure.core.exceptions import ResourceNotFoundError

azure_ai_foundry_project_endpoint = os.environ["AZURE_AI_FOUNDRY_PROJECT_ENDPOINT"]
azure_openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", os.environ.get("AZURE_AI_SERVICES_ENDPOINT", ""))
azure_openai_api_key = os.environ["AZURE_OPENAI_API_KEY"]
azure_openai_eval_model_deployment_name = os.environ["AZURE_OPENAI_EVAL_MODEL_DEPLOYMENT_NAME"]

# Validate that we have an Azure OpenAI endpoint
if "openai.azure.com" not in azure_openai_endpoint:
  print(f"Warning: Model endpoint '{azure_openai_endpoint}' may not be a valid Azure OpenAI endpoint.")
  print("Expected format: https://your-resource-name.openai.azure.com/")
  print("Please set AZURE_OPENAI_ENDPOINT environment variable to your Azure OpenAI endpoint.")

# Create both clients - evaluation client for running evaluations, project client for dataset operations
eval_client = AIProjectClient(endpoint=azure_ai_foundry_project_endpoint, credential=DefaultAzureCredential())
project_client = ProjectClient(endpoint=azure_ai_foundry_project_endpoint, credential=DefaultAzureCredential())

# 1) Upload your JSONL as a dataset version (only if it doesn't exist)
filename = "Eval_Calibration_01_MathScoreModel.jsonl"
file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", filename)
dataset_name = filename.replace(".", "_")
dataset_version = "1.0"

# Check if dataset version already exists
try:
  existing_dataset = eval_client.datasets.get_version(name=dataset_name, version=dataset_version)
  print(f"Dataset {dataset_name} version {dataset_version} already exists, using existing dataset")
  dataset = existing_dataset
except ResourceNotFoundError:
  print(f"Dataset {dataset_name} version {dataset_version} not found, uploading new dataset")
  # In Azure, assign the role 'Azure AI Project Manager' to your user or Service Principal or Managed Identity
  dataset = project_client.datasets.upload_file(name=dataset_name, version=dataset_version, file_path=file_path)
  print(f"Dataset uploaded successfully: {dataset.name}")

data_id = dataset.id

# 2) Configure evaluator
# Use exact field names from QA evaluator signature: query, response, context, ground_truth
evaluators = {
    "relevance": EvaluatorConfiguration(
        id=EvaluatorIds.QA.value,
        init_params={"deployment_name": azure_openai_eval_model_deployment_name},
        data_mapping={
            "query": "${data.query}",
            "response": "${data.response}",
            "context": "${data.context}",
            "ground_truth": "${data.ground_truth}",
        },
    )
}

# 3) Submit the cloud evaluation (dataset already contains responses -> no target)
evaluation = Evaluation(
    display_name=f"QA Eval - {dataset_name} ({datetime.now().strftime('%Y-%m-%d %H:%M')})",
    description="Grades existing responses in JSONL",
    data=InputDataset(id=data_id),
    evaluators=evaluators,
)

resp = eval_client.evaluations.create_run(
    evaluation,
    headers={"model-endpoint": azure_openai_endpoint, "api-key": azure_openai_api_key},
)

print("Evaluation name:", resp.display_name)
print("Status:", resp.status)
# Tip: poll with client.evaluations.get(resp.name) until Completed
