#!/usr/bin/env python3
"""
transcribe-image-to-markdown-advanced.py - Ensemble transcription with judge and refinement.

Pipeline:
1. Generate N transcriptions concurrently (ensemble)
2. Judge all N concurrently, select highest score
3. If score < threshold, refine with complete judge feedback and re-judge
4. Output includes final score for quality assurance

Usage:
  python transcribe-image-to-markdown-advanced.py --input-file doc.png --output-file doc.md
  python transcribe-image-to-markdown-advanced.py --input-folder images/ --output-folder out/ --workers 4
"""

import os
import sys
import json
import time
import base64
import asyncio
import argparse
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

EFFORT_LEVELS = ['none', 'minimal', 'low', 'medium', 'high', 'xhigh']
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
DEFAULT_MODEL = 'gpt-5-mini'
DEFAULT_JUDGE_MODEL = 'gpt-5-mini'
DEFAULT_INITIAL_CANDIDATES = 3
DEFAULT_MIN_SCORE = 3.5
DEFAULT_MAX_REFINEMENTS = 1
DEFAULT_WORKERS = 4


def get_script_dir() -> Path:
    return Path(__file__).parent


def load_configs(script_dir: Path) -> tuple[dict, dict, dict | None]:
    """Load model-registry.json, model-parameter-mapping.json, model-pricing.json."""
    registry_file = script_dir / 'model-registry.json'
    mapping_file = script_dir / 'model-parameter-mapping.json'
    pricing_file = script_dir / 'model-pricing.json'
    
    if not registry_file.exists():
        print(f"[ERROR] Config not found: {registry_file}", file=sys.stderr)
        sys.exit(1)
    if not mapping_file.exists():
        print(f"[ERROR] Config not found: {mapping_file}", file=sys.stderr)
        sys.exit(1)
    
    with open(registry_file, 'r', encoding='utf-8') as f:
        registry = json.load(f)
    with open(mapping_file, 'r', encoding='utf-8') as f:
        mapping = json.load(f)
    
    pricing = None
    if pricing_file.exists():
        with open(pricing_file, 'r', encoding='utf-8') as f:
            pricing = json.load(f)
    
    return registry, mapping, pricing


def get_model_config(model: str, registry: dict) -> dict:
    """Return model config from registry using prefix matching."""
    for entry in registry.get('model_id_startswith', []):
        if model.startswith(entry['prefix']):
            return entry
    known = [e['prefix'] for e in registry.get('model_id_startswith', [])]
    print(f"[ERROR] Unknown model: {model}. Known prefixes: {known}", file=sys.stderr)
    sys.exit(1)


def build_api_params(model: str, mapping: dict, registry: dict,
                     temperature: str, reasoning_effort: str, output_length: str) -> tuple[dict, str, str]:
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
    elif method == 'thinking':
        factor = effort_map[reasoning_effort]['anthropic_thinking_factor']
        budget = int(factor * model_config.get('thinking_max', 100000))
        if budget > 0:
            params['thinking'] = {'type': 'enabled', 'budget_tokens': budget}
    
    output_factor = effort_map[output_length]['output_length_factor']
    max_output = model_config.get('max_output', 16384)
    params['max_tokens'] = int(output_factor * max_output)
    
    if 'thinking' in params and params['thinking'].get('budget_tokens', 0) > 0:
        thinking_budget = params['thinking']['budget_tokens']
        if params['max_tokens'] <= thinking_budget:
            params['max_tokens'] = thinking_budget + 1024
    
    return params, method, provider


def calculate_cost(model: str, input_tokens: int, output_tokens: int, 
                   pricing: dict | None, provider: str) -> float | None:
    """Calculate cost in USD based on token usage."""
    if not pricing:
        return None
    provider_pricing = pricing.get('pricing', {}).get(provider, {})
    model_pricing = provider_pricing.get(model)
    if not model_pricing:
        return None
    input_cost = (input_tokens / 1_000_000) * model_pricing['input_per_1m']
    output_cost = (output_tokens / 1_000_000) * model_pricing['output_per_1m']
    return round(input_cost + output_cost, 6)


