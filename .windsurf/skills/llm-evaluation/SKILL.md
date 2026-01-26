# LLM Evaluation Skill

Generic skill for LLM evaluation pipelines - works with images, text documents, or any content.

## Setup

Run `SETUP.md` once to install dependencies in `[WORKSPACE_FOLDER]/.tools/llm-eval-venv/`.

## File Type Detection

Auto-detect by suffix only (no override):
- **Image**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`
- **Text**: `.txt`, `.md`, `.json`, `.py`, `.html`, `.xml`, `.csv`
- **Unknown**: Script exits with error

## Scripts

### call-llm.py - Single LLM Call

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

### call-llm-batch.py - Batch Processing

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

**Features:**
- Parallel processing with configurable workers
- Resume capability (skips existing outputs)
- Incremental save after each item
- Token usage tracking per model

### generate-questions.py - Question Generation

```powershell
python generate-questions.py --model claude-opus-4-20250514 --input-folder images/ --output-file questions.json
```

**Parameters:**
- `--model` - API model ID (required)
- `--input-folder` - Folder with source files
- `--output-file` - Output JSON file
- `--schema-file` - Question schema (default: schemas/default-questions.json)
- `--workers` - Parallel workers (default: 4)

### generate-answers.py - Answer Generation

```powershell
python generate-answers.py --model gpt-5-mini --input-folder transcriptions/ --output-folder answers/ --questions-file questions.json
```

**Parameters:**
- `--model` - API model ID (required)
- `--input-folder` - Folder with processed text files
- `--output-folder` - Folder for answer JSON files
- `--questions-file` - Questions JSON (from generate-questions.py)
- `--workers` - Parallel workers (default: 4)

### evaluate-answers.py - Scoring

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

### analyze-costs.py - Cost Analysis

```powershell
python analyze-costs.py --input-folder transcriptions/ --output-file costs.json
```

**Parameters:**
- `--input-folder` - Folder with _token_usage__.json files
- `--output-file` - Output JSON file
- `--pricing` - Custom pricing file (default: model-pricing.json)

### compare-transcription-runs.py - Hybrid Comparison

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

### llm-evaluation-selftest.py - Self-Test

```powershell
python llm-evaluation-selftest.py [--skip-api-calls]
```

**Purpose:**
Validates all scripts work correctly and detects breaking changes during development.

**Tests:**
- Configuration file loading (model-registry.json, model-pricing.json, model-parameter-mapping.json)
- Script help text availability
- File type detection logic
- JSON output schema validation
- API integration (optional, requires valid API keys)

**Exit codes:**
- 0 - All tests passed
- 1 - One or more tests failed

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
- `prompts/compare-image-transcription.md` - Semantic similarity scoring for image transcriptions (0-100)

## Judge Prompt Calibration

The `compare-image-transcription.md` prompt has been calibrated with degradation test cases (0%, 25%, 50%, 75%, 98% similarity).

**Tested models:**
- **gpt-4o**: Overestimates 75% similarity (95% vs expected 65-85), otherwise acceptable
- **gpt-5-mini**: Best calibration, all test cases within tolerance (recommended)
- **claude-sonnet-4-5-20250929**: Parse error with extended thinking output (known issue)

**Recommendation:** Use gpt-5-mini as default judge model for best accuracy.

## Pipeline Example

Full evaluation pipeline:

```powershell
$venv = ".tools\llm-eval-venv\Scripts\python.exe"
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

## Tested Models

Session testing from **2026-01-22 to 2026-01-24**:

