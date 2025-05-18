# OpenAI-BackendTools
A collection of tools to test, operate and maintain Azure OpenAI backends

## AzureOpenAI

| Source       | Links                                                        |                                                              |                                                              |                                                              |                                                              |
| ------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Open AI Docs | [Models](https://platform.openai.com/docs/models)            | [Pricing](https://platform.openai.com/docs/pricing)          | [Cookbook](https://cookbook.openai.com/)                     | [Assistants](https://platform.openai.com/docs/assistants/overview) | [Agents](https://platform.openai.com/docs/guides/agents)     |
| Open AI Docs | [Built-In tools](https://platform.openai.com/docs/guides/agents) | [Evals](https://platform.openai.com/docs/guides/evals)       | [Fine-tuning](https://platform.openai.com/docs/guides/fine-tuning) | [Retrieval / Search](https://platform.openai.com/docs/guides/retrieval) | [Actions](https://platform.openai.com/docs/actions/introduction) |
| Open AI API  | [Responses](https://platform.openai.com/docs/api-reference/responses) | [Completions](https://platform.openai.com/docs/api-reference/chat) | [Files](https://platform.openai.com/docs/api-reference/files) | [Vector stores](https://platform.openai.com/docs/api-reference/vector-stores) | [Assistants](https://platform.openai.com/docs/api-reference/assistants) |



### Service Types

There is two types of Azure Open AI endpoints. The difference is in the URL (`cognitiveservices` vs. `openai`).

1) **Azure AI Services** (OpenAI + other ML services): `https://<your_open_ai_service_name>.cognitiveservices.azure.com/`
   or
   `https://<your_azure_ai_fondry_open_ai_service>.openai.azure.com/`

2) **Azure OpenAI Service** (OpenAI only):
   `https://<your_open_ai_service_name>.openai.azure.com/`

### Access types

- **Service Principal** - In `.env` file:  `AZURE_CLIENT_ID` and`AZURE_CLIENT_SECRET`.
- **Managed Identity**  - In `.env` file:  `AZURE_CLIENT_ID`
- **API Key** - In `.env` file:  `AZURE_OPENAI_API_KEY`

### Access roles and restrictions

Source: [https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/role-based-access-control](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/role-based-access-control)

1. Open AI Service - **API key access** - read / write to everything except:

   - Usage Metrics (quota and usage viewing)
   - Billing (cost/pricing info)

2. Open AI Service - **Service Principal or Managed Identity**

   - **Cognitive Services OpenAI User** role:

     List <u>models</u>, use completions ([legacy](https://platform.openai.com/docs/guides/completions)), create / list / delete / use <u>assistants</u> ([legacy](https://platform.openai.com/docs/assistants/whats-new#march-2025)), create / list / delete / use <u>response models</u>, create <u>images</u> , upload <u>files</u>, create <u>vector stores</u>, create <u>embeddings</u>, access <u>realtime api</u>

   - **Cognitive Services OpenAI Contributor** role:
     Everything from Cognitive Services OpenAI User + delete <u>files</u>, delete <u>vector stores</u>, manage <u>fine-tunings</u>, create / use <u>evals</u>, create <u>batch</u> jobs, create / manage <u>fine-tunings</u>, 

   - **Cognitive Services Usages Reader**: access <u>usage metrics</u>

   - **Cost Management Reader** or **Owner/Contributor**: view <u>cost and billing</u>

   - **Owner** or **User Access Administrator**: modify <u>role assignments</u>

### Terminology

- **What is a service principal?**
  An Azure App Registration with a client id (`AZURE_CLIENT_ID`) -  also known as "app id" - to be used by a computer with a known password (`AZURE_CLIENT_SECRET`). In PowerShell the App Registration and the Service Principal can be created separately. The service principal is needed to assign RBAC roles for services. RBAC = Role-Based Access Control.

  ```powershell
  # Connect to Azure
  Connect-AzAccount
  
  # Create the application
  $app = New-AzADApplication -DisplayName "my-app" -IdentifierUris "http://my-app" -Password "PlainTextPassword123!"
  
  # Create the Service Principal
  $sp = New-AzADServicePrincipal -ApplicationId $app.ApplicationId
  
  # Assign a role
  New-AzRoleAssignment -RoleDefinitionName "Contributor" -ServicePrincipalName $sp.ApplicationId
  ```

  

- **What is a managed identity?**
  An account (`AZURE_CLIENT_ID`) to be used by a computer with password automatically rotated by Azure AD / Entra ID.

  An **Azure AI Foundry Hub** will automatically create a managed identity for itself that is then assigned the **Contributor** role on all connected Azure Open AI Services and Azure AI Services.

  In PowerShell you can create a managed identity like this for a virtual machine:

  ```powershell
  # Login to Azure
  Connect-AzAccount
  
  # Enable system-assigned identity on a Virtual Machine
  Set-AzVM -ResourceGroupName "myResourceGroup" -Name "myVM" -IdentityType SystemAssigned
  ```

  This managed identity can be assigned the **Cognitive Services OpenAI Contributor** role for an Azure Open AI Service. In this case you only need to store the `AZURE_CLIENT_ID` in the .env file and use the `azure.identity` Python library for authentication. All subsequent code will be able to access the Azure Open AI Service.

- **What is a tenant?**
  The Azure Active Directory (AAD) tenant that the service principal, the app registrations, and the managed identities belongs to (`AZURE_TENANT_ID`).

- **What is a client ID?** Also known as "**Application ID**" or "**App Registration ID**".
  The unique identifier of the service principal or managed identity (`AZURE_CLIENT_ID`).

- **What is a client secret?**
  The password of the service principal (`AZURE_CLIENT_SECRET`).


### Requirements / Packages
- azure-identity 1.23.0 ([releases](https://pypi.org/project/azure-identity/))
- requests 2.32.3 ([releases](https://pypi.org/project/requests/))
- python-dotenv 1.1.0 ([releases](https://pypi.org/project/python-dotenv/))
- openai version 1.79.0 ([releases](https://github.com/openai/openai-python/tags))

### Files
- files_tool.py

