#!/usr/bin/env python3
"""
Exhaustive test script for all Python scripts in .windsurf/skills/.

Tests that refactoring (indentation, import, logging changes) did not break
any script's core functionality.

Usage:
  python .tmp_test_all_scripts.py [--verbose]

Exit codes:
  0 - All tests passed
  1 - One or more tests failed
"""

import sys, os, json, py_compile, subprocess, tempfile, shutil
import importlib, importlib.util
from pathlib import Path

VERBOSE = "--verbose" in sys.argv or "-v" in sys.argv
SKILLS_DIR = Path(__file__).parent
WORKSPACE = SKILLS_DIR.parent.parent
ORIGINAL_SKILLS = WORKSPACE / "DevSystemV3.5" / "skills"

ALL_SCRIPTS = [
  "coding-conventions/reindent.py",
  "llm-evaluation/call-llm.py",
  "llm-evaluation/call-llm-batch.py",
  "llm-evaluation/generate-questions.py",
  "llm-evaluation/generate-answers.py",
  "llm-evaluation/evaluate-answers.py",
  "llm-evaluation/analyze-costs.py",
  "llm-evaluation/compare-transcription-runs.py",
  "llm-evaluation/find-workers-limit.py",
  "llm-evaluation/test-call-llm.py",
  "llm-evaluation/llm-evaluation-selftest.py",
  "llm-transcription/transcribe-image-to-markdown.py",
  "llm-transcription/transcribe-audio-to-markdown.py",
  "pdf-tools/compress-pdf.py",
  "pdf-tools/convert-pdf-to-jpg.py",
  "pdf-tools/downsize-pdf-images.py",
  "llm-computer-use/llm_computer_use/cli.py",
  "llm-computer-use/llm_computer_use/core.py",
]

HELP_SCRIPTS = [
  "coding-conventions/reindent.py",
  "llm-evaluation/call-llm.py",
  "llm-evaluation/call-llm-batch.py",
  "llm-evaluation/generate-questions.py",
  "llm-evaluation/generate-answers.py",
  "llm-evaluation/evaluate-answers.py",
  "llm-evaluation/analyze-costs.py",
  "llm-evaluation/compare-transcription-runs.py",
  "llm-evaluation/find-workers-limit.py",
  "llm-evaluation/test-call-llm.py",
  "llm-transcription/transcribe-image-to-markdown.py",
  "llm-transcription/transcribe-audio-to-markdown.py",
  "pdf-tools/compress-pdf.py",
  "pdf-tools/convert-pdf-to-jpg.py",
  "pdf-tools/downsize-pdf-images.py",
]


class TestResult:
  def __init__(self):
    self.passed = 0
    self.failed = 0
    self.skipped = 0
    self.errors = []

  def ok(self, msg):
    self.passed += 1
    if VERBOSE: print(f"  OK: {msg}")

  def fail(self, msg):
    self.failed += 1
    self.errors.append(msg)
    print(f"  FAIL: {msg}")

  def skip(self, msg):
    self.skipped += 1
    if VERBOSE: print(f"  SKIP: {msg}")

  def check(self, condition, msg):
    if condition:
      self.ok(msg)
    else:
      self.fail(msg)

  def summary(self):
    total = self.passed + self.failed + self.skipped
    status = "PASS" if self.failed == 0 else "FAIL"
    print(f"\n{'=' * 60}")
    print(f"Result: {status}")
    print(f"  Passed:  {self.passed}")
    print(f"  Failed:  {self.failed}")
    print(f"  Skipped: {self.skipped}")
    print(f"  Total:   {total}")
    if self.errors:
      print(f"\nFailures:")
      for e in self.errors:
        print(f"  - {e}")
    print(f"{'=' * 60}")
    return self.failed == 0


def run_script(script_path, args, timeout=30, cwd=None):
  """Run a Python script, return (exit_code, stdout, stderr)."""
  cmd = [sys.executable, str(script_path)] + args
  try:
    r = subprocess.run(
      cmd, capture_output=True, text=True, timeout=timeout,
      cwd=cwd or str(script_path.parent)
    )
    return r.returncode, r.stdout, r.stderr
  except subprocess.TimeoutExpired:
    return -1, "", "TIMEOUT"
  except Exception as e:
    return -2, "", str(e)


