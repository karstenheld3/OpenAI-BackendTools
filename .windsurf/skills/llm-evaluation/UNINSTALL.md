# LLM (Large Language Model) Evaluation Skill Uninstall

Remove LLM Evaluation Skill from your workspace.

## Quick Uninstall

Run this script and answer with a single character:

```powershell
# === LLM Evaluation Skill Uninstall ===

# Define what can be removed
$workspaceFolder = (Get-Location).Path
$venvDir = "$workspaceFolder\..\.tools\llm-venv"
$envFile = "$workspaceFolder\.env"
$toolsDir = "$workspaceFolder\..\.tools"

# Check current state
$hasVenv = Test-Path $venvDir
$hasEnv = Test-Path $envFile
$hasToolsDir = Test-Path $toolsDir

# Calculate sizes
$venvSize = 0
if ($hasVenv) {
    $venvSize = [math]::Round((Get-ChildItem $venvDir -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB, 0)
}

# Show current state
Write-Host ""
Write-Host "=== LLM Evaluation Skill Uninstall ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Workspace: $workspaceFolder" -ForegroundColor White
Write-Host ""
Write-Host "Current state:" -ForegroundColor White
Write-Host "  [V] Virtual environment: $(if ($hasVenv) { "Found ($venvSize MB)" } else { 'Not found' })" -ForegroundColor $(if ($hasVenv) { 'Yellow' } else { 'Gray' })
Write-Host "  [E] API keys (.env):     $(if ($hasEnv) { 'Found' } else { 'Not found' })" -ForegroundColor $(if ($hasEnv) { 'Yellow' } else { 'Gray' })
Write-Host ""
Write-Host "Options:" -ForegroundColor White
Write-Host "  1 = Minimal: Virtual environment only" -ForegroundColor White
Write-Host "  2 = Complete: Virtual environment + .env file" -ForegroundColor White
Write-Host "  Q = Quit (no changes)" -ForegroundColor White
Write-Host ""

$choice = Read-Host "What to remove? [1/2/Q]"

# Validate input
$validChoices = @('1', '2', 'Q', 'q')
if ($choice -notin $validChoices) {
    Write-Host "Invalid choice: '$choice'. Please enter 1, 2, or Q" -ForegroundColor Red
    return
}

if ($choice -eq 'Q' -or $choice -eq 'q') {
    Write-Host "Cancelled. No changes made." -ForegroundColor Yellow
    return
}

$removeVenv = $choice -in @('1', '2')
$removeEnv = $choice -eq '2'

Write-Host ""

# Remove Virtual Environment
if ($removeVenv -and $hasVenv) {
    try {
        # Check for running Python processes
        $pythonProcs = Get-Process python*, python -ErrorAction SilentlyContinue | Where-Object {
            $_.Path -like "*$venvDir*"
        }
        if ($pythonProcs) {
            Write-Host "[V] Warning: Python processes running from venv" -ForegroundColor Yellow
            $pythonProcs | ForEach-Object { Write-Host "    PID $($_.Id): $($_.Path)" -ForegroundColor Yellow }
        }
        
        Remove-Item $venvDir -Recurse -Force -ErrorAction Stop
        Write-Host "[V] Removed virtual environment ($venvSize MB)" -ForegroundColor Green
        
        # Check if .tools folder is now empty
        if ($hasToolsDir) {
            $remaining = Get-ChildItem $toolsDir -ErrorAction SilentlyContinue
            if (-not $remaining) {
                Remove-Item $toolsDir -Force -ErrorAction SilentlyContinue
                Write-Host "[V] Removed empty .tools folder" -ForegroundColor Green
            }
        }
    } catch {
        Write-Host "[V] Failed: Close any running scripts and delete manually: $venvDir" -ForegroundColor Red
    }
} elseif ($removeVenv) {
    Write-Host "[V] Virtual environment already removed" -ForegroundColor Gray
}

# Remove .env file
if ($removeEnv -and $hasEnv) {
    try {
        # Backup before removing
        $backupPath = "$envFile.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
        Copy-Item $envFile $backupPath -ErrorAction Stop
        Remove-Item $envFile -Force -ErrorAction Stop
        Write-Host "[E] Removed .env file (backup: $backupPath)" -ForegroundColor Green
    } catch {
        Write-Host "[E] Failed to remove .env: $_" -ForegroundColor Red
    }
} elseif ($removeEnv) {
    Write-Host "[E] .env file already removed" -ForegroundColor Gray
}

Write-Host ""
Write-Host "=== Done ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Note: Skill files in .windsurf/skills/llm-evaluation/ are not removed." -ForegroundColor White
Write-Host "To completely remove the skill, delete that folder manually." -ForegroundColor White
```

## What Gets Removed

- **Option 1 (Minimal)** - Virtual environment only
- **Option 2 (Complete)** - Virtual environment + .env file

**Components:**

- **Virtual environment**: Python venv at `../.tools/llm-venv/` (~100-200 MB)
  - Contains: openai, anthropic, and dependencies
  - Safe to remove: Can be recreated by running SETUP.md again

- **.env file**: API keys at workspace root
  - Contains: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`
  - **Warning**: Backup created before removal
  - You will need to recreate this if you reinstall

## What Is NOT Removed

- **Skill files**: `.windsurf/skills/llm-evaluation/` (scripts, prompts, configs)
- **Test outputs**: Any generated JSON files from running the scripts
- **Token usage files**: `_token_usage__*.json` files in output folders

To completely remove the skill:

```powershell
# After running uninstall script with option 2:
Remove-Item ".windsurf\skills\llm-evaluation" -Recurse -Force
```

## Reinstalling

To reinstall after uninstalling:

1. Run SETUP.md again to create virtual environment
2. Create new .env file with API keys
3. Test with: `python call-llm.py --help`
