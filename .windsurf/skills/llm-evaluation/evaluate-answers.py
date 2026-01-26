#!/usr/bin/env python3
"""
evaluate-answers.py - Evaluate answers using LLM-as-judge scoring (0-5).

Usage:
  python evaluate-answers.py --model gpt-4o --input-folder answers/ --output-folder scores/
"""

import os, sys, json, time, argparse, math
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

UNKNOWN = '[UNKNOWN]'


def load_api_keys(keys_file: Path) -> dict:
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
    model_lower = model_id.lower()
    if model_lower.startswith(('gpt-', 'o1-', 'o3-')):
        return 'openai'
    if model_lower.startswith('claude'):
        return 'anthropic'
    print(f"[ERROR] Cannot detect provider for model: {model_id}", file=sys.stderr)
    sys.exit(1)


def retry_with_backoff(fn, retries=3, backoff=(1, 2, 4)):
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


def log(worker_id: int, current: int, total: int, msg: str):
    print(f"[ worker {worker_id + 1} ] [ {current} / {total} ] {msg}", file=sys.stderr)


def atomic_write_json(path: Path, data: dict, lock: Lock):
    tmp_path = path.with_suffix('.tmp')
    with lock:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        tmp_path.rename(path)


def create_openai_client(keys: dict):
    from openai import OpenAI
    api_key = keys.get('OPENAI_API_KEY')
    if not api_key:
        print("[ERROR] OPENAI_API_KEY not found", file=sys.stderr)
        sys.exit(1)
    return OpenAI(api_key=api_key)


def create_anthropic_client(keys: dict):
    from anthropic import Anthropic
    api_key = keys.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("[ERROR] ANTHROPIC_API_KEY not found", file=sys.stderr)
        sys.exit(1)
    return Anthropic(api_key=api_key)


def call_openai(client, model: str, prompt: str):
    # Use max_completion_tokens for newer models (gpt-5, o1, o3), max_tokens for older
    token_param = "max_completion_tokens" if any(x in model for x in ['gpt-5', 'o1-', 'o3-']) else "max_tokens"
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        **{token_param: 1024}
    )
    return {
        "text": response.choices[0].message.content,
        "usage": {"input_tokens": response.usage.prompt_tokens, "output_tokens": response.usage.completion_tokens},
        "model": response.model
    }


def call_anthropic(client, model: str, prompt: str):
    response = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return {
        "text": response.content[0].text,
        "usage": {"input_tokens": response.usage.input_tokens, "output_tokens": response.usage.output_tokens},
        "model": response.model
    }


DEFAULT_JUDGE_PROMPT = """You are an evaluation judge. Score how well the model answer matches the reference answer.

Scoring criteria (0-5):
- 5: Perfect match - contains all key information, no errors
- 4: Good - minor omissions or phrasing differences, core facts correct
- 3: Acceptable - some key information present, some missing
- 2: Poor - significant errors or omissions, partially correct
- 1: Very poor - mostly incorrect or irrelevant
- 0: Wrong - completely incorrect or no relevant content

Question: {question}
Reference Answer: {reference_answer}
Model Answer: {model_answer}

Respond with ONLY a JSON object:
```json
{{"score": <0-5>, "rationale": "<brief explanation>"}}
```
"""


def build_judge_prompt(question: str, reference_answer: str, model_answer: str, custom_prompt: str = None) -> str:
    template = custom_prompt or DEFAULT_JUDGE_PROMPT
    return template.format(
        question=question,
        reference_answer=reference_answer,
        model_answer=model_answer
    )


def extract_json_from_response(text: str) -> dict:
    """Extract JSON object from response."""
    text = text.strip()
    if text.startswith('```'):
        lines = text.split('\n')
        start = 1 if lines[0].startswith('```') else 0
        end = len(lines)
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].strip() == '```':
                end = i
                break
        text = '\n'.join(lines[start:end])
    
    return json.loads(text)


