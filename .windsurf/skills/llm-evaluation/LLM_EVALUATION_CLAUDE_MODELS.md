# Claude Model ID Reference

Anthropic model IDs follow `{model-family}-{version}-{YYYYMMDD}` format. The date suffix is the **release date**, NOT a predictable pattern.

## Common Mistakes

- Using wrong dates (e.g., `20250514` for Opus 4.5 when correct is `20251101`)
- Using aliases without dates (e.g., `claude-opus-4-5` may not work via direct API)
- Assuming date patterns from other models apply universally

## Verified Model IDs (2026-01-25)

**Claude 4.5 Family:**
- `claude-opus-4-5-20251101` - Opus 4.5 (Nov 1, 2025)
- `claude-sonnet-4-5-20250929` - Sonnet 4.5 (Sep 29, 2025)
- `claude-haiku-4-5-20251001` - Haiku 4.5 (Oct 1, 2025)

**Claude 4 Family:**
- `claude-opus-4-20250514` - Opus 4 (May 14, 2025)
- `claude-sonnet-4-20250514` - Sonnet 4 (May 14, 2025)

**Claude 3.x Family:**
- `claude-3-7-sonnet-20250219` - 3.7 Sonnet (Feb 19, 2025)
- `claude-3-5-haiku-20241022` - 3.5 Haiku (Oct 22, 2024)

## Wrong IDs That Return 404

| Model | Wrong IDs Tried | Correct ID |
|-------|-----------------|------------|
| Opus 4.5 | `claude-opus-4-5-20250929`, `claude-opus-4-5-20251022` | `claude-opus-4-5-20251101` |
| Haiku 4.5 | `claude-haiku-4-5-20250514`, `claude-haiku-4-5-20251022` | `claude-haiku-4-5-20251001` |

## How to Find Correct Model IDs

1. Check third-party docs (OpenRouter, TypingMind, AI/ML API) - they often list exact IDs
2. Search for `"claude-{model}-{version}"` with release announcements
3. The date is the **release date** of that specific model version

## Sources

- https://docs.aimlapi.com/api-references/text-models-llm/anthropic/claude-4.5-opus
- https://www.typingmind.com/guide/anthropic/claude-haiku-4-5-20251001
- https://milvus.io/ai-quick-reference/how-do-i-call-claude-opus-45-via-the-claude-api
