#!/usr/bin/env python3
"""
transcribe-image-to-markdown.py - Convert images to structured markdown using vision LLMs.

Usage:
  python transcribe-image-to-markdown.py --input image.png --output result.md
  python transcribe-image-to-markdown.py --input document.jpg --model gpt-4o --output doc.md
  python transcribe-image-to-markdown.py --input-dir ./screenshots --output-dir ./transcripts
"""

import os
import sys
import json
import base64
import argparse
from pathlib import Path
from datetime import datetime, timezone

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
DEFAULT_MODEL = 'gpt-4o'

TRANSCRIPTION_PROMPT = """You are a document transcription expert. Convert the provided image to well-structured markdown.

INSTRUCTIONS:
1. Preserve ALL text content exactly as shown
2. Maintain document structure (headings, lists, tables, code blocks)
3. Use appropriate markdown formatting:
   - # ## ### for headings based on visual hierarchy
   - - or * for bullet lists
   - 1. 2. 3. for numbered lists
   - | for tables
   - ``` for code blocks
   - **bold** and *italic* where visually indicated
4. For diagrams/charts, describe them in a fenced block: ```diagram ... ```
5. For images within the document, note them as: ![description](image)
6. Preserve whitespace and indentation that conveys meaning
7. If text is unclear, use [unclear] placeholder

OUTPUT FORMAT:
- Return ONLY the markdown content
- No explanations, preamble, or metadata
- Start directly with the document content"""


def get_script_dir() -> Path:
    """Get directory containing this script."""
    return Path(__file__).parent


def load_api_keys() -> dict:
    """Load API keys from ~/.llm-keys or environment."""
    keys = {}
    
    # Try environment first
    if os.environ.get('OPENAI_API_KEY'):
        keys['OPENAI_API_KEY'] = os.environ['OPENAI_API_KEY']
    if os.environ.get('ANTHROPIC_API_KEY'):
        keys['ANTHROPIC_API_KEY'] = os.environ['ANTHROPIC_API_KEY']
    
    # Try ~/.llm-keys file
    keys_file = Path.home() / '.llm-keys'
    if keys_file.exists():
        with open(keys_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    keys[key.strip()] = value.strip()
    
    return keys


def detect_provider(model_id: str) -> str:
    """Detect provider from model ID."""
    model_lower = model_id.lower()
    if model_lower.startswith(('gpt-', 'o1-', 'o3-', 'o4-')):
        return 'openai'
    if model_lower.startswith('claude'):
        return 'anthropic'
    # Default to OpenAI for unknown models
    return 'openai'


def encode_image_base64(image_path: Path) -> tuple[str, str]:
    """Encode image to base64 and return with media type."""
    suffix = image_path.suffix.lower()
    media_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp'
    }
    media_type = media_types.get(suffix, 'image/png')
    
    with open(image_path, 'rb') as f:
        data = base64.b64encode(f.read()).decode('utf-8')
    
    return data, media_type


def call_openai(model: str, image_data: str, media_type: str, 
                prompt: str, api_key: str, max_tokens: int = 4096) -> dict:
    """Call OpenAI vision API."""
    import httpx
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'model': model,
        'max_tokens': max_tokens,
        'messages': [
            {
                'role': 'user',
                'content': [
                    {'type': 'text', 'text': prompt},
                    {
                        'type': 'image_url',
                        'image_url': {
                            'url': f'data:{media_type};base64,{image_data}'
                        }
                    }
                ]
            }
        ]
    }
    
    with httpx.Client(timeout=120.0) as client:
        response = client.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        result = response.json()
    
    return {
        'content': result['choices'][0]['message']['content'],
        'input_tokens': result['usage']['prompt_tokens'],
        'output_tokens': result['usage']['completion_tokens'],
        'model': result.get('model', model)
    }