def load_mod(name, filepath):
  """Import a .py file as module without running __main__."""
  spec = importlib.util.spec_from_file_location(name, filepath)
  if not spec:
    return None
  mod = importlib.util.module_from_spec(spec)
  try:
    spec.loader.exec_module(mod)
    return mod
  except (ImportError, SystemExit):
    return None


# ==============================================================
# TEST 1: py_compile
# ==============================================================
def test_1_py_compile(R):
  print("\n=== TEST 1: py_compile (syntax check) ===")
  for s in ALL_SCRIPTS:
    fp = SKILLS_DIR / s
    if not fp.exists():
      R.fail(f"File not found: {s}")
      continue
    try:
      py_compile.compile(str(fp), doraise=True)
      R.ok(f"py_compile: {s}")
    except py_compile.PyCompileError as e:
      R.fail(f"py_compile: {s} -> {e}")


# ==============================================================
# TEST 2: --help flag
# ==============================================================
def test_2_help(R):
  print("\n=== TEST 2: --help flag ===")
  for s in HELP_SCRIPTS:
    fp = SKILLS_DIR / s
    code, out, err = run_script(fp, ["--help"])
    combined = (out + err).lower()
    if code == 0 and ("usage" in combined or "options" in combined or "positional" in combined):
      R.ok(f"--help: {s}")
    else:
      R.fail(f"--help: {s} -> exit {code}, err: {err[:200]}")

  # llm-computer-use --version (package module)
  cu_dir = SKILLS_DIR / "llm-computer-use"
  try:
    r = subprocess.run(
      [sys.executable, "-m", "llm_computer_use", "--version"],
      capture_output=True, text=True, timeout=10, cwd=str(cu_dir)
    )
    if r.returncode == 0 and "llm-computer-use" in (r.stdout + r.stderr):
      R.ok("--version: llm-computer-use (package)")
    else:
      R.fail(f"--version: llm-computer-use -> exit {r.returncode}")
  except Exception as e:
    R.skip(f"llm-computer-use --version -> {e}")


# ==============================================================
# TEST 3: Config loading
# ==============================================================
def test_3_configs(R):
  print("\n=== TEST 3: Config loading (JSON) ===")
  for skill_dir in ["llm-evaluation", "llm-transcription"]:
    for name in ["model-registry.json", "model-parameter-mapping.json", "model-pricing.json"]:
      fp = SKILLS_DIR / skill_dir / name
      if not fp.exists():
        R.fail(f"Config missing: {skill_dir}/{name}")
        continue
      try:
        data = json.loads(fp.read_text(encoding='utf-8'))
        R.check(isinstance(data, dict), f"Config loads: {skill_dir}/{name}")
      except json.JSONDecodeError as e:
        R.fail(f"Config JSON error: {skill_dir}/{name} -> {e}")


# ==============================================================
# TEST 4a: reindent.py functions
# ==============================================================
def test_4a_reindent(R):
  print("\n=== TEST 4a: reindent.py functions ===")
  mod = load_mod("reindent", SKILLS_DIR / "coding-conventions" / "reindent.py")
  if not mod:
    R.skip("reindent.py: could not import")
    return

  # detect_indentation
  R.check(mod.detect_indentation("def f():\n    return\n") == 4,
       "detect_indentation(4-space) == 4")
  R.check(mod.detect_indentation("def f():\n  return\n") == 2,
       "detect_indentation(2-space) == 2")
  R.check(mod.detect_indentation("x = 1\ny = 2\n") == 4,
       "detect_indentation(flat) == 4 (default)")

  # reindent_content: 4->2
  inp = "def f():\n    if True:\n        return 1\n"
  exp = "def f():\n  if True:\n    return 1\n"
  R.check(mod.reindent_content(inp, 4, 2) == exp, "reindent 4->2")

  # reindent_content: 2->4
  inp2 = "def f():\n  if True:\n    return 1\n"
  exp2 = "def f():\n    if True:\n        return 1\n"
  R.check(mod.reindent_content(inp2, 2, 4) == exp2, "reindent 2->4")

  # no-op
  R.check(mod.reindent_content(inp2, 2, 2) == inp2, "reindent 2->2 no-op")

  # process_file on temp file
  tmp = Path(tempfile.mktemp(suffix=".py"))
  try:
    tmp.write_text("def f():\n    return 1\n", encoding='utf-8')
    changed, msg = mod.process_file(tmp, 2, dry_run=True)
    R.check(changed is True, f"process_file dry-run detects change: {msg}")
    changed2, msg2 = mod.process_file(tmp, 4, dry_run=True)
    R.check(changed2 is False, f"process_file dry-run no change for same indent: {msg2}")
  finally:
    tmp.unlink(missing_ok=True)


