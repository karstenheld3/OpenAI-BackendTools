# LLM Evaluation Scripts Reference

Detailed parameters and examples for all scripts.

## call-llm.py - Single LLM Call

```powershell
python call-llm.py --model gpt-4o --input-file photo.jpg --prompt-file prompts/transcribe-page.md
python call-llm.py --model claude-opus-4-20250514 --input-file doc.md --prompt-file prompts/summarize-text.md
```

**Parameters:**
- `--model` - API model ID (required)
- `--input-file` - Input file: image or text
- `--prompt-file` - Prompt file (.md)
- `--output-file` - Output file (default: stdout)
- `--keys-file` - API keys file (default: .env)
- `--write-json-metadata` - Write token usage to separate JSON file
- `--temperature` - Temperature effort level (default: medium)
- `--reasoning-effort` - Reasoning effort level (default: medium)
- `--output-length` - Output length effort level (default: medium)
- `--seed` - Random seed (OpenAI only)
- `--response-format` - Output format: text, json (default: text)
- `--use-prompt-caching` - Enable prompt caching (see Prompt Caching section)

## call-llm-batch.py - Batch Processing

```powershell
python call-llm-batch.py --model gpt-4o --input-folder images/ --output-folder out/ --prompt-file prompts/transcribe-page.md --runs 3 --workers 4
```

**Parameters:**
- `--model` - API model ID (required)
- `--input-folder` - Folder with input files
- `--output-folder` - Folder for output files
- `--prompt-file` - Prompt file (.md)
- `--runs` - Runs per file (default: 1)
- `--workers` - Parallel workers (default: 4)
- `--keys-file` - API keys file (default: .env)
- `--force` - Force reprocess existing files
- `--clear-folder` - Clear output folder before processing
- `--temperature` - Temperature effort level (default: medium)
- `--reasoning-effort` - Reasoning effort level (default: medium)
- `--output-length` - Output length effort level (default: medium)
- `--seed` - Random seed (OpenAI only)
- `--response-format` - Output format: text, json (default: text)
- `--use-prompt-caching` - Enable prompt caching (see Prompt Caching section)

**Features:**
- Parallel processing with configurable workers
- Resume capability (skips existing outputs)
- Incremental save after each item
- Token usage tracking per model
- Cache warm-up: first file processed before parallel workers (Anthropic only)

## find-workers-limit.py - Worker Limit Discovery

```powershell
python find-workers-limit.py --model gpt-5-nano --max-workers 120 --verbose
python find-workers-limit.py --model claude-4-5-haiku-20251022 --max-workers 60
```

**Parameters:**
- `--model` - API model ID (required)
- `--max-workers` - Maximum workers to test (default: 100)
- `--prompt` - Custom prompt text (default: 500-word essay)
- `--min-output-tokens` - Minimum output tokens (default: 500)
- `--keys-file` - API keys file (default: .env)
- `--output-file` - Output JSON file (default: {model}-limit.json)
- `--verbose` - Show detailed progress

**Algorithm:**
1. Start at 3 workers, double twice (to 12)
2. Scale by 1.5x up to max-workers
3. On rate limit: scale back by 0.8 to find highest passing count
4. Output recommended workers, max tested, runs, timestamp

## generate-questions.py - Question Generation

```powershell
python generate-questions.py --model claude-opus-4-20250514 --input-folder images/ --output-file questions.json
```

**Parameters:**
- `--model` - API model ID (required)
- `--input-folder` - Folder with source files
- `--output-file` - Output JSON file
- `--schema-file` - Question schema (default: schemas/default-questions.json)
- `--workers` - Parallel workers (default: 4)

## generate-answers.py - Answer Generation

```powershell
python generate-answers.py --model gpt-5-mini --input-folder transcriptions/ --output-folder answers/ --questions-file questions.json
```

**Parameters:**
- `--model` - API model ID (required)
- `--input-folder` - Folder with processed text files
- `--output-folder` - Folder for answer JSON files
- `--questions-file` - Questions JSON (from generate-questions.py)
- `--workers` - Parallel workers (default: 4)

## evaluate-answers.py - Scoring

```powershell
python evaluate-answers.py --model gpt-5 --input-folder answers/ --output-folder scores/
```

**Parameters:**
- `--model` - Judge model ID (required)
- `--input-folder` - Folder with answer JSON files
- `--output-folder` - Folder for score JSON files
- `--judge-prompt` - Custom judge prompt
- `--pass-threshold` - Pass threshold (default: 4)
- `--workers` - Parallel workers (default: 4)
- `--keys-file` - API keys file (default: .env)

## analyze-costs.py - Cost Analysis

```powershell
python analyze-costs.py --input-folder transcriptions/ --output-file costs.json
```

**Parameters:**
- `--input-folder` - Folder with _token_usage__.json files
- `--output-file` - Output JSON file
- `--pricing` - Custom pricing file (default: model-pricing.json)

## compare-transcription-runs.py - Hybrid Comparison

