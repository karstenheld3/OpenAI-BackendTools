# === Azure App Service Deploy Script ===
# Installs tools if missing, reads .env config, zips source, deploys to Azure.
# Adapt SOURCE_DIR, EXCLUDE_PATTERNS, and STARTUP_COMMAND to your project.

$ErrorActionPreference = 'Stop'

# === CONFIGURATION (adapt per project) ===
$SOURCE_DIR = "src"                    # Directory to zip and deploy (relative to project root)
$DEPLOY_ZIP = "deploy.zip"            # Temporary zip filename
$STARTUP_COMMAND = "{{STARTUP_COMMAND}}"  # App startup command
$EXCLUDE_PATTERNS = @('.git', '*.bat', '*.ps1', $DEPLOY_ZIP, '.vscode', '__pycache__', '.venv', '.env', 'LICENSE', '.gitignore')

# === Resolve paths ===
$projectRoot = Split-Path $PSScriptRoot -Parent
if ($PSScriptRoot -eq (Split-Path $MyInvocation.MyCommand.Path -Parent)) {
    $projectRoot = $PSScriptRoot
}
Set-Location $projectRoot

# === Read .env file ===
function Read-EnvFile {
    param([Parameter(Mandatory=$true)] [string]$Path)
    $envVars = @{}
    if (!(Test-Path $Path)) { throw "File '$Path' not found." }
    Get-Content $Path | ForEach-Object {
        if ($_ -match '^(?!#)([^=]+)=([^#]*)(?:#.*)?$') {
            $key = $matches[1].Trim(); $value = $matches[2].Trim()
            $envVars[$key] = $value
        }
    }
    return $envVars
}

$envPath = Join-Path $projectRoot ".env"
$config = Read-EnvFile -Path $envPath

# === Validate required vars ===
$requiredVars = @('AZURE_TENANT_ID', 'AZURE_SUBSCRIPTION_ID', 'AZURE_RESOURCE_GROUP', 'AZURE_APP_SERVICE_NAME')
foreach ($var in $requiredVars) {
    if ([string]::IsNullOrWhiteSpace($config[$var])) { throw "$var is required in .env file" }
}

# === 1. Check/install Az PowerShell module ===
if (-not (Get-Module -Name Az -ListAvailable)) {
    Write-Host "Installing Az PowerShell module..."
    Install-Module -Name Az -Scope CurrentUser -Force -AllowClobber
}

# === 2. Check/install Azure CLI ===
if (-not (Get-Command az -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Azure CLI..."
    $installerUrl = "https://aka.ms/installazurecliwindows"
    $installerPath = "$env:TEMP\AzureCLI.msi"
    Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath
    Start-Process msiexec.exe -Wait -ArgumentList "/I $installerPath /quiet"
    Remove-Item $installerPath
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
    if (-not (Get-Command az -ErrorAction SilentlyContinue)) {
        Write-Error "Azure CLI installation failed."
        exit 1
    }
}

# === 3. Login to Azure ===
Write-Host "Connecting to Azure..."
Clear-AzContext -Force
try { Connect-AzAccount -Tenant $config.AZURE_TENANT_ID -Subscription $config.AZURE_SUBSCRIPTION_ID | Out-Null }
catch { throw "Azure login failed: $_" }
Set-AzContext -Subscription $config.AZURE_SUBSCRIPTION_ID | Out-Null

# === 4. Verify app service exists ===
Write-Host "Checking app service '$($config.AZURE_APP_SERVICE_NAME)'..."
$webApp = Get-AzWebApp -ResourceGroupName $config.AZURE_RESOURCE_GROUP -Name $config.AZURE_APP_SERVICE_NAME
if ($null -eq $webApp) { throw "App service '$($config.AZURE_APP_SERVICE_NAME)' not found." }
Write-Host "  URL: https://$($config.AZURE_APP_SERVICE_NAME).azurewebsites.net" -ForegroundColor Cyan

# === 5. Create deployment package ===
Write-Host "Creating deployment package..."
$sourcePath = Join-Path $projectRoot $SOURCE_DIR
$zipPath = Join-Path $projectRoot $DEPLOY_ZIP
if (Test-Path $zipPath) { Remove-Item $zipPath -Force }

$items = Get-ChildItem -Path $sourcePath -Exclude $EXCLUDE_PATTERNS
$rootReq = Join-Path $projectRoot 'requirements.txt'
if (Test-Path $rootReq) { $items = @($items) + (Get-Item $rootReq) }
Compress-Archive -Path $items -DestinationPath $zipPath -Force

# === 6. Deploy ===
Write-Host "Deploying..."
Publish-AzWebApp -ResourceGroupName $config.AZURE_RESOURCE_GROUP -Name $config.AZURE_APP_SERVICE_NAME -ArchivePath $zipPath -Force | Out-Null

# === 7. Cleanup ===
if (Test-Path $zipPath) { Remove-Item $zipPath -Force }

# === 8. Verify ===
Write-Host ""
Write-Host "Deploy complete!" -ForegroundColor Green
Write-Host "Live at: https://$($config.AZURE_APP_SERVICE_NAME).azurewebsites.net" -ForegroundColor Cyan
