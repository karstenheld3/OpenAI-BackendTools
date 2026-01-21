# Microsoft Playwright MCP Uninstall

Remove Microsoft Playwright MCP server from your system.

## Quick Uninstall

Run this script and answer with a single character:

```powershell
# === Microsoft Playwright MCP Uninstall ===

# Define what can be removed
$configPath = "$env:USERPROFILE\.codeium\windsurf\mcp_config.json"
$profileDir = "$env:USERPROFILE\.ms-playwright-mcp-profile"
$browsersDir = "$env:LOCALAPPDATA\ms-playwright"
$authFiles = @(
    "$env:USERPROFILE\auth.json",
    "$env:USERPROFILE\.auth.json",
    ".\auth.json"
)
$npxCacheDir = "$env:LOCALAPPDATA\npm-cache\_npx"

# Check current state
$hasConfig = $false
$hasProfile = Test-Path $profileDir
$hasBrowsers = Test-Path $browsersDir
$hasAuth = ($authFiles | Where-Object { Test-Path $_ }).Count -gt 0
$hasNpmCache = $false
if (Test-Path $npxCacheDir) {
    $hasNpmCache = (Get-ChildItem $npxCacheDir -Directory -ErrorAction SilentlyContinue | Where-Object {
        Test-Path "$($_.FullName)\node_modules\@playwright" -ErrorAction SilentlyContinue
    }).Count -gt 0
}

if (Test-Path $configPath) {
    try {
        $config = Get-Content $configPath -Raw | ConvertFrom-Json -AsHashtable
        $hasConfig = $config.mcpServers -and $config.mcpServers.ContainsKey("playwright")
    } catch { }
}

# Show current state
Write-Host ""
Write-Host "=== Microsoft Playwright MCP Uninstall ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Current state:" -ForegroundColor White
Write-Host "  [C] MCP Config entry:    $(if ($hasConfig) { 'Found' } else { 'Not found' })" -ForegroundColor $(if ($hasConfig) { 'Yellow' } else { 'Gray' })
Write-Host "  [P] User profile:        $(if ($hasProfile) { 'Found' } else { 'Not found' })" -ForegroundColor $(if ($hasProfile) { 'Yellow' } else { 'Gray' })
Write-Host "  [A] Auth state files:    $(if ($hasAuth) { 'Found' } else { 'Not found' })" -ForegroundColor $(if ($hasAuth) { 'Yellow' } else { 'Gray' })
Write-Host "  [B] Playwright browsers: $(if ($hasBrowsers) { 'Found' } else { 'Not found' })" -ForegroundColor $(if ($hasBrowsers) { 'Yellow' } else { 'Gray' })
Write-Host "  [N] NPM/npx cache:       $(if ($hasNpmCache) { 'Found' } else { 'Not found' })" -ForegroundColor $(if ($hasNpmCache) { 'Yellow' } else { 'Gray' })
Write-Host ""
Write-Host "Options:" -ForegroundColor White
Write-Host "  1 = Minimal: Config only" -ForegroundColor White
Write-Host "  2 = Recommended: Config + Profile + Auth" -ForegroundColor White
Write-Host "  3 = Leave NPM package: Config + Profile + Auth + Browsers" -ForegroundColor White
Write-Host "  4 = All: Config + Profile + Auth + Browsers + NPM cache" -ForegroundColor White
Write-Host "  Q = Quit (no changes)" -ForegroundColor White
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
$removeProfile = $choice -in @('2', '3', '4')
$removeAuth = $choice -in @('2', '3', '4')
$removeBrowsers = $choice -in @('3', '4')
$removeNpmCache = $choice -eq '4'

Write-Host ""

# Remove MCP Config
if ($removeConfig -and $hasConfig) {
    try {
        # Re-read config fresh to ensure we have current data
        $configContent = Get-Content $configPath -Raw
        $config = $configContent | ConvertFrom-Json -AsHashtable
        
        # Handle PSCustomObject conversion for mcpServers
        if ($config.mcpServers -and $config.mcpServers -isnot [System.Collections.Hashtable]) {
            $serversHash = @{}
            $config.mcpServers.PSObject.Properties | ForEach-Object { $serversHash[$_.Name] = $_.Value }
            $config.mcpServers = $serversHash
        }
        
        # Verify playwright still exists before removal
        if (-not $config.mcpServers -or -not $config.mcpServers.ContainsKey("playwright")) {
            Write-Host "[C] Config already removed (changed since scan)" -ForegroundColor Gray
        } else {
            # Backup with error handling
            $backupPath = "$configPath._beforeRemovingMsPlaywrightMcp_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
            Copy-Item $configPath $backupPath -ErrorAction Stop
            
            $config.mcpServers.Remove("playwright")
            $config | ConvertTo-Json -Depth 10 | Set-Content $configPath -Encoding UTF8 -ErrorAction Stop
            Write-Host "[C] Removed MCP config entry (backup: $backupPath)" -ForegroundColor Green
        }
    } catch {
        Write-Host "[C] Failed to remove config: $_" -ForegroundColor Red
    }
} elseif ($removeConfig) {
    Write-Host "[C] Config already removed" -ForegroundColor Gray
}

# Remove Profile
if ($removeProfile -and $hasProfile) {
    try {
        # Check for running Chrome
        $chrome = Get-Process chrome -ErrorAction SilentlyContinue
        if ($chrome) {
            Write-Host "[P] Warning: Chrome running, profile may be locked" -ForegroundColor Yellow
        }
        Remove-Item $profileDir -Recurse -Force -ErrorAction Stop
        Write-Host "[P] Removed user profile" -ForegroundColor Green
    } catch {
        Write-Host "[P] Failed: Close Chrome and delete manually: $profileDir" -ForegroundColor Red
    }
} elseif ($removeProfile) {
    Write-Host "[P] Profile already removed" -ForegroundColor Gray
}

# Remove Auth files
if ($removeAuth) {
    $foundAuth = $authFiles | Where-Object { Test-Path $_ }
    if ($foundAuth) {
        $foundAuth | ForEach-Object {
            try {
                Remove-Item $_ -Force
                Write-Host "[A] Removed auth file: $_" -ForegroundColor Green
            } catch {
                Write-Host "[A] Failed to remove: $_" -ForegroundColor Red
            }
        }
    } else {
        Write-Host "[A] No auth files found" -ForegroundColor Gray
    }
}

# Remove Browsers
if ($removeBrowsers -and $hasBrowsers) {
    try {
        $size = [math]::Round((Get-ChildItem $browsersDir -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB, 0)
        Remove-Item $browsersDir -Recurse -Force -ErrorAction Stop
        Write-Host "[B] Removed Playwright browsers ($size MB)" -ForegroundColor Green
    } catch {
        Write-Host "[B] Failed: Delete manually: $browsersDir" -ForegroundColor Red
    }
} elseif ($removeBrowsers) {
    Write-Host "[B] Browsers already removed" -ForegroundColor Gray
}

# Remove NPM cache
if ($removeNpmCache -and $hasNpmCache) {
    try {
        $playwrightCacheDirs = Get-ChildItem $npxCacheDir -Directory -ErrorAction SilentlyContinue | Where-Object {
            Test-Path "$($_.FullName)\node_modules\@playwright" -ErrorAction SilentlyContinue
        }
        $playwrightCacheDirs | Remove-Item -Recurse -Force -ErrorAction Stop
        Write-Host "[N] Removed Playwright from npx cache" -ForegroundColor Green
    } catch {
        Write-Host "[N] Failed: Delete manually from $npxCacheDir" -ForegroundColor Red
    }
} elseif ($removeNpmCache) {
    Write-Host "[N] NPM cache already clean" -ForegroundColor Gray
}

Write-Host ""
Write-Host "=== Done ===" -ForegroundColor Cyan
Write-Host "Restart Windsurf to apply changes" -ForegroundColor White
```