def process_answer(worker_id: int, a_idx: int, total: int, answer: dict,
                   args, client, provider: str, results: list, lock: Lock, judge_prompt_text: str = None):
    question = answer.get("question", "")
    reference = answer.get("reference_answer", "")
    model_answer = answer.get("model_answer", "")
    
    log(worker_id, a_idx, total, f"Evaluating: {question[:50]}...")
    
    try:
        prompt = build_judge_prompt(question, reference, model_answer, judge_prompt_text)
        
        if provider == 'openai':
            result = retry_with_backoff(lambda: call_openai(client, args.model, prompt))
        else:
            result = retry_with_backoff(lambda: call_anthropic(client, args.model, prompt))
        
        evaluation = extract_json_from_response(result["text"])
        score = evaluation.get("score", 0)
        rationale = evaluation.get("rationale", "")
        
        score_data = {
            "question": question,
            "category": answer.get("category", ""),
            "reference_answer": reference,
            "model_answer": model_answer,
            "score": score,
            "rationale": rationale,
            "passed": score >= args.pass_threshold,
            "judge_model": result["model"],
            "source_file": answer.get("source_file", ""),
            "answer_model": answer.get("model", "")
        }
        
        with lock:
            results.append(score_data)
        
        status = "PASS" if score >= args.pass_threshold else "FAIL"
        log(worker_id, a_idx, total, f"Score: {score}/5 [{status}]")
        
    except Exception as e:
        log(worker_id, a_idx, total, f"ERROR: {e}")


OPENAI_EVAL_PROMPT_TEMPLATE = """You are an expert evaluator for a QA system.
Compare the generated model output ('model_output' tag) to the reference answer ('reference' tag).
If you have the question ('input' tag), also consider the input when comparing the model output to the reference answer.
Assign an **integer score from 0 to 5** where:
- Score 0 = completely unrelated and incorrect
- Score 1 = related but completely incorrect
- Score 2 = mostly incorrect
- Score 3 = partially correct
- Score 4 = mostly correct
- Score 5 = completely correct

Also explain your reasoning. Return exactly:
```json
{
  "score": <0-5>,
  "rationale": [ "<reasoning>" ]
}
```

<input>
{{ item.input }}
</input>

<reference>
{{ item.reference }}
</reference>

<model_output>
{{ item.output_text }}
</model_output>
"""