def load_api_keys(keys_file: Path) -> dict:
    """Load API keys from .env file."""
    keys = {}
    if os.environ.get('OPENAI_API_KEY'):
        keys['OPENAI_API_KEY'] = os.environ['OPENAI_API_KEY']
    if os.environ.get('ANTHROPIC_API_KEY'):
        keys['ANTHROPIC_API_KEY'] = os.environ['ANTHROPIC_API_KEY']
    
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
    """Detect provider from model ID prefix."""
    model_lower = model_id.lower()
    if model_lower.startswith(('gpt-', 'o1', 'o3', 'o4')):
        return 'openai'
    if model_lower.startswith('claude'):
        return 'anthropic'
    return 'openai'


def encode_image_to_base64(image_path: Path) -> str:
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


def get_image_media_type(image_path: Path) -> str:
    suffix = image_path.suffix.lower()
    media_types = {
        '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
        '.png': 'image/png', '.gif': 'image/gif', '.webp': 'image/webp'
    }
    return media_types.get(suffix, 'image/jpeg')


def log(worker_id: int, current: int, total: int, msg: str):
    """Log with worker ID and progress to stderr."""
    print(f"[ worker {worker_id + 1} ] [ {current} / {total} ] {msg}", file=sys.stderr)


def get_temp_dir(temp_folder: Path | None = None) -> Path:
    """Get or create temp directory."""
    if temp_folder:
        temp_dir = temp_folder
    else:
        temp_dir = Path.cwd() / '.tools' / '_image_to_markdown'
    temp_dir.mkdir(parents=True, exist_ok=True)
    return temp_dir


def make_temp_prefix() -> str:
    """Generate temp file prefix with timestamp."""
    now = datetime.now()
    return f".tmp_{now.strftime('%Y-%m-%d_%H-%M-%S')}-{now.microsecond // 1000:03d}_"


def save_temp_file(temp_dir: Path, prefix: str, suffix: str, content: str) -> Path:
    """Save content to temp file."""
    temp_path = temp_dir / f"{prefix}{suffix}"
    temp_path.write_text(content, encoding='utf-8')
    return temp_path


def cleanup_temp_files(temp_dir: Path, prefix: str):
    """Delete all temp files with given prefix."""
    for f in temp_dir.glob(f"{prefix}*"):
        try:
            f.unlink()
        except Exception:
            pass


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


