# === Netlify Deploy Script ===
# Installs tools if missing, builds project, deploys to Netlify.
# Adapt SITE_NAME, BUILD_COMMAND, and PUBLISH_DIR to your project.

$ErrorActionPreference = 'Stop'

# === CONFIGURATION (adapt per project) ===
$SITE_NAME = "{{SITE_NAME}}"          # Netlify site name (subdomain)
$BUILD_COMMAND = "npm run build"       # Build command
$PUBLISH_DIR = "dist"                  # Build output directory (relative to project root)

# === Resolve paths ===
$projectRoot = Split-Path $PSScriptRoot -Parent
if ($PSScriptRoot -eq (Split-Path $MyInvocation.MyCommand.Path -Parent)) {
    # Script is in project root (not scripts/ subfolder)
    $projectRoot = $PSScriptRoot
}
Set-Location $projectRoot

# === 1. Check/install Node.js ===
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Error "Node.js not found. Install from https://nodejs.org/"
    exit 1
}
Write-Host "Node.js: $(node --version)" -ForegroundColor Green

# === 2. Check/install Netlify CLI ===
if (-not (Get-Command netlify -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Netlify CLI..."
    npm install -g netlify-cli
    if (-not (Get-Command netlify -ErrorAction SilentlyContinue)) {
        Write-Error "Netlify CLI installation failed. Run: npm install -g netlify-cli"
        exit 1
    }
}
Write-Host "Netlify CLI: $(netlify --version)" -ForegroundColor Green

# === 3. Check auth ===
$status = netlify status 2>&1
if ($status -match "Not logged in") {
    Write-Host "Not logged in to Netlify. Running 'netlify login'..."
    netlify login
}

# === 4. Install dependencies ===
if (Test-Path "package.json") {
    if (-not (Test-Path "node_modules")) {
        Write-Host "Installing dependencies..."
        npm install
    }
}

# === 5. Build ===
Write-Host "Building project..."
Invoke-Expression $BUILD_COMMAND
if ($LASTEXITCODE -ne 0) {
    Write-Error "Build failed with exit code $LASTEXITCODE"
    exit 1
}

# === 6. Deploy ===
Write-Host "Deploying to Netlify..."
$deployArgs = "deploy --prod --dir=$PUBLISH_DIR"
if ($SITE_NAME -ne "{{SITE_NAME}}") {
    $deployArgs += " --site-name=$SITE_NAME"
}
Invoke-Expression "netlify $deployArgs"
if ($LASTEXITCODE -ne 0) {
    Write-Error "Deploy failed with exit code $LASTEXITCODE"
    exit 1
}

# === 7. Verify ===
Write-Host ""
Write-Host "Deploy complete!" -ForegroundColor Green
if ($SITE_NAME -ne "{{SITE_NAME}}") {
    Write-Host "Live at: https://$SITE_NAME.netlify.app" -ForegroundColor Cyan
}
