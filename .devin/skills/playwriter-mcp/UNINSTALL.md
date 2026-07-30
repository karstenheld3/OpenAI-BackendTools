# Playwriter MCP Uninstall

Remove Playwriter components from your system.

## 1. Remove from Windsurf MCP Config

```powershell
# === Remove Playwriter from Windsurf MCP Config ===

$configPath = "$env:USERPROFILE\.codeium\windsurf\mcp_config.json"

if (-not (Test-Path $configPath)) {
    Write-Host "MCP config not found at: $configPath" -ForegroundColor Yellow
    return
}

# Read existing config
try {
    $configContent = Get-Content $configPath -Raw
    $config = $configContent | ConvertFrom-Json -AsHashtable
} catch {
    Write-Host "Error reading config: $_" -ForegroundColor Red
    return
}

# Convert to hashtable if needed
if ($config -isnot [System.Collections.Hashtable]) {
    $configHash = @{}
    $config.PSObject.Properties | ForEach-Object { $configHash[$_.Name] = $_.Value }
    $config = $configHash
}

# Check if playwriter exists
if (-not $config.mcpServers -or -not $config.mcpServers.ContainsKey("playwriter")) {
    Write-Host "Playwriter not found in MCP config" -ForegroundColor Yellow
    return
}

# Backup before removal
$backupPath = "$configPath._beforeRemovingPlaywriter_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Copy-Item $configPath $backupPath
Write-Host "Backup: $backupPath" -ForegroundColor Cyan

# Remove playwriter
$config.mcpServers.Remove("playwriter")

# Write updated config
$config | ConvertTo-Json -Depth 10 | Set-Content $configPath -Encoding UTF8
Write-Host "Removed Playwriter from Windsurf MCP config" -ForegroundColor Green
Write-Host "Restart Windsurf to complete" -ForegroundColor Yellow
```

## 2. Uninstall CLI

```powershell
npm uninstall -g playwriter
```

**Verify removal:**
```powershell
Get-Command playwriter -ErrorAction SilentlyContinue
# Should return nothing
```

## 3. Remove Chrome Extension

1. Open Chrome
2. Go to `chrome://extensions/`
3. Find "Playwriter MCP"
4. Click "Remove"

## 4. Clean Up Data (Optional)

Remove relay server logs and state:
```powershell
$playwriterDir = "$env:USERPROFILE\.playwriter"
if (Test-Path $playwriterDir) {
    Remove-Item $playwriterDir -Recurse -Force
    Write-Host "Removed: $playwriterDir" -ForegroundColor Green
} else {
    Write-Host "No Playwriter data directory found" -ForegroundColor Yellow
}
```

## 5. Remove Skill (if installed)

```powershell
npx -y skills remove remorses/playwriter
```

## Uninstall Checklist

- [ ] Removed from MCP config
- [ ] CLI uninstalled (`npm uninstall -g playwriter`)
- [ ] Chrome extension removed
- [ ] (Optional) Data directory cleaned up
- [ ] (Optional) Skill removed
- [ ] Windsurf restarted

## Verify Complete Removal

```powershell
# Check CLI removed
Get-Command playwriter -ErrorAction SilentlyContinue

# Check MCP config
$config = Get-Content "$env:USERPROFILE\.codeium\windsurf\mcp_config.json" | ConvertFrom-Json
$config.mcpServers | Get-Member -Name playwriter

# Check data directory
Test-Path "$env:USERPROFILE\.playwriter"
```

All commands should return empty/false after complete removal.