def score_answers_using_openai_eval(client, all_answers: list, eval_model: str, pass_threshold: int, judge_prompt: str = None):
    """Score answers using OpenAI Eval API with score_model grader."""
    import copy
    
    eval_name = f"llm_eval_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    prompt_template = judge_prompt or OPENAI_EVAL_PROMPT_TEMPLATE
    
    # Convert answers to eval items format
    items = []
    for idx, answer in enumerate(all_answers):
        items.append({
            "item": {
                "index": idx,
                "input": answer.get("question", ""),
                "reference": answer.get("reference_answer", ""),
                "output_text": answer.get("model_answer", ""),
                "category": answer.get("category", ""),
                "source_file": answer.get("source_file", ""),
                "answer_model": answer.get("model", "")
            }
        })
    
    print(f"Creating OpenAI Eval with {len(items)} items...", file=sys.stderr)
    
    # Build testing criteria for score_model grader
    testing_criteria_item = {
        "type": "score_model",
        "name": "Answer Quality Score",
        "model": eval_model,
        "input": [{"role": "system", "content": prompt_template}],
        "range": [0, 5],
        "pass_threshold": pass_threshold
    }
    
    # Remove temperature for reasoning models (o1, o3, gpt-5)
    if not (eval_model.startswith('o') or 'gpt-5' in eval_model):
        testing_criteria_item["sampling_params"] = {"temperature": 0}
    
    # Create evaluation configuration
    eval_cfg = client.evals.create(
        name=eval_name,
        data_source_config={
            "type": "custom",
            "item_schema": {
                "type": "object",
                "properties": {
                    "input": {"type": "string"},
                    "reference": {"type": "string"},
                    "output_text": {"type": "string"},
                    "index": {"type": "integer"},
                    "category": {"type": "string"},
                    "source_file": {"type": "string"},
                    "answer_model": {"type": "string"}
                },
                "required": ["input", "reference", "output_text"]
            },
            "include_sample_schema": False
        },
        testing_criteria=[testing_criteria_item]
    )
    print(f"  Created eval config: {eval_cfg.id}", file=sys.stderr)
    
    # Create and run evaluation
    eval_run = client.evals.runs.create(
        name=f"{eval_name}_run",
        eval_id=eval_cfg.id,
        data_source={
            "type": "jsonl",
            "source": {"type": "file_content", "content": items}
        }
    )
    print(f"  Created eval run: {eval_run.id}", file=sys.stderr)
    print(f"  View results at: {eval_run.report_url}", file=sys.stderr)
    
    # Poll for completion
    sleep_time = 10
    max_attempts = math.ceil((10 * len(items)) / sleep_time) + 5
    attempts = 0
    
    while attempts < max_attempts:
        try:
            status = client.evals.runs.retrieve(eval_run.id, eval_id=eval_cfg.id).status
        except Exception as e:
            print(f"  Polling error: {e}", file=sys.stderr)
            status = "unknown"
        
        if status == "completed":
            print("  Evaluation completed.", file=sys.stderr)
            break
        elif status == "failed":
            print("  [ERROR] Evaluation failed.", file=sys.stderr)
            return [], "FAIL"
        else:
            attempts += 1
            print(f"  [ {attempts} / {max_attempts} ] Waiting {sleep_time}s for completion (status: {status})...", file=sys.stderr)
            time.sleep(sleep_time)
    
    if attempts >= max_attempts:
        print(f"  [ERROR] Evaluation timed out after {max_attempts} attempts", file=sys.stderr)
        return [], "TIMEOUT"
    
    # Get all output items with pagination
    output_items = []
    after = None
    while True:
        if after:
            page = client.evals.runs.output_items.list(run_id=eval_run.id, eval_id=eval_cfg.id, after=after, limit=100)
        else:
            page = client.evals.runs.output_items.list(run_id=eval_run.id, eval_id=eval_cfg.id, limit=100)
        output_items.extend(page.data)
        if not page.has_more:
            break
        after = page.data[-1].id
    
    print(f"  Retrieved {len(output_items)} output items", file=sys.stderr)
    
    # Extract scores from output items
    results = []
    for output_item in output_items:
        try:
            ds_item = output_item.datasource_item
            item_index = ds_item.get("index", -1)
            
            # Get score from results
            score = 0
            rationale = ""
            if output_item.results and len(output_item.results) > 0:
                result = output_item.results[0]
                score = getattr(result, 'score', 0) or 0
                rationale = getattr(result, 'rationale', '') or ''
            
            # Find original answer data
            original = all_answers[item_index] if 0 <= item_index < len(all_answers) else {}
            
            score_data = {
                "question": ds_item.get("input", ""),
                "category": ds_item.get("category", ""),
                "reference_answer": ds_item.get("reference", ""),
                "model_answer": ds_item.get("output_text", ""),
                "score": score,
                "rationale": rationale,
                "passed": score >= pass_threshold,
                "judge_model": eval_model,
                "source_file": ds_item.get("source_file", ""),
                "answer_model": ds_item.get("answer_model", "")
            }
            results.append(score_data)
            
        except Exception as e:
            print(f"  [WARN] Error processing output item: {e}", file=sys.stderr)
    
    # Cleanup: delete the eval config (optional, comment out to keep for debugging)
    try:
        client.evals.delete(eval_cfg.id)
        print(f"  Cleaned up eval config: {eval_cfg.id}", file=sys.stderr)
    except Exception as e:
        print(f"  [WARN] Could not cleanup eval: {e}", file=sys.stderr)
    
    return results, "OK"


def parse_args():
    parser = argparse.ArgumentParser(description='Evaluate answers using LLM-as-judge scoring.')
    parser.add_argument('--model', required=True, help='Judge model ID')
    parser.add_argument('--input-folder', type=Path, required=True, help='Folder with answer JSON files')
    parser.add_argument('--output-folder', type=Path, required=True, help='Output folder for scores')
    parser.add_argument('--method', choices=['llm', 'openai-eval'], default='llm', 
                        help='Evaluation method: llm (LLM-as-judge) or openai-eval (OpenAI Eval API)')
    parser.add_argument('--judge-prompt', type=Path, help='Custom judge prompt file (.md, use {question}, {reference_answer}, {model_answer})')
    parser.add_argument('--pass-threshold', type=int, default=4, help='Pass threshold score (default: 4)')
    parser.add_argument('--workers', type=int, default=4, help='Parallel workers (default: 4)')
    parser.add_argument('--keys-file', type=Path, default=Path('.env'), help='API keys file')
    parser.add_argument('--clear-folder', action='store_true', help='Clear output folder before processing')
    return parser.parse_args()


