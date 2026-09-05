---
name: image-tools
description: Apply when converting, resizing, compressing, or batch-processing image files (PNG, JPG, WebP, TIFF, SVG rasterization)
compatibility: Requires ImageMagick 7+ (magick CLI) at [WORKSPACE_FOLDER]/../.tools/magick/. Python Pillow available in llm-venv as fallback.
---

# Image Tools Guide

Rules and usage for image processing tools in `[WORKSPACE_FOLDER]/../.tools/`.

**References** (loaded on demand):
- [IMGTOOLS_REFERENCE.md](IMGTOOLS_REFERENCE.md) - Full procedure catalog (conversion, resize, crop, batch, Pillow fallback)
- [SETUP.md](SETUP.md) - ImageMagick installation and verification

## MUST-NOT-FORGET

1. Use `magick` not `convert` - Windows `convert.exe` is a disk utility, not ImageMagick
2. Always quote paths containing `@` (retina filenames like `file@2x.png`)
3. For batch operations: test on single file first, verify output, then scale
4. Default output: same directory as source unless `--output` specified
5. PNG to JPG creates white background (PNG transparency becomes white)
6. Never overwrite originals without explicit user request - use new filename or output folder

## Intent Lookup

- **Convert format** (PNG to JPG, WebP, etc.) → IMGTOOLS_REFERENCE.md > Format Conversion
- **Resize/scale images** → IMGTOOLS_REFERENCE.md > Resize Operations
- **Compress/optimize for web** → IMGTOOLS_REFERENCE.md > Compression
- **Batch process folder** → IMGTOOLS_REFERENCE.md > Batch Operations
- **Get image info** (dimensions, format, size) → IMGTOOLS_REFERENCE.md > Image Analysis
- **Create thumbnails** → IMGTOOLS_REFERENCE.md > Resize Operations (with `-thumbnail`)
- **Strip metadata** → IMGTOOLS_REFERENCE.md > Metadata Operations
- **Crop images** → IMGTOOLS_REFERENCE.md > Crop Operations
- **No ImageMagick available** → IMGTOOLS_REFERENCE.md > Pillow Fallback

## Tool Location

ImageMagick: `../.tools/magick/magick.exe`
Python Pillow: `../.tools/llm-venv/Scripts/python.exe` (pre-installed)

Set `$magick` before use:
```powershell
$magick = Join-Path (Split-Path $PWD.Path -Qualifier) "Dev\.tools\magick\magick.exe"
```

## Quick Reference

### Convert format
```powershell
& $magick input.png -background white -flatten -quality 80 output.jpg
& $magick input.jpg -quality 80 output.webp
```

### Resize (maintain aspect ratio)
```powershell
& $magick input.jpg -resize 800x output.jpg       # by width
& $magick input.jpg -resize x600 output.jpg       # by height
& $magick input.jpg -resize "1920x>" output.jpg   # max width, no upscale
```

### Compress
```powershell
& $magick input.jpg -quality 85 output.jpg        # high
& $magick input.jpg -quality 70 output.jpg        # web
& $magick input.jpg -quality 50 output.jpg        # aggressive
```

### Crop
```powershell
& $magick input.jpg -crop 400x300+100+50 output.jpg   # region WxH+X+Y
& $magick input.png -trim +repage output.png           # auto-trim whitespace
```

### Analyze
```powershell
& $magick identify input.jpg                       # format, dimensions, size
& $magick identify -format "%wx%h" input.jpg       # just WxH
```

### Strip metadata
```powershell
& $magick input.jpg -strip output.jpg
```

### Batch (PNG to JPG, full folder)
```powershell
Get-ChildItem "*.png" | ForEach-Object {
    $out = $_.FullName -replace '\.png$', '.jpg'
    & $magick $_.FullName -background white -flatten -quality 80 $out
    Write-Host "$($_.Name) done"
}
```

### Pillow fallback (no ImageMagick)
```powershell
& "../.tools/llm-venv/Scripts/python.exe" -c "
from PIL import Image; import sys
img = Image.open(sys.argv[1])
if img.mode in ('RGBA', 'P'): img = img.convert('RGB')
img.save(sys.argv[2], 'JPEG', quality=80)
" input.png output.jpg
```

## Gotchas

- **Windows `convert.exe` conflict** - Always use full path or `$magick` variable. Never call `convert` directly.
- **`@` in filenames** - ImageMagick treats `@` as list-file indicator. Quote paths: `"file@2x.png"`
- **Transparency to JPG** - No alpha channel. Always use `-background white -flatten` or get black backgrounds.
- **DPI vs pixels** - `-density` sets DPI metadata, `-resize` changes actual pixels. For web, pixels matter.
- **Color profile** - Use `-colorspace sRGB` when converting for web display.
- **Memory on large batches** - Process sequentially, not via `mogrify` on 1000+ files.

## Quality Guidelines

- **Web hero image** - JPG, quality 80, max 1920px
- **Web thumbnail** - JPG, quality 75, max 400px
- **Photo archive** - JPG, quality 90, original size
- **Logo/icon** - PNG, original size
- **Web modern** - WebP, quality 80, max 1920px
- **Print** - TIFF, quality 100, 300 DPI

## Setup

For initial installation, see [SETUP.md](SETUP.md).

Tool locations:
- ImageMagick: `../.tools/magick/`
- Python Pillow: `../.tools/llm-venv/` (pre-installed)
