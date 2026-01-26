#!/usr/bin/env python3
"""
call-llm.py - Single LLM call with auto-detection of image/text input.

Usage:
  python call-llm.py --model gpt-4o --input-file image.jpg --prompt-file prompt.md
  python call-llm.py --model claude-opus-4-20250514 --input-file doc.md --prompt-file prompt.md
"""

import os, sys, json, time, base64, argparse
from pathlib import Path
from datetime import datetime, timezone

UNKNOWN = '[UNKNOWN]'
EFFORT_LEVELS = ['none', 'minimal', 'low', 'medium', 'high', 'xhigh']


def get_script_dir() -> Path:
    """Get directory containing this script."""
    return Path(__file__).parent


def load_configs(script_dir: Path) -> tuple[dict, dict]:
    """Load model-parameter-mapping.json and model-registry.json."""
    mapping_file = script_dir / 'model-parameter-mapping.json'
    registry_file = script_dir / 'model-registry.json'
    
    if not mapping_file.exists():
        print(f"[ERROR] Config not found: {mapping_file}", file=sys.stderr)
        sys.exit(1)
    if not registry_file.exists():
        print(f"[ERROR] Config not found: {registry_file}", file=sys.stderr)
        sys.exit(1)
    
    with open(mapping_file, 'r', encoding='utf-8') as f:
        mapping = json.load(f)
    with open(registry_file, 'r', encoding='utf-8') as f:
        registry = json.load(f)
    
    return mapping, registry


def get_model_config(model: str, registry: dict) -> dict:
    """Return model config from registry using prefix matching."""
    for entry in registry['model_id_startswith']:
        if model.startswith(entry['prefix']):
            return entry
    known = [e['prefix'] for e in registry['model_id_startswith']]
    print(f"[ERROR] Unknown model: {model}. Known prefixes: {known}", file=sys.stderr)
    sys.exit(1)


def build_api_params(model: str, mapping: dict, registry: dict,
                     temperature: str, reasoning_effort: str,
                     output_length: str, seed: int = None) -> dict:
    """Build API parameters using effort levels."""
    model_config = get_model_config(model, registry)
    effort_map = mapping['effort_mapping']
    params = {}
    
    method = model_config.get('method', 'temperature')
    provider = model_config.get('provider', 'openai')
    
    if method == 'temperature':
        factor = effort_map[temperature]['temperature_factor']
        params['temperature'] = factor * model_config.get('temp_max', 2.0)
    elif method == 'reasoning_effort':
        params['reasoning_effort'] = effort_map[reasoning_effort]['openai_reasoning_effort']
    elif method == 'effort':
        params['effort'] = effort_map[reasoning_effort]['openai_reasoning_effort']
    elif method == 'thinking':
        factor = effort_map[reasoning_effort]['anthropic_thinking_factor']
        budget = int(factor * model_config.get('thinking_max', 100000))
        if budget > 0:
            params['thinking'] = {'type': 'enabled', 'budget_tokens': budget}
    
    output_factor = effort_map[output_length]['output_length_factor']
    max_output = model_config.get('max_output', 16384)
    params['max_tokens'] = int(output_factor * max_output)
    
    # Anthropic constraint: max_tokens must be > thinking.budget_tokens
    if 'thinking' in params and params['thinking'].get('budget_tokens', 0) > 0:
        thinking_budget = params['thinking']['budget_tokens']
        if params['max_tokens'] <= thinking_budget:
            params['max_tokens'] = thinking_budget + 1024
            print(f"[WARN] max_tokens adjusted to {params['max_tokens']} (must be > thinking budget {thinking_budget})", file=sys.stderr)
    
    if seed is not None:
        if model_config.get('seed', False):
            params['seed'] = seed
        else:
            print(f"[WARN] --seed ignored for {model} (not supported)", file=sys.stderr)
    
    return params, method, provider

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
TEXT_EXTENSIONS = {'.txt', '.md', '.json', '.py', '.html', '.xml', '.csv'}


def load_api_keys(keys_file: Path) -> dict:
    """Load API keys from .env or key=value file."""
    keys = {}
    if not keys_file.exists():
        print(f"[ERROR] Keys file not found: {keys_file}", file=sys.stderr)
        sys.exit(1)
    
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
    """Detect provider from model ID prefix."""
    model_lower = model_id.lower()
    if model_lower.startswith(('gpt-', 'o1-', 'o3-', 'davinci', 'curie', 'babbage', 'ada')):
        return 'openai'
    if model_lower.startswith('claude'):
        return 'anthropic'
    print(f"[ERROR] Cannot detect provider for model: {model_id}", file=sys.stderr)
    sys.exit(1)


