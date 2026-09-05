# SharePoint App Catalog Uninstall

## Remove PnP PowerShell

```powershell
Uninstall-Module -Name PnP.PowerShell -AllVersions -Force
```

## Remove Gulp CLI

```powershell
npm uninstall -g gulp-cli
```

## Disconnect Auth

```powershell
Disconnect-PnPOnline
```

## Remove App from Site (destructive)

```powershell
Connect-PnPOnline -Url "https://TENANT.sharepoint.com/sites/SITE" -Interactive
Uninstall-PnPApp -Identity "APP_ID" -Scope Site
Remove-PnPApp -Identity "APP_ID" -Scope Site
```
