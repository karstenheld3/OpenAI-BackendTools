# ImageMagick and Pillow Reference

Detailed procedures for image processing. Invoked from SKILL.md Intent Lookup.

All commands use `$magick` variable. Set before use:
```powershell
$magick = Join-Path (Split-Path $PWD.Path -Qualifier) "Dev\.tools\magick\magick.exe"
```

## Format Conversion

### Single file
```powershell
& $magick input.png output.jpg
& $magick input.png -quality 80 output.jpg
& $magick input.jpg output.webp
```

### PNG to JPG (white background for transparency)
```powershell
& $magick input.png -background white -flatten -quality 80 output.jpg
```

### Batch convert all PNG to JPG in folder
```powershell
Get-ChildItem "*.png" | ForEach-Object {
    $out = $_.FullName -replace '\.png$', '.jpg'
    & $magick $_.FullName -background white -flatten -quality 80 $out
}
```

### Batch convert preserving `@2x` naming
```powershell
Get-ChildItem "*.png" | ForEach-Object {
    $out = $_.FullName -replace '\.png$', '.jpg'
    & $magick "`"$($_.FullName)`"" -background white -flatten -quality 80 "`"$out`""
}
```

## Resize Operations

### Resize to specific width (maintain aspect ratio)
```powershell
& $magick input.jpg -resize 800x output.jpg
```

### Resize to specific height
```powershell
& $magick input.jpg -resize x600 output.jpg
```

### Resize to exact dimensions (may distort)
```powershell
& $magick input.jpg -resize 800x600! output.jpg
```

### Resize to fit within bounds (no upscale)
```powershell
& $magick input.jpg -resize "800x600>" output.jpg
```

### Create thumbnail (strips metadata, optimized)
```powershell
& $magick input.jpg -thumbnail 200x200 thumb.jpg
```

### Batch resize all images to max width
```powershell
Get-ChildItem "*.jpg" | ForEach-Object {
    & $magick $_.FullName -resize "1920x>" $_.FullName
}
```

## Compression

### JPG quality levels
```powershell
& $magick input.jpg -quality 85 output.jpg   # high quality
& $magick input.jpg -quality 70 output.jpg   # web optimized
& $magick input.jpg -quality 50 output.jpg   # aggressive
```

### PNG optimization (lossless)
```powershell
& $magick input.png -strip -define png:compression-level=9 output.png
```

### WebP conversion (lossy)
```powershell
& $magick input.jpg -quality 80 output.webp
```

### WebP lossless
```powershell
& $magick input.png -define webp:lossless=true output.webp
```

## Crop Operations

### Crop to specific region (WxH+X+Y)
```powershell
& $magick input.jpg -crop 400x300+100+50 output.jpg
```

### Auto-crop whitespace borders
```powershell
& $magick input.png -trim +repage output.png
```

### Center crop to aspect ratio
```powershell
& $magick input.jpg -gravity center -crop 16:9 +repage output.jpg
```

## Image Analysis

### Get dimensions and format
```powershell
& $magick identify input.jpg
```

### Verbose info (DPI, color space, compression)
```powershell
& $magick identify -verbose input.jpg
```

### Get just dimensions
```powershell
& $magick identify -format "%wx%h" input.jpg
```

### Batch get dimensions
```powershell
Get-ChildItem *.jpg, *.png | ForEach-Object {
    $dims = & $magick identify -format "%wx%h" $_.FullName
    "$($_.Name): $dims"
}
```

## Metadata Operations

### Strip all metadata (EXIF, IPTC, XMP)
```powershell
& $magick input.jpg -strip output.jpg
```

### Strip metadata from all images in folder
```powershell
Get-ChildItem *.jpg | ForEach-Object {
    & $magick $_.FullName -strip $_.FullName
}
```

## Batch Operations

### Convert folder with progress
```powershell
$files = Get-ChildItem "*.png"
$total = $files.Count
$i = 0
$files | ForEach-Object {
    $i++
    $out = $_.FullName -replace '\.png$', '.jpg'
    & $magick $_.FullName -background white -flatten -quality 80 $out
    Write-Host "[$i / $total] $($_.Name)"
}
```

### Batch resize + convert + compress (pipeline)
```powershell
$outputDir = ".\optimized"
New-Item -ItemType Directory -Force -Path $outputDir | Out-Null
Get-ChildItem *.png, *.jpg | ForEach-Object {
    $out = Join-Path $outputDir ($_.BaseName + ".jpg")
    & $magick $_.FullName -resize "1920x>" -background white -flatten -quality 80 -strip $out
}
```

### Delete originals after verified conversion
```powershell
Get-ChildItem "*.png" | ForEach-Object {
    $jpg = $_.FullName -replace '\.png$', '.jpg'
    if (Test-Path $jpg) { Remove-Item $_.FullName }
}
```

## Pillow Fallback (Python)

When ImageMagick is unavailable, use Pillow from llm-venv.

Python path: `[WORKSPACE_FOLDER]/../.tools/llm-venv/Scripts/python.exe`

### Convert PNG to JPG
```powershell
& "../.tools/llm-venv/Scripts/python.exe" -c "
from PIL import Image
import sys
img = Image.open(sys.argv[1])
if img.mode in ('RGBA', 'P'):
    img = img.convert('RGB')
img.save(sys.argv[2], 'JPEG', quality=80)
" input.png output.jpg
```

### Batch convert with Pillow
```powershell
& "../.tools/llm-venv/Scripts/python.exe" -c "
from PIL import Image
from pathlib import Path
import sys
folder = Path(sys.argv[1])
quality = int(sys.argv[2]) if len(sys.argv) > 2 else 80
for f in folder.glob('*.png'):
    img = Image.open(f)
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')
    out = f.with_suffix('.jpg')
    img.save(out, 'JPEG', quality=quality)
    print(f'{f.name} -> {out.name}')
" "path\to\folder" 80
```

### Resize with Pillow
```powershell
& "../.tools/llm-venv/Scripts/python.exe" -c "
from PIL import Image
import sys
img = Image.open(sys.argv[1])
w = int(sys.argv[3]) if len(sys.argv) > 3 else None
h = int(sys.argv[4]) if len(sys.argv) > 4 else None
if w and not h:
    h = int(img.height * w / img.width)
elif h and not w:
    w = int(img.width * h / img.height)
img = img.resize((w, h), Image.LANCZOS)
img.save(sys.argv[2])
" input.jpg output.jpg 800
```