# ==============================================================
# TEST 4b: call-llm.py functions (config load, param build)
# ==============================================================
def test_4b_call_llm(R):
  print("\n=== TEST 4b: call-llm.py functions ===")
  eval_dir = SKILLS_DIR / "llm-evaluation"
  mod = load_mod("call_llm", eval_dir / "call-llm.py")
  if not mod:
    R.skip("call-llm.py: could not import (missing openai/anthropic?)")
    return

  # load_configs
  try:
    mapping, registry = mod.load_configs(eval_dir)
    R.check(isinstance(mapping, dict), "load_configs -> mapping dict")
    R.check(isinstance(registry, dict), "load_configs -> registry dict")
    R.check('effort_mapping' in mapping, "mapping has 'effort_mapping'")
    R.check('model_id_startswith' in registry, "registry has 'model_id_startswith'")
  except SystemExit:
    R.fail("load_configs raised SystemExit")
    return

  # get_model_config
  try:
    cfg = mod.get_model_config("gpt-4o", registry)
    R.check(isinstance(cfg, dict), "get_model_config('gpt-4o') -> dict")
  except SystemExit:
    R.fail("get_model_config('gpt-4o') -> SystemExit")
    return

  # build_api_params for temperature model
  try:
    params, method, provider = mod.build_api_params(
      "gpt-4o", mapping, registry, "medium", "medium", "medium"
    )
    R.check(isinstance(params, dict), "build_api_params -> dict")
    R.check('max_tokens' in params, "params has 'max_tokens'")
    R.check(provider in ('openai', 'anthropic'), f"provider valid: {provider}")
  except Exception as e:
    R.fail(f"build_api_params error: {e}")

  # detect_provider
  R.check(mod.detect_provider("gpt-4o") == "openai", "detect_provider('gpt-4o') == 'openai'")
  R.check(mod.detect_provider("claude-3-5-sonnet") == "anthropic",
       "detect_provider('claude-...') == 'anthropic'")

  # load_api_keys with fake file
  tmp = Path(tempfile.mktemp(suffix=".env"))
  try:
    tmp.write_text("OPENAI_API_KEY=sk-test123\nANTHROPIC_API_KEY=sk-ant-test\n", encoding='utf-8')
    keys = mod.load_api_keys(tmp)
    R.check(keys.get('OPENAI_API_KEY') == 'sk-test123', "load_api_keys reads OPENAI key")
    R.check(keys.get('ANTHROPIC_API_KEY') == 'sk-ant-test', "load_api_keys reads ANTHROPIC key")
  finally:
    tmp.unlink(missing_ok=True)

  # load_api_keys with missing file -> should exit
  missing = Path(tempfile.mktemp(suffix=".env"))
  missing.unlink(missing_ok=True)
  try:
    mod.load_api_keys(missing)
    R.fail("load_api_keys(missing) should SystemExit")
  except SystemExit:
    R.ok("load_api_keys(missing) -> SystemExit as expected")