def detect_file_type(file_path: Path) -> str:
    """Detect file type by suffix."""
    suffix = file_path.suffix.lower()
    if suffix in IMAGE_EXTENSIONS:
        return 'image'
    if suffix in TEXT_EXTENSIONS:
        return 'text'
    print(f"[ERROR] Unknown file type: {suffix}. Supported: {IMAGE_EXTENSIONS | TEXT_EXTENSIONS}", file=sys.stderr)
    sys.exit(1)


def retry_with_backoff(fn, retries=3, backoff=(1, 2, 4)):
    """Retry function with exponential backoff."""
    last_error = None
    for attempt in range(retries):
        try:
            return fn()
        except Exception as e:
            last_error = e
            if attempt < retries - 1:
                wait = backoff[attempt] if attempt < len(backoff) else backoff[-1]
                print(f"  Retry ({attempt + 1}/{retries}) in {wait}s: {e}", file=sys.stderr)
                time.sleep(wait)
    raise last_error


def encode_image_to_base64(file_path: Path) -> str:
    """Encode image file to base64."""
    with open(file_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


def get_image_media_type(file_path: Path) -> str:
    """Get media type for image."""
    suffix = file_path.suffix.lower()
    media_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp'
    }
    return media_types.get(suffix, 'image/jpeg')


def create_openai_client(keys: dict):
    """Create OpenAI client."""
    from openai import OpenAI
    api_key = keys.get('OPENAI_API_KEY')
    if not api_key:
        print("[ERROR] OPENAI_API_KEY not found in keys file", file=sys.stderr)
        sys.exit(1)
    return OpenAI(api_key=api_key)


def create_anthropic_client(keys: dict):
    """Create Anthropic client."""
    from anthropic import Anthropic
    api_key = keys.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("[ERROR] ANTHROPIC_API_KEY not found in keys file", file=sys.stderr)
        sys.exit(1)
    return Anthropic(api_key=api_key)


def call_openai(client, model: str, prompt: str, api_params: dict,
                image_data: str = None, image_media_type: str = None):
    """Call OpenAI API with configurable parameters."""
    if image_data:
        content = [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:{image_media_type};base64,{image_data}"}}
        ]
    else:
        content = prompt
    
    messages = [{"role": "user", "content": content}]
    
    call_params = {'model': model, 'messages': messages}
    
    if 'temperature' in api_params:
        call_params['temperature'] = api_params['temperature']
    if 'reasoning_effort' in api_params:
        call_params['reasoning_effort'] = api_params['reasoning_effort']
    if 'seed' in api_params:
        call_params['seed'] = api_params['seed']
    
    token_param = 'max_completion_tokens' if any(x in model for x in ['gpt-5', 'o1-', 'o3-', 'o4-']) else 'max_tokens'
    call_params[token_param] = api_params.get('max_tokens', 4096)
    
    response = client.chat.completions.create(**call_params)
    
    result = {
        "text": response.choices[0].message.content,
        "usage": {
            "input_tokens": response.usage.prompt_tokens,
            "output_tokens": response.usage.completion_tokens
        },
        "model": response.model
    }
    
    if hasattr(response, 'system_fingerprint') and response.system_fingerprint:
        result['system_fingerprint'] = response.system_fingerprint
    
    return result


