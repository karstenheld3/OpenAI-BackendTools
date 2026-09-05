# Image Tools Setup

Installation of ImageMagick 7+ portable for Windows.

All paths relative to `[WORKSPACE_FOLDER]` (e.g., `../.tools/` = `[WORKSPACE_FOLDER]/../.tools/`).

## Pre-Installation Verification

### 1. Check if already installed
```powershell
$toolsDir = Join-Path (Split-Path $PWD.Path -Qualifier) "Dev\.tools"
Test-Path "$toolsDir\magick\magick.exe"
```
Expected: `True` if already installed.

### 2. Test Python Pillow fallback
```powershell
& "$toolsDir\llm-venv\Scripts\python.exe" -c "from PIL import Image; print('Pillow OK:', Image.__version__)"
```
Expected: `Pillow OK: 12.x.x`

### Pre-Installation Checklist
- [ ] `../.tools/magick/` does not exist (or needs upgrade)
- [ ] Pillow fallback verified
- [ ] Internet access available for download

**If all checks pass, proceed to installation.**

## Installation

ImageMagick portable (no system PATH modification, no admin required).

### Step 1: Download portable archive

Download latest ImageMagick 7 portable from:
`https://download.imagemagick.org/archive/binaries/`

Choose: `ImageMagick-7.x.x-xx-portable-Q16-HDRI-x64.7z`

Save to: `../.tools/_installer/`

Requires 7-Zip (`../.tools/7z/7z.exe`) for extraction.

### Step 2: Extract to tools folder
```powershell
$toolsDir = Join-Path (Split-Path $PWD.Path -Qualifier) "Dev\.tools"
$archive = Get-ChildItem "$toolsDir\_installer\ImageMagick-*-portable*.7z" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $archive) { throw "No ImageMagick portable .7z found in _installer/" }

$targetDir = "$toolsDir\magick"
if (Test-Path $targetDir) {
    $backup = "${targetDir}_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    Rename-Item $targetDir $backup
    Write-Host "Existing installation backed up to: $backup"
}

New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
& "$toolsDir\7z\7z.exe" x -y -o"$targetDir" $archive.FullName

Write-Host "Installed to: $targetDir"
```

### Step 3: Verify installation
```powershell
& "$toolsDir\magick\magick.exe" --version
```
Expected: `Version: ImageMagick 7.x.x ...`

### Step 4: Quick functional test
```powershell
$magick = "$toolsDir\magick\magick.exe"
& $magick -size 100x100 xc:red "$toolsDir\magick\test_output.png"
& $magick identify "$toolsDir\magick\test_output.png"
Remove-Item "$toolsDir\magick\test_output.png"
```
Expected: `test_output.png PNG 100x100 ...`

## Post-Installation Verification

1. Format conversion works:
```powershell
$magick = "$toolsDir\magick\magick.exe"
& $magick -size 50x50 xc:blue png:- | & $magick png:- -quality 80 "$toolsDir\magick\test.jpg"
& $magick identify "$toolsDir\magick\test.jpg"
Remove-Item "$toolsDir\magick\test.jpg"
```

2. Delegates available (JPG, PNG, WebP support):
```powershell
& $magick -list format | Select-String "JPEG|PNG|WEBP"
```
Expected: JPEG, PNG, WEBP all show `rw` (read-write).

## Troubleshooting

- **"not recognized"** - Use full path via `$magick` variable, not just `magick`
- **No WebP support** - Portable build may lack `libwebp`. Download full portable ZIP or use Pillow fallback for WebP
- **Permission denied** - Ensure output folder exists and is writable
- **Out of memory** - Process files one at a time, not via `mogrify` on large batches