# ==============================================================
# TEST 4c: call-llm-batch.py functions
# ==============================================================
def test_4c_call_llm_batch(R):
  print("\n=== TEST 4c: call-llm-batch.py functions ===")
  eval_dir = SKILLS_DIR / "llm-evaluation"
  mod = load_mod("call_llm_batch", eval_dir / "call-llm-batch.py")
  if not mod:
    R.skip("call-llm-batch.py: could not import")
    return

  # load_configs
  try:
    mapping, registry = mod.load_configs(eval_dir)
    R.check('effort_mapping' in mapping, "batch: mapping has 'effort_mapping'")
  except SystemExit:
    R.fail("batch: load_configs -> SystemExit")
    return

  # build_api_params for reasoning model
  try:
    params, method, provider = mod.build_api_params(
      "o3-mini", mapping, registry, "medium", "medium", "medium"
    )
    R.check(isinstance(params, dict), "batch: build_api_params('o3-mini') -> dict")
    R.check(method in ('temperature', 'reasoning_effort', 'thinking', 'effort'),
         f"batch: method valid: {method}")
  except Exception as e:
    R.fail(f"batch: build_api_params error: {e}")

  # detect_file_type
  R.check(mod.detect_file_type(Path("photo.jpg")) == "image",
       "detect_file_type('.jpg') == 'image'")
  R.check(mod.detect_file_type(Path("doc.md")) == "text",
       "detect_file_type('.md') == 'text'")
  R.check(mod.detect_file_type(Path("file.xyz")) is None,
       "detect_file_type('.xyz') == None")


# ==============================================================
# TEST 4d: transcribe-image-to-markdown.py functions
# ==============================================================
def test_4d_transcribe_image(R):
  print("\n=== TEST 4d: transcribe-image-to-markdown.py functions ===")
  trans_dir = SKILLS_DIR / "llm-transcription"
  mod = load_mod("transcribe_img", trans_dir / "transcribe-image-to-markdown.py")
  if not mod:
    R.skip("transcribe-image-to-markdown.py: could not import")
    return

  # load_configs
  try:
    registry, mapping, pricing = mod.load_configs(trans_dir)
    R.check(isinstance(registry, dict), "trans: registry dict")
    R.check(isinstance(mapping, dict), "trans: mapping dict")
  except SystemExit:
    R.fail("trans: load_configs -> SystemExit")
    return

  # get_model_config
  try:
    cfg = mod.get_model_config("gpt-5-mini", registry)
    R.check(isinstance(cfg, dict), "trans: get_model_config('gpt-5-mini')")
  except SystemExit:
    R.fail("trans: get_model_config -> SystemExit")

  # encode_image_to_base64
  tmp = Path(tempfile.mktemp(suffix=".png"))
  try:
    tmp.write_bytes(b'\x89PNG\r\n\x1a\n' + b'\x00' * 16)
    b64 = mod.encode_image_to_base64(tmp)
    R.check(isinstance(b64, str) and len(b64) > 0, "encode_image_to_base64 -> non-empty string")
  finally:
    tmp.unlink(missing_ok=True)

  # get_image_media_type
  R.check(mod.get_image_media_type(Path("f.jpg")) == "image/jpeg", "media_type('.jpg')")
  R.check(mod.get_image_media_type(Path("f.png")) == "image/png", "media_type('.png')")
  R.check(mod.get_image_media_type(Path("f.webp")) == "image/webp", "media_type('.webp')")

  # detect_provider
  R.check(mod.detect_provider("gpt-4o") == "openai", "trans: detect_provider('gpt-4o')")
  R.check(mod.detect_provider("claude-3") == "anthropic", "trans: detect_provider('claude-3')")


