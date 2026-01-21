#!/usr/bin/env python3
"""
Downsize PDF images using Ghostscript.
Reduces file size by resampling images to specified DPI.

Output: .tools/_pdf_output/[PDF_FILENAME]_[DPI]dpi.pdf

Usage:
  python downsize-pdf-images.py <input.pdf> [--output <dir>] [--dpi <dpi>] [--preset <preset>]

Examples:
  python downsize-pdf-images.py report.pdf
  python downsize-pdf-images.py report.pdf --dpi 150
  python downsize-pdf-images.py report.pdf --preset screen
  python downsize-pdf-images.py report.pdf --output ./output --dpi 72
"""

import argparse, os, sys, subprocess
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR)))
GS_PATH = os.path.join(WORKSPACE_ROOT, ".tools", "gs", "bin", "gswin64c.exe")
DEFAULT_OUTPUT_DIR = os.path.join(WORKSPACE_ROOT, ".tools", "_pdf_output")
DEFAULT_DPI = 150

PRESETS = {
    "screen": {"dpi": 72, "desc": "72 DPI, smallest file size"},
    "ebook": {"dpi": 150, "desc": "150 DPI, medium quality"},
    "printer": {"dpi": 300, "desc": "300 DPI, high quality"},
    "prepress": {"dpi": 300, "desc": "300 DPI, color preserving"},
}

def get_file_size_mb(path: str) -> float:
    """Get file size in MB."""
    return os.path.getsize(path) / (1024 * 1024)

def downsize_pdf(input_pdf: str, output_dir: str, dpi: int, preset: str = None) -> str:
    """Downsize PDF images using Ghostscript. Returns output file path."""
    
    if not os.path.exists(GS_PATH):
        print(f"ERROR: Ghostscript not found at {GS_PATH}")
        print("Run SETUP.md to install Ghostscript.")
        sys.exit(1)
    
    input_path = Path(input_pdf)
    if not input_path.exists():
        print(f"ERROR: File not found: {input_pdf}")
        sys.exit(1)
    
    # Determine DPI from preset or argument
    if preset and preset in PRESETS:
        dpi = PRESETS[preset]["dpi"]
        pdf_settings = f"/{preset}"
    else:
        # Map DPI to closest preset for -dPDFSETTINGS
        if dpi <= 72:
            pdf_settings = "/screen"
        elif dpi <= 150:
            pdf_settings = "/ebook"
        elif dpi <= 300:
            pdf_settings = "/printer"
        else:
            pdf_settings = "/prepress"
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Generate output filename
    base_name = input_path.stem
    output_file = output_path / f"{base_name}_{dpi}dpi.pdf"
    
    original_size = get_file_size_mb(str(input_path))
    print(f"Downsizing '{input_path.name}' to {dpi} DPI...")
    print(f"  Original size: {original_size:.2f} MB")
    
    # Build Ghostscript command
    gs_args = [
        GS_PATH,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS={pdf_settings}",
        "-dDownsampleColorImages=true",
        f"-dColorImageResolution={dpi}",
        "-dDownsampleGrayImages=true",
        f"-dGrayImageResolution={dpi}",
        "-dDownsampleMonoImages=true",
        f"-dMonoImageResolution={dpi}",
        "-dNOPAUSE",
        "-dBATCH",
        f"-sOutputFile={output_file}",
        str(input_path)
    ]
    
    try:
        result = subprocess.run(gs_args, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"ERROR: Ghostscript failed")
            print(result.stderr)
            sys.exit(1)
        
        new_size = get_file_size_mb(str(output_file))
        reduction = ((original_size - new_size) / original_size) * 100
        
        print(f"  New size: {new_size:.2f} MB")
        print(f"  Reduction: {reduction:.1f}%")
        print(f"Done. Output: {output_file}")
        
        return str(output_file)
        
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='Downsize PDF images using Ghostscript',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Presets:
  screen    - 72 DPI, smallest file size
  ebook     - 150 DPI, medium quality (default)
  printer   - 300 DPI, high quality
  prepress  - 300 DPI, color preserving
"""
    )
    parser.add_argument('input_pdf', help='Input PDF file path')
    parser.add_argument('--output', default=DEFAULT_OUTPUT_DIR,
                        help=f'Output directory (default: {DEFAULT_OUTPUT_DIR})')
    parser.add_argument('--dpi', type=int, default=DEFAULT_DPI,
                        help=f'Resolution in DPI (default: {DEFAULT_DPI})')
    parser.add_argument('--preset', choices=list(PRESETS.keys()),
                        help='Quality preset (overrides --dpi)')
    
    args = parser.parse_args()
    downsize_pdf(args.input_pdf, args.output, args.dpi, args.preset)

if __name__ == '__main__':
    main()
