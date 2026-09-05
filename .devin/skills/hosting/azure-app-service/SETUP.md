# Azure App Service Setup

## Prerequisites

- PowerShell 7+ installed
- Azure subscription with resource group
- `.env` file with Azure configuration variables

## Install CLI Tools

### Azure CLI

```powershell
# Check if installed
az --version

# Install (Windows MSI)
$installerUrl = "https://aka.ms/installazurecliwindows"
$installerPath = "$env:TEMP\AzureCLI.msi"
Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath
Start-Process msiexec.exe -Wait -ArgumentList "/I $installerPath /quiet"
Remove-Item $installerPath
```

### Az PowerShell Module

```powershell
Install-Module -Name Az -Scope CurrentUser -Force -AllowClobber
```

Verify: `Get-Module -Name Az -ListAvailable`

## Authenticate

```powershell
# Interactive login
Connect-AzAccount -Tenant "TENANT_ID" -Subscription "SUBSCRIPTION_ID"

# Or via Azure CLI
az login --tenant TENANT_ID
az account set --subscription SUBSCRIPTION_ID
```

## Required Configuration

`.env` file in project root with:
```
AZURE_TENANT_ID=...
AZURE_SUBSCRIPTION_ID=...
AZURE_RESOURCE_GROUP=...
AZURE_APP_SERVICE_NAME=...
AZURE_APP_SERVICE_PLAN=...
```

## Deploy Commands

```powershell
# Zip deploy via PowerShell
Publish-AzWebApp -ResourceGroupName RG -Name APP -ArchivePath deploy.zip -Force

# Or via Azure CLI
az webapp deploy --resource-group RG --name APP --src-path deploy.zip --type zip
```

## Key Facts

- Supports Python, Node.js, .NET, Java, PHP, Docker
- Oryx build system auto-detects language from requirements.txt / package.json
- Set `SCM_DO_BUILD_DURING_DEPLOYMENT=1` for server-side build
- Startup command configurable via `az webapp config set --startup-file`
- Managed Identity for secure auth to other Azure services
