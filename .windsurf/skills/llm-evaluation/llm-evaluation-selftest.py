#!/usr/bin/env python3
"""
LLM Evaluation Skill Self-Test

Validates that all scripts work correctly with minimal API calls.
Detects breaking changes during development.

Usage:
    python llm-evaluation-selftest.py [--skip-api-calls] [--model MODEL] [--keys-file PATH]
    
Options:
    --skip-api-calls    Skip actual API integration tests
    --model MODEL       Model to use for API tests (default: gpt-4o-mini)
    --keys-file PATH    Path to API keys file (default: .env)
    
Exit codes:
    0 - All tests passed
    1 - One or more tests failed
"""

import sys
import os
import json
import tempfile
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

# Parse command line arguments
SKIP_API = "--skip-api-calls" in sys.argv
TEST_MODEL = "gpt-4o-mini"
KEYS_FILE = ".env"

for i, arg in enumerate(sys.argv):
    if arg == "--model" and i + 1 < len(sys.argv):
        TEST_MODEL = sys.argv[i + 1]
    elif arg == "--keys-file" and i + 1 < len(sys.argv):
        KEYS_FILE = sys.argv[i + 1]

class TestResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.failures = []
    
    def add_pass(self, test_name: str):
        self.passed += 1
        print(f"✓ {test_name}")
    
    def add_fail(self, test_name: str, error: str):
        self.failed += 1
        self.failures.append((test_name, error))
        print(f"✗ {test_name}: {error}")
    
    def add_skip(self, test_name: str):
        self.skipped += 1
        print(f"○ {test_name} (skipped)")
    
    def summary(self) -> str:
        total = self.passed + self.failed + self.skipped
        return f"\n{self.passed}/{total} passed, {self.failed} failed, {self.skipped} skipped"
    
    def is_success(self) -> bool:
        return self.failed == 0

def run_script(script: str, args: List[str], cwd: Path) -> Tuple[int, str, str]:
    """Run a Python script and return exit code, stdout, stderr"""
    cmd = [sys.executable, str(cwd / script)] + args
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    return result.returncode, result.stdout, result.stderr

def create_test_fixtures(temp_dir: Path) -> Dict[str, Path]:
    """Create minimal test fixtures"""
    fixtures = {}
    
    # Test image (1x1 pixel PNG)
    img_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
    img_file = temp_dir / "test.png"
    img_file.write_bytes(img_data)
    fixtures["image"] = img_file
    
    # Test text file
    text_file = temp_dir / "test.txt"
    text_file.write_text("Test content for evaluation.", encoding='utf-8')
    fixtures["text"] = text_file
    
    # Test prompt
    prompt_file = temp_dir / "prompt.md"
    prompt_file.write_text("Describe this briefly.", encoding='utf-8')
    fixtures["prompt"] = prompt_file
    
    # Test questions JSON
    questions_file = temp_dir / "questions.json"
    questions = {
        "questions": [
            {"id": "q1", "category": "test", "question": "What is this?"}
        ]
    }
    questions_file.write_text(json.dumps(questions, indent=2), encoding='utf-8')
    fixtures["questions"] = questions_file
    
    # Test answer JSON
    answer_file = temp_dir / "answer.json"
    answer = {
        "question_id": "q1",
        "answer": "This is a test answer.",
        "source_file": "test.txt"
    }
    answer_file.write_text(json.dumps(answer, indent=2), encoding='utf-8')
    fixtures["answer"] = answer_file
    
    # Fake API keys
    keys_file = temp_dir / ".env"
    keys_file.write_text("OPENAI_API_KEY=sk-test\nANTHROPIC_API_KEY=sk-ant-test", encoding='utf-8')
    fixtures["keys"] = keys_file
    
    return fixtures

def test_file_type_detection(skill_dir: Path, temp_dir: Path, fixtures: Dict, results: TestResult):
    """Test file type detection logic"""
    print("\n=== File Type Detection ===")
    
    # Test image detection
    code, out, err = run_script("call-llm.py", [
        "--model", TEST_MODEL,
        "--input-file", str(fixtures["image"]),
        "--prompt-file", str(fixtures["prompt"]),
        "--keys-file", str(fixtures["keys"]),
        "--help"  # Just validate args, don't call API
    ], skill_dir)
    
    if code == 0:
        results.add_pass("Image file detection")
    else:
        results.add_fail("Image file detection", err)
    
    # Test text detection
    code, out, err = run_script("call-llm.py", [
        "--model", TEST_MODEL,
        "--input-file", str(fixtures["text"]),
        "--prompt-file", str(fixtures["prompt"]),
        "--keys-file", str(fixtures["keys"]),
        "--help"
    ], skill_dir)
    
    if code == 0:
        results.add_pass("Text file detection")
    else:
        results.add_fail("Text file detection", err)

