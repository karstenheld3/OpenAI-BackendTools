#!/usr/bin/env python3
"""
test-call-llm.py - Test all models with various parameter combinations.

Usage:
  python test-call-llm.py --keys-file path/to/keys.txt
  python test-call-llm.py --keys-file path/to/keys.txt --provider openai
  python test-call-llm.py --keys-file path/to/keys.txt --model gpt-5.4
"""

import sys, json, argparse, subprocess
from pathlib import Path
from datetime import datetime

# Test prompt - minimal tokens
TEST_PROMPT = "What is 2+2? Answer in one word."

# Test configurations: (model, effort_level, output_length, verbosity, expected_method)
# Only test models that are enabled and available in registry
# Keep output_length=none to minimize tokens, we just want crash detection
OPENAI_TESTS = [
  # Temperature models - basic + output-length variations
  ("gpt-4o-mini", "none", "none", None, "temperature"),
  ("gpt-4o-mini", "medium", "low", None, "temperature"),
  ("gpt-4o-mini", "high", "medium", None, "temperature"),
  ("gpt-4o", "low", "none", None, "temperature"),
  ("gpt-4.1", "medium", "none", None, "temperature"),
    
  # Reasoning models - gpt-5 family (no none support)
  ("gpt-5", "minimal", "none", None, "reasoning_effort"),
  ("gpt-5", "high", "low", None, "reasoning_effort"),
  ("gpt-5-mini", "minimal", "none", None, "reasoning_effort"),
  ("gpt-5-mini", "high", "none", None, "reasoning_effort"),
  ("gpt-5-nano", "minimal", "none", None, "reasoning_effort"),
  ("gpt-5-nano", "high", "low", None, "reasoning_effort"),
    
  # Reasoning models - gpt-5.x (supports none, no minimal) + verbosity tests
  ("gpt-5.1", "none", "none", None, "reasoning_effort"),
  ("gpt-5.1", "high", "low", None, "reasoning_effort"),
  ("gpt-5.2", "none", "none", None, "reasoning_effort"),
  ("gpt-5.2", "high", "none", None, "reasoning_effort"),
  ("gpt-5.2", "xhigh", "low", None, "reasoning_effort"),
  ("gpt-5.4", "none", "none", None, "reasoning_effort"),
  ("gpt-5.4", "none", "none", "low", "reasoning_effort"),      # verbosity test
  ("gpt-5.4", "none", "none", "medium", "reasoning_effort"),   # verbosity test
  ("gpt-5.4", "none", "none", "high", "reasoning_effort"),     # verbosity test
  ("gpt-5.4", "low", "none", None, "reasoning_effort"),
  ("gpt-5.4", "high", "low", None, "reasoning_effort"),
  ("gpt-5.4", "xhigh", "none", None, "reasoning_effort"),
    
  # Reasoning models - gpt-5.5 family
  ("gpt-5.5", "none", "none", None, "reasoning_effort"),
  ("gpt-5.5", "low", "none", None, "reasoning_effort"),
  ("gpt-5.5", "high", "none", None, "reasoning_effort"),
  ("gpt-5.5-pro", "high", "none", None, "reasoning_effort"),
]

ANTHROPIC_TESTS = [
  # Temperature models + output-length variations
  ("claude-haiku-4-5-20251001", "low", "none", None, "temperature"),
  ("claude-haiku-4-5-20251001", "medium", "low", None, "temperature"),
  ("claude-haiku-4-5-20251001", "high", "medium", None, "temperature"),
    
  # Thinking models (use low/medium to avoid streaming requirement)
  ("claude-sonnet-4-20250514", "low", "none", None, "thinking"),
  ("claude-sonnet-4-20250514", "medium", "none", None, "thinking"),
  ("claude-sonnet-4-5-20250929", "low", "none", None, "thinking"),
  ("claude-sonnet-4-5-20250929", "medium", "low", None, "thinking"),
]