def call_anthropic(model: str, image_data: str, media_type: str,
                   prompt: str, api_key: str, max_tokens: int = 4096) -> dict:
    """Call Anthropic vision API."""
    import httpx
    
    headers = {
        'x-api-key': api_key,
        'anthropic-version': '2023-06-01',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'model': model,
        'max_tokens': max_tokens,
        'messages': [
            {
                'role': 'user',
                'content': [
                    {
                        'type': 'image',
                        'source': {
                            'type': 'base64',
                            'media_type': media_type,
                            'data': image_data
                        }
                    },
                    {'type': 'text', 'text': prompt}
                ]
            }
        ]
    }
    
    with httpx.Client(timeout=120.0) as client:
        response = client.post(
            'https://api.anthropic.com/v1/messages',
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        result = response.json()
    
    content = ''
    for block in result.get('content', []):
        if block.get('type') == 'text':
            content += block.get('text', '')
    
    return {
        'content': content,
        'input_tokens': result['usage']['input_tokens'],
        'output_tokens': result['usage']['output_tokens'],
        'model': result.get('model', model)
    }


def transcribe_image(image_path: Path, model: str, api_keys: dict,
                     prompt: str = None, max_tokens: int = 4096) -> dict:
    """Transcribe a single image to markdown."""
    if prompt is None:
        prompt = TRANSCRIPTION_PROMPT
    
    # Validate image
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    suffix = image_path.suffix.lower()
    if suffix not in IMAGE_EXTENSIONS:
        raise ValueError(f"Unsupported image format: {suffix}. Supported: {IMAGE_EXTENSIONS}")
    
    # Encode image
    image_data, media_type = encode_image_base64(image_path)
    
    # Detect provider and call API
    provider = detect_provider(model)
    
    if provider == 'openai':
        api_key = api_keys.get('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in keys")
        return call_openai(model, image_data, media_type, prompt, api_key, max_tokens)
    
    elif provider == 'anthropic':
        api_key = api_keys.get('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in keys")
        return call_anthropic(model, image_data, media_type, prompt, api_key, max_tokens)
    
    else:
        raise ValueError(f"Unknown provider: {provider}")


def process_single(input_path: Path, output_path: Path, model: str,
                   api_keys: dict, prompt: str = None, verbose: bool = False) -> dict:
    """Process a single image file."""
    start_time = datetime.now(timezone.utc)
    
    if verbose:
        print(f"Processing: {input_path}")
    
    result = transcribe_image(input_path, model, api_keys, prompt)
    
    # Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result['content'])
    
    elapsed = (datetime.now(timezone.utc) - start_time).total_seconds()
    
    if verbose:
        print(f"  -> {output_path} ({result['input_tokens']} + {result['output_tokens']} tokens, {elapsed:.1f}s)")
    
    return {
        'input': str(input_path),
        'output': str(output_path),
        'model': result['model'],
        'input_tokens': result['input_tokens'],
        'output_tokens': result['output_tokens'],
        'elapsed_seconds': elapsed
    }


def process_batch(input_dir: Path, output_dir: Path, model: str,
                  api_keys: dict, prompt: str = None, verbose: bool = False) -> list:
    """Process all images in a directory."""
    results = []
    
    image_files = [f for f in input_dir.iterdir() 
                   if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS]
    
    if not image_files:
        print(f"No image files found in {input_dir}")
        return results
    
    print(f"Found {len(image_files)} images to process")
    
    for image_file in sorted(image_files):
        output_file = output_dir / (image_file.stem + '.md')
        try:
            result = process_single(image_file, output_file, model, api_keys, prompt, verbose)
            results.append(result)
        except Exception as e:
            print(f"[ERROR] Failed to process {image_file}: {e}", file=sys.stderr)
            results.append({
                'input': str(image_file),
                'error': str(e)
            })
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description='Convert images to structured markdown using vision LLMs.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python transcribe-image-to-markdown.py --input screenshot.png --output result.md
  python transcribe-image-to-markdown.py --input doc.jpg --model claude-sonnet-4-20250514 --output doc.md
  python transcribe-image-to-markdown.py --input-dir ./images --output-dir ./transcripts
        """
    )
    
    # Input/Output
    parser.add_argument('--input', '-i', type=Path, help='Input image file')
    parser.add_argument('--output', '-o', type=Path, help='Output markdown file')
    parser.add_argument('--input-dir', type=Path, help='Input directory for batch processing')
    parser.add_argument('--output-dir', type=Path, help='Output directory for batch processing')
    
    # Model
    parser.add_argument('--model', '-m', default=DEFAULT_MODEL,
                        help=f'Model to use (default: {DEFAULT_MODEL})')
    parser.add_argument('--max-tokens', type=int, default=4096,
                        help='Maximum output tokens (default: 4096)')
    
    # Custom prompt
    parser.add_argument('--prompt-file', type=Path,
                        help='Custom prompt file (overrides default)')
    
    # Output
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Verbose output')
    parser.add_argument('--json', action='store_true',
                        help='Output results as JSON')
    
    args = parser.parse_args()
    
    # Validate arguments
    single_mode = args.input is not None
    batch_mode = args.input_dir is not None
    
    if not single_mode and not batch_mode:
        parser.error("Either --input or --input-dir is required")
    
    if single_mode and batch_mode:
        parser.error("Cannot use both --input and --input-dir")
    
    if single_mode and not args.output:
        args.output = args.input.with_suffix('.md')
    
    if batch_mode and not args.output_dir:
        args.output_dir = args.input_dir / 'transcripts'
    
    # Load API keys
    api_keys = load_api_keys()
    if not api_keys:
        print("[ERROR] No API keys found. Set OPENAI_API_KEY or create ~/.llm-keys", file=sys.stderr)
        sys.exit(1)
    
    # Load custom prompt if provided
    prompt = None
    if args.prompt_file:
        if not args.prompt_file.exists():
            print(f"[ERROR] Prompt file not found: {args.prompt_file}", file=sys.stderr)
            sys.exit(1)
        prompt = args.prompt_file.read_text(encoding='utf-8')
    
    # Process
    try:
        if single_mode:
            result = process_single(args.input, args.output, args.model,
                                    api_keys, prompt, args.verbose)
            results = [result]
        else:
            results = process_batch(args.input_dir, args.output_dir, args.model,
                                    api_keys, prompt, args.verbose)
        
        # Output summary
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            total_input = sum(r.get('input_tokens', 0) for r in results)
            total_output = sum(r.get('output_tokens', 0) for r in results)
            errors = sum(1 for r in results if 'error' in r)
            
            print(f"\nSummary: {len(results)} files processed, {errors} errors")
            print(f"Tokens: {total_input} input + {total_output} output = {total_input + total_output} total")
    
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