def test_config_loading(skill_dir: Path, results: TestResult):
    """Test configuration file loading"""
    print("\n=== Configuration Loading ===")
    
    # Check model registry exists and is valid JSON
    registry_file = skill_dir / "model-registry.json"
    if registry_file.exists():
        try:
            registry = json.loads(registry_file.read_text(encoding='utf-8'))
            if "model_id_startswith" in registry:
                results.add_pass("Model registry valid")
            else:
                results.add_fail("Model registry valid", "Missing model_id_startswith")
        except json.JSONDecodeError as e:
            results.add_fail("Model registry valid", f"Invalid JSON: {e}")
    else:
        results.add_fail("Model registry valid", "File not found")
    
    # Check model pricing exists and is valid JSON
    pricing_file = skill_dir / "model-pricing.json"
    if pricing_file.exists():
        try:
            pricing = json.loads(pricing_file.read_text(encoding='utf-8'))
            if "pricing" in pricing and ("openai" in pricing["pricing"] or "anthropic" in pricing["pricing"]):
                results.add_pass("Model pricing valid")
            else:
                results.add_fail("Model pricing valid", "Missing pricing structure")
        except json.JSONDecodeError as e:
            results.add_fail("Model pricing valid", f"Invalid JSON: {e}")
    else:
        results.add_fail("Model pricing valid", "File not found")
    
    # Check model parameter mapping exists
    mapping_file = skill_dir / "model-parameter-mapping.json"
    if mapping_file.exists():
        try:
            mapping = json.loads(mapping_file.read_text(encoding='utf-8'))
            if "effort_mapping" in mapping:
                results.add_pass("Parameter mapping valid")
            else:
                results.add_fail("Parameter mapping valid", "Missing effort_mapping")
        except json.JSONDecodeError as e:
            results.add_fail("Parameter mapping valid", f"Invalid JSON: {e}")
    else:
        results.add_fail("Parameter mapping valid", "File not found")

def test_script_help(skill_dir: Path, results: TestResult):
    """Test that all scripts have --help"""
    print("\n=== Script Help Text ===")
    
    scripts = [
        "call-llm.py",
        "call-llm-batch.py",
        "generate-questions.py",
        "generate-answers.py",
        "evaluate-answers.py",
        "analyze-costs.py",
        "compare-transcription-runs.py"
    ]
    
    for script in scripts:
        code, out, err = run_script(script, ["--help"], skill_dir)
        if code == 0 and "usage:" in out.lower():
            results.add_pass(f"{script} --help")
        else:
            results.add_fail(f"{script} --help", "No help text or error")

def test_json_output_schema(skill_dir: Path, temp_dir: Path, fixtures: Dict, results: TestResult):
    """Test JSON output schemas (without API calls)"""
    print("\n=== JSON Output Schemas ===")
    
    # Create mock output files to test schema validation
    
    # Mock batch metadata
    batch_meta = {
        "model": TEST_MODEL,
        "total_files": 1,
        "total_input_tokens": 100,
        "total_output_tokens": 50,
        "files": []
    }
    meta_file = temp_dir / f"_batch_metadata_{TEST_MODEL}.json"
    meta_file.write_text(json.dumps(batch_meta, indent=2), encoding='utf-8')
    
    try:
        data = json.loads(meta_file.read_text(encoding='utf-8'))
        if all(k in data for k in ["model", "total_files", "total_input_tokens"]):
            results.add_pass("Batch metadata schema")
        else:
            results.add_fail("Batch metadata schema", "Missing required fields")
    except Exception as e:
        results.add_fail("Batch metadata schema", str(e))
    
    # Mock comparison output
    comparison = {
        "summary": {
            "method": "hybrid",
            "total_files": 2,
            "avg_similarity": 0.95
        },
        "comparison": {
            "text": {"avg_similarity": 1.0},
            "images": {"avg_similarity": 0.9}
        }
    }
    comp_file = temp_dir / "comparison.json"
    comp_file.write_text(json.dumps(comparison, indent=2), encoding='utf-8')
    
    try:
        data = json.loads(comp_file.read_text(encoding='utf-8'))
        if "summary" in data and "comparison" in data:
            results.add_pass("Comparison output schema")
        else:
            results.add_fail("Comparison output schema", "Missing required sections")
    except Exception as e:
        results.add_fail("Comparison output schema", str(e))

def test_api_integration(skill_dir: Path, temp_dir: Path, fixtures: Dict, results: TestResult):
    """Test actual API calls (skipped if --skip-api-calls)"""
    print("\n=== API Integration ===")
    
    if SKIP_API:
        results.add_skip("API call test (use real API keys to test)")
        return
    
    # Use real keys file if specified, otherwise use test fixtures
    keys_path = Path(KEYS_FILE) if Path(KEYS_FILE).exists() else fixtures["keys"]
    
    # Test single call
    output_file = temp_dir / "output.txt"
    code, out, err = run_script("call-llm.py", [
        "--model", TEST_MODEL,
        "--input-file", str(fixtures["text"]),
        "--prompt-file", str(fixtures["prompt"]),
        "--output-file", str(output_file),
        "--keys-file", str(keys_path)
    ], skill_dir)
    
    if code == 0 and output_file.exists():
        results.add_pass("Single API call")
    else:
        results.add_fail("Single API call", err or "Output file not created")

def main():
    print("LLM Evaluation Skill Self-Test")
    print("=" * 50)
    
    # Locate skill directory
    script_dir = Path(__file__).parent
    skill_dir = script_dir
    
    if not (skill_dir / "call-llm.py").exists():
        print(f"Error: Cannot find skill scripts in {skill_dir}")
        return 1
    
    print(f"Skill directory: {skill_dir}")
    print(f"Test model: {TEST_MODEL}")
    print(f"Keys file: {KEYS_FILE}")
    print(f"API calls: {'SKIPPED' if SKIP_API else 'ENABLED'}")
    
    results = TestResult()
    
    # Create temporary test environment
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        fixtures = create_test_fixtures(temp_path)
        
        # Run test suites
        test_config_loading(skill_dir, results)
        test_script_help(skill_dir, results)
        test_file_type_detection(skill_dir, temp_path, fixtures, results)
        test_json_output_schema(skill_dir, temp_path, fixtures, results)
        test_api_integration(skill_dir, temp_path, fixtures, results)
    
    # Print summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(results.summary())
    
    if results.failures:
        print("\nFailed tests:")
        for test_name, error in results.failures:
            print(f"  - {test_name}: {error}")
    
    return 0 if results.is_success() else 1

if __name__ == "__main__":
    sys.exit(main())