**Self-test passed (15/15 API integration tests):**
- `gpt-5.2` - OpenAI, reasoning model
- `gpt-5.1` - OpenAI, reasoning model
- `gpt-5` - OpenAI, reasoning model
- `gpt-5-mini` - OpenAI, reasoning model
- `gpt-5-nano` - OpenAI, reasoning model
- `gpt-4.1` - OpenAI, temperature model, multi-modal
- `gpt-4.1-mini` - OpenAI, temperature model, multi-modal
- `gpt-4.1-nano` - OpenAI, temperature model, multi-modal
- `gpt-4o` - OpenAI, temperature model
- `gpt-4o-mini` - OpenAI, temperature model
- `claude-opus-4-5-20251101` - Anthropic, Claude Opus 4.5
- `claude-sonnet-4-5-20250929` - Anthropic, Claude Sonnet 4.5
- `claude-haiku-4-5-20251001` - Anthropic, Claude Haiku 4.5
- `claude-sonnet-4-20250514` - Anthropic, Claude Sonnet 4
- `claude-3-7-sonnet-20250219` - Anthropic, Claude 3.7 Sonnet
- `claude-3-5-haiku-20241022` - Anthropic, Claude 3.5 Haiku

**Pipeline tested (full evaluation workflow):**
- `claude-opus-4-1-20250805` - Transcription: 130K tokens, $4.82 cost
- `gpt-4o-mini` - Batch processing, questions, answers, evaluation
- `gpt-5-mini` - Question generation, answer generation
- `gpt-5` - LLM-as-judge scoring (81.1% pass rate, 4.14/5 avg)

**Judge prompt calibration tested:**
- `gpt-4o` - Overestimates 75% similarity (95% vs expected 65-85)
- `gpt-5-mini` - Best calibration, all 5 degradation levels within tolerance (recommended)
- `claude-sonnet-4-5-20250929` - Parse error with extended thinking output

**Disabled/blocked:**
- `o1-preview`, `o1-mini` - No API access
- `claude-opus-4-20250514` - Requires streaming for extended thinking (>10 min timeout)
- `claude-3-5-sonnet-20241022` - Model deprecated (404 error)

## Claude Model ID Reference

**Why Claude models return 404 errors:** [VERIFIED]

Anthropic model IDs follow `{model-family}-{version}-{YYYYMMDD}` format. The date suffix is the **release date**, NOT a predictable pattern. Common mistakes:
- Using wrong dates (e.g., `20250514` for Opus 4.5 when correct is `20251101`)
- Using aliases without dates (e.g., `claude-opus-4-5` may not work via direct API)
- Assuming date patterns from other models apply universally

**Research findings (2026-01-25):**

| Model | Wrong IDs Tried (404) | Correct ID | Release Date |
|-------|----------------------|------------|--------------|
| Opus 4.5 | `claude-opus-4-5-20250929`, `claude-opus-4-5-20251022` | `claude-opus-4-5-20251101` | Nov 1, 2025 |
| Haiku 4.5 | `claude-haiku-4-5-20250514`, `claude-haiku-4-5-20251022` | `claude-haiku-4-5-20251001` | Oct 1, 2025 |
| Sonnet 4.5 | - | `claude-sonnet-4-5-20250929` | Sep 29, 2025 |
| Sonnet 4 | - | `claude-sonnet-4-20250514` | May 14, 2025 |
| Opus 4 | - | `claude-opus-4-20250514` | May 14, 2025 |
| 3.7 Sonnet | - | `claude-3-7-sonnet-20250219` | Feb 19, 2025 |
| 3.5 Haiku | - | `claude-3-5-haiku-20241022` | Oct 22, 2024 |

**How to find correct model IDs:**
1. Check third-party docs (OpenRouter, TypingMind, AI/ML API) - they often list exact IDs
2. Search for `"claude-{model}-{version}"` with release announcements
3. The date is the **release date** of that specific model version

**Sources:**
- https://docs.aimlapi.com/api-references/text-models-llm/anthropic/claude-4.5-opus
- https://www.typingmind.com/guide/anthropic/claude-haiku-4-5-20251001
- https://milvus.io/ai-quick-reference/how-do-i-call-claude-opus-45-via-the-claude-api

## Key Patterns

**Retry with backoff:**
- 3 retries with exponential backoff (1s, 2s, 4s)
- Skip item after all retries fail

**Atomic writes:**
- Write to `.tmp` file first
- Rename to final on success
- Enables reliable resume

**Logging format:**
```
[ worker_id ] [ x / n ] action...
```

