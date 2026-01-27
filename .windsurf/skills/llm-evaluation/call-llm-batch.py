#!/usr/bin/env python3
"""
call-llm-batch.py - Batch LLM calls with parallel processing, resume, and incremental save.

Usage:
  python call-llm-batch.py --model gpt-4o --input-folder images/ --output-folder out/ --prompt-file prompt.md
"""

import os, sys, json, time, base64, argparse
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

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


def save_used_settings(output_folder: Path, model: str, cli_params: dict, api_params: dict, prompt_file: Path):
    """Save used_settings_{model}.json at batch start."""
    safe_model = model.replace('/', '_').replace(':', '_')
    settings_file = output_folder / f"used_settings_{safe_model}.json"
    
    data = {
        "model": model,
        "cli_parameters": cli_params,
        "api_parameters": api_params,
        "prompt_file": str(prompt_file),
        "batch_started": datetime.now(timezone.utc).isoformat()
    }
    
    settings_file.write_text(json.dumps(data, indent=2), encoding='utf-8')
    print(f"Settings saved to: {settings_file}", file=sys.stderr)

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
    return None


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


def log(worker_id: int, current: int, total: int, msg: str):
    """Log with worker ID and progress."""
    print(f"[ worker {worker_id + 1} ] [ {current} / {total} ] {msg}", file=sys.stderr)


def atomic_write_json(path: Path, data: dict, lock: Lock):
    """Write JSON atomically using temp file pattern."""
    tmp_path = path.with_suffix('.tmp')
    with lock:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        tmp_path.rename(path)


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
    
    if hasattr(response.usage, 'prompt_tokens_details') and response.usage.prompt_tokens_details:
        cached = getattr(response.usage.prompt_tokens_details, 'cached_tokens', 0)
        if cached:
            result["usage"]["cached_tokens"] = cached
    
    if hasattr(response, 'system_fingerprint') and response.system_fingerprint:
        result['system_fingerprint'] = response.system_fingerprint
    
    return result


def call_anthropic(client, model: str, prompt: str, api_params: dict, method: str,
                   image_data: str = None, image_media_type: str = None,
                   use_prompt_caching: bool = False):
    """Call Anthropic API with configurable parameters and optional prompt caching."""
    
    if use_prompt_caching:
        system_content = []
        user_content = []
        
        if image_data:
            user_content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": image_media_type,
                    "data": image_data
                },
                "cache_control": {"type": "ephemeral"}
            })
        
        system_content.append({
            "type": "text",
            "text": prompt,
            "cache_control": {"type": "ephemeral"}
        })
        
        user_content.append({"type": "text", "text": "Process the content above according to the instructions."})
        
        call_params = {
            'model': model,
            'max_tokens': api_params.get('max_tokens', 4096),
            'system': system_content,
            'messages': [{"role": "user", "content": user_content}]
        }
    else:
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
    
    text_content = ""
    for block in response.content:
        if hasattr(block, 'text'):
            text_content = block.text
            break
    
    usage = {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens
    }
    
    if hasattr(response.usage, 'cache_creation_input_tokens'):
        usage["cache_write_tokens"] = response.usage.cache_creation_input_tokens
    if hasattr(response.usage, 'cache_read_input_tokens'):
        usage["cache_read_tokens"] = response.usage.cache_read_input_tokens
    
    return {
        "text": text_content,
        "usage": usage,
        "model": response.model
    }


def get_output_path(input_file: Path, output_folder: Path, model: str, run: int) -> Path:
    """Generate output path for content (.md)."""
    safe_model = model.replace('/', '_').replace(':', '_')
    base_name = f"{input_file.stem}_processed_{safe_model}_run{run:02d}"
    return output_folder / f"{base_name}.md"


def should_process(content_path: Path, force: bool) -> bool:
    """Check if file should be processed (resume logic)."""
    if force:
        return True
    return not content_path.exists()


def update_batch_metadata(output_folder: Path, model: str, entry: dict, lock: Lock):
    """Update consolidated batch metadata file."""
    safe_model = model.replace('/', '_').replace(':', '_')
    meta_file = output_folder / f"_batch_metadata_{safe_model}.json"
    
    with lock:
        if meta_file.exists():
            try:
                data = json.loads(meta_file.read_text(encoding='utf-8'))
            except:
                data = {"model": model, "files": []}
        else:
            data = {"model": model, "files": []}
        
        data["files"].append(entry)
        data["last_updated"] = datetime.now(timezone.utc).isoformat()
        data["total_files"] = len(data["files"])
        
        meta_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')