```powershell
python compare-transcription-runs.py --files run1/*.md run2/*.md --output-file comparison.json --method hybrid --judge-model gpt-5-mini --judge-prompt prompts/compare-image-transcription.md
```

**Parameters:**
- `--files` - List of files to compare (2+ files)
- `--input-folder` - Folder with files (alternative to --files)
- `--output-file` - Output JSON file (required)
- `--method` - Comparison method: levenshtein, semantic, hybrid (default: levenshtein)
- `--judge-model` - LLM judge model (required for semantic/hybrid)
- `--judge-prompt` - Judge prompt file (default: built-in)
- `--temperature` - Effort level: none, minimal, low, medium, high, xhigh (default: medium)
- `--reasoning-effort` - Reasoning effort level (for reasoning models)
- `--output-length` - Output length effort level (default: medium)
- `--baseline` - Baseline file for comparison
- `--grouped` - Group files by source name
- `--keys-file` - API keys file (default: .env)

**Features:**
- Hybrid comparison: Levenshtein for text, LLM judge for images
- Section parsing: splits by `<transcription_image>` tags
- Effort level control: temperature, reasoning_effort, output_length
- Model-aware parameter building (temperature vs reasoning models)

## llm-evaluation-selftest.py - Self-Test

```powershell
python llm-evaluation-selftest.py [--skip-api-calls]
```

**Tests:**
- Configuration file loading (model-registry.json, model-pricing.json, model-parameter-mapping.json)
- Script help text availability
- File type detection logic
- JSON output schema validation
- API integration (optional, requires valid API keys)

**Exit codes:** 0 = passed, 1 = failed

## Configuration Files

- `model-registry.json` - Model definitions with provider, method (temperature/reasoning_effort/thinking), max_output, and parameter constraints
- `model-pricing.json` - Token costs per model (USD)
- `model-parameter-mapping.json` - Effort level mappings (none/minimal/low/medium/high/xhigh) to API parameters
- `schemas/default-questions.json` - Default question categories

## Prompts

- `prompts/transcribe-page.md` - Image transcription
- `prompts/summarize-text.md` - Text summarization
- `prompts/answer-from-text.md` - Question answering
- `prompts/judge-answer.md` - Answer scoring (0-5)
- `prompts/compare-image-transcription.md` - Semantic similarity scoring (0-100)

## Pipeline Example

```powershell
$venv = ".tools\llm-venv\Scripts\python.exe"
$skill = ".windsurf\skills\llm-evaluation"

# 1. Transcribe images
& $venv "$skill\call-llm-batch.py" --model gpt-4o --input-folder images/ --output-folder transcriptions/ --prompt-file "$skill\prompts\transcribe-page.md" --runs 3

# 2. Generate questions from original images
& $venv "$skill\generate-questions.py" --model claude-opus-4-20250514 --input-folder images/ --output-file questions.json

# 3. Generate answers from transcriptions
& $venv "$skill\generate-answers.py" --model gpt-5-mini --input-folder transcriptions/ --output-folder answers/ --questions-file questions.json

# 4. Score answers
& $venv "$skill\evaluate-answers.py" --model gpt-5 --input-folder answers/ --output-folder scores/

# 5. Analyze costs
& $venv "$skill\analyze-costs.py" --input-folder transcriptions/ --output-file cost_analysis.json
```

## Key Patterns

**Retry with backoff:** 3 retries with exponential backoff (1s, 2s, 4s). Skip item after all retries fail.

**Atomic writes:** Write to `.tmp` file first, rename to final on success. Enables reliable resume.

**Logging format:** `[ worker_id ] [ x / n ] action...`

**File type detection:** Auto-detect by suffix only (no override)
- Image: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`
- Text: `.txt`, `.md`, `.json`, `.py`, `.html`, `.xml`, `.csv`

## Prompt Caching

Reduce costs and latency for repetitive LLM calls with large prompts.

```powershell
# Single call with caching
python call-llm.py --model claude-sonnet-4-20250514 --prompt-file large_prompt.md --use-prompt-caching

# Batch with caching (automatic cache warm-up)
python call-llm-batch.py --model claude-sonnet-4-20250514 --input-folder images/ --output-folder out/ --prompt-file prompts/transcribe.md --use-prompt-caching
```

**Provider behavior:**
- **OpenAI** - Automatic caching, no API changes needed. Prompts >1024 tokens eligible. 50% discount on cached tokens.
- **Anthropic** - Explicit `cache_control` on system blocks. Minimum 1024-4096 tokens depending on model. 90% read discount, 25% write premium.

**Batch cache warm-up (Anthropic):** First file processes synchronously to populate cache, then remaining files process in parallel. All parallel requests benefit from cache reads.

**Cache metrics in metadata:**
- `cached_tokens` - OpenAI cached input tokens
- `cache_write_tokens` - Anthropic cache creation tokens
- `cache_read_tokens` - Anthropic cache hit tokens
