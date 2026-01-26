#!/usr/bin/env python3
"""
generate-questions.py - Generate evaluation questions from source content.

Usage:
  python generate-questions.py --model gpt-4o --input-folder images/ --output-file questions.json
"""

import os, sys, json, time, base64, argparse
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

UNKNOWN = '[UNKNOWN]'

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
TEXT_EXTENSIONS = {'.txt', '.md', '.json', '.py', '.html', '.xml', '.csv'}

DEFAULT_SCHEMA = {
    "categories": [
        {"name": "easy", "count": 2, "description": "Simple facts - single numbers, names, titles, dates"},
        {"name": "medium_facts", "count": 2, "description": "Combined facts requiring synthesis of 2-3 pieces"},
        {"name": "medium_inference", "count": 2, "description": "Questions requiring simple logical inference"},
        {"name": "hard_reasoning", "count": 2, "description": "Questions requiring multi-step reasoning or analysis"},
        {"name": "hard_details", "count": 2, "description": "Questions about specific details requiring careful reading"}
    ]
}


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


def detect_file_type(file_path: Path) -> str:
    suffix = file_path.suffix.lower()
    if suffix in IMAGE_EXTENSIONS:
        return 'image'
    if suffix in TEXT_EXTENSIONS:
        return 'text'
    return None


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


def encode_image_to_base64(file_path: Path) -> str:
    with open(file_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


def get_image_media_type(file_path: Path) -> str:
    suffix = file_path.suffix.lower()
    return {'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'png': 'image/png', 
            'gif': 'image/gif', 'webp': 'image/webp'}.get(suffix.lstrip('.'), 'image/jpeg')


def log(worker_id: int, current: int, total: int, msg: str):
    print(f"[ worker {worker_id + 1} ] [ {current} / {total} ] {msg}", file=sys.stderr)


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


def build_question_prompt(schema: dict) -> str:
    categories = schema.get("categories", DEFAULT_SCHEMA["categories"])
    
    prompt = """Generate evaluation questions based on the provided content.

For each question, provide:
- question: The question text
- category: One of the specified categories
- reference_answer: The correct answer based on the content
- answerable: true if answerable from the content, false otherwise

Categories and counts:
"""
    for cat in categories:
        prompt += f"- {cat['name']}: {cat['count']} questions ({cat['description']})\n"
    
    prompt += """
Output ONLY a JSON array of question objects:
```json
[
  {"question": "...", "category": "easy", "reference_answer": "...", "answerable": true},
  ...
]
```
"""
    return prompt


def call_openai(client, model: str, prompt: str, image_data: str = None, image_media_type: str = None):
    if image_data:
        content = [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:{image_media_type};base64,{image_data}"}}
        ]
    else:
        content = prompt
    
    # Use max_completion_tokens for newer models (gpt-5, o1, o3), max_tokens for older
    token_param = "max_completion_tokens" if any(x in model for x in ['gpt-5', 'o1-', 'o3-']) else "max_tokens"
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": content}],
        **{token_param: 4096}
    )
    
    return {
        "text": response.choices[0].message.content,
        "usage": {"input_tokens": response.usage.prompt_tokens, "output_tokens": response.usage.completion_tokens},
        "model": response.model
    }


def call_anthropic(client, model: str, prompt: str, image_data: str = None, image_media_type: str = None):
    content = []
    if image_data:
        content.append({"type": "image", "source": {"type": "base64", "media_type": image_media_type, "data": image_data}})
    content.append({"type": "text", "text": prompt})
    
    response = client.messages.create(model=model, max_tokens=4096, messages=[{"role": "user", "content": content}])
    
    return {
        "text": response.content[0].text,
        "usage": {"input_tokens": response.usage.input_tokens, "output_tokens": response.usage.output_tokens},
        "model": response.model
    }


def extract_json_from_response(text: str) -> list:
    """Extract JSON array from response, handling markdown fences."""
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


def process_file(worker_id: int, file_idx: int, total: int, input_file: Path,
                 args, client, provider: str, prompt: str, results: list, lock: Lock):
    file_type = detect_file_type(input_file)
    if not file_type:
        log(worker_id, file_idx, total, f"Skipping unknown type: {input_file.name}")
        return
    
    log(worker_id, file_idx, total, f"Processing: {input_file.name}")
    
    try:
        image_data = None
        image_media_type = None
        file_prompt = prompt
        
        if file_type == 'image':
            image_data = retry_with_backoff(lambda: encode_image_to_base64(input_file))
            image_media_type = get_image_media_type(input_file)
        else:
            text_content = input_file.read_text(encoding='utf-8')
            file_prompt = f"{prompt}\n\nContent:\n{text_content}"
        
        if provider == 'openai':
            result = retry_with_backoff(lambda: call_openai(client, args.model, file_prompt, image_data, image_media_type))
        else:
            result = retry_with_backoff(lambda: call_anthropic(client, args.model, file_prompt, image_data, image_media_type))
        
        questions = extract_json_from_response(result["text"])
        
        for q in questions:
            q["source_file"] = str(input_file)
        
        with lock:
            results.extend(questions)
        
        log(worker_id, file_idx, total, f"Generated {len(questions)} questions from {input_file.name}")
        
    except Exception as e:
        log(worker_id, file_idx, total, f"ERROR: {input_file.name}: {e}")


def parse_args():
    parser = argparse.ArgumentParser(description='Generate evaluation questions from source content.')
    parser.add_argument('--model', required=True, help='API model ID')
    parser.add_argument('--input-folder', type=Path, required=True, help='Input folder with files')
    parser.add_argument('--output-file', type=Path, required=True, help='Output JSON file')
    parser.add_argument('--schema-file', type=Path, help='Question schema JSON (default: built-in)')
    parser.add_argument('--workers', type=int, default=4, help='Parallel workers (default: 4)')
    parser.add_argument('--keys-file', type=Path, default=Path('.env'), help='API keys file')
    return parser.parse_args()


def main():
    args = parse_args()
    
    keys = load_api_keys(args.keys_file)
    provider = detect_provider(args.model)
    
    if not args.input_folder.exists():
        print(f"[ERROR] Input folder not found: {args.input_folder}", file=sys.stderr)
        sys.exit(1)
    
    schema = DEFAULT_SCHEMA
    if args.schema_file and args.schema_file.exists():
        schema = json.loads(args.schema_file.read_text(encoding='utf-8'))
    
    prompt = build_question_prompt(schema)
    
    all_extensions = IMAGE_EXTENSIONS | TEXT_EXTENSIONS
    input_files = sorted([f for f in args.input_folder.iterdir() if f.is_file() and f.suffix.lower() in all_extensions])
    
    if not input_files:
        print(f"[ERROR] No files found in {args.input_folder}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Generating questions from {len(input_files)} files with {args.workers} workers", file=sys.stderr)
    
    if provider == 'openai':
        client = create_openai_client(keys)
    else:
        client = create_anthropic_client(keys)
    
    results = []
    lock = Lock()
    
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {}
        for idx, f in enumerate(input_files, 1):
            worker_id = (idx - 1) % args.workers
            future = executor.submit(process_file, worker_id, idx, len(input_files), f, args, client, provider, prompt, results, lock)
            futures[future] = f
        
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"[ERROR] {futures[future]}: {e}", file=sys.stderr)
    
    output = {
        "model": args.model,
        "total_questions": len(results),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "questions": results
    }
    
    args.output_file.parent.mkdir(parents=True, exist_ok=True)
    args.output_file.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding='utf-8')
    
    print(f"Generated {len(results)} questions -> {args.output_file}", file=sys.stderr)


if __name__ == '__main__':
    main()
