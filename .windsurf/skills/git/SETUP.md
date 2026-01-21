# Git Setup Guide

Install and configure Git for Windows.

## Prerequisites

- Windows 10/11
- PowerShell 5.1+ or PowerShell Core 7+
- Administrator access (for system-wide install)

## Check if Git is Installed

```powershell
git --version
```

If command returns version number, Git is already installed. Skip to [Configuration](#configuration).

## Installation Methods

### Method 1: Winget (Recommended)

```powershell
winget install --id Git.Git -e --source winget
```

After installation, restart terminal or run:
```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
```

### Method 2: Chocolatey

```powershell
choco install git -y
```

### Method 3: Manual Download

1. Download from https://git-scm.com/download/win
2. Run installer with defaults
3. Restart terminal

## Configuration

### Set Identity (Required)

```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Verify Configuration

```powershell
git config --global --list
```

### Recommended Settings

```powershell
# Default branch name
git config --global init.defaultBranch main

# Line ending handling (Windows)
git config --global core.autocrlf true

# Default editor (VSCode)
git config --global core.editor "code --wait"

# Credential helper (Windows)
git config --global credential.helper manager
```

## Verification

```powershell
# Check version
git --version

# Check config
git config --global user.name
git config --global user.email

# Test with a simple operation
git init test-repo
cd test-repo
echo "test" > test.txt
git add .
git commit -m "test commit"
git log --oneline
cd ..
Remove-Item -Recurse -Force test-repo
```

## Troubleshooting

### Git not found after installation

Restart terminal or refresh PATH:
```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
```

### Permission denied errors

Run PowerShell as Administrator for system-wide operations.

### SSL certificate problems

```powershell
git config --global http.sslBackend schannel
```