# ==============================================================
# TEST 5: Error handling (missing files produce ERROR: messages)
# ==============================================================
def test_5_error_messages(R):
  print("\n=== TEST 5: Error messages for missing files ===")

  # call-llm.py with missing keys file
  fp = SKILLS_DIR / "llm-evaluation" / "call-llm.py"
  code, out, err = run_script(fp, [
    "--model", "gpt-4o",
    "--prompt-file", "nonexistent_prompt.md",
    "--keys-file", "nonexistent_keys.env"
  ])
  R.check(code != 0, "call-llm.py exits non-zero for missing keys")
  R.check("ERROR:" in err, f"call-llm.py stderr has 'ERROR:' for missing keys")

  # reindent.py with missing path
  fp = SKILLS_DIR / "coding-conventions" / "reindent.py"
  code, out, err = run_script(fp, ["nonexistent_folder"])
  R.check(code != 0, "reindent.py exits non-zero for missing path")
  R.check("ERROR:" in err, "reindent.py stderr has 'ERROR:' for missing path")

  # compress-pdf.py with missing input
  fp = SKILLS_DIR / "pdf-tools" / "compress-pdf.py"
  code, out, err = run_script(fp, ["nonexistent.pdf"])
  # compress-pdf may handle missing file internally (print ERROR but exit 0)
  R.check("ERROR:" in (out + err) or code != 0,
       "compress-pdf.py reports error for missing input")

  # analyze-costs.py with missing folder
  fp = SKILLS_DIR / "llm-evaluation" / "analyze-costs.py"
  code, out, err = run_script(fp, [
    "--input-folder", "nonexistent_folder",
    "--output-file", "out.json"
  ])
  R.check(code != 0, "analyze-costs.py exits non-zero for missing folder")
  R.check("ERROR:" in err, "analyze-costs.py stderr has 'ERROR:'")


# ==============================================================
# TEST 6: Compare with DevSystemV3.5 originals
# ==============================================================
def test_6_compare_originals(R):
  print("\n=== TEST 6: Compare key functions with DevSystemV3.5 ===")

  if not ORIGINAL_SKILLS.exists():
    R.skip(f"DevSystemV3.5/skills not found at {ORIGINAL_SKILLS}")
    return

  # Compare function signatures and key logic by loading both versions
  pairs = [
    ("call_llm_orig", "llm-evaluation/call-llm.py", "build_api_params"),
    ("call_llm_batch_orig", "llm-evaluation/call-llm-batch.py", "build_api_params"),
    ("reindent_orig", "coding-conventions/reindent.py", "detect_indentation"),
  ]

  for mod_name, rel_path, func_name in pairs:
    orig_path = ORIGINAL_SKILLS / rel_path
    new_path = SKILLS_DIR / rel_path
    if not orig_path.exists():
      R.skip(f"Original not found: {rel_path}")
      continue

    orig_mod = load_mod(mod_name, orig_path)
    new_mod = load_mod(mod_name + "_new", new_path)

    if not orig_mod:
      R.skip(f"Could not load original: {rel_path}")
      continue
    if not new_mod:
      R.skip(f"Could not load modified: {rel_path}")
      continue

    orig_fn = getattr(orig_mod, func_name, None)
    new_fn = getattr(new_mod, func_name, None)

    if not orig_fn or not new_fn:
      R.fail(f"Function '{func_name}' missing in {rel_path}")
      continue

    # Compare function signatures (parameter names)
    import inspect
    orig_sig = inspect.signature(orig_fn)
    new_sig = inspect.signature(new_fn)
    R.check(
      list(orig_sig.parameters.keys()) == list(new_sig.parameters.keys()),
      f"{rel_path}:{func_name} signature matches original"
    )

  # Compare build_api_params output for same inputs
  eval_dir = SKILLS_DIR / "llm-evaluation"
  orig_mod = load_mod("call_llm_cmp_orig", ORIGINAL_SKILLS / "llm-evaluation" / "call-llm.py")
  new_mod = load_mod("call_llm_cmp_new", eval_dir / "call-llm.py")

  if orig_mod and new_mod:
    try:
      orig_map, orig_reg = orig_mod.load_configs(ORIGINAL_SKILLS / "llm-evaluation")
      new_map, new_reg = new_mod.load_configs(eval_dir)

      for model in ["gpt-4o", "o3-mini", "claude-3-5-sonnet"]:
        try:
          orig_result = orig_mod.build_api_params(model, orig_map, orig_reg, "medium", "medium", "medium")
          new_result = new_mod.build_api_params(model, new_map, new_reg, "medium", "medium", "medium")
          R.check(orig_result == new_result,
               f"build_api_params('{model}') output matches original")
        except SystemExit:
          R.skip(f"build_api_params('{model}') -> SystemExit (model not in registry?)")
    except SystemExit:
      R.skip("Config loading failed for comparison")
  else:
    R.skip("Could not load both versions for build_api_params comparison")