def call_anthropic(client, model: str, prompt: str, api_params: dict, method: str,
                   image_data: str = None, image_media_type: str = None):
    """Call Anthropic API with configurable parameters."""
    content = []
    
    if image_data:
        content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": image_media_type,
                "data": image_data
            }
        })
    
    content.append({"type": "text", "text": prompt})
    
    call_params = {
        'model': model,
        'max_tokens': api_params.get('max_tokens', 4096),
        'messages': [{"role": "user", "content": content}]
    }
    
    if 'temperature' in api_params:
        call_params['temperature'] = api_params['temperature']
    
    if 'thinking' in api_params and api_params['thinking'].get('budget_tokens', 0) > 0:
        call_params['thinking'] = api_params['thinking']
    
    response = client.messages.create(**call_params)
    
    # Handle thinking responses: find text block (skip ThinkingBlock)
    text_content = ""
    for block in response.content:
        if hasattr(block, 'text'):
            text_content = block.text
            break
    
    return {
        "text": text_content,
        "usage": {
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens
        },
        "model": response.model
    }


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Single LLM call with auto-detection of image/text input.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python call-llm.py --model gpt-4o --input-file photo.jpg --prompt-file prompts/transcribe.md
  python call-llm.py --model claude-opus-4-20250514 --prompt-file prompts/question.md
        """
    )
    parser.add_argument('--model', required=True, help='API model ID (e.g., gpt-4o, claude-opus-4-20250514)')
    parser.add_argument('--input-file', type=Path, help='Input file (image or text)')
    parser.add_argument('--prompt-file', type=Path, required=True, help='Prompt file (.md)')
    parser.add_argument('--output-file', type=Path, help='Output file (default: stdout)')
    parser.add_argument('--keys-file', type=Path, default=Path('.env'), help='API keys file (default: .env)')
    parser.add_argument('--write-json-metadata', action='store_true', help='Write JSON with token usage')
    parser.add_argument('--temperature', choices=EFFORT_LEVELS, default='medium', help='Temperature control (default: medium)')
    parser.add_argument('--reasoning-effort', choices=EFFORT_LEVELS, default='medium', help='Reasoning effort (default: medium)')
    parser.add_argument('--output-length', choices=EFFORT_LEVELS, default='medium', help='Output length (default: medium)')
    parser.add_argument('--seed', type=int, default=None, help='Random seed (OpenAI only)')
    parser.add_argument('--response-format', choices=['text', 'json'], default='text', help='Response format (default: text)')
    return parser.parse_args()


def main():
    args = parse_args()
    
    keys = load_api_keys(args.keys_file)
    script_dir = get_script_dir()
    mapping, registry = load_configs(script_dir)
    
    api_params, method, provider = build_api_params(
        args.model, mapping, registry,
        args.temperature, getattr(args, 'reasoning_effort', 'medium'),
        getattr(args, 'output_length', 'medium'), args.seed
    )
    
    print(f"API params: {api_params}", file=sys.stderr)
    
    if not args.prompt_file.exists():
        print(f"[ERROR] Prompt file not found: {args.prompt_file}", file=sys.stderr)
        sys.exit(1)
    
    prompt = args.prompt_file.read_text(encoding='utf-8')
    
    image_data = None
    image_media_type = None
    
    if args.input_file:
        if not args.input_file.exists():
            print(f"[ERROR] Input file not found: {args.input_file}", file=sys.stderr)
            sys.exit(1)
        
        input_type = detect_file_type(args.input_file)
        
        if input_type == 'image':
            print(f"Processing image: {args.input_file}", file=sys.stderr)
            image_data = retry_with_backoff(lambda: encode_image_to_base64(args.input_file))
            image_media_type = get_image_media_type(args.input_file)
        else:
            print(f"Processing text: {args.input_file}", file=sys.stderr)
            text_content = args.input_file.read_text(encoding='utf-8')
            prompt = f"{prompt}\n\n---\n\n{text_content}"
    
    if provider == 'openai':
        client = create_openai_client(keys)
        call_fn = lambda: call_openai(client, args.model, prompt, api_params, image_data, image_media_type)
    else:
        client = create_anthropic_client(keys)
        call_fn = lambda: call_anthropic(client, args.model, prompt, api_params, method, image_data, image_media_type)
    
    print(f"Calling {provider} API with model {args.model}...", file=sys.stderr)
    result = retry_with_backoff(call_fn)
    
    output_text = result["text"]
    
    if args.output_file:
        args.output_file.parent.mkdir(parents=True, exist_ok=True)
        args.output_file.write_text(output_text, encoding='utf-8')
        print(f"Output written to: {args.output_file}", file=sys.stderr)
    else:
        print(output_text)
    
    if args.write_json_metadata:
        metadata = {
            "model": result["model"],
            "usage": result["usage"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "input_file": str(args.input_file) if args.input_file else None,
            "prompt_file": str(args.prompt_file)
        }
        
        if args.output_file:
            meta_file = args.output_file.with_suffix('.meta.json')
        else:
            meta_file = Path(f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.meta.json")
        
        meta_file.write_text(json.dumps(metadata, indent=2), encoding='utf-8')
        print(f"Metadata written to: {meta_file}", file=sys.stderr)
    
    print(f"Done. Tokens: {result['usage']['input_tokens']} in, {result['usage']['output_tokens']} out", file=sys.stderr)


if __name__ == '__main__':
    main()
