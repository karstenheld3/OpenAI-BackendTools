# Microsoft Playwright MCP Setup

Run once to configure Microsoft Playwright MCP server for browser automation.

## 1. Verify Node.js Installation

```powershell
node --version
npm --version
npx --version
```

Expected: Node.js 18+ installed and in PATH.
If not installed: Download from https://nodejs.org (LTS version recommended).

## 2. Verify npx Path

**Find npx location:**
```powershell
(Get-Command npx).Source
```

**If npx not found in MCP config**, use full path:
```powershell
# Common locations:
# Windows (nvm): [USER_PROFILE_PATH]\.nvm\versions\node\v20.19.0\bin\npx.cmd
# Windows (default): [PROGRAM_FILES]\nodejs\npx.cmd
# Windows (Chocolatey): [PROGRAM_DATA]\chocolatey\bin\npx.exe
```

## 3. Test Playwright MCP

**Quick test (runs temporarily):**
```powershell
npx @playwright/mcp@latest --help
```

This downloads the package and shows available options.

## 4. Add to Windsurf Global Config

Run this PowerShell script to add Playwright MCP without modifying existing servers:

```powershell
# === Add Microsoft Playwright MCP to Windsurf ===

# Pre-checks
Write-Host "=== Pre-flight Checks ===" -ForegroundColor Cyan

# Check npx availability
$npxPath = Get-Command npx -ErrorAction SilentlyContinue
if (-not $npxPath) {
    Write-Host "[FAIL] npx not found in PATH" -ForegroundColor Red
    Write-Host "Install Node.js 18+ from https://nodejs.org" -ForegroundColor Yellow
    return
}
Write-Host "[OK] npx found: $($npxPath.Source)" -ForegroundColor Green

# Check Node.js version
$nodeVersion = node --version 2>$null
if ($nodeVersion -match 'v(\d+)') {
    $majorVersion = [int]$matches[1]
    if ($majorVersion -lt 18) {
        Write-Host "[WARN] Node.js $nodeVersion detected, v18+ recommended" -ForegroundColor Yellow
    } else {
        Write-Host "[OK] Node.js $nodeVersion" -ForegroundColor Green
    }
}

Write-Host ""

$configPath = "$env:USERPROFILE\.codeium\windsurf\mcp_config.json"

# Expected target config
$targetServer = @{
    command = "npx"
    args = @("@playwright/mcp@latest")
}

# Read existing config or create empty structure
$needsUpdate = $false
if (Test-Path $configPath) {
    try {
        $configContent = Get-Content $configPath -Raw
        if ([string]::IsNullOrWhiteSpace($configContent)) {
            $config = @{ mcpServers = @{} }
            $needsUpdate = $true
        } else {
            $config = $configContent | ConvertFrom-Json -AsHashtable
        }
    } catch {
        Write-Host "Error reading config: $_" -ForegroundColor Red
        Write-Host "Creating new config" -ForegroundColor Yellow
        $config = @{ mcpServers = @{} }
        $needsUpdate = $true
    }
} else {
    # Create directory if needed
    $configDir = Split-Path $configPath
    if (-not (Test-Path $configDir)) {
        New-Item -ItemType Directory -Path $configDir -Force | Out-Null
    }
    $config = @{ mcpServers = @{} }
    $needsUpdate = $true
}

# Ensure mcpServers key exists (handle both Hashtable and PSCustomObject)
if ($config -is [System.Collections.Hashtable]) {
    if (-not $config.ContainsKey("mcpServers") -or $null -eq $config.mcpServers) {
        $config.mcpServers = @{}
        $needsUpdate = $true
    }
} else {
    # PSCustomObject from JSON - convert to hashtable for easier manipulation
    $configHash = @{}
    $config.PSObject.Properties | ForEach-Object { $configHash[$_.Name] = $_.Value }
    $config = $configHash
    if (-not $config.mcpServers) {
        $config.mcpServers = @{}
        $needsUpdate = $true
    }
}

# Convert mcpServers to hashtable if needed
if ($config.mcpServers -and $config.mcpServers -isnot [System.Collections.Hashtable]) {
    $serversHash = @{}
    $config.mcpServers.PSObject.Properties | ForEach-Object { $serversHash[$_.Name] = $_.Value }
    $config.mcpServers = $serversHash
}

# Check current state vs target state
if ($config.mcpServers.ContainsKey("playwright")) {
    $current = $config.mcpServers.playwright
    $currentJson = $current | ConvertTo-Json -Depth 5 -Compress
    $targetJson = $targetServer | ConvertTo-Json -Depth 5 -Compress
    
    if ($currentJson -eq $targetJson) {
        Write-Host "Playwright MCP already configured with correct settings" -ForegroundColor Green
        Write-Host "No changes needed" -ForegroundColor Gray
    } else {
        Write-Host "Playwright MCP exists but with different settings:" -ForegroundColor Yellow
        Write-Host "Current: $currentJson" -ForegroundColor Gray
        Write-Host "Target:  $targetJson" -ForegroundColor Gray
        $response = Read-Host "Update to target settings? (y/n)"
        if ($response -eq 'y') {
            $needsUpdate = $true
            $config.mcpServers["playwright"] = $targetServer
        }
    }
} else {
    $needsUpdate = $true
    $config.mcpServers["playwright"] = $targetServer
}

# Only write if changes are needed
if ($needsUpdate) {
    # Backup before modifying
    if (Test-Path $configPath) {
        $backupPath = "$configPath._beforeAddingMsPlaywrightMcp_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
        try {
            Copy-Item $configPath $backupPath -ErrorAction Stop
            Write-Host "Backup: $backupPath" -ForegroundColor Cyan
        } catch {
            Write-Host "[FAIL] Could not create backup: $_" -ForegroundColor Red
            Write-Host "Aborting to prevent data loss" -ForegroundColor Yellow
            return
        }
    }
    
    try {
        $config | ConvertTo-Json -Depth 10 | Set-Content $configPath -Encoding UTF8 -ErrorAction Stop
        Write-Host "Added Playwright MCP to Windsurf" -ForegroundColor Green
    } catch {
        Write-Host "[FAIL] Could not write config: $_" -ForegroundColor Red
        if ($backupPath -and (Test-Path $backupPath)) {
            Write-Host "Restoring from backup..." -ForegroundColor Yellow
            Copy-Item $backupPath $configPath -Force
        }
        return
    }
}

# === Installation Summary ===
Write-Host ""
Write-Host "=== Installation Summary ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Installed components:" -ForegroundColor White

# MCP Config
Write-Host "  [C] MCP Config entry" -ForegroundColor Green
Write-Host "      Path: $configPath" -ForegroundColor Gray

# NPM package (downloaded on first use)
$npxCacheDir = "$env:LOCALAPPDATA\npm-cache\_npx"
$hasNpmCache = $false
if (Test-Path $npxCacheDir) {
    $playwrightCache = Get-ChildItem $npxCacheDir -Directory -ErrorAction SilentlyContinue | Where-Object {
        Test-Path "$($_.FullName)\node_modules\@playwright" -ErrorAction SilentlyContinue
    } | Select-Object -First 1
    if ($playwrightCache) {
        $hasNpmCache = $true
        Write-Host "  [N] NPM package (cached)" -ForegroundColor Green
        Write-Host "      Path: $($playwrightCache.FullName)" -ForegroundColor Gray
    }
}
if (-not $hasNpmCache) {
    Write-Host "  [N] NPM package (will download on first use)" -ForegroundColor Yellow
    Write-Host "      Path: $npxCacheDir\<hash>\node_modules\@playwright" -ForegroundColor Gray
}

# Playwright browsers
$browsersDir = "$env:LOCALAPPDATA\ms-playwright"
if (Test-Path $browsersDir) {
    $size = [math]::Round((Get-ChildItem $browsersDir -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB, 0)
    Write-Host "  [B] Playwright browsers ($size MB)" -ForegroundColor Green
    Write-Host "      Path: $browsersDir" -ForegroundColor Gray
} else {
    Write-Host "  [B] Playwright browsers (will download on first use)" -ForegroundColor Yellow
    Write-Host "      Path: $browsersDir" -ForegroundColor Gray
}

# User profile (if configured)
$profileDir = "$env:USERPROFILE\.ms-playwright-mcp-profile"
if (Test-Path $profileDir) {
    Write-Host "  [P] User profile (persistent logins)" -ForegroundColor Green
    Write-Host "      Path: $profileDir" -ForegroundColor Gray
} else {
    Write-Host "  [P] User profile (not configured)" -ForegroundColor Gray
    Write-Host "      Path: $profileDir (create with --user-data-dir)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor White
Write-Host "  1. Restart Windsurf" -ForegroundColor White
Write-Host "  2. Check MCP status: Command Palette > 'MCP: Show Servers'" -ForegroundColor White
Write-Host "  3. Test: Ask AI to 'Navigate to https://example.com'" -ForegroundColor White
Write-Host ""
```