def main():
    args = parse_args()
    
    if args.clear_folder and args.output_folder.exists():
        import shutil
        shutil.rmtree(args.output_folder)
        print(f"Cleared output folder: {args.output_folder}", file=sys.stderr)
    
    args.output_folder.mkdir(parents=True, exist_ok=True)
    
    keys = load_api_keys(args.keys_file)
    provider = detect_provider(args.model)
    
    if not args.input_folder.exists():
        print(f"[ERROR] Input folder not found: {args.input_folder}", file=sys.stderr)
        sys.exit(1)
    
    judge_prompt_text = None
    if args.judge_prompt:
        if not args.judge_prompt.exists():
            print(f"[ERROR] Judge prompt file not found: {args.judge_prompt}", file=sys.stderr)
            sys.exit(1)
        judge_prompt_text = args.judge_prompt.read_text(encoding='utf-8')
        print(f"Using custom judge prompt from: {args.judge_prompt}", file=sys.stderr)
    
    all_answers = []
    for f in args.input_folder.iterdir():
        if f.is_file() and f.suffix.lower() == '.json':
            try:
                data = json.loads(f.read_text(encoding='utf-8'))
                answers = data.get("answers", [])
                all_answers.extend(answers)
            except Exception as e:
                print(f"[WARN] Could not load {f}: {e}", file=sys.stderr)
    
    if not all_answers:
        print("[ERROR] No answers found in input folder", file=sys.stderr)
        sys.exit(1)
    
    print(f"Evaluating {len(all_answers)} answers", file=sys.stderr)
    print(f"Method: {args.method}, Judge model: {args.model}, Pass threshold: {args.pass_threshold}", file=sys.stderr)
    
    # OpenAI Eval API method (requires OpenAI provider, fallback to LLM for others)
    if args.method == 'openai-eval':
        if provider != 'openai':
            print(f"[WARN] OpenAI Eval API not available for {provider} models. Falling back to --method llm", file=sys.stderr)
            args.method = 'llm'
    
    if args.method == 'openai-eval':
        client = create_openai_client(keys)
        results, status = score_answers_using_openai_eval(
            client, all_answers, args.model, args.pass_threshold, judge_prompt_text
        )
        
        if status != "OK":
            print(f"[ERROR] OpenAI Eval failed with status: {status}", file=sys.stderr)
            sys.exit(1)
    
    # LLM-as-judge method (default or fallback)
    else:
        if provider == 'openai':
            client = create_openai_client(keys)
        else:
            client = create_anthropic_client(keys)
        
        results = []
        lock = Lock()
        
        print(f"Using {args.workers} workers", file=sys.stderr)
        
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = {}
            for idx, answer in enumerate(all_answers, 1):
                worker_id = (idx - 1) % args.workers
                future = executor.submit(process_answer, worker_id, idx, len(all_answers), answer,
                                         args, client, provider, results, lock, judge_prompt_text)
                futures[future] = answer
            
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"[ERROR] {e}", file=sys.stderr)
    
    passed = sum(1 for r in results if r.get("passed"))
    failed = len(results) - passed
    avg_score = sum(r.get("score", 0) for r in results) / len(results) if results else 0
    
    output = {
        "judge_model": args.model,
        "pass_threshold": args.pass_threshold,
        "total_evaluated": len(results),
        "passed": passed,
        "failed": failed,
        "pass_rate": round(passed / len(results) * 100, 1) if results else 0,
        "average_score": round(avg_score, 2),
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
        "scores": results
    }
    
    output_file = args.output_folder / f"scores_{args.model.replace('/', '_')}.json"
    output_file.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding='utf-8')
    
    print(f"\nResults: {passed}/{len(results)} passed ({output['pass_rate']}%), avg score: {avg_score:.2f}", file=sys.stderr)
    print(f"Output: {output_file}", file=sys.stderr)


if __name__ == '__main__':
    main()
