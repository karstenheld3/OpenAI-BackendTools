# Google Account Skill Uninstall (gogcli)

Remove gogcli and associated configuration from your system.

## Quick Uninstall

Run this script and answer with a single character:

```powershell
# === gogcli Uninstall ===

# Define what can be removed
$wslInstalled = $false
$gogInstalled = $false
$hasConfig = $false
$hasCredentials = $false

# Check WSL
try {
    $wslCheck = wsl --list --quiet 2>$null
    $wslInstalled = $LASTEXITCODE -eq 0 -and $wslCheck
} catch { }

# Check gog in WSL
if ($wslInstalled) {
    try {
        $gogCheck = wsl bash -c 'command -v gog' 2>$null
        $gogInstalled = $LASTEXITCODE -eq 0 -and $gogCheck
    } catch { }
}

# Check config in WSL
if ($wslInstalled) {
    try {
        $configCheck = wsl bash -c 'test -d ~/.config/gogcli && echo "exists"' 2>$null
        $hasConfig = $configCheck -eq "exists"
    } catch { }
}

# Check Windows native config
$windowsConfigPath = "$env:APPDATA\gogcli"
$hasWindowsConfig = Test-Path $windowsConfigPath

# Check for credential files (including shared .tools folder)
# .tools is sibling to workspace: [WORKSPACE]/../.tools/
$toolsFolder = Join-Path (Split-Path (Get-Location).Path -Parent) ".tools"
$credentialFiles = @(
    (Join-Path $toolsFolder "gogcli-client-secret.json"),
    "$env:USERPROFILE\client_secret.json",
    "$env:USERPROFILE\.client_secret.json",
    "$env:USERPROFILE\Downloads\client_secret*.json"
)
$foundCredentials = @()
foreach ($pattern in $credentialFiles) {
    $found = Get-Item $pattern -ErrorAction SilentlyContinue
    if ($found) { $foundCredentials += $found.FullName }
}
$hasCredentials = $foundCredentials.Count -gt 0

# Show current state
Write-Host ""
Write-Host "=== gogcli Uninstall ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Current state:" -ForegroundColor White
Write-Host "  [W] WSL:              $(if ($wslInstalled) { 'Installed' } else { 'Not found' })" -ForegroundColor $(if ($wslInstalled) { 'Yellow' } else { 'Gray' })
Write-Host "  [G] gogcli (in WSL):  $(if ($gogInstalled) { 'Installed' } else { 'Not found' })" -ForegroundColor $(if ($gogInstalled) { 'Yellow' } else { 'Gray' })
Write-Host "  [C] Config (WSL):     $(if ($hasConfig) { 'Found' } else { 'Not found' })" -ForegroundColor $(if ($hasConfig) { 'Yellow' } else { 'Gray' })
Write-Host "  [N] Config (Windows): $(if ($hasWindowsConfig) { 'Found' } else { 'Not found' })" -ForegroundColor $(if ($hasWindowsConfig) { 'Yellow' } else { 'Gray' })
Write-Host "  [K] Credential files: $(if ($hasCredentials) { "$($foundCredentials.Count) found" } else { 'Not found' })" -ForegroundColor $(if ($hasCredentials) { 'Yellow' } else { 'Gray' })
Write-Host ""
Write-Host "Options:" -ForegroundColor White
Write-Host "  1 = Minimal: Remove gogcli config only (keeps WSL, credentials)" -ForegroundColor White
Write-Host "  2 = Standard: Remove gogcli + config (keeps WSL, credentials)" -ForegroundColor White
Write-Host "  3 = Full: Remove gogcli + config + credentials (keeps WSL)" -ForegroundColor White
Write-Host "  4 = Complete: Remove everything including WSL" -ForegroundColor White
Write-Host "  Q = Quit (no changes)" -ForegroundColor White
Write-Host ""
Write-Host "WARNING: Option 4 removes WSL which may be used by other applications!" -ForegroundColor Red
Write-Host ""

$choice = Read-Host "What to remove? [1/2/3/4/Q]"

# Validate input
$validChoices = @('1', '2', '3', '4', 'Q', 'q')
if ($choice -notin $validChoices) {
    Write-Host "Invalid choice: '$choice'. Please enter 1, 2, 3, 4, or Q" -ForegroundColor Red
    return
}

if ($choice -eq 'Q' -or $choice -eq 'q') {
    Write-Host "Cancelled. No changes made." -ForegroundColor Yellow
    return
}

$removeConfig = $choice -in @('1', '2', '3', '4')
$removeGog = $choice -in @('2', '3', '4')
$removeCredentials = $choice -in @('3', '4')
$removeWsl = $choice -eq '4'

Write-Host ""

# Remove WSL config
if ($removeConfig) {
    if ($hasConfig) {
        try {
            wsl bash -c 'rm -rf ~/.config/gogcli' 2>$null
            Write-Host "[C] Removed WSL config (~/.config/gogcli)" -ForegroundColor Green
        } catch {
            Write-Host "[C] Failed to remove WSL config: $_" -ForegroundColor Red
        }
    } else {
        Write-Host "[C] WSL config not found" -ForegroundColor Gray
    }
    
    if ($hasWindowsConfig) {
        try {
            Remove-Item $windowsConfigPath -Recurse -Force -ErrorAction Stop
            Write-Host "[N] Removed Windows config ($windowsConfigPath)" -ForegroundColor Green
        } catch {
            Write-Host "[N] Failed to remove Windows config: $_" -ForegroundColor Red
        }
    } else {
        Write-Host "[N] Windows config not found" -ForegroundColor Gray
    }
}

# Remove gogcli
if ($removeGog -and $gogInstalled) {
    try {
        # Try Homebrew first
        $brewResult = wsl bash -c 'brew uninstall gogcli 2>/dev/null && echo "success"' 2>$null
        if ($brewResult -eq "success") {
            Write-Host "[G] Removed gogcli (Homebrew)" -ForegroundColor Green
        } else {
            # Try removing binary manually
            wsl bash -c 'rm -f ~/gogcli/bin/gog ~/go/bin/gog /usr/local/bin/gog 2>/dev/null'
            Write-Host "[G] Removed gogcli binary" -ForegroundColor Green
        }
    } catch {
        Write-Host "[G] Failed to remove gogcli: $_" -ForegroundColor Red
        Write-Host "    Manual removal: wsl bash -c 'brew uninstall gogcli' or delete ~/gogcli" -ForegroundColor Yellow
    }
} elseif ($removeGog) {
    Write-Host "[G] gogcli not found" -ForegroundColor Gray
}

# Remove credentials
if ($removeCredentials) {
    if ($hasCredentials) {
        foreach ($file in $foundCredentials) {
            try {
                Remove-Item $file -Force -ErrorAction Stop
                Write-Host "[K] Removed credential: $file" -ForegroundColor Green
            } catch {
                Write-Host "[K] Failed to remove: $file - $_" -ForegroundColor Red
            }
        }
    } else {
        Write-Host "[K] No credential files found" -ForegroundColor Gray
    }
}

# Remove WSL (with extra confirmation)
if ($removeWsl -and $wslInstalled) {
    Write-Host ""
    Write-Host "!!! DANGER: About to remove WSL !!!" -ForegroundColor Red
    Write-Host "This will remove ALL WSL distributions and data!" -ForegroundColor Red
    Write-Host "Other applications may depend on WSL." -ForegroundColor Yellow
    Write-Host ""
    $confirm = Read-Host "Type 'REMOVE WSL' to confirm (or anything else to skip)"
    
    if ($confirm -eq 'REMOVE WSL') {
        try {
            # Unregister all distributions
            $distros = wsl --list --quiet 2>$null
            foreach ($distro in $distros) {
                if ($distro) {
                    wsl --unregister $distro.Trim() 2>$null
                    Write-Host "[W] Unregistered: $($distro.Trim())" -ForegroundColor Green
                }
            }
            Write-Host "[W] WSL distributions removed" -ForegroundColor Green
            Write-Host "    To fully remove WSL feature, run in Admin PowerShell:" -ForegroundColor Yellow
            Write-Host "    dism.exe /online /disable-feature /featurename:Microsoft-Windows-Subsystem-Linux" -ForegroundColor Yellow
        } catch {
            Write-Host "[W] Failed to remove WSL: $_" -ForegroundColor Red
        }
    } else {
        Write-Host "[W] WSL removal skipped" -ForegroundColor Yellow
    }
} elseif ($removeWsl) {
    Write-Host "[W] WSL not found" -ForegroundColor Gray
}

Write-Host ""
Write-Host "=== Done ===" -ForegroundColor Cyan
```