## 5. Configuration Options

### Persistent User Profile (remembers logins)

Modify the args in your config:
```json
"args": [
  "@playwright/mcp@latest",
  "--user-data-dir", "[USER_PROFILE_PATH]/.ms-playwright-mcp-profile"
]
```

**Create profile directory:**
```powershell
$profileDir = "$env:USERPROFILE\.ms-playwright-mcp-profile"
if (-not (Test-Path $profileDir)) { New-Item -ItemType Directory -Path $profileDir }
```

### Headless Mode (no visible browser)

```json
"args": ["@playwright/mcp@latest", "--headless"]
```

### Specific Browser

```json
"args": ["@playwright/mcp@latest", "--browser", "firefox"]
```

Options: `chromium` (default), `firefox`, `webkit`

### Storage State (pre-authenticated)

```json
"args": [
  "@playwright/mcp@latest",
  "--isolated",
  "--storage-state", "[AUTH_STATE_PATH]"
]
```

### Browser Extension Mode

Connect to existing browser with remote debugging:
```json
"args": ["@playwright/mcp@latest", "--extension"]
```

**Start Chrome with debugging enabled:**
```powershell
& "[PROGRAM_FILES]\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
```

## 6. Verify Installation

After configuring, restart Windsurf.

**Check MCP server status:**
- View > Command Palette > "MCP: Show Servers"
- Playwright should show green status