## What Gets Removed

- **Option 1 (Quick disable)** - Config only
- **Option 2 (Clean uninstall)** - Config + Profile + Auth
- **Option 3 (Complete removal)** - Config + Profile + Auth + Browsers
- **Option 4 (Full purge)** - Config + Profile + Auth + Browsers + NPM

**Components:**
- **Config**: Entry in `mcp_config.json` (required to disable MCP)
- **Profile**: Browser profile with cookies/logins at `[USER_PROFILE_PATH]\.ms-playwright-mcp-profile`
- **Auth**: Storage state files (`auth.json`, `.auth.json`)
- **Browsers**: Chromium/Firefox/WebKit at `[LOCALAPPDATA]\ms-playwright` (~500MB-2GB)
- **NPM**: Cached @playwright packages in npx cache at `[LOCALAPPDATA]\npm-cache\_npx`

## Manual Removal

If the script fails, remove manually:

### 1. Config Entry

Edit `[USER_PROFILE_PATH]\.codeium\windsurf\mcp_config.json`:
```json
{
  "mcpServers": {
    "playwright": { ... }  // <-- DELETE THIS
  }
}
```

### 2. Profile Directory

```powershell
Remove-Item "$env:USERPROFILE\.ms-playwright-mcp-profile" -Recurse -Force
```

### 3. Auth Files

```powershell
Remove-Item "$env:USERPROFILE\auth.json" -Force -ErrorAction SilentlyContinue
Remove-Item "$env:USERPROFILE\.auth.json" -Force -ErrorAction SilentlyContinue
Remove-Item ".\auth.json" -Force -ErrorAction SilentlyContinue
```

### 4. Playwright Browsers

```powershell
Remove-Item "$env:LOCALAPPDATA\ms-playwright" -Recurse -Force
```

## Troubleshooting

### "Access Denied" on profile

Chrome is holding a lock:
1. Close all Chrome windows
2. Task Manager > End "chrome.exe" processes
3. Try again

### Config backup location

Backups are saved as:
```
mcp_config.json._beforeRemovingMsPlaywrightMcp_YYYYMMDD_HHMMSS
```

To restore:
```powershell
# List backups
Get-ChildItem "$env:USERPROFILE\.codeium\windsurf\mcp_config.json.*"

# Restore
Copy-Item "[BACKUP_PATH]" "$env:USERPROFILE\.codeium\windsurf\mcp_config.json" -Force
```