# Fallback tests - verify fallback mapping works
FALLBACK_TESTS = [
  ("gpt-5-mini", "none", "none", None, "reasoning_effort"),  # none -> minimal
  ("gpt-5.4", "minimal", "none", None, "reasoning_effort"),   # minimal -> low
  ("gpt-5.2", "minimal", "none", None, "reasoning_effort"),   # minimal -> low
]

def get_script_dir() -> Path:
  return Path(__file__).parent

def create_test_prompt_file(script_dir: Path) -> Path:
  prompt_file = script_dir / "prompts" / "_test_auto.md"
  prompt_file.parent.mkdir(parents=True, exist_ok=True)
  prompt_file.write_text(TEST_PROMPT, encoding='utf-8')
  return prompt_file

def cleanup_test_prompt_file(prompt_file: Path):
  if prompt_file.exists():
    prompt_file.unlink()

def run_test(model: str, effort: str, output_len: str, verbosity: str, method: str, keys_file: Path, prompt_file: Path, script_dir: Path) -> dict:
  """Run a single test and return result."""
    
  # Build command based on method
  cmd = [
    sys.executable, str(script_dir / "call-llm.py"),
    "--model", model,
    "--prompt-file", str(prompt_file),
    "--keys-file", str(keys_file),
    "--output-length", output_len
  ]
    
  if method == "temperature":
    cmd.extend(["--temperature", effort])
  else:
    cmd.extend(["--reasoning-effort", effort])
    
  if verbosity:
    cmd.extend(["--verbosity", verbosity])
    
  try:
    result = subprocess.run(
      cmd,
      cwd=str(script_dir),
      capture_output=True,
      text=True,
      timeout=120
    )
        
    success = result.returncode == 0
    output = result.stderr + result.stdout
        
    # Extract token info if successful
    tokens_in = None
    tokens_out = None
    if success and "Tokens:" in output:
      try:
        tokens_line = [l for l in output.split('\n') if 'Tokens:' in l][0]
        parts = tokens_line.split('Tokens:')[1].strip().split()
        tokens_in = int(parts[0])
        tokens_out = int(parts[2])
      except:
        pass
        
    # Check for fallback warning
    fallback = "[WARN]" in output and "falling back" in output
        
    return {
      "success": success,
      "tokens_in": tokens_in,
      "tokens_out": tokens_out,
      "fallback": fallback,
      "error": result.stderr if not success else None
    }
  except subprocess.TimeoutExpired:
    return {"success": False, "error": "Timeout (120s)", "fallback": False}
  except Exception as e:
    return {"success": False, "error": str(e), "fallback": False}

def print_result(index: int, total: int, model: str, effort: str, output_len: str, verbosity: str, method: str, result: dict):
  """Print test result following LOG-SC rules."""
  fallback_note = " (fallback applied)" if result.get("fallback") else ""
    
  # Build descriptive params string using key='value' format (LOG-GN-06)
  if method == "temperature":
    params = f"temperature='{effort}' output_length='{output_len}'"
  else:
    params = f"reasoning_effort='{effort}' output_length='{output_len}'"
  if verbosity:
    params += f" verbosity='{verbosity}'"
    
  if result["success"]:
    tokens_in = result.get('tokens_in', '?')
    tokens_out = result.get('tokens_out', '?')
    # LOG-SC-05: OK. with details
    print(f"[ {index:2} / {total:2} ] Testing model='{model}' {params}...")
    print(f"  OK. {tokens_in} tokens in, {tokens_out} tokens out.{fallback_note}")
  else:
    error = result.get("error", "Unknown error")
    # Extract first line of error for brevity
    error_line = error.split('\n')[0][:80] if error else "Unknown error"
    print(f"[ {index:2} / {total:2} ] Testing model='{model}' {params}...")
    print(f"  FAIL: {error_line}")