def call_openai_vision(model: str, image_data: str, media_type: str,
                       prompt: str, api_key: str, api_params: dict) -> dict:
    """Call OpenAI vision API synchronously."""
    import httpx
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    # gpt-5 and o-series models use max_completion_tokens instead of max_tokens
    uses_completion_tokens = any(x in model for x in ['gpt-5', 'o1-', 'o3-', 'o4-'])
    token_param = 'max_completion_tokens' if uses_completion_tokens else 'max_tokens'
    
    payload = {
        'model': model,
        token_param: api_params.get('max_tokens', 8192),
        'messages': [{
            'role': 'user',
            'content': [
                {'type': 'text', 'text': prompt},
                {'type': 'image_url', 'image_url': {'url': f'data:{media_type};base64,{image_data}'}}
            ]
        }]
    }
    if 'temperature' in api_params:
        payload['temperature'] = api_params['temperature']
    if 'reasoning_effort' in api_params:
        payload['reasoning_effort'] = api_params['reasoning_effort']
    
    with httpx.Client(timeout=180.0) as client:
        response = client.post('https://api.openai.com/v1/chat/completions',
                               headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
    
    return {
        'content': result['choices'][0]['message']['content'],
        'input_tokens': result['usage']['prompt_tokens'],
        'output_tokens': result['usage']['completion_tokens'],
        'model': result.get('model', model)
    }


def call_anthropic_vision(model: str, image_data: str, media_type: str,
                          prompt: str, api_key: str, api_params: dict) -> dict:
    """Call Anthropic vision API synchronously."""
    import httpx
    
    headers = {
        'x-api-key': api_key,
        'anthropic-version': '2023-06-01',
        'Content-Type': 'application/json'
    }
    
    messages = [{
        'role': 'user',
        'content': [
            {'type': 'image', 'source': {'type': 'base64', 'media_type': media_type, 'data': image_data}},
            {'type': 'text', 'text': prompt}
        ]
    }]
    
    payload = {
        'model': model,
        'max_tokens': api_params.get('max_tokens', 8192),
        'messages': messages
    }
    if 'thinking' in api_params:
        payload['thinking'] = api_params['thinking']
    
    with httpx.Client(timeout=180.0) as client:
        response = client.post('https://api.anthropic.com/v1/messages',
                               headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
    
    content = ''
    for block in result.get('content', []):
        if block.get('type') == 'text':
            content += block.get('text', '')
    
    usage = result.get('usage', {})
    return {
        'content': content,
        'input_tokens': usage.get('input_tokens', 0),
        'output_tokens': usage.get('output_tokens', 0),
        'model': result.get('model', model)
    }


def call_vision_api(model: str, image_data: str, media_type: str, prompt: str,
                    api_keys: dict, api_params: dict, provider: str) -> dict:
    """Call appropriate vision API based on provider."""
    if provider == 'anthropic':
        api_key = api_keys.get('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found")
        return retry_with_backoff(
            lambda: call_anthropic_vision(model, image_data, media_type, prompt, api_key, api_params)
        )
    else:
        api_key = api_keys.get('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found")
        return retry_with_backoff(
            lambda: call_openai_vision(model, image_data, media_type, prompt, api_key, api_params)
        )


async def generate_transcription_async(image_data: str, media_type: str, prompt: str,
                                        model: str, api_keys: dict, api_params: dict, 
                                        provider: str) -> dict:
    """Generate transcription asynchronously."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None, 
        lambda: call_vision_api(model, image_data, media_type, prompt, api_keys, api_params, provider)
    )


def parse_judge_response(content: str) -> dict:
    """Parse JSON from judge response, handling markdown fences."""
    content = content.strip()
    if content.startswith('```'):
        lines = content.split('\n')
        content = '\n'.join(lines[1:])
        if '```' in content:
            content = content.rsplit('```', 1)[0]
    
    start = content.find('{')
    end = content.rfind('}') + 1
    if start >= 0 and end > start:
        return json.loads(content[start:end])
    raise ValueError("No JSON found in judge response")


def calculate_weighted_score(judge_data: dict) -> float:
    """Calculate weighted score from judge dimensions."""
    text = judge_data.get('text_accuracy', {}).get('score', 3)
    structure = judge_data.get('page_structure', {}).get('score', 3)
    graphics = judge_data.get('graphics_quality', {}).get('score', 3)
    return text * 0.25 + structure * 0.35 + graphics * 0.40


async def judge_transcription_async(image_data: str, media_type: str, transcription: str,
                                     judge_prompt: str, judge_model: str, api_keys: dict,
                                     api_params: dict, provider: str) -> dict:
    """Judge a transcription asynchronously."""
    full_prompt = f"""{judge_prompt}

---

## Image
[Provided as attachment]

## Transcription to Judge

{transcription}
"""
    
    result = await generate_transcription_async(
        image_data, media_type, full_prompt, judge_model, api_keys, api_params, provider
    )
    
    try:
        judge_data = parse_judge_response(result['content'])
        weighted_score = judge_data.get('weighted_score')
        if weighted_score is None:
            weighted_score = calculate_weighted_score(judge_data)
            judge_data['weighted_score'] = weighted_score
    except (json.JSONDecodeError, ValueError):
        judge_data = {'error': 'Failed to parse judge response', 'raw': result['content'][:500]}
        weighted_score = 3.0
        judge_data['weighted_score'] = weighted_score
    
    return {
        'judge_data': judge_data,
        'weighted_score': weighted_score,
        'input_tokens': result['input_tokens'],
        'output_tokens': result['output_tokens']
    }


async def process_image_ensemble(image_data: str, media_type: str,
                                  transcribe_prompt: str, judge_prompt: str,
                                  model: str, judge_model: str, initial_candidates: int,
                                  api_keys: dict, api_params: dict, judge_api_params: dict,
                                  provider: str, judge_provider: str,
                                  min_score: float, max_refinements: int,
                                  worker_id: int, file_idx: int, total_files: int) -> dict:
    """Run ensemble + judge + select + maybe refine pipeline."""
    total_input_tokens = 0
    total_output_tokens = 0
    
    log(worker_id, file_idx, total_files, f"Transcribing ({initial_candidates} candidates)...")
    transcription_tasks = [
        generate_transcription_async(image_data, media_type, transcribe_prompt, 
                                      model, api_keys, api_params, provider)
        for _ in range(initial_candidates)
    ]
    transcriptions = await asyncio.gather(*transcription_tasks, return_exceptions=True)
    
    valid_transcriptions = []
    for t in transcriptions:
        if isinstance(t, Exception):
            continue
        valid_transcriptions.append(t)
        total_input_tokens += t['input_tokens']
        total_output_tokens += t['output_tokens']
    
    if not valid_transcriptions:
        raise RuntimeError("All transcription attempts failed")
    
    log(worker_id, file_idx, total_files, f"Judging {len(valid_transcriptions)} candidates...")
    judge_tasks = [
        judge_transcription_async(image_data, media_type, t['content'], judge_prompt,
                                   judge_model, api_keys, judge_api_params, judge_provider)
        for t in valid_transcriptions
    ]
    judge_results = await asyncio.gather(*judge_tasks, return_exceptions=True)
    
    valid_judges = []
    for i, j in enumerate(judge_results):
        if isinstance(j, Exception):
            valid_judges.append({'weighted_score': 3.0, 'judge_data': {'error': str(j)}, 
                                'input_tokens': 0, 'output_tokens': 0})
        else:
            valid_judges.append(j)
            total_input_tokens += j['input_tokens']
            total_output_tokens += j['output_tokens']
    
    best_idx = max(range(len(valid_judges)), key=lambda i: valid_judges[i]['weighted_score'])
    best_transcription = valid_transcriptions[best_idx]
    best_judge = valid_judges[best_idx]
    all_scores = [j['weighted_score'] for j in valid_judges]
    
    log(worker_id, file_idx, total_files, 
        f"Best score: {best_judge['weighted_score']:.2f} (candidate {best_idx + 1})")
    
    refinement_applied = False
    if best_judge['weighted_score'] < min_score and max_refinements > 0:
        log(worker_id, file_idx, total_files, 
            f"Score {best_judge['weighted_score']:.2f} < {min_score}, refining...")
        
        refinement_prompt = f"""{transcribe_prompt}

---

Previous transcription (score: {best_judge['weighted_score']:.2f}/5.0):

{best_transcription['content']}

---

Judge feedback (improve based on this):

```json
{json.dumps(best_judge['judge_data'], indent=2)}
```

Please improve the transcription based on the judge feedback above.
"""
        
        try:
            refined = await generate_transcription_async(
                image_data, media_type, refinement_prompt, model, api_keys, api_params, provider
            )
            total_input_tokens += refined['input_tokens']
            total_output_tokens += refined['output_tokens']
            
            refined_judge = await judge_transcription_async(
                image_data, media_type, refined['content'], judge_prompt,
                judge_model, api_keys, judge_api_params, judge_provider
            )
            total_input_tokens += refined_judge['input_tokens']
            total_output_tokens += refined_judge['output_tokens']
            
            log(worker_id, file_idx, total_files, 
                f"Refined score: {refined_judge['weighted_score']:.2f}")
            
            if refined_judge['weighted_score'] > best_judge['weighted_score']:
                best_transcription = refined
                best_judge = refined_judge
                refinement_applied = True
        except Exception as e:
            log(worker_id, file_idx, total_files, f"Refinement failed: {e}")
    
    return {
        'content': best_transcription['content'],
        'final_score': best_judge['weighted_score'],
        'candidate_scores': all_scores,
        'selected_candidate': best_idx + 1,
        'refinement_applied': refinement_applied,
        'total_input_tokens': total_input_tokens,
        'total_output_tokens': total_output_tokens
    }


def process_single_image(worker_id: int, file_idx: int, total_files: int,
                         image_path: Path, output_path: Path, args,
                         api_keys: dict, api_params: dict, judge_api_params: dict,
                         provider: str, judge_provider: str,
                         transcribe_prompt: str, judge_prompt: str,
                         pricing: dict | None, results_lock: Lock,
                         temp_dir: Path, keep_temp: bool) -> dict:
    """Process a single image file."""
    start_time = time.time()
    temp_prefix = make_temp_prefix()
    
    log(worker_id, file_idx, total_files, f"Processing: {image_path.name}")
    
    try:
        image_data = encode_image_to_base64(image_path)
        media_type = get_image_media_type(image_path)
        
        result = asyncio.run(process_image_ensemble(
            image_data, media_type, transcribe_prompt, judge_prompt,
            args.model, args.judge_model, args.initial_candidates,
            api_keys, api_params, judge_api_params, provider, judge_provider,
            args.min_score, args.max_refinements,
            worker_id, file_idx, total_files
        ))
        
        elapsed = time.time() - start_time
        
        with results_lock:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(result['content'], encoding='utf-8')
        
        cost = calculate_cost(args.model, result['total_input_tokens'], 
                             result['total_output_tokens'], pricing, provider)
        
        refined_str = " (refined)" if result['refinement_applied'] else ""
        cost_str = f", ${cost:.4f}" if cost else ""
        log(worker_id, file_idx, total_files, 
            f"Done: {output_path.name} ({result['final_score']:.2f}{refined_str}, "
            f"{result['total_input_tokens']}+{result['total_output_tokens']} tokens{cost_str}, {elapsed:.1f}s)")
        
        if not keep_temp:
            cleanup_temp_files(temp_dir, temp_prefix)
        
        return {
            'input': str(image_path),
            'output': str(output_path),
            'model': args.model,
            'judge_model': args.judge_model,
            'final_score': result['final_score'],
            'candidates': args.initial_candidates,
            'candidate_scores': result['candidate_scores'],
            'selected_candidate': result['selected_candidate'],
            'refinement_applied': result['refinement_applied'],
            'total_input_tokens': result['total_input_tokens'],
            'total_output_tokens': result['total_output_tokens'],
            'total_cost_usd': cost,
            'elapsed_seconds': round(elapsed, 2),
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
    
    except Exception as e:
        elapsed = time.time() - start_time
        log(worker_id, file_idx, total_files, f"FAILED: {image_path.name} - {e}")
        return {
            'input': str(image_path),
            'error': str(e),
            'elapsed_seconds': round(elapsed, 2),
            'timestamp': datetime.now(timezone.utc).isoformat()
        }


def parse_args():
    parser = argparse.ArgumentParser(
        description='Ensemble image transcription with judge and refinement.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Pipeline:
  1. Generate N transcriptions concurrently (ensemble)
  2. Judge all N concurrently, select highest score
  3. If score < threshold, refine with judge feedback and re-judge

Examples:
  python transcribe-image-to-markdown-advanced.py --input-file doc.png --output-file doc.md
  python transcribe-image-to-markdown-advanced.py --input-folder images/ --output-folder out/ --workers 4
        """
    )
    
    parser.add_argument('--input-file', type=Path, help='Single input image file')
    parser.add_argument('--output-file', type=Path, help='Output markdown file')
    parser.add_argument('--input-folder', type=Path, help='Input folder for batch mode')
    parser.add_argument('--output-folder', type=Path, help='Output folder for batch mode')
    
    parser.add_argument('--model', default=DEFAULT_MODEL, help=f'Transcription model (default: {DEFAULT_MODEL})')
    parser.add_argument('--judge-model', default=DEFAULT_JUDGE_MODEL, help=f'Judge model (default: {DEFAULT_JUDGE_MODEL})')
    
    parser.add_argument('--transcribe-prompt-file', type=Path, help='Transcription prompt file')
    parser.add_argument('--judge-prompt-file', type=Path, help='Judge prompt file')
    
    parser.add_argument('--initial-candidates', type=int, default=DEFAULT_INITIAL_CANDIDATES,
                        help=f'Candidates to generate (default: {DEFAULT_INITIAL_CANDIDATES})')
    parser.add_argument('--min-score', type=float, default=DEFAULT_MIN_SCORE,
                        help=f'Threshold for refinement (default: {DEFAULT_MIN_SCORE})')
    parser.add_argument('--max-refinements', type=int, default=DEFAULT_MAX_REFINEMENTS,
                        help=f'Max refinement iterations (default: {DEFAULT_MAX_REFINEMENTS})')
    parser.add_argument('--workers', type=int, default=DEFAULT_WORKERS,
                        help=f'Parallel workers (default: {DEFAULT_WORKERS})')
    
    parser.add_argument('--keys-file', type=Path, default=Path('.env'), help='API keys file (default: .env)')
    parser.add_argument('--temperature', default='medium', choices=EFFORT_LEVELS,
                        help='Temperature effort level (default: medium)')
    parser.add_argument('--reasoning-effort', default='medium', choices=EFFORT_LEVELS,
                        help='Reasoning effort level (default: medium)')
    parser.add_argument('--output-length', default='medium', choices=EFFORT_LEVELS,
                        help='Output length effort level (default: medium)')
    
    parser.add_argument('--force', action='store_true', help='Force reprocess existing files')
    parser.add_argument('--keep-temp', action='store_true', help='Preserve temp files after success')
    parser.add_argument('--temp-folder', type=Path, help='Custom temp folder')
    parser.add_argument('--json', action='store_true', help='Output results as JSON')
    
    return parser.parse_args()


def main():
    args = parse_args()
    
    single_mode = args.input_file is not None
    batch_mode = args.input_folder is not None
    
    if not single_mode and not batch_mode:
        print("[ERROR] Must specify --input-file or --input-folder", file=sys.stderr)
        sys.exit(1)
    if single_mode and batch_mode:
        print("[ERROR] Cannot use both --input-file and --input-folder", file=sys.stderr)
        sys.exit(1)
    
    if single_mode:
        if not args.input_file.exists():
            print(f"[ERROR] File not found: {args.input_file}", file=sys.stderr)
            sys.exit(1)
        if args.input_file.suffix.lower() not in IMAGE_EXTENSIONS:
            print(f"[ERROR] Unsupported format. Use: {', '.join(IMAGE_EXTENSIONS)}", file=sys.stderr)
            sys.exit(1)
        if not args.output_file:
            args.output_file = args.input_file.with_suffix('.md')
    
    if batch_mode:
        if not args.input_folder.exists():
            print(f"[ERROR] Folder not found: {args.input_folder}", file=sys.stderr)
            sys.exit(1)
        if not args.output_folder:
            args.output_folder = args.input_folder / 'transcripts'
    
    script_dir = get_script_dir()
    registry, mapping, pricing = load_configs(script_dir)
    
    api_keys = load_api_keys(args.keys_file)
    if not api_keys.get('OPENAI_API_KEY') and not api_keys.get('ANTHROPIC_API_KEY'):
        print("[ERROR] No API keys found. Set OPENAI_API_KEY or ANTHROPIC_API_KEY in .env", file=sys.stderr)
        sys.exit(1)
    
    prompts_dir = script_dir / 'prompts'
    if args.transcribe_prompt_file:
        transcribe_prompt = args.transcribe_prompt_file.read_text(encoding='utf-8')
    elif (prompts_dir / 'transcription.md').exists():
        transcribe_prompt = (prompts_dir / 'transcription.md').read_text(encoding='utf-8')
    else:
        print("[ERROR] No transcription prompt. Use --transcribe-prompt-file or create prompts/transcription.md", file=sys.stderr)
        sys.exit(1)
    
    if args.judge_prompt_file:
        judge_prompt = args.judge_prompt_file.read_text(encoding='utf-8')
    elif (prompts_dir / 'judge.md').exists():
        judge_prompt = (prompts_dir / 'judge.md').read_text(encoding='utf-8')
    else:
        print("[ERROR] No judge prompt. Use --judge-prompt-file or create prompts/judge.md", file=sys.stderr)
        sys.exit(1)
    
    provider = detect_provider(args.model)
    judge_provider = detect_provider(args.judge_model)
    
    api_params, _, _ = build_api_params(args.model, mapping, registry,
                                         args.temperature, args.reasoning_effort, args.output_length)
    judge_api_params, _, _ = build_api_params(args.judge_model, mapping, registry,
                                               args.temperature, args.reasoning_effort, 'medium')
    
    temp_dir = get_temp_dir(args.temp_folder)
    results_lock = Lock()
    results = []
    
    if single_mode:
        result = process_single_image(
            0, 1, 1, args.input_file, args.output_file, args,
            api_keys, api_params, judge_api_params, provider, judge_provider,
            transcribe_prompt, judge_prompt, pricing, results_lock, temp_dir, args.keep_temp
        )
        results.append(result)
    else:
        image_files = sorted([
            f for f in args.input_folder.iterdir()
            if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS
        ])
        
        if not image_files:
            print(f"[ERROR] No images found in {args.input_folder}", file=sys.stderr)
            sys.exit(1)
        
        print(f"Found {len(image_files)} images, processing with {args.workers} workers", file=sys.stderr)
        
        def process_wrapper(idx_and_file):
            idx, image_file = idx_and_file
            output_file = args.output_folder / (image_file.stem + '.md')
            if output_file.exists() and not args.force:
                log(idx % args.workers, idx + 1, len(image_files), f"Skipping: {image_file.name} (exists)")
                return {'input': str(image_file), 'skipped': True}
            return process_single_image(
                idx % args.workers, idx + 1, len(image_files), image_file, output_file, args,
                api_keys, api_params, judge_api_params, provider, judge_provider,
                transcribe_prompt, judge_prompt, pricing, results_lock, temp_dir, args.keep_temp
            )
        
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = {executor.submit(process_wrapper, (i, f)): f for i, f in enumerate(image_files)}
            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append({'input': str(futures[future]), 'error': str(e)})
    
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        successful = [r for r in results if 'final_score' in r]
        failed = [r for r in results if 'error' in r]
        skipped = [r for r in results if r.get('skipped')]
        
        if successful:
            avg_score = sum(r['final_score'] for r in successful) / len(successful)
            total_input = sum(r['total_input_tokens'] for r in successful)
            total_output = sum(r['total_output_tokens'] for r in successful)
            total_cost = sum(r.get('total_cost_usd') or 0 for r in successful)
            refinements = sum(1 for r in successful if r['refinement_applied'])
            total_elapsed = sum(r['elapsed_seconds'] for r in successful)
            
            print(f"\n{'='*60}", file=sys.stderr)
            print(f"Summary: {len(successful)} successful, {len(failed)} failed, {len(skipped)} skipped", file=sys.stderr)
            print(f"Average score: {avg_score:.2f}, {refinements} refined", file=sys.stderr)
            print(f"Total tokens: {total_input}+{total_output} = {total_input + total_output}", file=sys.stderr)
            if total_cost > 0:
                print(f"Total cost: ${total_cost:.4f}", file=sys.stderr)
            print(f"Total time: {total_elapsed:.1f}s", file=sys.stderr)
            
            batch_summary = {
                'total_images': len(results),
                'successful': len(successful),
                'failed': len(failed),
                'skipped': len(skipped),
                'average_score': round(avg_score, 2),
                'refinements_applied': refinements,
                'total_input_tokens': total_input,
                'total_output_tokens': total_output,
                'total_cost_usd': round(total_cost, 4) if total_cost > 0 else None,
                'total_elapsed_seconds': round(total_elapsed, 1)
            }
            
            if batch_mode:
                summary_file = args.output_folder / '_batch_summary.json'
                summary_file.write_text(json.dumps(batch_summary, indent=2), encoding='utf-8')
                print(f"Batch summary: {summary_file}", file=sys.stderr)


if __name__ == '__main__':
    main()
