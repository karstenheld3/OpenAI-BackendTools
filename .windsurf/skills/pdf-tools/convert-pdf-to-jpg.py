#!/usr/bin/env python3
"""
Convert PDF pages to JPG images for Windsurf Agent vision analysis.
Uses Poppler's pdftoppm via pdf2image library.

Output: .tools/_pdf_to_jpg_converted/[PDF_FILENAME]/[PDF_FILENAME]_page001.jpg
Each PDF gets its own subfolder to track previous conversions.

Usage:
  python convert-pdf-to-jpg.py <input.pdf> [--output <dir>] [--dpi <dpi>] [--pages <range>]

Examples:
  python convert-pdf-to-jpg.py invoice.pdf
  python convert-pdf-to-jpg.py invoice.pdf --dpi 200 --pages 1-2
  python convert-pdf-to-jpg.py invoice.pdf --pages 1
"""

import argparse, os, sys
from pathlib import Path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR)))
POPPLER_PATH = os.path.join(WORKSPACE_ROOT, ".tools", "poppler", "Library", "bin")
DEFAULT_OUTPUT_DIR = os.path.join(WORKSPACE_ROOT, ".tools", "_pdf_to_jpg_converted")
DEFAULT_DPI = 150

def parse_page_range(page_str: str, total_pages: int) -> tuple[int, int]:
  """Parse page range string like '1', '1-3', or 'all'."""
  if not page_str or page_str.lower() == 'all':
    return 1, total_pages
  if '-' in page_str:
    start, end = page_str.split('-')
    return int(start), int(end)
  page = int(page_str)
  return page, page

def convert_pdf_to_jpg(input_pdf: str, output_dir: str, dpi: int, pages: str = None) -> list[str]:
  """Convert PDF pages to JPG images. Returns list of output file paths."""
  try:
    from pdf2image import convert_from_path
    from pdf2image.exceptions import PDFInfoNotInstalledError, PDFPageCountError
  except ImportError:
    print("ERROR: pdf2image not installed. Run: pip install pdf2image Pillow")
    sys.exit(1)

  input_path = Path(input_pdf)
  if not input_path.exists():
    print(f"ERROR: File not found: {input_pdf}")
    sys.exit(1)

  base_name = input_path.stem
  
  # Create subfolder per PDF filename
  output_path = Path(output_dir) / base_name
  output_path.mkdir(parents=True, exist_ok=True)

  try:
    # First get page count
    from pdf2image import pdfinfo_from_path
    info = pdfinfo_from_path(str(input_path), poppler_path=POPPLER_PATH)
    total_pages = info['Pages']
    
    first_page, last_page = parse_page_range(pages, total_pages)
    
    print(f"Converting '{input_path.name}' pages {first_page}-{last_page} at {dpi} DPI...")
    
    images = convert_from_path(
      str(input_path),
      dpi=dpi,
      first_page=first_page,
      last_page=last_page,
      poppler_path=POPPLER_PATH,
      fmt='jpeg'
    )
    
    output_files = []
    for i, image in enumerate(images, start=first_page):
      output_file = output_path / f"{base_name}_page{i:03d}.jpg"
      image.save(str(output_file), 'JPEG', quality=90)
      output_files.append(str(output_file))
      print(f"  OK: {output_file.name}")
    
    print(f"Done. {len(output_files)} file(s) created in '{output_dir}'")
    return output_files

  except PDFInfoNotInstalledError:
    print(f"ERROR: Poppler not found at {POPPLER_PATH}")
    print("Run /setup-everything workflow to install Poppler.")
    sys.exit(1)
  except PDFPageCountError:
    print(f"ERROR: Could not read PDF: {input_pdf}")
    sys.exit(1)
  except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)

def main():
  parser = argparse.ArgumentParser(description='Convert PDF pages to JPG images')
  parser.add_argument('input_pdf', help='Input PDF file path')
  parser.add_argument('--output', default=DEFAULT_OUTPUT_DIR, help=f'Output directory (default: {DEFAULT_OUTPUT_DIR})')
  parser.add_argument('--dpi', type=int, default=DEFAULT_DPI, help=f'Resolution in DPI (default: {DEFAULT_DPI})')
  parser.add_argument('--pages', help='Page range: "1", "1-3", or "all" (default: all)')
  
  args = parser.parse_args()
  convert_pdf_to_jpg(args.input_pdf, args.output, args.dpi, args.pages)

if __name__ == '__main__':
  main()
