# Model Registry Update - Captures Model Selector Screenshots
# 
# WARNING: This script OPENS the model selector popup and sends keystrokes.
# DO NOT use for general screenshots - use windows-desktop-control/simple-screenshot.ps1 instead.
#
# Captures fullscreen screenshots while scrolling through the model selector list.

param(
    [string]$WindowTitle = "*Windsurf*",
    [string]$OutputFolder = "",
    [int]$ScrollsPerSection = 7,
    [int]$MaxSections = 10
)

# Default output folder if not specified
if (-not $OutputFolder) {
    # Navigate up: script -> update-model-registry -> windsurf-auto-model-switcher -> skills -> .windsurf -> workspace
    $workspaceRoot = (Get-Item $PSScriptRoot).Parent.Parent.Parent.Parent.Parent.FullName
    $OutputFolder = Join-Path $workspaceRoot "..\.tools\_screenshots"
}

# Timestamp prefix for filenames (with milliseconds and script name)
$filePrefix = "capture-model-selector_" + (Get-Date -Format "yyyy-MM-dd_HH-mm-ss-fff")

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Get PHYSICAL screen resolution (handles DPI scaling)
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public class ScreenMetrics {
    [DllImport("user32.dll")]
    public static extern IntPtr GetDC(IntPtr hwnd);
    [DllImport("user32.dll")]
    public static extern int ReleaseDC(IntPtr hwnd, IntPtr hdc);
    [DllImport("gdi32.dll")]
    public static extern int GetDeviceCaps(IntPtr hdc, int nIndex);
    public const int DESKTOPHORZRES = 118;
    public const int DESKTOPVERTRES = 117;
}
"@ -ErrorAction SilentlyContinue

$hdc = [ScreenMetrics]::GetDC([IntPtr]::Zero)
$physWidth = [ScreenMetrics]::GetDeviceCaps($hdc, [ScreenMetrics]::DESKTOPHORZRES)
$physHeight = [ScreenMetrics]::GetDeviceCaps($hdc, [ScreenMetrics]::DESKTOPVERTRES)
[ScreenMetrics]::ReleaseDC([IntPtr]::Zero, $hdc) | Out-Null

Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32 {
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")]
    public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
    public const byte VK_CONTROL = 0x11;
    public const byte VK_SHIFT = 0x10;
    public const byte VK_F9 = 0x78;
    public const byte VK_UP = 0x26;
    public const byte VK_DOWN = 0x28;
    public const byte VK_TAB = 0x09;
    public const byte VK_SPACE = 0x20;
    public const byte VK_ESCAPE = 0x1B;
    public const uint KEYEVENTF_KEYUP = 0x0002;

    public static void SendKey(byte key) {
        keybd_event(key, 0, 0, UIntPtr.Zero);
        System.Threading.Thread.Sleep(30);
        keybd_event(key, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
        System.Threading.Thread.Sleep(30);
    }
    public static void SendCtrlShiftF9() {
        keybd_event(VK_CONTROL, 0, 0, UIntPtr.Zero);
        keybd_event(VK_SHIFT, 0, 0, UIntPtr.Zero);
        keybd_event(VK_F9, 0, 0, UIntPtr.Zero);
        System.Threading.Thread.Sleep(50);
        keybd_event(VK_F9, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
        keybd_event(VK_SHIFT, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
        keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
    }
}
"@

if (-not (Test-Path $OutputFolder)) {
    New-Item -ItemType Directory -Path $OutputFolder | Out-Null
}

$proc = Get-Process -Name "Windsurf" -ErrorAction SilentlyContinue |
    Where-Object { $_.MainWindowTitle -like $WindowTitle -and $_.MainWindowTitle -ne "" } |
    Select-Object -First 1

if (-not $proc) { Write-Error "No Windsurf window found"; exit 1 }

[Win32]::SetForegroundWindow($proc.MainWindowHandle) | Out-Null
Start-Sleep -Milliseconds 500

# Open model selector
[Win32]::SendCtrlShiftF9()
Start-Sleep -Milliseconds 400

# Navigate to model list
[Win32]::SendKey([Win32]::VK_UP)
Start-Sleep -Milliseconds 100
[Win32]::SendKey([Win32]::VK_TAB)
Start-Sleep -Milliseconds 100
[Win32]::SendKey([Win32]::VK_SPACE)
Start-Sleep -Milliseconds 100
[Win32]::SendKey([Win32]::VK_DOWN)
Start-Sleep -Milliseconds 300

Write-Host "Capturing $MaxSections fullscreen sections at ${physWidth}x${physHeight}"

for ($section = 1; $section -le $MaxSections; $section++) {
    # Capture fullscreen using physical resolution
    $bitmap = New-Object System.Drawing.Bitmap($physWidth, $physHeight)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.CopyFromScreen(0, 0, 0, 0, $bitmap.Size)
    $filename = Join-Path $OutputFolder ("${filePrefix}_section_{0:D2}.jpg" -f $section)
    $bitmap.Save($filename, [System.Drawing.Imaging.ImageFormat]::Jpeg)
    $graphics.Dispose()
    $bitmap.Dispose()
    
    Write-Host "Captured section $section"
    
    # Scroll down
    for ($i = 0; $i -lt $ScrollsPerSection; $i++) {
        [Win32]::SendKey([Win32]::VK_DOWN)
    }
    Start-Sleep -Milliseconds 150
}

[Win32]::SendKey([Win32]::VK_ESCAPE)
Write-Host "`nDone! Screenshots saved to: $OutputFolder"
Write-Host "Cascade: Read screenshots, extract models, then delete folder."
