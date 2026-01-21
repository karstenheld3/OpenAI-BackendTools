#!/usr/bin/env python3
"""
Compress PDF files using Ghostscript with intelligent strategy selection.

Analyzes PDF structure and applies appropriate compression based on content.
Verifies results and escalates to more aggressive compression if needed.

Usage:
  python compress-pdf.py <input.pdf> [--compression high|medium|low] [--output output.pdf]

Examples:
  python compress-pdf.py report.pdf
  python compress-pdf.py report.pdf --compression high
  python compress-pdf.py report.pdf --compression medium --output smaller.pdf
"""

import argparse
import os
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR)))
TOOLS_DIR = os.path.join(WORKSPACE_ROOT, ".tools")
GS_PATH = os.path.join(TOOLS_DIR, "gs", "bin", "gswin64c.exe")
PDFINFO_PATH = os.path.join(TOOLS_DIR, "poppler", "Library", "bin", "pdfinfo.exe")
PDFIMAGES_PATH = os.path.join(TOOLS_DIR, "poppler", "Library", "bin", "pdfimages.exe")
QPDF_PATH = os.path.join(TOOLS_DIR, "qpdf", "bin", "qpdf.exe")
DEFAULT_OUTPUT_DIR = os.path.join(TOOLS_DIR, "_pdf_output")

# Target reduction percentages by compression level
TARGETS = {
    "high": 50,    # Target 50%+ reduction
    "medium": 25,  # Target 25%+ reduction
    "low": 10,     # Target 10%+ reduction
}

# Minimum improvement to justify more aggressive approach
MIN_IMPROVEMENT_THRESHOLD = 5  # 5% additional reduction required


def get_file_size_mb(path: str) -> float:
    """Get file size in MB."""
    return os.path.getsize(path) / (1024 * 1024)


def analyze_pdf(input_path: str) -> dict:
    """Analyze PDF to determine optimal compression strategy."""
    analysis = {
        "pages": 0,
        "file_size_mb": get_file_size_mb(input_path),
        "optimized": False,
        "image_count": 0,
        "has_jpeg2000": False,
        "has_high_dpi": False,
        "avg_dpi": 0,
        "has_cmyk": False,
        "many_small_images": False,
    }
    
    # Get PDF info
    try:
        result = subprocess.run(
            [PDFINFO_PATH, input_path],
            capture_output=True, text=True, timeout=30
        )
        for line in result.stdout.splitlines():
            if line.startswith("Pages:"):
                analysis["pages"] = int(line.split(":")[1].strip())
            elif line.startswith("Optimized:"):
                analysis["optimized"] = "yes" in line.lower()
    except Exception as e:
        print(f"  Warning: Could not get PDF info: {e}")
    
    # Analyze images
    try:
        result = subprocess.run(
            [PDFIMAGES_PATH, "-list", input_path],
            capture_output=True, text=True, timeout=60
        )
        lines = result.stdout.splitlines()
        image_lines = [l for l in lines if l.strip() and not l.startswith("page") and not l.startswith("-")]
        analysis["image_count"] = len(image_lines)
        
        dpi_values = []
        small_images = 0
        
        for line in image_lines:
            parts = line.split()
            if len(parts) >= 14:
                try:
                    width = int(parts[2])
                    height = int(parts[3])
                    color = parts[4]
                    enc = parts[8]
                    x_dpi = int(parts[12])
                    
                    if enc == "jpx":
                        analysis["has_jpeg2000"] = True
                    if x_dpi > 150:
                        analysis["has_high_dpi"] = True
                    if color == "cmyk":
                        analysis["has_cmyk"] = True
                    if width < 100 and height < 100:
                        small_images += 1
                    
                    dpi_values.append(x_dpi)
                except (ValueError, IndexError):
                    pass
        
        if dpi_values:
            analysis["avg_dpi"] = sum(dpi_values) // len(dpi_values)
        
        # Many small images if >50% are small
        if analysis["image_count"] > 0:
            analysis["many_small_images"] = (small_images / analysis["image_count"]) > 0.5
            
    except Exception as e:
        print(f"  Warning: Could not analyze images: {e}")
    
    return analysis


