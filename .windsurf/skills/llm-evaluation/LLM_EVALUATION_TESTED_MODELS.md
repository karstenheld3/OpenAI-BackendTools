# Tested Models

Session testing from **2026-01-22 to 2026-01-26**.

## Self-Test Passed (16 models)

All passed 15/15 API integration tests via `llm-evaluation-selftest.py`:

**OpenAI - Reasoning Models:**
- `gpt-5.2`
- `gpt-5.1`
- `gpt-5`
- `gpt-5-mini`
- `gpt-5-nano`

**OpenAI - Temperature Models:**
- `gpt-4.1` (multi-modal)
- `gpt-4.1-mini` (multi-modal)
- `gpt-4.1-nano` (multi-modal)
- `gpt-4o`
- `gpt-4o-mini`

**Anthropic:**
- `claude-opus-4-5-20251101` - Claude Opus 4.5
- `claude-sonnet-4-5-20250929` - Claude Sonnet 4.5
- `claude-haiku-4-5-20251001` - Claude Haiku 4.5
- `claude-sonnet-4-20250514` - Claude Sonnet 4
- `claude-3-7-sonnet-20250219` - Claude 3.7 Sonnet
- `claude-3-5-haiku-20241022` - Claude 3.5 Haiku

## Pipeline Tested (Full Evaluation Workflow)

- `claude-opus-4-1-20250805` - Transcription: 130K tokens, $4.82 cost
- `gpt-4o-mini` - Batch processing, questions, answers, evaluation
- `gpt-5-mini` - Question generation, answer generation
- `gpt-5` - LLM-as-judge scoring (81.1% pass rate, 4.14/5 avg)

## Judge Prompt Calibration

Tested with degradation cases (0%, 25%, 50%, 75%, 98% similarity):

- **gpt-4o** - Overestimates 75% similarity (95% vs expected 65-85)
- **gpt-5-mini** - Best calibration, all 5 levels within tolerance (RECOMMENDED)
- **claude-sonnet-4-5-20250929** - Parse error with extended thinking output

## Worker Limits (2026-01-26)

Burst capacity tested via `find-workers-limit.py`:

- **gpt-5-nano**: 120+ workers, ~402K TPM
- **gpt-5-mini**: 120+ workers, ~164K TPM
- **claude-4-5-haiku**: 60+ workers, ~450K TPM
- **claude-4-5-sonnet**: 60+ workers, ~467K TPM
- **claude-4-5-opus**: 60+ workers, ~473K TPM

## Disabled/Blocked Models

- `o1-preview`, `o1-mini` - No API access
- `claude-opus-4-20250514` - Requires streaming for extended thinking (>10 min timeout)
- `claude-3-5-sonnet-20241022` - Model deprecated (404 error)