def run_tests(tests: list, keys_file: Path, prompt_file: Path, script_dir: Path, provider: str) -> tuple:
  """Run all tests and return (passed, failed) counts."""
  passed = 0
  failed = 0
  total = len(tests)
    
  # LOG-SC-02: Phase header format
  print(f"\n===== {provider.upper()} TESTS ({total} tests) =====")
  print()
    
  for index, (model, effort, output_len, verbosity, method) in enumerate(tests, 1):
    result = run_test(model, effort, output_len, verbosity, method, keys_file, prompt_file, script_dir)
    print_result(index, total, model, effort, output_len, verbosity, method, result)
        
    if result["success"]:
      passed += 1
    else:
      failed += 1
    
  return passed, failed

def parse_args():
  parser = argparse.ArgumentParser(description='Test all LLM models with parameter combinations')
  parser.add_argument('--keys-file', type=Path, required=True, help='Path to API keys file')
  parser.add_argument('--provider', choices=['openai', 'anthropic', 'all'], default='all',
            help='Provider to test (default: all)')
  parser.add_argument('--model', type=str, help='Test specific model only')
  parser.add_argument('--include-fallback', action='store_true', help='Include fallback tests')
  return parser.parse_args()

def main():
  args = parse_args()
  script_dir = get_script_dir()
    
  if not args.keys_file.exists():
    print(f"ERROR: Keys file not found: '{args.keys_file}'", file=sys.stderr)
    sys.exit(1)
    
  # Create test prompt file
  prompt_file = create_test_prompt_file(script_dir)
    
  try:
    # LOG-SC-02: 100-char START header
    header = "START: LLM MODEL TEST SUITE"
    pad = (100 - len(header) - 2) // 2
    print(f"\n{'=' * pad} {header} {'=' * pad}")
    print(f"Testing API parameter combinations for crash detection.")
    print()
        
    total_passed = 0
    total_failed = 0
        
    # Filter tests if specific model requested
    openai_tests = OPENAI_TESTS
    anthropic_tests = ANTHROPIC_TESTS
    fallback_tests = FALLBACK_TESTS if args.include_fallback else []
        
    if args.model:
      openai_tests = [t for t in OPENAI_TESTS if t[0] == args.model]
      anthropic_tests = [t for t in ANTHROPIC_TESTS if t[0] == args.model]
      fallback_tests = [t for t in FALLBACK_TESTS if t[0] == args.model]
        
    # Run OpenAI tests
    if args.provider in ['openai', 'all'] and openai_tests:
      passed, failed = run_tests(openai_tests, args.keys_file, prompt_file, script_dir, "OpenAI")
      total_passed += passed
      total_failed += failed
        
    # Run Anthropic tests
    if args.provider in ['anthropic', 'all'] and anthropic_tests:
      passed, failed = run_tests(anthropic_tests, args.keys_file, prompt_file, script_dir, "Anthropic")
      total_passed += passed
      total_failed += failed
        
    # Run fallback tests
    if fallback_tests:
      passed, failed = run_tests(fallback_tests, args.keys_file, prompt_file, script_dir, "Fallback")
      total_passed += passed
      total_failed += failed
        
    # LOG-SC-07: Summary with counts and result
    total_tests = total_passed + total_failed
    print(f"\n===== TEST SUITE COMPLETE =====")
    print(f"OK: {total_passed}, FAIL: {total_failed}")
    print()
        
    # Final result line (LOG-SC-07)
    if total_failed == 0:
      result_str = "PASSED"
    else:
      result_str = "FAILED"
    print(f"RESULT: {result_str}")
        
    # LOG-SC-02: 100-char END footer
    footer = "END: LLM MODEL TEST SUITE"
    pad = (100 - len(footer) - 2) // 2
    print(f"{'=' * pad} {footer} {'=' * pad}")
        
    sys.exit(0 if total_failed == 0 else 1)
        
  finally:
    cleanup_test_prompt_file(prompt_file)

if __name__ == '__main__':
  main()
