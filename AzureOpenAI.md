# Azure Open AI

## Creating your .env file

The `.env` file contains

- Open AI service endpoints
- Your Open AI service API keys (if you are using key access)
- Your Client ID (if you are using managed identity or service principal access)
- Your Client Secret (if you are using service principal access)
- Your Azure tenant ID
- Your Azure Open AI deployment name, model name and API version

**Where to get this information:**

- Tenant ID: [Azure > Microsoft Entra ID > Overview](https://portal.azure.com/#view/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/~/Overview)
- Open AI endpoint and key:
  - **Azure Open AI Service** deployment ('*.openai.azure.com'):
    Azure > Resource group > Azure OpenAI > Resource Management > Keys and Endpoint
    Looks like this: `https://<your_azure_openai_endpoint>.openai.azure.com/`
  - **Azure AI Foundry** deployment ('cognitiveservices.azure.com' AND 'openai.azure.com' - both used):
    Azure AI Foundry > Your project > My assets > Models + endpoints > Deployed model (deploy one if none) > Target URI and Key
    Copy only `https://<your_azure_openai_endpoint>.cognitiveservices.azure.com/` from `https://<your_azure_openai_endpoint>.cognitiveservices.azure.com/openai/deployments/<model>/chat/completions?api-version=<version>`
  - **Azure AI Services** deployment ('cognitiveservices.azure.com' INSTEAD OF 'openai.azure.com'):
    Azure > Resource group > Azure AI services multi-service account> Resource Management > Keys and Endpoint
    Looks like this: `https://<your_azure_openai_endpoint>.cognitiveservices.azure.com/`
- Client ID (for managed identity access):
    - If not created yet: Go to your App Service or Function App or other Azure service > Identity > System assigned > On > Save > "Enable system assigned managed identity" > Yes
    - Go to your App Service or Function App or other Azure service > Identity > System assigned > Copy the Object ID
    - Go to Azure > Microsoft Entra ID > [Enterprise Applications](https://portal.azure.com/#view/Microsoft_AAD_EnterpriseApp/AllAppsBlade) > Paste Object ID in the search box > Click on found application > Copy the Application ID
- Client ID and Client Secret (for service principal access):
    - If not created yet: Go to Azure > Microsoft Entra ID > [App registrations](https://portal.azure.com/#view/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/~/RegisteredApps) > New registration > Name > Register
    - To get the Client ID: Go to Azure > Microsoft Entra ID > [App registrations](https://portal.azure.com/#view/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/~/RegisteredApps) > Click on your application > Overview > Copy the Application (client) ID
    - To get the Client Secret: Go to Azure > Microsoft Entra ID > [App registrations](https://portal.azure.com/#view/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/~/RegisteredApps) > Click on your application > Certificates & secrets > New client secret > Copy the value

**Example .env - Access via API key**

```python
AZURE_OPENAI_ENDPOINT=https://<your_azure_openai_endpoint>.openai.azure.com/
AZURE_OPENAI_API_KEY=<your_azure_openai_key>

AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_MODEL_NAME=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2025-04-01-preview
```

**Example .env - Access via Managed Identity**

```python
AZURE_OPENAI_ENDPOINT=https://<your_azure_openai_endpoint>.openai.azure.com/
AZURE_OPENAI_API_KEY=<your_azure_openai_key>
AZURE_TENANT_ID=aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa
AZURE_CLIENT_ID=bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbb # Managed Identity
# Client secret not neeeded as password will be handled and rotated automatically by Entra ID

AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_MODEL_NAME=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2025-04-01-preview
```

**Example .env - Access via Service Principal (App registration with client ID and client secret)**

```python
AZURE_OPENAI_ENDPOINT=https://<your_azure_openai_endpoint>.openai.azure.com/
AZURE_OPENAI_API_KEY=<your_azure_openai_key>
AZURE_TENANT_ID=aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa
AZURE_CLIENT_ID=bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbb # Azure AD App registration client ID
AZURE_CLIENT_SECRET=<your_client_secret>

AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_MODEL_NAME=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2025-04-01-preview
```


### Azure Open AI Deployment Types

There is 3 types of Azure Open AI deployments with 2 types of endpoints. The difference is in the URL (`cognitiveservices` vs. `openai`).

1. **Azure Open AI Service** deployment ('*.openai.azure.com'):
    - `https://<your_azure_openai_endpoint>.openai.azure.com/`
2. **Azure AI Foundry** deployment ('cognitiveservices.azure.com' AND 'openai.azure.com' - both used):
    - `https://<your_azure_openai_endpoint>.cognitiveservices.azure.com/`
    - `https://<your_azure_openai_endpoint>.openai.azure.com/`
3. **Azure AI Services** deployment ('cognitiveservices.azure.com' INSTEAD OF 'openai.azure.com'):
    - `https://<your_azure_openai_endpoint>.cognitiveservices.azure.com/`
  
### Azure Open AI Access Types

- **API Key** - In `.env` file:  `AZURE_OPENAI_API_KEY`
- **Managed Identity**  - In `.env` file:  `AZURE_CLIENT_ID`
- **Service Principal** - In `.env` file:  `AZURE_CLIENT_ID` and`AZURE_CLIENT_SECRET`.

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

