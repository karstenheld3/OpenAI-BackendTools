#!/usr/bin/env python3
"""
transcribe-audio-to-markdown.py - Convert audio files to markdown transcripts using Whisper API.

Usage:
  python transcribe-audio-to-markdown.py --input recording.mp3 --output transcript.md
  python transcribe-audio-to-markdown.py --input meeting.wav --format --output meeting.md
  python transcribe-audio-to-markdown.py --input-dir ./audio --output-dir ./transcripts
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone

AUDIO_EXTENSIONS = {'.mp3', '.wav', '.m4a', '.ogg', '.flac', '.webm', '.mp4', '.mpeg', '.mpga'}
DEFAULT_MODEL = 'whisper-1'
DEFAULT_FORMAT_MODEL = 'gpt-4o-mini'

FORMATTING_PROMPT = """You are a transcript editor. Format the provided raw transcript into clean, readable markdown.

INSTRUCTIONS:
1. Add paragraph breaks at natural pauses and topic changes
2. Use headings (##) for major topic shifts or sections
3. Use bullet points for lists mentioned verbally
4. Clean up filler words (um, uh, like) unless they convey meaning
5. Fix obvious transcription errors when context makes intent clear
6. Add speaker labels if multiple speakers are evident: **Speaker 1:**, **Speaker 2:**
7. Preserve all meaningful content - do not summarize or omit information
8. Use **bold** for emphasized words/phrases
9. Use > blockquotes for direct quotes or citations mentioned

OUTPUT FORMAT:
- Return ONLY the formatted markdown
- No explanations or metadata
- Start directly with the transcript content"""


def load_api_keys() -> dict:
    """Load API keys from ~/.llm-keys or environment."""
    keys = {}
    
    if os.environ.get('OPENAI_API_KEY'):
        keys['OPENAI_API_KEY'] = os.environ['OPENAI_API_KEY']
    if os.environ.get('ANTHROPIC_API_KEY'):
        keys['ANTHROPIC_API_KEY'] = os.environ['ANTHROPIC_API_KEY']
    
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


def transcribe_audio(audio_path: Path, api_key: str, model: str = DEFAULT_MODEL,
                     language: str = None, response_format: str = 'text') -> dict:
    """Transcribe audio using OpenAI Whisper API."""
    import httpx
    
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    suffix = audio_path.suffix.lower()
    if suffix not in AUDIO_EXTENSIONS:
        raise ValueError(f"Unsupported audio format: {suffix}. Supported: {AUDIO_EXTENSIONS}")
    
    # Prepare multipart form data
    with open(audio_path, 'rb') as f:
        audio_data = f.read()
    
    files = {
        'file': (audio_path.name, audio_data, 'audio/mpeg'),
        'model': (None, model),
        'response_format': (None, response_format),
    }
    
    if language:
        files['language'] = (None, language)
    
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    
    with httpx.Client(timeout=300.0) as client:
        response = client.post(
            'https://api.openai.com/v1/audio/transcriptions',
            headers=headers,
            files=files
        )
        response.raise_for_status()
        
        if response_format == 'json' or response_format == 'verbose_json':
            result = response.json()
            text = result.get('text', '')
            duration = result.get('duration', 0)
        else:
            text = response.text
            duration = 0
    
    return {
        'text': text,
        'duration': duration,
        'model': model
    }


def format_transcript(text: str, api_key: str, model: str = DEFAULT_FORMAT_MODEL,
                      prompt: str = None) -> dict:
    """Format raw transcript using LLM."""
    import httpx
    
    if prompt is None:
        prompt = FORMATTING_PROMPT
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'model': model,
        'max_tokens': 8192,
        'messages': [
            {'role': 'system', 'content': prompt},
            {'role': 'user', 'content': f"Format this transcript:\n\n{text}"}
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


def process_single(input_path: Path, output_path: Path, api_keys: dict,
                   model: str = DEFAULT_MODEL, language: str = None,
                   do_format: bool = False, format_model: str = DEFAULT_FORMAT_MODEL,
                   format_prompt: str = None, verbose: bool = False) -> dict:
    """Process a single audio file."""
    start_time = datetime.now(timezone.utc)
    
    api_key = api_keys.get('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found")
    
    if verbose:
        print(f"Transcribing: {input_path}")
    
    # Transcribe
    response_format = 'verbose_json' if verbose else 'text'
    transcript = transcribe_audio(input_path, api_key, model, language, response_format)
    
    text = transcript['text']
    format_tokens = {'input': 0, 'output': 0}
    
    # Optional formatting
    if do_format and text.strip():
        if verbose:
            print(f"  Formatting with {format_model}...")
        format_result = format_transcript(text, api_key, format_model, format_prompt)
        text = format_result['content']
        format_tokens = {
            'input': format_result['input_tokens'],
            'output': format_result['output_tokens']
        }
    
    # Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)
    
    elapsed = (datetime.now(timezone.utc) - start_time).total_seconds()
    
    if verbose:
        duration_info = f", {transcript['duration']:.1f}s audio" if transcript['duration'] else ""
        print(f"  -> {output_path} ({elapsed:.1f}s{duration_info})")
    
    return {
        'input': str(input_path),
        'output': str(output_path),
        'whisper_model': transcript['model'],
        'format_model': format_model if do_format else None,
        'audio_duration': transcript['duration'],
        'format_input_tokens': format_tokens['input'],
        'format_output_tokens': format_tokens['output'],
        'elapsed_seconds': elapsed
    }


def process_batch(input_dir: Path, output_dir: Path, api_keys: dict,
                  model: str = DEFAULT_MODEL, language: str = None,
                  do_format: bool = False, format_model: str = DEFAULT_FORMAT_MODEL,
                  format_prompt: str = None, verbose: bool = False) -> list:
    """Process all audio files in a directory."""
    results = []
    
    audio_files = [f for f in input_dir.iterdir()
                   if f.is_file() and f.suffix.lower() in AUDIO_EXTENSIONS]
    
    if not audio_files:
        print(f"No audio files found in {input_dir}")
        return results
    
    print(f"Found {len(audio_files)} audio files to process")
    
    for audio_file in sorted(audio_files):
        output_file = output_dir / (audio_file.stem + '.md')
        try:
            result = process_single(
                audio_file, output_file, api_keys, model, language,
                do_format, format_model, format_prompt, verbose
            )
            results.append(result)
        except Exception as e:
            print(f"[ERROR] Failed to process {audio_file}: {e}", file=sys.stderr)
            results.append({
                'input': str(audio_file),
                'error': str(e)
            })
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description='Convert audio files to markdown transcripts using Whisper API.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python transcribe-audio-to-markdown.py --input recording.mp3 --output transcript.md
  python transcribe-audio-to-markdown.py --input meeting.wav --format --output meeting.md
  python transcribe-audio-to-markdown.py --input-dir ./audio --output-dir ./transcripts --format
        """
    )
    
    # Input/Output
    parser.add_argument('--input', '-i', type=Path, help='Input audio file')
    parser.add_argument('--output', '-o', type=Path, help='Output markdown file')
    parser.add_argument('--input-dir', type=Path, help='Input directory for batch processing')
    parser.add_argument('--output-dir', type=Path, help='Output directory for batch processing')
    
    # Whisper options
    parser.add_argument('--model', '-m', default=DEFAULT_MODEL,
                        help=f'Whisper model (default: {DEFAULT_MODEL})')
    parser.add_argument('--language', '-l',
                        help='Language code (e.g., en, de, fr). Auto-detect if not specified.')
    
    # Formatting options
    parser.add_argument('--format', '-f', action='store_true',
                        help='Format transcript with LLM for better readability')
    parser.add_argument('--format-model', default=DEFAULT_FORMAT_MODEL,
                        help=f'Model for formatting (default: {DEFAULT_FORMAT_MODEL})')
    parser.add_argument('--format-prompt-file', type=Path,
                        help='Custom formatting prompt file')
    
    # Output options
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
    if not api_keys.get('OPENAI_API_KEY'):
        print("[ERROR] OPENAI_API_KEY not found. Set it or create ~/.llm-keys", file=sys.stderr)
        sys.exit(1)
    
    # Load custom format prompt if provided
    format_prompt = None
    if args.format_prompt_file:
        if not args.format_prompt_file.exists():
            print(f"[ERROR] Format prompt file not found: {args.format_prompt_file}", file=sys.stderr)
            sys.exit(1)
        format_prompt = args.format_prompt_file.read_text(encoding='utf-8')
    
    # Process
    try:
        if single_mode:
            result = process_single(
                args.input, args.output, api_keys, args.model, args.language,
                args.format, args.format_model, format_prompt, args.verbose
            )
            results = [result]
        else:
            results = process_batch(
                args.input_dir, args.output_dir, api_keys, args.model, args.language,
                args.format, args.format_model, format_prompt, args.verbose
            )
        
        # Output summary
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            total_duration = sum(r.get('audio_duration', 0) for r in results)
            total_format_tokens = sum(r.get('format_input_tokens', 0) + r.get('format_output_tokens', 0) for r in results)
            errors = sum(1 for r in results if 'error' in r)
            
            print(f"\nSummary: {len(results)} files processed, {errors} errors")
            if total_duration:
                print(f"Audio duration: {total_duration:.1f} seconds")
            if args.format:
                print(f"Formatting tokens: {total_format_tokens}")
    
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