def predict_compression_potential(analysis: dict) -> str:
    """Predict compression potential based on analysis."""
    if analysis["has_jpeg2000"]:
        return "excellent"  # JPEG2000 converts very well
    if analysis["has_high_dpi"] and not analysis["many_small_images"]:
        return "good"
    if analysis["optimized"]:
        return "limited"
    if analysis["many_small_images"]:
        return "limited"
    return "moderate"


def run_ghostscript(input_path: str, output_path: str, preset: str, extra_flags: list = None) -> bool:
    """Run Ghostscript with specified preset."""
    args = [
        GS_PATH,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS=/{preset}",
        "-dDetectDuplicateImages=true",
        "-dCompressFonts=true",
        "-dSubsetFonts=true",
        "-dConvertCMYKImagesToRGB=true",
        "-dColorImageDownsampleType=/Bicubic",
        "-dGrayImageDownsampleType=/Bicubic",
        "-dNOPAUSE",
        "-dBATCH",
    ]
    
    if extra_flags:
        args.extend(extra_flags)
    
    args.extend([f"-sOutputFile={output_path}", input_path])
    
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=600)
        return result.returncode == 0
    except Exception as e:
        print(f"  Error running Ghostscript: {e}")
        return False


def run_qpdf_optimize(input_path: str, output_path: str) -> bool:
    """Run QPDF structure optimization."""
    args = [
        QPDF_PATH,
        "--linearize",
        "--object-streams=generate",
        "--compress-streams=y",
        "--recompress-flate",
        input_path,
        output_path,
    ]
    
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=300)
        return result.returncode == 0
    except Exception as e:
        print(f"  Error running QPDF: {e}")
        return False