def update_token_usage(output_folder: Path, model: str, usage: dict, lock: Lock):
    """Update token usage file for model."""
    safe_model = model.replace('/', '_').replace(':', '_')
    usage_file = output_folder / f"_token_usage_{safe_model}.json"
    
    with lock:
        if usage_file.exists():
            try:
                data = json.loads(usage_file.read_text(encoding='utf-8'))
            except:
                data = {"model": model, "total_input_tokens": 0, "total_output_tokens": 0, "calls": 0}
        else:
            data = {"model": model, "total_input_tokens": 0, "total_output_tokens": 0, "calls": 0}
        
        data["total_input_tokens"] += usage.get("input_tokens", 0)
        data["total_output_tokens"] += usage.get("output_tokens", 0)
        data["calls"] += 1
        data["last_updated"] = datetime.now(timezone.utc).isoformat()
        
        usage_file.write_text(json.dumps(data, indent=2), encoding='utf-8')


def process_file(worker_id: int, file_idx: int, total_files: int, input_file: Path, 
                 args, client, provider: str, method: str, api_params: dict,
                 prompt: str, results_lock: Lock, usage_lock: Lock, use_caching: bool = False):
    """Process a single file."""
    file_type = detect_file_type(input_file)
    if not file_type:
        log(worker_id, file_idx, total_files, f"Skipping unknown type: {input_file.name}")
        return
    
    for run in range(1, args.runs + 1):
        content_path = get_output_path(input_file, args.output_folder, args.model, run)
        
        if not should_process(content_path, args.force):
            log(worker_id, file_idx, total_files, f"Skipping (exists): {content_path.name}")
            continue
        
        log(worker_id, file_idx, total_files, f"Processing: {input_file.name} run {run}")
        
        try:
            image_data = None
            image_media_type = None
            file_prompt = prompt
            
            if file_type == 'image':
                image_data = retry_with_backoff(lambda: encode_image_to_base64(input_file))
                image_media_type = get_image_media_type(input_file)
            else:
                text_content = input_file.read_text(encoding='utf-8')
                file_prompt = f"{prompt}\n\n---\n\n{text_content}"
            
            if provider == 'openai':
                result = retry_with_backoff(
                    lambda: call_openai(client, args.model, file_prompt, api_params, image_data, image_media_type)
                )
            else:
                result = retry_with_backoff(
                    lambda: call_anthropic(client, args.model, file_prompt, api_params, method, image_data, image_media_type, use_caching)
                )
            
            # Write content to .md file
            with results_lock:
                content_path.write_text(result["text"], encoding='utf-8')
            
            # Update consolidated metadata file
            meta_entry = {
                "output_file": content_path.name,
                "source_file": str(input_file),
                "model": result["model"],
                "run": run,
                "usage": result["usage"],
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            update_batch_metadata(args.output_folder, args.model, meta_entry, results_lock)
            update_token_usage(args.output_folder, args.model, result["usage"], usage_lock)
            
            cache_info = ""
            if result['usage'].get('cached_tokens'):
                cache_info = f" [{result['usage']['cached_tokens']} cached]"
            if result['usage'].get('cache_read_tokens'):
                cache_info = f" [{result['usage']['cache_read_tokens']} cache read]"
            if result['usage'].get('cache_write_tokens'):
                cache_info += f" [{result['usage']['cache_write_tokens']} cache write]"
            
            log(worker_id, file_idx, total_files, f"Done: {content_path.name} ({result['usage']['input_tokens']}+{result['usage']['output_tokens']} tokens){cache_info}")
            
        except Exception as e:
            log(worker_id, file_idx, total_files, f"ERROR: {input_file.name} run {run}: {e}")


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Batch LLM calls with parallel processing, resume, and incremental save.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--model', required=True, help='API model ID')
    parser.add_argument('--input-folder', type=Path, required=True, help='Input folder with files')
    parser.add_argument('--output-folder', type=Path, required=True, help='Output folder for results')
    parser.add_argument('--prompt-file', type=Path, required=True, help='Prompt file (.md)')
    parser.add_argument('--runs', type=int, default=1, help='Runs per file (default: 1)')
    parser.add_argument('--workers', type=int, default=4, help='Parallel workers (default: 4)')
    parser.add_argument('--keys-file', type=Path, default=Path('.env'), help='API keys file (default: .env)')
    parser.add_argument('--force', action='store_true', help='Force reprocess existing files')
    parser.add_argument('--clear-folder', action='store_true', help='Clear output folder before processing')
    parser.add_argument('--temperature', choices=EFFORT_LEVELS, default='medium', help='Temperature control (default: medium)')
    parser.add_argument('--reasoning-effort', choices=EFFORT_LEVELS, default='medium', help='Reasoning effort (default: medium)')
    parser.add_argument('--output-length', choices=EFFORT_LEVELS, default='medium', help='Output length (default: medium)')
    parser.add_argument('--seed', type=int, default=None, help='Random seed (OpenAI only)')
    parser.add_argument('--response-format', choices=['text', 'json'], default='text', help='Response format (default: text)')
    parser.add_argument('--use-prompt-caching', action='store_true', help='Enable prompt caching (Anthropic explicit, OpenAI automatic)')
    return parser.parse_args()


def main():
    args = parse_args()
    
    if args.workers < 1:
        print("[WARN] Workers set to 0, defaulting to 1", file=sys.stderr)
        args.workers = 1
    
    keys = load_api_keys(args.keys_file)
    script_dir = get_script_dir()
    mapping, registry = load_configs(script_dir)
    
    api_params, method, provider = build_api_params(
        args.model, mapping, registry,
        args.temperature, getattr(args, 'reasoning_effort', 'medium'),
        getattr(args, 'output_length', 'medium'), args.seed
    )
    
    print(f"API params: {api_params}", file=sys.stderr)
    
    if not args.input_folder.exists():
        print(f"[ERROR] Input folder not found: {args.input_folder}", file=sys.stderr)
        sys.exit(1)
    
    if not args.prompt_file.exists():
        print(f"[ERROR] Prompt file not found: {args.prompt_file}", file=sys.stderr)
        sys.exit(1)
    
    prompt = args.prompt_file.read_text(encoding='utf-8')
    
    if args.clear_folder and args.output_folder.exists():
        import shutil
        shutil.rmtree(args.output_folder)
        print(f"Cleared output folder: {args.output_folder}", file=sys.stderr)
    
    args.output_folder.mkdir(parents=True, exist_ok=True)
    
    all_extensions = IMAGE_EXTENSIONS | TEXT_EXTENSIONS
    input_files = [f for f in args.input_folder.iterdir() 
                   if f.is_file() and f.suffix.lower() in all_extensions]
    
    if not input_files:
        print(f"[ERROR] No files found in {args.input_folder}", file=sys.stderr)
        sys.exit(1)
    
    input_files.sort()
    total_files = len(input_files)
    
    print(f"Processing {total_files} files with {args.workers} workers, {args.runs} run(s) each", file=sys.stderr)
    print(f"Model: {args.model} ({provider})", file=sys.stderr)
    
    cli_params = {
        'temperature': args.temperature,
        'reasoning_effort': getattr(args, 'reasoning_effort', 'medium'),
        'output_length': getattr(args, 'output_length', 'medium'),
        'seed': args.seed
    }
    save_used_settings(args.output_folder, args.model, cli_params, api_params, args.prompt_file)
    
    use_caching = getattr(args, 'use_prompt_caching', False)
    
    if provider == 'openai':
        client = create_openai_client(keys)
        if use_caching:
            print("[INFO] OpenAI prompt caching is automatic (no API changes needed)", file=sys.stderr)
    else:
        client = create_anthropic_client(keys)
        if use_caching:
            print("[INFO] Anthropic prompt caching enabled via cache_control", file=sys.stderr)
    
    results_lock = Lock()
    usage_lock = Lock()
    
    # For Anthropic caching: process first file synchronously to warm up cache before parallel workers
    remaining_files = input_files
    if use_caching and provider == 'anthropic' and len(input_files) > 1:
        print("[INFO] Cache warm-up: processing first file before parallel workers...", file=sys.stderr)
        first_file = input_files[0]
        process_file(0, 1, total_files, first_file, args, client, provider, method, 
                     api_params, prompt, results_lock, usage_lock, use_caching)
        remaining_files = input_files[1:]
    
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {}
        start_idx = total_files - len(remaining_files) + 1
        for idx, input_file in enumerate(remaining_files, start_idx):
            worker_id = (idx - 1) % args.workers
            future = executor.submit(
                process_file, worker_id, idx, total_files, input_file,
                args, client, provider, method, api_params, prompt, results_lock, usage_lock, use_caching
            )
            futures[future] = input_file
        
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"[ERROR] Unhandled: {futures[future]}: {e}", file=sys.stderr)
    
    print(f"Batch complete. Output: {args.output_folder}", file=sys.stderr)


if __name__ == '__main__':
    main()
