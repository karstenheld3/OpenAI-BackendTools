# === SharePoint App Catalog Deploy Script ===
# Installs tools if missing, builds SPFx package, uploads to Site Collection App Catalog.
# Adapt SPFX_PROJECT_DIR, TARGET_SITE_URL, and APP_CATALOG_SCOPE to your project.

$ErrorActionPreference = 'Stop'

# === CONFIGURATION (adapt per project) ===
$SPFX_PROJECT_DIR = "{{SPFX_PROJECT_DIR}}"    # SPFx project folder (relative to project root)
$TARGET_SITE_URL = "{{TARGET_SITE_URL}}"       # SharePoint site URL
$APP_CATALOG_SCOPE = "Site"                     # "Site" or "Tenant"
$SPPKG_RELATIVE_PATH = "sharepoint/solution"   # Relative to SPFX_PROJECT_DIR

# === Resolve paths ===
$projectRoot = Split-Path $PSScriptRoot -Parent
if ($PSScriptRoot -eq (Split-Path $MyInvocation.MyCommand.Path -Parent)) {
    $projectRoot = $PSScriptRoot
}
Set-Location $projectRoot

# === 1. Check/install PnP.PowerShell ===
if (-not (Get-Module -Name PnP.PowerShell -ListAvailable)) {
    Write-Host "Installing PnP.PowerShell module..."
    Install-Module -Name PnP.PowerShell -Scope CurrentUser -Force
}

# === 2. Check Node.js version ===
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Error "Node.js not found. SPFx 1.20 requires Node.js 18.x."
    exit 1
}
$nodeVersion = (node --version) -replace 'v', ''
$majorVersion = [int]($nodeVersion.Split('.')[0])
if ($majorVersion -ne 18) {
    Write-Warning "Node.js $nodeVersion detected. SPFx 1.20 requires Node.js 18.x."
    Write-Host "Run: fnm use 18" -ForegroundColor Yellow
}

# === 3. Check Gulp CLI ===
if (-not (Get-Command gulp -ErrorAction SilentlyContinue)) {
    Write-Host "Installing gulp-cli..."
    npm install -g gulp-cli
}

# === 4. Build SPFx package ===
$spfxDir = Join-Path $projectRoot $SPFX_PROJECT_DIR
Set-Location $spfxDir

Write-Host "Installing dependencies..."
if (-not (Test-Path "node_modules")) { npm install }

Write-Host "Building SPFx package (--ship)..."
gulp clean --no-color
gulp bundle --ship --no-color
gulp package-solution --ship --no-color

# === 5. Find .sppkg file ===
$sppkgDir = Join-Path $spfxDir $SPPKG_RELATIVE_PATH
$sppkgFile = Get-ChildItem -Path $sppkgDir -Filter "*.sppkg" | Select-Object -First 1
if ($null -eq $sppkgFile) { throw "No .sppkg file found in $sppkgDir" }
Write-Host "Package: $($sppkgFile.Name)" -ForegroundColor Green

# === 6. Connect to SharePoint ===
Write-Host "Connecting to $TARGET_SITE_URL..."
Connect-PnPOnline -Url $TARGET_SITE_URL -Interactive

# === 7. Upload and publish ===
Write-Host "Uploading to App Catalog..."
Add-PnPApp -Path $sppkgFile.FullName -Scope $APP_CATALOG_SCOPE -Overwrite -Publish

# === 8. Verify ===
Set-Location $projectRoot
Write-Host ""
Write-Host "Deploy complete!" -ForegroundColor Green
Write-Host "Site: $TARGET_SITE_URL" -ForegroundColor Cyan
