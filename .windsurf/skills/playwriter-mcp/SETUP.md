# Playwriter MCP Setup

Run once to configure Playwriter for real browser automation with existing logins.

## 1. Verify Node.js Installation

```powershell
node --version
npm --version
```

Expected: Node.js 18+ installed and in PATH.
If not installed: Download from https://nodejs.org (LTS version recommended).

## 2. Install Chrome Extension

**Install from Chrome Web Store:**
https://chromewebstore.google.com/detail/playwriter-mcp/jfeammnjpkecdekppnclgkkffahnhfhe

After installation:
- Click extension icon on any tab you want to control
- Icon turns **green** = connected and controllable
- Icon stays **gray** = not attached to this tab

## 3. Install CLI

```powershell
npm i -g playwriter
```

**Verify installation:**
```powershell
playwriter --help
```

## 4. Test Connection

```powershell
# Create a session
playwriter session new

# Should output a session ID (e.g., 1)
```

**Multiple browsers/profiles detected?** If you see a list of browsers, specify which one:
```powershell
playwriter session new --browser "browser:Chrome"
# or use a specific profile:
playwriter session new --browser "profile:<profile-id>"
```

```powershell
# Navigate (replace 1 with your session ID)
playwriter -s 1 -e 'await page.goto("https://example.com")'
```

If successful, the tab with the green extension icon will navigate to example.com.

## 5. Install Skill for Agents (Recommended)

This teaches AI agents how to use Playwriter:

```powershell
npx -y skills add remorses/playwriter
```

## 6. Add to Windsurf MCP Config (Optional)

If you prefer direct MCP configuration instead of skill-based:

```powershell
# === Add Playwriter to Windsurf MCP Config ===

# Pre-flight checks
Write-Host "=== Pre-flight Checks ===" -ForegroundColor Cyan

# Check Node.js
$nodeVersion = node --version 2>$null
if ($nodeVersion -match 'v(\d+)') {
    $majorVersion = [int]$matches[1]
    if ($majorVersion -lt 18) {
        Write-Host "[WARN] Node.js $nodeVersion detected, v18+ recommended" -ForegroundColor Yellow
    } else {
        Write-Host "[OK] Node.js $nodeVersion" -ForegroundColor Green
    }
} else {
    Write-Host "[FAIL] Node.js not found" -ForegroundColor Red
    Write-Host "Install from https://nodejs.org" -ForegroundColor Yellow
    return
}

# Check playwriter CLI
$pwCli = Get-Command playwriter -ErrorAction SilentlyContinue
if (-not $pwCli) {
    Write-Host "[WARN] playwriter CLI not installed" -ForegroundColor Yellow
    Write-Host "Run: npm i -g playwriter" -ForegroundColor Yellow
} else {
    Write-Host "[OK] playwriter CLI found: $($pwCli.Source)" -ForegroundColor Green
}

Write-Host ""

$configPath = "$env:USERPROFILE\.codeium\windsurf\mcp_config.json"

# Target config
$targetServer = @{
    command = "npx"
    args = @("playwriter@latest")
}

# Read existing config
if (Test-Path $configPath) {
    try {
        $configContent = Get-Content $configPath -Raw
        if ([string]::IsNullOrWhiteSpace($configContent)) {
            $config = @{ mcpServers = @{} }
        } else {
            $config = $configContent | ConvertFrom-Json -AsHashtable
        }
    } catch {
        Write-Host "Error reading config: $_" -ForegroundColor Red
        $config = @{ mcpServers = @{} }
    }
} else {
    $configDir = Split-Path $configPath
    if (-not (Test-Path $configDir)) {
        New-Item -ItemType Directory -Path $configDir -Force | Out-Null
    }
    $config = @{ mcpServers = @{} }
}

# Ensure mcpServers exists
if ($config -isnot [System.Collections.Hashtable]) {
    $configHash = @{}
    $config.PSObject.Properties | ForEach-Object { $configHash[$_.Name] = $_.Value }
    $config = $configHash
}
if (-not $config.mcpServers) {
    $config.mcpServers = @{}
}
if ($config.mcpServers -isnot [System.Collections.Hashtable]) {
    $serversHash = @{}
    $config.mcpServers.PSObject.Properties | ForEach-Object { $serversHash[$_.Name] = $_.Value }
    $config.mcpServers = $serversHash
}

# Add playwriter
$config.mcpServers["playwriter"] = $targetServer

# Backup and write
if (Test-Path $configPath) {
    $backupPath = "$configPath._beforeAddingPlaywriter_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    Copy-Item $configPath $backupPath
    Write-Host "Backup: $backupPath" -ForegroundColor Cyan
}

$config | ConvertTo-Json -Depth 10 | Set-Content $configPath -Encoding UTF8
Write-Host "Added Playwriter to Windsurf MCP config" -ForegroundColor Green

# === Installation Summary ===
Write-Host ""
Write-Host "=== Installation Summary ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Installed components:" -ForegroundColor White

# MCP Config
Write-Host "  [C] MCP Config entry" -ForegroundColor Green
Write-Host "      Path: $configPath" -ForegroundColor Gray

# CLI
$globalNpmPath = npm root -g 2>$null
if ($globalNpmPath -and (Test-Path "$globalNpmPath\playwriter")) {
    Write-Host "  [N] playwriter CLI (global)" -ForegroundColor Green
    Write-Host "      Path: $globalNpmPath\playwriter" -ForegroundColor Gray
} else {
    Write-Host "  [N] playwriter CLI (not installed globally)" -ForegroundColor Yellow
}

# Relay logs location
Write-Host "  [L] Relay server logs" -ForegroundColor Gray
Write-Host "      Path: ~/.playwriter/relay-server.log" -ForegroundColor Gray

Write-Host ""
Write-Host "Next steps:" -ForegroundColor White
Write-Host "  1. Install Chrome extension from Web Store" -ForegroundColor White
Write-Host "  2. Restart Windsurf" -ForegroundColor White
Write-Host "  3. Click extension icon on a tab (turns green)" -ForegroundColor White
Write-Host "  4. Test: playwriter session new" -ForegroundColor White
Write-Host ""
```

