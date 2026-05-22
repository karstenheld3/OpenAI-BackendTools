# LLM Evaluation Skill Setup

Setup for LLM (Large Language Model) evaluation pipelines. Run once to install Python dependencies in `[WORKSPACE_FOLDER]/../.tools/llm-venv/`.

## 1. Set Workspace Folder

```powershell
$workspaceFolder = (Get-Location).Path  # or set explicitly: $workspaceFolder = "C:\Projects\MyProject"
$toolsDir = "$workspaceFolder\..\.tools"
$venvDir = "$toolsDir\llm-venv"

# Create .tools folder if needed
if (-not (Test-Path $toolsDir)) { New-Item -ItemType Directory -Path $toolsDir }
```

## 2. Verify Python Installation

```powershell
python --version
```

Expected: Python 3.10+ installed and in PATH.
If not installed: Download from https://python.org

## 3. Create Virtual Environment

**Check if already exists:**
```powershell
Test-Path "$venvDir\Scripts\python.exe"
```

**If not exists, create:**
```powershell
python -m venv $venvDir
```

**Verify creation:**
```powershell
& "$venvDir\Scripts\python.exe" --version
```

## 4. Install Dependencies

**Activate venv and install:**
```powershell
& "$venvDir\Scripts\Activate.ps1"
pip install "openai==2.8.0" "anthropic>=0.18.0,<1.0.0"
deactivate
```

**Or install without activating:**
```powershell
& "$venvDir\Scripts\pip.exe" install "openai==2.8.0" "anthropic>=0.18.0,<1.0.0"
```

**Verify packages:**
```powershell
& "$venvDir\Scripts\pip.exe" list | Select-String "openai|anthropic"
```

## 5. Configure API Keys

Create `.env` file in your working directory (where you run scripts). Use `--keys-file` parameter if running scripts from a different directory:

```powershell
$envFile = ".env"
if (-not (Test-Path $envFile)) {
    @"
# LLM API Keys
OPENAI_API_KEY=sk-proj-your-key-here
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
"@ | Set-Content $envFile
    Write-Host "Created $envFile - edit with your API keys" -ForegroundColor Yellow
} else {
    Write-Host "$envFile already exists" -ForegroundColor Green
}
```

**IMPORTANT:** Add `.env` to `.gitignore`:
```powershell
$gitignore = ".gitignore"
if (Test-Path $gitignore) {
    $content = Get-Content $gitignore -Raw
    if ($content -notmatch "\.env") {
        Add-Content $gitignore "`n# API Keys`n.env"
        Write-Host "Added .env to .gitignore" -ForegroundColor Green
    }
}
```

## 6. Test API Connection

**Test OpenAI:**
```powershell
& "$venvDir\Scripts\python.exe" -c @"
import os
from openai import OpenAI
key = os.environ.get('OPENAI_API_KEY')
if not key:
    print('[FAIL] OPENAI_API_KEY not set - create .env file or set environment variable')
    exit(1)
client = OpenAI(api_key=key)
print('[OK] OpenAI client created successfully')
"@
```

**Test Anthropic:**
```powershell
& "$venvDir\Scripts\python.exe" -c @"
import os
from anthropic import Anthropic
key = os.environ.get('ANTHROPIC_API_KEY')
if not key:
    print('[FAIL] ANTHROPIC_API_KEY not set - create .env file or set environment variable')
    exit(1)
client = Anthropic(api_key=key)
print('[OK] Anthropic client created successfully')
"@
```

## 7. Running Scripts

Always use the venv Python:

```powershell
# Single call
& "$venvDir\Scripts\python.exe" call-llm.py --model gpt-4o --input-file image.jpg --prompt-file prompt.md

# Batch processing
& "$venvDir\Scripts\python.exe" call-llm-batch.py --model claude-opus-4-20250514 --input-folder images/ --output-folder out/ --prompt-file prompt.md

# Or activate venv first
& "$venvDir\Scripts\Activate.ps1"
python call-llm.py --help
deactivate
```

## 8. Final Verification

```powershell
Write-Host "=== LLM Evaluation Setup Verification ===" -ForegroundColor Cyan

# Check venv
if (Test-Path "$venvDir\Scripts\python.exe") {
    Write-Host "[OK] Virtual environment: $venvDir" -ForegroundColor Green
} else {
    Write-Host "[FAIL] Virtual environment not found" -ForegroundColor Red
}

# Check packages
$packages = & "$venvDir\Scripts\pip.exe" list 2>$null
if ($packages -match "openai") {
    Write-Host "[OK] openai package installed" -ForegroundColor Green
} else {
    Write-Host "[FAIL] openai package missing" -ForegroundColor Red
}
if ($packages -match "anthropic") {
    Write-Host "[OK] anthropic package installed" -ForegroundColor Green
} else {
    Write-Host "[FAIL] anthropic package missing" -ForegroundColor Red
}

# Check .env
if (Test-Path ".env") {
    Write-Host "[OK] .env file exists" -ForegroundColor Green
} else {
    Write-Host "[WARN] .env file not found - create with API keys" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Setup complete. Run scripts with:" -ForegroundColor White
Write-Host "  & `"$venvDir\Scripts\python.exe`" <script.py> [args]" -ForegroundColor Gray
```

## 9. Cleanup (Optional)

Remove virtual environment to reinstall:
```powershell
Remove-Item $venvDir -Recurse -Force
```

## 10. Troubleshooting

### Virtual environment activation fails

**Error:** "running scripts is disabled on this system"

**Fix:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### pip install fails with SSL error

**Fix:** Use trusted host:
```powershell
& "$venvDir\Scripts\pip.exe" install --trusted-host pypi.org --trusted-host pypi.python.org openai anthropic
```

### API key not found

Ensure `.env` file is in the current working directory when running scripts, or set environment variable:
```powershell
$env:OPENAI_API_KEY = "sk-proj-your-key"
$env:ANTHROPIC_API_KEY = "sk-ant-api03-your-key"
```

## Completion

Setup complete:
- **Virtual environment**: `[WORKSPACE_FOLDER]/../.tools/llm-venv/`
- **Python packages**: openai, anthropic
- **API keys**: `.env` file (user-created)

