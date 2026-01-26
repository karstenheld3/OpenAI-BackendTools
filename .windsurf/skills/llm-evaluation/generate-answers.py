#!/usr/bin/env python3
"""
generate-answers.py - Generate answers to questions from transcribed content.

Usage:
  python generate-answers.py --model gpt-4o --input-folder transcriptions/ --output-folder answers/ --questions-file questions.json
"""

import os, sys, json, time, argparse
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
        **{token_param: 2048}
    )
    return {
        "text": response.choices[0].message.content,
        "usage": {"input_tokens": response.usage.prompt_tokens, "output_tokens": response.usage.completion_tokens},
        "model": response.model
    }


def call_anthropic(client, model: str, prompt: str):
    response = client.messages.create(
        model=model,
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )
    return {
        "text": response.content[0].text,
        "usage": {"input_tokens": response.usage.input_tokens, "output_tokens": response.usage.output_tokens},
        "model": response.model
    }


DEFAULT_ANSWER_PROMPT = """Based on the provided text, answer the following question.

Rules:
- Answer ONLY using information from the provided text
- If the answer is not in the text, respond: "Cannot answer from provided text"
- Be concise - one sentence if possible

Question: {question}

Text:
{text_content}
"""


def build_answer_prompt(question: str, text_content: str, custom_prompt: str = None) -> str:
    template = custom_prompt if custom_prompt else DEFAULT_ANSWER_PROMPT
    return template.format(question=question, text_content=text_content)


def find_transcription_for_source(source_file: str, input_folder: Path) -> Path:
    """Find transcription file matching source file."""
    source_path = Path(source_file)
    source_stem = source_path.stem
    
    for f in input_folder.iterdir():
        if f.is_file() and source_stem in f.stem:
            return f
    
    return None


def process_question(worker_id: int, q_idx: int, total: int, question: dict,
                     transcriptions_mapped: dict, args, client, provider: str, 
                     results: list, lock: Lock, custom_prompt: str = None):
    source_file = question.get("source_file", "")
    q_text = question.get("question", "")
    
    transcription = transcriptions_mapped.get(source_file)
    if not transcription:
        log(worker_id, q_idx, total, f"No transcription for: {source_file}")
        return
    
    log(worker_id, q_idx, total, f"Answering: {q_text[:50]}...")
    
    try:
        prompt = build_answer_prompt(q_text, transcription, custom_prompt)
        
        if provider == 'openai':
            result = retry_with_backoff(lambda: call_openai(client, args.model, prompt))
        else:
            result = retry_with_backoff(lambda: call_anthropic(client, args.model, prompt))
        
        answer_data = {
            "question": q_text,
            "category": question.get("category", ""),
            "reference_answer": question.get("reference_answer", ""),
            "model_answer": result["text"],
            "source_file": source_file,
            "model": result["model"],
            "usage": result["usage"]
        }
        
        with lock:
            results.append(answer_data)
        
        log(worker_id, q_idx, total, f"Answered ({result['usage']['output_tokens']} tokens)")
        
    except Exception as e:
        log(worker_id, q_idx, total, f"ERROR: {e}")


def parse_args():
    parser = argparse.ArgumentParser(description='Generate answers to questions from transcribed content.')
    parser.add_argument('--model', required=True, help='API model ID')
    parser.add_argument('--input-folder', type=Path, required=True, help='Folder with transcription files')
    parser.add_argument('--output-folder', type=Path, required=True, help='Output folder for answers')
    parser.add_argument('--questions-file', type=Path, required=True, help='Questions JSON file')
    parser.add_argument('--workers', type=int, default=4, help='Parallel workers (default: 4)')
    parser.add_argument('--prompt-file', type=Path, help='Custom answering prompt file (use {question} and {text_content} placeholders)')
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
    
    if not args.questions_file.exists():
        print(f"[ERROR] Questions file not found: {args.questions_file}", file=sys.stderr)
        sys.exit(1)
    
    questions_data = json.loads(args.questions_file.read_text(encoding='utf-8'))
    questions = questions_data.get("questions", [])
    
    if not questions:
        print("[ERROR] No questions found in file", file=sys.stderr)
        sys.exit(1)
    
    transcriptions = {}
    for f in args.input_folder.iterdir():
        if f.is_file() and f.suffix.lower() in {'.txt', '.md'}:
            if f.name.startswith('_'):
                continue
            if '.meta.' in f.name:
                continue
            content = f.read_text(encoding='utf-8')
            if content.strip():
                transcriptions[f.stem] = content
    
    for q in questions:
        source = q.get("source_file", "")
        source_stem = Path(source).stem if source else ""
        for key in transcriptions:
            if source_stem in key or key in source_stem:
                q["_transcription_key"] = key
                break
    
    custom_prompt = None
    if args.prompt_file:
        if not args.prompt_file.exists():
            print(f"[ERROR] Prompt file not found: {args.prompt_file}", file=sys.stderr)
            sys.exit(1)
        custom_prompt = args.prompt_file.read_text(encoding='utf-8')
        print(f"Using custom prompt from: {args.prompt_file}", file=sys.stderr)
    
    print(f"Generating answers for {len(questions)} questions with {args.workers} workers", file=sys.stderr)
    
    if provider == 'openai':
        client = create_openai_client(keys)
    else:
        client = create_anthropic_client(keys)
    
    results = []
    lock = Lock()
    
    transcriptions_mapped = {}
    for q in questions:
        source = q.get("source_file", "")
        key = q.get("_transcription_key")
        if key and key in transcriptions:
            transcriptions_mapped[source] = transcriptions[key]
    
    print(f"Loaded {len(transcriptions)} transcription files, mapped {len(transcriptions_mapped)} to questions", file=sys.stderr)
    if transcriptions_mapped:
        for k, v in list(transcriptions_mapped.items())[:1]:
            print(f"  Mapped key: '{k}' (len={len(v)} chars)", file=sys.stderr)
    if not transcriptions_mapped and transcriptions:
        print(f"  Transcription keys: {list(transcriptions.keys())[:3]}...", file=sys.stderr)
        print(f"  Question source stems: {[Path(q.get('source_file','')).stem for q in questions[:3]]}...", file=sys.stderr)
    
    args.output_folder.mkdir(parents=True, exist_ok=True)
    
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {}
        for idx, q in enumerate(questions, 1):
            worker_id = (idx - 1) % args.workers
            future = executor.submit(process_question, worker_id, idx, len(questions), q,
                                     transcriptions_mapped, args, client, provider, results, lock, custom_prompt)
            futures[future] = q
        
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"[ERROR] {e}", file=sys.stderr)
    
    output = {
        "model": args.model,
        "total_answers": len(results),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "answers": results
    }
    
    output_file = args.output_folder / f"answers_{args.model.replace('/', '_')}.json"
    output_file.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding='utf-8')
    
    print(f"Generated {len(results)} answers -> {output_file}", file=sys.stderr)


if __name__ == '__main__':
    main()
