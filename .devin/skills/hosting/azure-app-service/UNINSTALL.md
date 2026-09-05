# Azure App Service Uninstall

## Remove Azure CLI

```powershell
# Windows - uninstall via Programs and Features
# Or via MSI:
Start-Process msiexec.exe -Wait -ArgumentList "/X {product-code} /quiet"
```

## Remove Az PowerShell Module

```powershell
Uninstall-Module -Name Az -AllVersions -Force
```

## Disconnect Auth

```powershell
Disconnect-AzAccount
az logout
```

## Delete App Service (destructive)

```powershell
az webapp delete --resource-group RG --name APP_NAME
```
