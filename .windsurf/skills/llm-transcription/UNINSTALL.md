# LLM Transcription Skill Uninstall

Remove LLM Transcription skill from your system.

## Quick Uninstall

Run this script and answer with a single character:

```powershell
# === LLM Transcription Skill Uninstall ===

# Define what can be removed
$workspaceRoot = (Get-Location).Path
$skillDir = Join-Path $workspaceRoot ".windsurf\skills\llm-transcription"
$sharedVenv = Join-Path $workspaceRoot ".tools\llm-venv"
$tempOutputDir = Join-Path $workspaceRoot ".tools\_transcription_output"

# Check current state
$hasSkill = Test-Path $skillDir
$hasSharedVenv = Test-Path $sharedVenv
$hasTempOutput = Test-Path $tempOutputDir

# Check if other skills use the shared venv
$otherSkillsUsingVenv = @()
$llmEvalSkill = Join-Path $workspaceRoot ".windsurf\skills\llm-evaluation"
$llmComputerUse = Join-Path $workspaceRoot ".windsurf\skills\llm-computer-use"
if (Test-Path $llmEvalSkill) { $otherSkillsUsingVenv += "llm-evaluation" }
if (Test-Path $llmComputerUse) { $otherSkillsUsingVenv += "llm-computer-use" }

# Show current state
Write-Host ""
Write-Host "=== LLM Transcription Skill Uninstall ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Current state:" -ForegroundColor White
Write-Host "  [S] Skill folder:        $(if ($hasSkill) { 'Found' } else { 'Not found' })" -ForegroundColor $(if ($hasSkill) { 'Yellow' } else { 'Gray' })
Write-Host "  [O] Temp output folder:  $(if ($hasTempOutput) { 'Found' } else { 'Not found' })" -ForegroundColor $(if ($hasTempOutput) { 'Yellow' } else { 'Gray' })
Write-Host "  [V] Shared venv:         $(if ($hasSharedVenv) { 'Found' } else { 'Not found' })" -ForegroundColor $(if ($hasSharedVenv) { 'Yellow' } else { 'Gray' })

if ($otherSkillsUsingVenv.Count -gt 0) {
    Write-Host ""
    Write-Host "  WARNING: Shared venv also used by: $($otherSkillsUsingVenv -join ', ')" -ForegroundColor Red
}

Write-Host ""
Write-Host "Options:" -ForegroundColor White
Write-Host "  1 = Minimal: Skill folder only (keeps venv)" -ForegroundColor White
Write-Host "  2 = Recommended: Skill folder + temp output (keeps venv)" -ForegroundColor White
Write-Host "  3 = Full: Skill folder + temp output + shared venv" -ForegroundColor White
Write-Host "  Q = Quit (no changes)" -ForegroundColor White
Write-Host ""

if ($otherSkillsUsingVenv.Count -gt 0) {
    Write-Host "  Note: Option 3 will break: $($otherSkillsUsingVenv -join ', ')" -ForegroundColor Red
    Write-Host ""
}

$choice = Read-Host "What to remove? [1/2/3/Q]"

# Validate input
$validChoices = @('1', '2', '3', 'Q', 'q')
if ($choice -notin $validChoices) {
    Write-Host "Invalid choice: '$choice'. Please enter 1, 2, 3, or Q" -ForegroundColor Red
    return
}

if ($choice -eq 'Q' -or $choice -eq 'q') {
    Write-Host "Cancelled. No changes made." -ForegroundColor Yellow
    return
}

$removeSkill = $choice -in @('1', '2', '3')
$removeTempOutput = $choice -in @('2', '3')
$removeVenv = $choice -eq '3'

Write-Host ""

# Remove Skill folder
if ($removeSkill -and $hasSkill) {
    try {
        Remove-Item $skillDir -Recurse -Force -ErrorAction Stop
        Write-Host "[S] Removed skill folder" -ForegroundColor Green
    } catch {
        Write-Host "[S] Failed to remove skill folder: $_" -ForegroundColor Red
    }
} elseif ($removeSkill) {
    Write-Host "[S] Skill folder already removed" -ForegroundColor Gray
}

# Remove temp output
if ($removeTempOutput -and $hasTempOutput) {
    try {
        $size = [math]::Round((Get-ChildItem $tempOutputDir -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB, 0)
        Remove-Item $tempOutputDir -Recurse -Force -ErrorAction Stop
        Write-Host "[O] Removed temp output folder ($size MB)" -ForegroundColor Green
    } catch {
        Write-Host "[O] Failed to remove temp output: $_" -ForegroundColor Red
    }
} elseif ($removeTempOutput) {
    Write-Host "[O] Temp output folder not found" -ForegroundColor Gray
}

# Remove shared venv
if ($removeVenv -and $hasSharedVenv) {
    if ($otherSkillsUsingVenv.Count -gt 0) {
        $confirm = Read-Host "This will break $($otherSkillsUsingVenv -join ', '). Continue? [y/N]"
        if ($confirm -ne 'y' -and $confirm -ne 'Y') {
            Write-Host "[V] Skipped venv removal" -ForegroundColor Yellow
        } else {
            try {
                $size = [math]::Round((Get-ChildItem $sharedVenv -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB, 0)
                Remove-Item $sharedVenv -Recurse -Force -ErrorAction Stop
                Write-Host "[V] Removed shared venv ($size MB)" -ForegroundColor Green
            } catch {
                Write-Host "[V] Failed to remove venv: $_" -ForegroundColor Red
            }
        }
    } else {
        try {
            $size = [math]::Round((Get-ChildItem $sharedVenv -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB, 0)
            Remove-Item $sharedVenv -Recurse -Force -ErrorAction Stop
            Write-Host "[V] Removed shared venv ($size MB)" -ForegroundColor Green
        } catch {
            Write-Host "[V] Failed to remove venv: $_" -ForegroundColor Red
        }
    }
} elseif ($removeVenv) {
    Write-Host "[V] Shared venv already removed" -ForegroundColor Gray
}

Write-Host ""
Write-Host "=== Done ===" -ForegroundColor Cyan
```

## What Gets Removed

- **Option 1 (Minimal)** - Skill folder only
- **Option 2 (Recommended)** - Skill folder + temp output
- **Option 3 (Full)** - Skill folder + temp output + shared venv

**Components:**
- **Skill folder**: `.windsurf/skills/llm-transcription/` (~50KB)
- **Temp output**: `.tools/_transcription_output/` (variable size)
- **Shared venv**: `.tools/llm-venv/` (~200MB, shared with llm-evaluation, llm-computer-use)

## Manual Removal

If the script fails, remove manually:

### 1. Skill Folder

```powershell
Remove-Item ".windsurf\skills\llm-transcription" -Recurse -Force
```

### 2. Temp Output

```powershell
Remove-Item ".tools\_transcription_output" -Recurse -Force
```

### 3. Shared Venv (breaks other LLM skills)

```powershell
Remove-Item ".tools\llm-venv" -Recurse -Force
```

## Notes

- **API keys file is NOT removed** - Located at `[WORKSPACE_FOLDER]\..\.api-keys.txt`, shared across all projects
- **Shared venv warning** - The `.tools/llm-venv/` folder is shared between llm-transcription, llm-evaluation, and llm-computer-use skills. Removing it will break all three.