# ==============================================================
# TEST 7: Indentation consistency (all files use 2-space)
# ==============================================================
def test_7_indentation(R):
  print("\n=== TEST 7: 2-space indentation check ===")
  for s in ALL_SCRIPTS:
    fp = SKILLS_DIR / s
    if not fp.exists():
      continue
    text = fp.read_text(encoding='utf-8')
    has_4space = False
    for i, line in enumerate(text.splitlines(), 1):
      stripped = line.lstrip(' ')
      if not stripped or stripped.startswith('#') or stripped.startswith('"""') or stripped.startswith("'''"):
        continue
      leading = len(line) - len(stripped)
      if leading > 0 and leading % 4 == 0 and leading % 2 == 0:
        # Could be 2-space or 4-space; check if there are any lines with exactly 2-space indent
        pass
      if leading == 4:
        # Check if this is 2x2 or 1x4
        # Heuristic: if ANY line has leading=2, it's 2-space indented
        pass

    # Simpler approach: use reindent's detect_indentation
    mod = load_mod("reindent_check", SKILLS_DIR / "coding-conventions" / "reindent.py")
    if mod:
      detected = mod.detect_indentation(text)
      R.check(detected == 2, f"Indentation {s}: detected={detected}, expected=2")
    else:
      R.skip(f"Indentation {s}: could not load reindent module")


# ==============================================================
# TEST 8: No broken backreferences remain
# ==============================================================
def test_8_no_backrefs(R):
  print("\n=== TEST 8: No broken backreferences ===")
  patterns = ['{\\2}', '{\\3}', '{\\1}']
  for s in ALL_SCRIPTS:
    fp = SKILLS_DIR / s
    if not fp.exists():
      continue
    text = fp.read_text(encoding='utf-8')
    found = []
    for pat in patterns:
      if pat in text:
        found.append(pat)
    if found:
      R.fail(f"Broken backrefs in {s}: {found}")
    else:
      R.ok(f"No backrefs: {s}")


# ==============================================================
# TEST 9: Logging format compliance
# ==============================================================
def test_9_logging_format(R):
  print("\n=== TEST 9: Logging format (ERROR: not [ERROR]) ===")
  for s in ALL_SCRIPTS:
    fp = SKILLS_DIR / s
    if not fp.exists():
      continue
    text = fp.read_text(encoding='utf-8')
    lines = text.splitlines()
    bad_lines = []
    for i, line in enumerate(lines, 1):
      stripped = line.strip()
      if '[ERROR]' in stripped and 'print(' in stripped:
        bad_lines.append(i)
    if bad_lines:
      R.fail(f"[ERROR] format in {s} at lines: {bad_lines}")
    else:
      R.ok(f"Logging format: {s}")


# ==============================================================
# MAIN
# ==============================================================
def main():
  print("=" * 60)
  print("Skills Script Test Suite")
  print(f"Skills dir: {SKILLS_DIR}")
  print(f"Original:   {ORIGINAL_SKILLS}")
  print(f"Python:     {sys.executable}")
  print("=" * 60)

  R = TestResult()

  test_1_py_compile(R)
  test_2_help(R)
  test_3_configs(R)
  test_4a_reindent(R)
  test_4b_call_llm(R)
  test_4c_call_llm_batch(R)
  test_4d_transcribe_image(R)
  test_5_error_messages(R)
  test_6_compare_originals(R)
  test_7_indentation(R)
  test_8_no_backrefs(R)
  test_9_logging_format(R)

  success = R.summary()
  sys.exit(0 if success else 1)

if __name__ == '__main__':
  main()
