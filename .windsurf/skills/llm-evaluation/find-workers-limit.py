#!/usr/bin/env python3
"""
find-workers-limit.py - Discover maximum concurrent workers for LLM API calls.

This script tests burst capacity by progressively scaling up concurrent workers
until rate limits are hit, then scaling back to find a stable limit.

NOTE: This tests BURST capacity (max concurrent requests), not sustained RPM.
Results are specific to the API key used and may vary based on server load.

Usage:
  python find-workers-limit.py --model gpt-4o --keys-file .api-keys.txt
  python find-workers-limit.py --model claude-3-5-sonnet-20241022 --output-file limits.json --verbose
"""

import os, sys, json, time, argparse
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed

DEFAULT_PROMPT = """Write a detailed 500-word essay about the history of computing, 
covering the evolution from mechanical calculators to modern AI systems. Include 
key milestones such as the invention of the transistor, the development of 
programming languages, the rise of personal computers, and the emergence of 
artificial intelligence. Discuss how each advancement built upon previous 
innovations and shaped the technology landscape we have today."""


def get_script_dir() -> Path:
    """Get directory containing this script."""
    return Path(__file__).parent


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
    if model_lower.startswith(('gpt-', 'o1-', 'o3-', 'o4-', 'davinci', 'curie', 'babbage', 'ada')):
        return 'openai'
    if model_lower.startswith('claude'):
        return 'anthropic'
    print(f"[ERROR] Cannot detect provider for model: {model_id}", file=sys.stderr)
    sys.exit(1)


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


def is_rate_limit_error(e: Exception) -> bool:
    """Check if exception is a rate limit error (FR-21)."""
    error_str = str(e).lower()
    if '429' in error_str or 'rate' in error_str:
        return True
    if hasattr(e, 'status_code') and e.status_code == 429:
        return True
    return type(e).__name__ in ('RateLimitError', 'APIStatusError')


def next_worker_count(current: int, max_workers: int) -> int:
    """Calculate next worker count in scaling sequence (FR-20)."""
    if current == 3:
        return min(6, max_workers)
    if current == 6:
        return min(12, max_workers)
    next_count = int(current * 1.5)
    return min(next_count, max_workers)


def scale_back_count(current: int) -> int:
    """Calculate scaled-back worker count (FR-22)."""
    return max(1, int(current * 0.8))


def single_call(client, model: str, prompt: str, provider: str, 
                min_tokens: int, timeout: int = 120) -> tuple:
    """
    Make single LLM call. Returns (success, is_rate_limited, usage).
    Uses retry for non-rate-limit errors (FR-27).
    Timeout: 120 seconds per call (Fix RV-013).
    """
    max_retries = 3
    backoff = [1, 2, 4]
    
    for attempt in range(max_retries):
        try:
            if provider == 'openai':
                token_param = 'max_completion_tokens' if any(x in model for x in ['gpt-5', 'o1-', 'o3-', 'o4-']) else 'max_tokens'
                call_params = {
                    'model': model,
                    'messages': [{"role": "user", "content": prompt}],
                    token_param: min_tokens,
                    'timeout': timeout
                }
                response = client.chat.completions.create(**call_params)
                usage = {
                    'input_tokens': response.usage.prompt_tokens,
                    'output_tokens': response.usage.completion_tokens
                }
            else:
                response = client.messages.create(
                    model=model,
                    max_tokens=min_tokens,
                    messages=[{"role": "user", "content": prompt}]
                )
                # Correctly access attributes from Anthropic Usage object
                usage = {
                    'input_tokens': response.usage.input_tokens,
                    'output_tokens': response.usage.output_tokens
                }
                # Check for successful response content
                success = any(hasattr(block, 'text') and block.text for block in response.content)
                return (success, False, usage)
        
        except Exception as e:
            if is_rate_limit_error(e):
                return (False, True, {})
            
            if attempt < max_retries - 1:
                time.sleep(backoff[attempt])
            else:
                return (False, False, {})
    
    return (False, False, {})


def run_test(client, model: str, prompt: str, provider: str,
             worker_count: int, min_tokens: int, verbose: bool) -> dict:
    """
    Run test with worker_count concurrent workers (FR-25).
    Sends (worker_count * 2) prompts, minimum 6.
    """
    num_prompts = max(6, worker_count * 2)
    if verbose:
        print(f"Testing {worker_count} workers with {num_prompts} prompts...", file=sys.stderr)
    
    start_time = time.time()
    success_count = 0
    rate_limit_count = 0
    total_usage = {'input_tokens': 0, 'output_tokens': 0}
    
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        futures = [
            executor.submit(single_call, client, model, prompt, provider, min_tokens)
            for _ in range(num_prompts)
        ]
        
        for future in as_completed(futures):
            try:
                success, is_rate_limited, usage = future.result(timeout=150)
                if success:
                    success_count += 1
                    total_usage['input_tokens'] += usage.get('input_tokens', 0)
                    total_usage['output_tokens'] += usage.get('output_tokens', 0)
                if is_rate_limited:
                    rate_limit_count += 1
            except Exception as e:
                if verbose:
                    print(f"  [WARN] Future error: {e}", file=sys.stderr)
    
    duration_ms = int((time.time() - start_time) * 1000)
    status = "passed" if rate_limit_count == 0 else "rate_limited"
    
    if verbose:
        status_str = "PASSED" if rate_limit_count == 0 else f"RATE LIMITED ({rate_limit_count})"
        print(f"  -> {status_str} in {duration_ms}ms", file=sys.stderr)
    
    return {
        "workers": worker_count,
        "prompts": num_prompts,
        "success": success_count,
        "rate_limited": rate_limit_count,
        "status": status,
        "duration_ms": duration_ms,
        "usage": total_usage
    }


