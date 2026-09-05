# === Vercel Deploy Script ===
# Installs tools if missing, builds project, deploys to Vercel.
# Adapt BUILD_COMMAND and OUTPUT_DIR to your project.

$ErrorActionPreference = 'Stop'

# === CONFIGURATION (adapt per project) ===
$buildCommand = "npm run build"        # Build command
$outputDir = "dist"                    # Build output directory (relative to project root)

# === Resolve paths ===
$projectRoot = Split-Path $PSScriptRoot -Parent
if ($PSScriptRoot -eq (Split-Path $MyInvocation.MyCommand.Path -Parent)) {
    $projectRoot = $PSScriptRoot
}
Set-Location $projectRoot

# === 1. Check/install Node.js ===
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Error "Node.js not found. Install from https://nodejs.org/"
    exit 1
}
Write-Host "Node.js: $(node --version)" -ForegroundColor Green

# === 2. Check/install Vercel CLI ===
if (-not (Get-Command vercel -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Vercel CLI..."
    npm install -g vercel
    if (-not (Get-Command vercel -ErrorAction SilentlyContinue)) {
        Write-Error "Vercel CLI installation failed. Run: npm install -g vercel"
        exit 1
    }
}
Write-Host "Vercel CLI: $(vercel --version)" -ForegroundColor Green

# === 3. Check auth ===
$whoami = vercel whoami 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Not logged in to Vercel. Running 'vercel login'..."
    vercel login
}

# === 4. Install dependencies ===
if (Test-Path "package.json") {
    if (-not (Test-Path "node_modules")) {
        Write-Host "Installing dependencies..."
        npm install
    }
}

# === 5. Build and Deploy ===
Write-Host "Deploying to Vercel (production)..."
vercel --prod
if ($LASTEXITCODE -ne 0) {
    Write-Error "Deploy failed with exit code $LASTEXITCODE"
    exit 1
}

# === 6. Verify ===
Write-Host ""
Write-Host "Deploy complete!" -ForegroundColor Green
