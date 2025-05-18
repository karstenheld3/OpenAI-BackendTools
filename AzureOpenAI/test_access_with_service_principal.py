import os
import logging
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
load_dotenv()

###
# This script will test if the service principal configured in the .env file can access the Azure OpenAI service in the .env file.
#
# What is a service principal? An account (AZURE_CLIENT_ID) to be used by a computer with a known password (AZURE_CLIENT_SECRET).
# What is a tenant? The Azure Active Directory (AAD) tenant that the service principal belongs to (AZURE_TENANT_ID).
# What is a client ID? The unique identifier of the service principal (AZURE_CLIENT_ID).
# What is a client secret? The password of the service principal (AZURE_CLIENT_SECRET).
#
# There is two types of Azure Open AI endpoints. The difference is in the URL ('cognitiveservices' vs. 'openai'):
#    1) Azure AI Services (OpenAI + other ML services):
#       - https://<your_open_ai_service_name>.cognitiveservices.azure.com/
#       - or https://<your_azure_ai_fondry_open_ai_service>.openai.azure.com/
#    2) Azure OpenAI Service (OpenAI only):
#       - https://<your_open_ai_service_name>.openai.azure.com/
#
# You will have to set the following environment variables in the .env file:
#    AZURE_OPENAI_ENDPOINT=https://<your_open_ai_service_name>.openai.azure.com/
#    AZURE_TENANT_ID=1111111-2222-3333-4444-555555555555
#    AZURE_CLIENT_ID=6666666-7777-8888-9999-000000000000 # App registration ID
#    AZURE_CLIENT_SECRET=<your_app_registration_secret>
#    AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
#    AZURE_OPENAI_MODEL_NAME=gpt-4o-mini
#    AZURE_OPENAI_API_VERSION=2024-12-01-preview
###

endpoint = os.environ.get('AZURE_OPENAI_ENDPOINT')
model_name = os.environ.get('AZURE_OPENAI_MODEL_NAME')
deployment = os.environ.get('AZURE_OPENAI_DEPLOYMENT')
api_version = os.environ.get('AZURE_OPENAI_API_VERSION')

# Uncomment the following lines if you want to use a different endpoint
# endpoint = "https://<your_open_ai_service_name>.openai.azure.com/"
# model_name = "gpt-4o-mini"
# deployment = "gpt-4o-mini"
# api_version = "2024-12-01-preview"

# Set up logging before creating the credential
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('azure')
logger.setLevel(logging.DEBUG)

# Gets token provider which tries to create based on .env file in this order:
# 1) Service Principal (AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET)
# 2) Workload Identity Credential (AZURE_TENANT_ID, WORKLOAD_IDENTITY_VARS, AZURE_FEDERATED_TOKEN_FILE)
# 3) Managed Identity (AZURE_TENANT_ID, AZURE_CLIENT_ID)
# 4) Windows: User signed in with a Microsoft application (or AZURE_USERNAME)
# 5) Azure CLI
# 6) Azure PowerShell
# 7) Azure Developer CLI
cred = DefaultAzureCredential()
token_provider = get_bearer_token_provider(cred, "https://cognitiveservices.azure.com/.default")

# Reset logging level
logger.setLevel(logging.ERROR)

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    azure_ad_token_provider=token_provider,
)

question = "Who was the 3rd roman emperor? Give me just the name and the time span he reigned."
response = client.chat.completions.create(
    messages=[
        { "role": "system", "content": "You are history professor." },
        { "role": "user", "content": question }
    ],
    max_tokens=200, temperature=1.0, top_p=0.1,
    model=deployment
)
print(f"Question: {question}")
print(f"Answer: {response.choices[0].message.content}")

# Output should look like this:
# 
# INFO:azure.identity._credentials.environment:Environment is configured for ClientSecretCredential
# INFO:azure.identity._credentials.managed_identity:ManagedIdentityCredential will use IMDS with client_id: 6666666-7777-8888-9999-000000000000
# INFO:httpx:HTTP Request: POST https://<your_open_ai_service_name>.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-12-01-preview "HTTP/1.1 200 OK"
# Question: Who was the 3rd roman emperor? Give me just the name and the time span he reigned.
# Answer: The 3rd Roman Emperor was Caligula, who reigned from AD 37 to AD 41.