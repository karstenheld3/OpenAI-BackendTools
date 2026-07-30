# Windsurf Auto Model Switcher - Select specific model by query
# Opens model selector (Ctrl+Shift+F9), types query, selects first match

param(
    [Parameter(Mandatory = $true)]
    [string]$Query,

    [string]$WindowTitle = "*Windsurf*",

    [int]$OpenDelayMs = 400,
    [int]$AfterEnterDelayMs = 300,
    
    [switch]$DryRun
)

Add-Type -AssemblyName System.Windows.Forms

# MANDATORY: Find best matching model in registry before ANY keyboard events
$registryPath = Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Path) "windsurf-model-registry.json"

# Hardcoded safe fallback models (always available in Windsurf)
# DEFAULT: Claude Sonnet 4 (2x) - used when no match found
$safeFallbackModels = @(
    @{Name="Claude Sonnet 4"; cost="2x"},
    @{Name="Claude Haiku 4.5"; cost="1x"},
    @{Name="Claude Opus 4.5 (Thinking)"; cost="5x"}
)

if (-not (Test-Path $registryPath)) {
    Write-Host "Registry not found. Using safe fallback models." -ForegroundColor Yellow
    Write-Host "Tip: Run update-model-registry workflow to get full model list" -ForegroundColor Cyan
    $registry = @{models = $safeFallbackModels}
} else {
    $registry = Get-Content $registryPath -Raw | ConvertFrom-Json
}

# Fuzzy match: score by word matches, prefer lower cost when tied
$queryWords = $Query.ToLower().Split(' ')
$scored = $registry.models | ForEach-Object {
    $modelName = $_.name.ToLower()
    $score = 0
    foreach ($word in $queryWords) {
        if ($modelName.Contains($word)) { $score++ }
    }
    # Parse cost multiplier (e.g., "2x" -> 2, "0.5x" -> 0.5, "Free" -> 0)
    $costStr = $_.cost
    $costNum = if ($costStr -eq "Free") { 0 } 
               elseif ($costStr -match '^([\d.]+)x$') { [double]$Matches[1] }
               else { 999 }
    [PSCustomObject]@{
        Name = $_.name
        Score = $score
        Cost = $costNum
    }
} | Where-Object { $_.Score -gt 0 } | Sort-Object -Property @{Expression="Score";Descending=$true}, @{Expression="Cost";Descending=$false}

if ($scored.Count -eq 0) {
    Write-Host "No match for '$Query'. Defaulting to Claude Sonnet 4" -ForegroundColor Yellow
    $Query = "Claude Sonnet 4"
    $finalCost = "2x"
} else {
    $bestMatch = $scored[0].Name
    $bestCost = $scored[0].Cost
    if ($bestMatch -ne $Query) {
        $costDisplay = "$bestCost" + "x"
        Write-Host "Fuzzy match: '$Query' -> '$bestMatch' ($costDisplay)"
    }
    $Query = $bestMatch
    $finalCost = "$bestCost" + "x"
}

# DRY RUN MODE - Preview selection without executing
if ($DryRun) {
    Write-Host ""
    Write-Host "=== DRY RUN MODE ===" -ForegroundColor Cyan
    Write-Host "Would select: $Query" -ForegroundColor Green
    Write-Host "Cost: $finalCost" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To execute: Run without -DryRun parameter" -ForegroundColor Gray
    exit 0
}

Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32 {
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")]
    public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
    [DllImport("user32.dll")]
    public static extern bool SetCursorPos(int X, int Y);
    [DllImport("user32.dll")]
    public static extern void mouse_event(uint dwFlags, int dx, int dy, uint dwData, UIntPtr dwExtraInfo);

    public const byte VK_CONTROL = 0x11;
    public const byte VK_SHIFT = 0x10;
    public const byte VK_F9 = 0x78;
    public const byte VK_A = 0x41;
    public const byte VK_RETURN = 0x0D;
    public const byte VK_ESCAPE = 0x1B;
    public const byte VK_DOWN = 0x28;
    public const uint KEYEVENTF_KEYUP = 0x0002;
    public const uint MOUSEEVENTF_LEFTDOWN = 0x0002;
    public const uint MOUSEEVENTF_LEFTUP = 0x0004;

    public static void SendCtrlShiftF9() {
        keybd_event(VK_CONTROL, 0, 0, UIntPtr.Zero);
        keybd_event(VK_SHIFT, 0, 0, UIntPtr.Zero);
        keybd_event(VK_F9, 0, 0, UIntPtr.Zero);
        System.Threading.Thread.Sleep(50);
        keybd_event(VK_F9, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
        keybd_event(VK_SHIFT, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
        keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
    }

    public static void SendDown() {
        keybd_event(VK_DOWN, 0, 0, UIntPtr.Zero);
        System.Threading.Thread.Sleep(30);
        keybd_event(VK_DOWN, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
    }

    public static void SendEnter() {
        keybd_event(VK_RETURN, 0, 0, UIntPtr.Zero);
        System.Threading.Thread.Sleep(30);
        keybd_event(VK_RETURN, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
    }

    public static void SendEscape() {
        keybd_event(VK_ESCAPE, 0, 0, UIntPtr.Zero);
        System.Threading.Thread.Sleep(30);
        keybd_event(VK_ESCAPE, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
    }

    public static void SendCtrlShiftA() {
        keybd_event(VK_CONTROL, 0, 0, UIntPtr.Zero);
        keybd_event(VK_SHIFT, 0, 0, UIntPtr.Zero);
        keybd_event(VK_A, 0, 0, UIntPtr.Zero);
        System.Threading.Thread.Sleep(50);
        keybd_event(VK_A, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
        keybd_event(VK_SHIFT, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
        keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
    }
}
"@

$proc = Get-Process -Name "Windsurf" -ErrorAction SilentlyContinue |
    Where-Object { $_.MainWindowTitle -like $WindowTitle -and $_.MainWindowTitle -ne "" } |
    Select-Object -First 1

if (-not $proc) {
    Write-Error "No Windsurf window found matching: $WindowTitle"
    exit 1
}

Write-Host "Focusing: $($proc.MainWindowTitle)"
[Win32]::SetForegroundWindow($proc.MainWindowHandle) | Out-Null
Start-Sleep -Milliseconds 400

# Close any open selector/menu first
[Win32]::SendEscape()
Start-Sleep -Milliseconds 120

# Open model selector (Ctrl+Shift+F9 - custom keybinding)
[Win32]::SendCtrlShiftF9()
Start-Sleep -Milliseconds $OpenDelayMs

# Select all and type query
[System.Windows.Forms.SendKeys]::SendWait('^a')
Start-Sleep -Milliseconds 50
[System.Windows.Forms.SendKeys]::SendWait($Query)
Start-Sleep -Milliseconds 150

# Select first match and confirm (Enter auto-closes selector)
[Win32]::SendDown()
Start-Sleep -Milliseconds 150
[Win32]::SendEnter()
Start-Sleep -Milliseconds 500

# Refocus Cascade chat (Ctrl+Shift+A - official Windsurf toggle)
[Win32]::SendCtrlShiftA()
Start-Sleep -Milliseconds 200

Write-Host "Done. Model should be: $Query"

