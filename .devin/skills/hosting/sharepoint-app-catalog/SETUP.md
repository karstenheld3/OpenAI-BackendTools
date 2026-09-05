# SharePoint App Catalog Setup

## Prerequisites

- PowerShell 7+ installed
- Node.js 18.x (SPFx 1.20 requirement)
- SharePoint Online tenant with Site Collection App Catalog enabled

## Install CLI Tools

### PnP PowerShell

```powershell
Install-Module -Name PnP.PowerShell -Scope CurrentUser -Force
```

Verify: `Get-Module -Name PnP.PowerShell -ListAvailable`

### Gulp CLI (SPFx build)

```powershell
npm install -g gulp-cli
```

### Node Version Manager (fnm)

```powershell
# Install fnm
winget install Schniz.fnm

# Use Node 18 (required for SPFx 1.20)
fnm install 18
fnm use 18
```

## Authenticate

```powershell
# Interactive login to SharePoint
Connect-PnPOnline -Url "https://TENANT.sharepoint.com/sites/SITE" -Interactive
```

Or with App ID (certificate auth):
```powershell
Connect-PnPOnline -Url "https://TENANT.sharepoint.com/sites/SITE" `
    -ClientId "APP_ID" -Tenant "TENANT.onmicrosoft.com" `
    -CertificatePath "cert.pfx" -CertificatePassword (ConvertTo-SecureString "pass" -AsPlainText -Force)
```

## Enable Site Collection App Catalog

```powershell
# Required before first deploy to a site
Connect-PnPOnline -Url "https://TENANT-admin.sharepoint.com" -Interactive
Add-PnPSiteCollectionAppCatalog -Site "https://TENANT.sharepoint.com/sites/SITE"
```

## Deploy Commands

```powershell
# Upload .sppkg to site app catalog
Add-PnPApp -Path "solution.sppkg" -Scope Site -Overwrite -Publish
```

## Key Facts

- SPFx 1.20 requires Node.js 18.x (not 20+)
- `.sppkg` is a zip containing bundled JS/CSS (no CDN needed with `includeClientSideAssets: true`)
- Site Collection App Catalog is per-site (not tenant-wide)
- After upload, app must be installed on the site via `Install-PnPApp`
- Version auto-increments on `--ship` build (4th segment in `package-solution.json`)