**Test basic navigation:**
Ask the AI: "Navigate to https://example.com and take a screenshot"

## 7. Troubleshooting

### npx not found

**Solution 1: Use full path**
```json
{
  "command": "[NPX_FULL_PATH]",
  "args": ["@playwright/mcp@latest"]
}
```

**Solution 2: Add Node to PATH**
```powershell
$nodePath = "[NODEJS_INSTALL_PATH]"
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";$nodePath", "User")
```

### Profile lock error

Browser profile is locked by another process:
```powershell
# Close Chrome processes using the profile
Get-Process chrome -ErrorAction SilentlyContinue | Stop-Process -Force

# Remove lock file
$profileDir = "$env:USERPROFILE\.ms-playwright-mcp-profile"
Remove-Item "$profileDir\SingletonLock" -Force -ErrorAction SilentlyContinue
```

### MCP server shows orange/red status

1. Check if npx works in terminal: `npx --version`
2. Try running MCP manually: `npx @playwright/mcp@latest --help`
3. Check for error messages in MCP client logs
4. Restart Windsurf

### Extension mode not connecting

Known issue (GitHub #921): `--extension` flag may launch new Chrome instead of connecting.

**Workaround:** Start Chrome with `--remote-debugging-port=9222` before enabling extension mode.

### Playwright browsers not installed

If you see "Browser not found" errors:
```powershell
npx playwright install chromium
npx playwright install firefox
npx playwright install webkit
```

### Linux inotify exhaustion

Error: "no space left on device" (not disk space - inotify watches)

**Fix:**
```bash
echo "fs.inotify.max_user_watches = 2097152" | sudo tee /etc/sysctl.d/99-playwright.conf
sudo sysctl -p /etc/sysctl.d/99-playwright.conf
```

## 8. Security Considerations

### Credential Storage

- Use `--user-data-dir` for persistent sessions (stores cookies locally)
- Use `--storage-state` to load pre-saved auth (JSON file)
- Never commit auth.json or profile directories to git

### Add to .gitignore

```gitignore
# Playwright MCP
.ms-playwright-mcp-profile/
auth.json
*.auth.json
```

### Headless vs Headed

- **Headed** (default): Browser window visible, easier to debug
- **Headless**: No window, faster, but some sites detect and block

## 9. Completion Checklist

- [ ] Node.js 18+ installed
- [ ] npx accessible (full path if needed)
- [ ] Ran setup script (Section 4)
- [ ] MCP server shows green status
- [ ] Test navigation works
- [ ] (Optional) Persistent profile configured

## Quick Reference

- **Default** - Clean isolated sessions
- **`--user-data-dir`** - Persistent logins
- **`--headless`** - Background automation
- **`--isolated --storage-state`** - Pre-authenticated
- **`--extension`** - Connect to existing browser