def compress_pdf(input_path: str, output_path: str, compression: str) -> dict:
    """
    Compress PDF with intelligent strategy selection.
    
    Returns dict with results including final path and statistics.
    """
    results = {
        "success": False,
        "original_size_mb": 0,
        "final_size_mb": 0,
        "reduction_percent": 0,
        "strategy_used": "",
        "attempts": [],
    }
    
    # Verify tools exist
    for tool, path in [("Ghostscript", GS_PATH), ("pdfinfo", PDFINFO_PATH), ("pdfimages", PDFIMAGES_PATH)]:
        if not os.path.exists(path):
            print(f"ERROR: {tool} not found at {path}")
            print("Run SETUP.md to install tools.")
            return results
    
    input_path = os.path.abspath(input_path)
    output_path = os.path.abspath(output_path)
    
    if not os.path.exists(input_path):
        print(f"ERROR: File not found: {input_path}")
        return results
    
    original_size = get_file_size_mb(input_path)
    results["original_size_mb"] = original_size
    target_reduction = TARGETS[compression]
    
    print(f"Analyzing PDF...")
    analysis = analyze_pdf(input_path)
    potential = predict_compression_potential(analysis)
    
    print(f"  Pages: {analysis['pages']}")
    print(f"  Size: {original_size:.2f} MB")
    print(f"  Images: {analysis['image_count']}")
    print(f"  Optimized: {'Yes' if analysis['optimized'] else 'No'}")
    print(f"  JPEG2000: {'Yes' if analysis['has_jpeg2000'] else 'No'}")
    print(f"  High DPI (>150): {'Yes' if analysis['has_high_dpi'] else 'No'}")
    print(f"  Avg DPI: {analysis['avg_dpi']}")
    print(f"  Compression potential: {potential}")
    print()
    
    # Create temp directory for intermediate files
    temp_dir = tempfile.mkdtemp(prefix="pdf_compress_")
    
    try:
        # Determine initial strategy based on compression level and analysis
        if compression == "high":
            strategies = [
                ("screen", "Aggressive (72 DPI)"),
                ("screen_extra", "Aggressive + extra flags"),
            ]
        elif compression == "medium":
            strategies = [
                ("ebook", "Balanced (150 DPI)"),
                ("screen", "Aggressive (72 DPI)"),
            ]
        else:  # low
            strategies = [
                ("printer", "Quality (300 DPI)"),
                ("ebook", "Balanced (150 DPI)"),
            ]
        
        # Add QPDF-only for already optimized PDFs with limited potential
        if potential == "limited" and compression == "low":
            strategies.insert(0, ("qpdf_only", "Structure only (QPDF)"))
        
        best_result = None
        best_reduction = 0
        best_path = None
        
        for i, (strategy, description) in enumerate(strategies):
            temp_output = os.path.join(temp_dir, f"attempt_{i}.pdf")
            print(f"Attempt {i+1}: {description}...")
            
            success = False
            if strategy == "qpdf_only":
                success = run_qpdf_optimize(input_path, temp_output)
            elif strategy == "screen_extra":
                # More aggressive: lower quality, force downsampling
                extra = [
                    "-dColorImageResolution=72",
                    "-dGrayImageResolution=72",
                    "-dMonoImageResolution=72",
                    "-dDownsampleColorImages=true",
                    "-dDownsampleGrayImages=true",
                    "-dDownsampleMonoImages=true",
                ]
                success = run_ghostscript(input_path, temp_output, "screen", extra)
            else:
                success = run_ghostscript(input_path, temp_output, strategy)
            
            if success and os.path.exists(temp_output):
                new_size = get_file_size_mb(temp_output)
                reduction = ((original_size - new_size) / original_size) * 100
                
                results["attempts"].append({
                    "strategy": description,
                    "size_mb": new_size,
                    "reduction_percent": reduction,
                })
                
                print(f"  Result: {new_size:.2f} MB ({reduction:.1f}% reduction)")
                
                # Check if this is the best result so far
                if reduction > best_reduction:
                    best_reduction = reduction
                    best_result = description
                    if best_path and os.path.exists(best_path):
                        os.remove(best_path)
                    best_path = temp_output
                else:
                    os.remove(temp_output)
                
                # Check if we've reached target
                if reduction >= target_reduction:
                    print(f"  Target reached ({target_reduction}%+)")
                    break
                
                # Check if more aggressive approach is worth it
                if i > 0 and (reduction - best_reduction) < MIN_IMPROVEMENT_THRESHOLD:
                    print(f"  Insufficient improvement, reverting to previous best")
                    break
            else:
                print(f"  Failed")
                results["attempts"].append({
                    "strategy": description,
                    "size_mb": 0,
                    "reduction_percent": 0,
                    "error": True,
                })
        
        # Use best result
        if best_path and os.path.exists(best_path):
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            shutil.copy2(best_path, output_path)
            
            results["success"] = True
            results["final_size_mb"] = get_file_size_mb(output_path)
            results["reduction_percent"] = best_reduction
            results["strategy_used"] = best_result
            
            print()
            print(f"Done: {output_path}")
            print(f"  Original: {original_size:.2f} MB")
            print(f"  Final: {results['final_size_mb']:.2f} MB")
            print(f"  Reduction: {best_reduction:.1f}%")
            print(f"  Strategy: {best_result}")
        else:
            print("ERROR: All compression attempts failed")
            
    finally:
        # Cleanup temp directory
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Compress PDF with intelligent strategy selection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Compression levels:
  high   - Target 50%+ reduction, aggressive downsampling (72 DPI)
  medium - Target 25%+ reduction, balanced quality (150 DPI)
  low    - Target 10%+ reduction, preserve quality (300 DPI)

The script analyzes the PDF first, then applies appropriate compression.
If target reduction is not reached, it tries more aggressive approaches.
"""
    )
    parser.add_argument("input_pdf", help="Input PDF file path")
    parser.add_argument("--compression", choices=["high", "medium", "low"],
                        default="medium", help="Compression level (default: medium)")
    parser.add_argument("--output", help="Output PDF path (default: _pdf_output/<name>_compressed.pdf)")
    
    args = parser.parse_args()
    
    # Determine output path
    if args.output:
        output_path = args.output
    else:
        input_name = Path(args.input_pdf).stem
        os.makedirs(DEFAULT_OUTPUT_DIR, exist_ok=True)
        output_path = os.path.join(DEFAULT_OUTPUT_DIR, f"{input_name}_compressed.pdf")
    
    result = compress_pdf(args.input_pdf, output_path, args.compression)
    
    if not result["success"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
