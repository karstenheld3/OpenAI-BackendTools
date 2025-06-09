import os
import logging
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

###
# This script will test if the endpoint and api_key in the .env file can access the Azure OpenAI service in the .env file.
#
# There is two types of Azure Open AI endpoints. The difference is in the URL ('cognitiveservices' vs. 'openai'):
#    1) Azure AI Services (OpenAI + other ML services): https://<your_open_ai_service_name>.cognitiveservices.azure.com/
#    2) Azure OpenAI Service (OpenAI only): https://<your_open_ai_service_name>.openai.azure.com/
#
# You will have to set the following environment variables in the .env file:
#    AZURE_OPENAI_ENDPOINT=https://<your_open_ai_service_name>.openai.azure.com/
#    AZURE_OPENAI_API_KEY=<your_open_ai_api_key>
#    AZURE_OPENAI_MODEL_DEPLOYMENT_NAME=gpt-4o-mini
#    AZURE_OPENAI_API_VERSION=2024-12-01-preview
###

endpoint = os.environ.get('AZURE_OPENAI_ENDPOINT')
api_key = os.environ.get('AZURE_OPENAI_API_KEY')
model_deployment_name = os.environ.get('AZURE_OPENAI_MODEL_DEPLOYMENT_NAME')
api_version = os.environ.get('AZURE_OPENAI_API_VERSION')

# Uncomment the following lines if you want to use a different endpoint
# endpoint = "https://<your_open_ai_service_name>.openai.azure.com/"
# api_key = "<your_open_ai_api_key>"
# model_name = "gpt-4o-mini"
# api_version = "2024-12-01-preview"

# Set up logging before creating the credential
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('azure')
logger.setLevel(logging.ERROR)

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=api_key
)

question = "Who was the 3rd roman emperor? Give me just the name and the time span he reigned."
response = client.chat.completions.create(
    messages=[
        { "role": "system", "content": "You are history professor." },
        { "role": "user", "content": question }
    ],
    max_tokens=200, temperature=1.0, top_p=0.1,
    model=model_deployment_name
)
print(f"Question: {question}")
print(f"Answer: {response.choices[0].message.content}")

# Output should look like this:
# 
# INFO:httpx:HTTP Request: POST https://<your_open_ai_service_name>.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-12-01-preview "HTTP/1.1 200 OK"
# Question: Who was the 3rd roman emperor? Give me just the name and the time span he reigned.
# Answer: The 3rd Roman Emperor was Caligula, who reigned from AD 37 to AD 41.