## 7. Verify Setup

After configuration, restart Windsurf.

**Check MCP server status:**
- View > Command Palette > "MCP: Show Servers"
- Playwriter should show green status (if using MCP config)

**Test via CLI:**
```powershell
playwriter session new
playwriter -s 1 -e 'console.log(await page.title())'
```

## Troubleshooting

### Extension Icon Not Turning Green

1. Click directly on the extension icon (not right-click)
2. Ensure tab is a normal webpage (not chrome://, about:, or extension pages)
3. Try refreshing the page first

### CLI Says "No Sessions"

```powershell
playwriter session new
```

### Connection Errors

```powershell
playwriter session reset 1
```

### View Logs

```powershell
playwriter logfile
# Shows path to ~/.playwriter/relay-server.log
```

### All Pages Return about:blank

Restart Chrome completely (known Chrome bug).

## Completion Checklist

- [ ] Node.js 18+ installed
- [ ] Chrome extension installed from Web Store
- [ ] CLI installed (`npm i -g playwriter`)
- [ ] Extension icon turns green when clicked
- [ ] `playwriter session new` works
- [ ] Test navigation works
- [ ] (Optional) Skill installed for agents
- [ ] (Optional) MCP config added

## 8. Configuration Options

### Environment Variables

**Remote host** (connect to Playwriter on another machine):
```powershell
$env:PLAYWRITER_HOST = "192.168.1.10"  # LAN IP
# or
$env:PLAYWRITER_HOST = "https://my-machine.traforo.dev"  # Tunnel
```

**Authentication token** (required for remote access):
```powershell
$env:PLAYWRITER_TOKEN = "your-secret-token"
```

### MCP Config with Environment Variables

```json
{
  "mcpServers": {
    "playwriter": {
      "command": "npx",
      "args": ["playwriter@latest"],
      "env": {
        "PLAYWRITER_HOST": "192.168.1.10",
        "PLAYWRITER_TOKEN": "your-secret-token"
      }
    }
  }
}
```

### Server Mode (for remote access)

Start Playwriter as a server that accepts remote connections:
```powershell
npx -y playwriter serve --token <secret>
```

With tunnel for internet access:
```powershell
npx -y traforo -p 19988 -t my-machine -- npx -y playwriter serve --token <secret>
```

## Quick Reference

- **Extension**: Click icon on tab to enable (green = active)
- **CLI**: `playwriter -s <id> -e '<code>'`
- **Session**: `playwriter session new` / `list` / `reset`
- **Logs**: `playwriter logfile`
- **WebSocket**: `localhost:19988`
- **Remote**: Set `PLAYWRITER_HOST` and `PLAYWRITER_TOKEN`