## What Gets Removed

- **Option 1 (Minimal)** - Config only
  - WSL: `~/.config/gogcli/`
  - Windows: `%AppData%\gogcli\`

- **Option 2 (Standard)** - gogcli + Config
  - Everything in Option 1
  - gogcli binary (via Homebrew or manual)

- **Option 3 (Full)** - gogcli + Config + Credentials
  - Everything in Option 2
  - OAuth client secret files (`client_secret*.json`)

- **Option 4 (Complete)** - Everything including WSL
  - Everything in Option 3
  - WSL distributions (requires extra confirmation)

## Manual Removal

If the script fails, remove manually:

### 1. gogcli Config (WSL)

```bash
rm -rf ~/.config/gogcli
```

### 2. gogcli Config (Windows)

```powershell
Remove-Item "$env:APPDATA\gogcli" -Recurse -Force
```

### 3. gogcli Binary (Homebrew)

```bash
brew uninstall gogcli
```

### 4. gogcli Binary (Manual Install)

```bash
rm -f ~/gogcli/bin/gog
rm -rf ~/gogcli
```

### 5. OAuth Credentials

Delete `client_secret*.json` from:
- `~/Downloads/`
- `~/`
- Wherever you saved it

### 6. Environment Variables

Remove from `~/.bashrc` or `~/.profile`:

```bash
# Remove these lines
export GOG_ACCOUNT='...'
export GOG_KEYRING_BACKEND='...'
export GOG_KEYRING_PASSWORD='...'
export GOG_ENABLE_COMMANDS='...'
```

### 7. Revoke OAuth Access (Optional)

1. Go to: https://myaccount.google.com/permissions
2. Find your gogcli app
3. Click "Remove Access"

## Troubleshooting

### "Cannot remove config - permission denied"

Close any terminals using WSL, then retry.

### "Homebrew uninstall failed"

Remove binary manually:
```bash
rm -f $(which gog)
```

### "WSL removal failed"

Run PowerShell as Administrator:
```powershell
wsl --shutdown
wsl --unregister Ubuntu  # or your distro name
```

## Keep vs Remove Guidance

**Keep WSL if you use:**
- Docker Desktop
- VS Code Remote - WSL
- Other Linux tools
- Development workflows

**Safe to remove:**
- Config files (can be recreated)
- gogcli binary (can be reinstalled)
- Credential files (can be redownloaded from Google Cloud Console)

**Cannot recover after removal:**
- OAuth tokens (must re-authorize)
- WSL data (unless backed up)
