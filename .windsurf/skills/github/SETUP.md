# GitHub CLI Setup

Run once to install GitHub CLI locally in `[WORKSPACE_FOLDER]/.tools/`.

## 1. Set Workspace Folder

```powershell
$workspaceFolder = (Get-Location).Path  # or set explicitly: $workspaceFolder = "C:\Dev\MyProject"
$toolsDir = "$workspaceFolder\.tools"
$installerDir = "$toolsDir\_installer"

# Create folders if needed
if (-not (Test-Path $toolsDir)) { New-Item -ItemType Directory -Path $toolsDir }
if (-not (Test-Path $installerDir)) { New-Item -ItemType Directory -Path $installerDir }
```

## 2. Install GitHub CLI Locally

**Check if already installed:**
```powershell
Test-Path "$toolsDir\gh\bin\gh.exe"
```

**If not installed, download and extract:**
```powershell
$ghDir = "$toolsDir\gh"

# Download latest GitHub CLI for Windows (64-bit)
$ghUrl = "https://github.com/cli/cli/releases/download/v2.63.2/gh_2.63.2_windows_amd64.zip"
$zipPath = "$installerDir\gh.zip"

Invoke-WebRequest -Uri $ghUrl -OutFile $zipPath

# Extract to gh folder (zip contains bin/ and LICENSE at root)
New-Item -ItemType Directory -Path $ghDir -Force | Out-Null
Expand-Archive -Path $zipPath -DestinationPath $ghDir -Force
```

**Verify installation:**
```powershell
& "$toolsDir\gh\bin\gh.exe" --version
```

## 3. Authenticate with GitHub

**Check authentication status:**
```powershell
& "$toolsDir\gh\bin\gh.exe" auth status
```

**If not authenticated, login:**
```powershell
& "$toolsDir\gh\bin\gh.exe" auth login
```

Follow the prompts to authenticate via browser or token.

## 4. Configure Git (Optional)

Set gh as credential helper for seamless git operations:
```powershell
& "$toolsDir\gh\bin\gh.exe" auth setup-git
```

## Completion

GitHub CLI ready:
- **gh**: GitHub CLI (`[WORKSPACE_FOLDER]/.tools/gh/bin/`)
- Run `gh auth login` to authenticate with your GitHub account
