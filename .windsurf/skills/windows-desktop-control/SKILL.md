# Windows Desktop Control

Utilities for Windows desktop automation: screenshots, window management, keyboard/mouse simulation.

## Prerequisites

- Windows OS
- PowerShell 5.1+

## Tools

### simple-screenshot.ps1

Takes a passive screenshot without any UI interaction. Handles DPI scaling correctly.

**Usage:**
```powershell
# Full screen (uses physical resolution, handles DPI scaling)
.\simple-screenshot.ps1

# Custom output path
.\simple-screenshot.ps1 -OutputPath "C:\temp\screenshot.jpg"

# Custom region
.\simple-screenshot.ps1 -Width 1920 -Height 1080 -X 0 -Y 0
```

**Parameters:**
- `-OutputPath` - Output file path (default: `.tools/_screenshots/YYYY-MM-DD_HH-mm-ss_screenshot.jpg`)
- `-Width` - Capture width in pixels (default: full screen physical width)
- `-Height` - Capture height in pixels (default: full screen physical height)
- `-X` - Capture X offset (default: 0)
- `-Y` - Capture Y offset (default: 0)

**DPI Scaling:**
Uses Win32 `GetDeviceCaps(DESKTOPHORZRES/DESKTOPVERTRES)` to get physical resolution, not logical. This ensures correct capture on systems with DPI scaling (125%, 150%, etc.).

## Notes

- Screenshots saved as JPEG
- Default output folder created automatically if missing
- No keyboard/mouse input sent - purely passive capture