def find_limit(client, model: str, prompt: str, provider: str,
               max_workers: int, min_tokens: int, verbose: bool) -> dict:
    """
    Discover maximum safe worker count (FR-20, FR-22, FR-23).
    Returns TestResult dict.
    """
    tested_counts = {}
    runs = []
    current = 3
    highest_passed = 0
    
    if verbose:
        print(f"\n=== Finding worker limit for {model} ===", file=sys.stderr)
        print(f"WARNING: This test consumes API quota shared across your organization.\n", file=sys.stderr)
    
    while current <= max_workers:
        result = run_test(client, model, prompt, provider, current, min_tokens, verbose)
        runs.append(result)
        tested_counts[current] = result["status"]
        
        if result["status"] == "passed":
            highest_passed = current
        
        if result["status"] == "rate_limited":
            break
        
        if current >= max_workers:
            return {
                "recommended_workers": current,
                "max_tested": current,
                "runs": runs
            }
        
        current = next_worker_count(current, max_workers)
    
    while current > 1:
        target = scale_back_count(current)
        
        if target == current:
            break
        
        if target in tested_counts and tested_counts[target] == "passed":
            return {
                "recommended_workers": target,
                "max_tested": max(tested_counts.keys()),
                "runs": runs
            }
        
        result = run_test(client, model, prompt, provider, target, min_tokens, verbose)
        runs.append(result)
        tested_counts[target] = result["status"]
        
        if result["status"] == "passed":
            if target > highest_passed:
                highest_passed = target
            return {
                "recommended_workers": target,
                "max_tested": max(tested_counts.keys()),
                "runs": runs
            }
        
        current = target
    
    if highest_passed > 0:
        return {
            "recommended_workers": highest_passed,
            "max_tested": max(tested_counts.keys()),
            "runs": runs
        }
    
    return {
        "recommended_workers": 0,
        "max_tested": max(tested_counts.keys()) if tested_counts else 0,
        "error": "Rate limited even at 1 worker",
        "runs": runs
    }


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Discover maximum concurrent workers for LLM API calls.',
        epilog='NOTE: Results represent burst capacity, not sustained RPM.')
    
    parser.add_argument('--model', required=True, 
                        help='API model ID (e.g., gpt-4o, claude-3-5-sonnet-20241022)')
    parser.add_argument('--keys-file', type=Path, default=Path('.env'),
                        help='API keys file (default: .env)')
    parser.add_argument('--max-workers', type=int, default=100,
                        help='Maximum workers to test (default: 100)')
    parser.add_argument('--prompt-file', type=Path, default=None,
                        help='Custom prompt file (default: built-in 500-word essay prompt)')
    parser.add_argument('--output-file', type=Path, default=None,
                        help='Save results JSON to file')
    parser.add_argument('--min-output-tokens', type=int, default=500,
                        help='Minimum output tokens per prompt (default: 500)')
    parser.add_argument('--verbose', action='store_true',
                        help='Print detailed progress')
    
    return parser.parse_args()


def main():
    args = parse_args()
    
    if args.output_file:
        try:
            args.output_file.parent.mkdir(parents=True, exist_ok=True)
            args.output_file.touch()
        except (OSError, PermissionError) as e:
            print(f"Error: Cannot write to {args.output_file}: {e}", file=sys.stderr)
            sys.exit(1)
    
    keys = load_api_keys(args.keys_file)
    provider = detect_provider(args.model)
    
    if provider == 'openai':
        client = create_openai_client(keys)
    else:
        client = create_anthropic_client(keys)
    
    if args.prompt_file:
        if not args.prompt_file.exists():
            print(f"Error: Prompt file not found: {args.prompt_file}", file=sys.stderr)
            sys.exit(1)
        prompt = args.prompt_file.read_text(encoding='utf-8')
    else:
        prompt = DEFAULT_PROMPT
    
    result = find_limit(client, args.model, prompt, provider,
                        args.max_workers, args.min_output_tokens, args.verbose)
    
    result["model"] = args.model
    result["provider"] = provider
    result["timestamp"] = datetime.now(timezone.utc).isoformat()
    result["settings"] = {
        "max_workers": args.max_workers,
        "min_output_tokens": args.min_output_tokens,
        "prompt_file": str(args.prompt_file) if args.prompt_file else "built-in"
    }
    
    print(result["recommended_workers"])
    
    if args.output_file:
        args.output_file.write_text(json.dumps(result, indent=2), encoding='utf-8')
        print(f"Results saved to: {args.output_file}", file=sys.stderr)
    
    if args.verbose:
        print(f"\n=== Summary ===", file=sys.stderr)
        print(f"Model: {args.model}", file=sys.stderr)
        print(f"Recommended workers: {result['recommended_workers']}", file=sys.stderr)
        print(f"Max tested: {result.get('max_tested', 'N/A')}", file=sys.stderr)
        if "error" in result:
            print(f"Error: {result['error']}", file=sys.stderr)


if __name__ == '__main__':
    main()
