# PDF Tools Setup

Run once to install tools locally in `[WORKSPACE_FOLDER]/.tools/`.

## 1. Set Workspace Folder

```powershell
$workspaceFolder = (Get-Location).Path  # or set explicitly: $workspaceFolder = "C:\Dev\MyProject"
$toolsDir = "$workspaceFolder\.tools"
$installerDir = "$toolsDir\_installer"

# Create folders if needed
if (-not (Test-Path $toolsDir)) { New-Item -ItemType Directory -Path $toolsDir }
if (-not (Test-Path $installerDir)) { New-Item -ItemType Directory -Path $installerDir }
```

## 2. Verify Python Installation

```powershell
python --version
```

Expected: Python 3.10+ installed and in PATH.
If not installed: Ask user to install Python from https://python.org

## 3. Install 7-Zip Locally

7-Zip is required to extract Ghostscript from its NSIS installer. The standalone `7za.exe` cannot extract NSIS archives - the full 7z.exe with plugins is required.

**Check if already installed:**
```powershell
Test-Path "$toolsDir\7z\7z.exe"
```

**If not installed, download and extract:**
```powershell
$7zDir = "$toolsDir\7z"

# Download 7-Zip MSI
$7zUrl = "https://www.7-zip.org/a/7z2408-x64.msi"
$msiPath = "$installerDir\7z2408-x64.msi"

Invoke-WebRequest -Uri $7zUrl -OutFile $msiPath

# Extract MSI to temp folder, then move 7-Zip files
$tempDir = "$installerDir\7z-temp"
msiexec /a $msiPath /qn TARGETDIR="$tempDir"
Start-Sleep -Seconds 3

# Move extracted 7-Zip to final location
Move-Item "$tempDir\Files\7-Zip" $7zDir -Force
Remove-Item $tempDir -Recurse -Force -ErrorAction SilentlyContinue
```

**Verify installation:**
```powershell
& "$toolsDir\7z\7z.exe" --help | Select-Object -First 3
```

## 4. Install Poppler Locally

Poppler provides `pdftoppm` for converting PDF pages to images.

**Check if already installed:**
```powershell
Test-Path "$toolsDir\poppler\Library\bin\pdftoppm.exe"
```

**If not installed, download and extract:**
```powershell
$popplerDir = "$toolsDir\poppler"

# Download latest Poppler for Windows
$popplerUrl = "https://github.com/oschwartz10612/poppler-windows/releases/download/v24.08.0-0/Release-24.08.0-0.zip"
$zipPath = "$installerDir\poppler.zip"

Invoke-WebRequest -Uri $popplerUrl -OutFile $zipPath
Expand-Archive -Path $zipPath -DestinationPath $toolsDir -Force

# Find extracted folder (poppler-*) and rename to poppler
$extractedFolder = Get-ChildItem $toolsDir -Directory | Where-Object { $_.Name -like "poppler-*" } | Select-Object -First 1
if ($extractedFolder) { Move-Item $extractedFolder.FullName $popplerDir -Force }
```

**Verify installation:**
```powershell
& "$toolsDir\poppler\Library\bin\pdftoppm.exe" -v
```

**Create output folder (tracked in git):**
```powershell
$jpgDir = "$toolsDir\_pdf_to_jpg_converted"
if (-not (Test-Path $jpgDir)) { New-Item -ItemType Directory -Path $jpgDir }
if (-not (Test-Path "$jpgDir\.gitkeep")) { New-Item -ItemType File -Path "$jpgDir\.gitkeep" }
```

## 5. Install QPDF Locally

QPDF is a command-line tool for PDF transformations (merge, split, encrypt, decrypt, repair).

**Check if already installed:**
```powershell
Test-Path "$toolsDir\qpdf\bin\qpdf.exe"
```

**If not installed, download and extract:**
```powershell
$qpdfDir = "$toolsDir\qpdf"

# Download latest QPDF for Windows
$qpdfUrl = "https://github.com/qpdf/qpdf/releases/download/v12.3.0/qpdf-12.3.0-msvc64.zip"
$zipPath = "$installerDir\qpdf.zip"

Invoke-WebRequest -Uri $qpdfUrl -OutFile $zipPath
Expand-Archive -Path $zipPath -DestinationPath $toolsDir -Force

# Find extracted folder (qpdf-*) and rename to qpdf
$extractedFolder = Get-ChildItem $toolsDir -Directory | Where-Object { $_.Name -like "qpdf-*" } | Select-Object -First 1
if ($extractedFolder) { Move-Item $extractedFolder.FullName $qpdfDir -Force }
```

**Verify installation:**
```powershell
& "$toolsDir\qpdf\bin\qpdf.exe" --version
```

## 6. Install Ghostscript Locally

Ghostscript is used for PDF image compression and downsizing. It only provides NSIS installers (no ZIP), so we extract it using 7-Zip.

**Check if already installed:**
```powershell
Test-Path "$toolsDir\gs\bin\gswin64c.exe"
```

**If not installed, download and extract with 7-Zip:**
```powershell
$gsDir = "$toolsDir\gs"

# Download Ghostscript installer (64-bit)
$gsUrl = "https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs10060/gs10060w64.exe"
$exePath = "$installerDir\gs10060w64.exe"

Invoke-WebRequest -Uri $gsUrl -OutFile $exePath

# Extract using 7-Zip (requires full 7z.exe, not 7za.exe)
& "$toolsDir\7z\7z.exe" x -y -o"$gsDir" "$exePath"

# Cleanup NSIS installer artifacts
Remove-Item "$gsDir\`$PLUGINSDIR" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$gsDir\*.nsis" -Force -ErrorAction SilentlyContinue
```

**Verify installation:**
```powershell
& "$toolsDir\gs\bin\gswin64c.exe" --version
```

## 7. Install uv/uvx (Python Package Runner)

uvx runs Python packages without installing them globally. Required for MCP servers.

**Check if already installed:**
```powershell
uvx --version
```

**If not installed:**
```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

Installs to `%USERPROFILE%\.local\bin\` (uv.exe, uvx.exe).

**Verify PATH:**
After installation, restart terminal or run:
```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","User") + ";" + [System.Environment]::GetEnvironmentVariable("Path","Machine")
uvx --version
```

## 8. Install Python Dependencies

```powershell
pip install pdf2image Pillow
```

## 9. Final Verification

Test Poppler conversion:
```powershell
& "$toolsDir\poppler\Library\bin\pdftoppm.exe" -jpeg -r 150 "input.pdf" "$toolsDir\_pdf_to_jpg_converted\output"
```

## 10. Cleanup (Optional)

Remove installers after successful installation:
```powershell
Remove-Item "$installerDir\*" -Force -ErrorAction SilentlyContinue
```

## Completion

All tools ready:
- **7-Zip**: Archive extraction (`[WORKSPACE_FOLDER]/.tools/7z/`)
- **Python**: Script execution
- **Poppler**: PDF to image conversion (`[WORKSPACE_FOLDER]/.tools/poppler/`)
- **QPDF**: PDF transformations (`[WORKSPACE_FOLDER]/.tools/qpdf/`)
- **Ghostscript**: PDF image compression (`[WORKSPACE_FOLDER]/.tools/gs/`)
- **uv/uvx**: Python package runner for MCP servers
- **Installers**: Downloaded to `[WORKSPACE_FOLDER]/.tools/_installer/`
- **Output folder**: `[WORKSPACE_FOLDER]/.tools/_pdf_to_jpg_converted/`
