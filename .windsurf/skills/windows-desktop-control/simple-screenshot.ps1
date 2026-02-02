# Simple Screenshot - No UI Interaction
# Takes a passive screenshot without sending any keystrokes
# Use this for testing/verification, NOT for model registry updates

param(
    [string]$OutputPath = "",
    [int]$Width = 0,
    [int]$Height = 0,
    [int]$X = 0,
    [int]$Y = 0
)

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

# Use physical screen size if no dimensions specified
if ($Width -eq 0) { $Width = $physWidth }
if ($Height -eq 0) { $Height = $physHeight }

# Default output path
if (-not $OutputPath) {
    # Navigate up: script -> windows-desktop-control -> skills -> .windsurf -> workspace
    $workspaceRoot = (Get-Item $PSScriptRoot).Parent.Parent.Parent.FullName
    $timestamp = "simple-screenshot_" + (Get-Date -Format "yyyy-MM-dd_HH-mm-ss-fff")
    $screenshotDir = Join-Path $workspaceRoot ".tools\_screenshots"
    
    if (-not (Test-Path $screenshotDir)) {
        New-Item -ItemType Directory -Path $screenshotDir | Out-Null
    }
    
    $OutputPath = Join-Path $screenshotDir "${timestamp}_screenshot.jpg"
}

# Capture screenshot
$bitmap = New-Object System.Drawing.Bitmap($Width, $Height)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen($X, $Y, 0, 0, $bitmap.Size)

# Save
$bitmap.Save($OutputPath, [System.Drawing.Imaging.ImageFormat]::Jpeg)
$graphics.Dispose()
$bitmap.Dispose()

Write-Host "Screenshot saved: $OutputPath"
Write-Host "Size: ${Width}x${Height} at ($X, $Y)"
