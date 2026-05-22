---
description: Translate markdown, PDF, or subtitle files to one or more target languages
auto_execution_mode: 1
---

# Translate Workflow

Translate a file or folder of files to one or more target languages with consistent terminology, native characters, and structure preservation.

**Goal**: Translated files with consistent terminology, native characters, and preserved structure

**Why**: Unstructured LLM translation produces inconsistent terminology, misses native characters, and breaks document structure.

## Usage

`/translate <file_or_folder> [L1] [L2] [L3] ...`

- Languages: ISO 639-1 codes (DE, HU, FR, ES, IT, PL, etc.)
- Input: .md, .pdf, .srt files, or no file (chat context)
- Output: file → `[filename]_[LANG].[ext]` in same folder; chat context → translated text in chat

Examples:
- `/translate c:\report.md DE` → `c:\report_DE.md`
- `/translate c:\report.md DE HU` → `c:\report_DE.md`, `c:\report_HU.md`
- `/translate c:\docs\ DE` → all supported files in folder, each translated
- `/translate c:\video.srt DE` → `c:\video_DE.srt`
- `/translate DE` → translate last agent output in chat to German

## Required Skills

- @skills:pdf-tools for PDF text extraction (pdftotext)
- @skills:write-documents for document quality rules
- @skills:write-documents `TRANSLATION_RULES.md` for quality dimensions, term pairs, prompt templates, improvement cycle

## Mandatory Re-read

**SESSION-MODE**: NOTES.md (translation settings from prior runs)

**PROJECT-MODE**: !NOTES.md or NOTES.md (translation settings from prior runs)

## MUST-NOT-FORGET

1. Native characters mandatory - DE: ä ö ü ß, HU: á é í ó ö ő ú ü ű, FR: é è ê ë ç, etc. Never ASCII approximations
2. Build TRANSLATION_TERM_PAIRS before translating - store in NOTES.md
3. Addressing form and tonality decisions documented before translating
4. Source language auto-detected, stored as SL
5. PDF input: pdftotext only (fast text extraction), no OCR, no transcription
6. SRT input: preserve all timing codes, match translated text length to source line length
7. Output naming: `[filename]_[LANG].md` (.md/.pdf input) or `[filename]_[LANG].srt` (.srt input)
8. Structure preserved exactly: headings, lists, code blocks, links, tables
9. Do NOT translate: code blocks, URLs, file paths, placeholders `[LIKE_THIS]`, HTML/XML tags
10. Run `/verify` after all translations complete

# EXECUTION

## Step 1: Read Input

Determine input type and read source content.

### Single file (.md)

Read the file. Auto-detect source language (SL).

### Single file (.pdf)

Fast text extraction via pdftotext (no transcription):

```powershell
$pdftotext = "[WORKSPACE_FOLDER]/../.tools/poppler/Library/bin/pdftotext.exe"
$inputPdf = "[INPUT_PATH]"
$outputMd = "[INPUT_FOLDER]/[FILENAME]_[SL].md"
& $pdftotext -layout $inputPdf $outputMd
```

Auto-detect SL from extracted text. Output `[filename]_[SL].md` in same folder as input PDF.
If pdftotext output is garbled or empty (scanned PDF), inform user and suggest `/transcribe` instead.

### Single file (.srt)

Read the subtitle file. Auto-detect source language (SL) from subtitle text content. Parse into blocks (sequence number, timing, text lines). Timing codes and sequence numbers are untranslatable.

### Chat context (no file argument)

When `/translate [L1]` is invoked without a file path, translate the last agent output in conversation:

1. Detect last agent output block in conversation context
2. Auto-detect source language (SL) from text content
3. Preserve original formatting (markdown structure, code blocks, lists, bold/italic)
4. Treat as in-memory document - proceed with Steps 2-5
5. Output translated text directly in chat (no file created)
6. If conversation contains no translatable agent output, ask user to specify text or file path

### Folder

List all .md, .pdf, and .srt files. Process each through Steps 1-4, sharing term pairs across files.

Emit before proceeding:

```json
{"input_type": "file|folder|chat", "format": "md|pdf|srt|chat", "source_language": "EN", "target_languages": ["DE", "HU"], "file_count": 1}
```

## Step 2: Analyze Translation Decisions

Read source text and extract decisions for each target language:

1. Addressing form - formal or informal (DE: Sie/du, HU: Ön/te, FR: vous/tu)
2. Tonality and register - academic, business, casual, technical, literary
3. Domain terminology - terms requiring consistent translation across the document
4. Proper nouns - brand names, product names, person names (keep original or translate?)
5. Abbreviations and acronyms - expand in target language or keep?
6. Localization - date formats, number formats (1,000.00 vs 1.000,00), measurement units
7. Untranslatable elements - code blocks, URLs, file paths, variable names
8. Idioms and cultural references - adaptation needed?

Emit decisions:

```json
{
  "addressing_form": {"DE": "formal (Sie)", "HU": "formal (Ön)"},
  "tonality": "technical",
  "keep_original": ["brand names", "code blocks", "URLs", "file paths"],
  "localize": {"dates": true, "numbers": true, "units": false},
  "research_needed": ["term1: best DE translation", "idiom2: HU equivalent"]
}
```

## Step 3: Build Term Pairs and MNF

### Research

For items in research_needed from Step 2: determine best translations per target language. Consider context, domain conventions, and target audience expectations.

### Build TRANSLATION_TERM_PAIRS

One entry per target language. Format matches `CONVERSATION_TEMPLATE.md`:

```
TRANSLATION_TERM_PAIRS_DE: workflow -> Arbeitsablauf | deployment -> Bereitstellung | repository -> Repository
TRANSLATION_TERM_PAIRS_HU: workflow -> munkafolyamat | deployment -> telepites | repository -> tarolo
```

### Translation Settings (store in NOTES.md)

Store before translating. Schema:

```
## Translation Settings ([FILENAME])
- Addressing form: [per language decisions]
- Tonality: [register choice]
- Untranslated: [list of items to keep in source language]
- Localization: [date/number/unit format per language]
- TRANSLATION_TERM_PAIRS_[LANG]: [pairs from above]
```

- SESSION-MODE: Append to session `NOTES.md`
- PROJECT-MODE: Append to workspace `NOTES.md`

When translating a folder (multiple files), store once for the batch. Reuse term pairs across files for consistency.

## Step 4: Translate

For each target language, for each input file: branch by text type.

Fill prompt template variables from Steps 2-3: `{SOURCE_LANG}`, `{TARGET_LANG}`, `{ADDRESSING_FORM}`, `{TONALITY}`, `{REGIONAL_VARIANT}`, `{TRANSLATION_TERM_PAIRS}`.

### Text type: Document (.md, .pdf)

Estimate source text token count (1 token ~ 4 characters for Latin scripts, ~1 token per CJK (Chinese, Japanese, Korean) character).

**Short document (<=5000 tokens):** Translate in a single Large Language Model (LLM) pass using the Reflection Translation Prompt from `TRANSLATION_RULES.md` (TR-IC-01).

**Long document (>5000 tokens):** Split into chapters, translate each, stitch together:

1. **Split** at heading boundaries (prefer `##` level). Each chapter must be <=5000 tokens. If a single section exceeds 5000 tokens, split at the next lower heading level or at paragraph boundaries.
2. **Translate** each chapter sequentially using TR-IC-01. Provide the last 500 tokens of the previous translated chapter as `{PREVIOUS_TRANSLATED_CHUNKS}` context (see chunked translation section in `TRANSLATION_RULES.md`).
3. **Stitch** all translated chapters in order into the output file. Verify no content lost at chapter boundaries (no duplicated or missing paragraphs).

Write output: `[input_folder]/[filename]_[LANG].md`

### Text type: Subtitle (.srt)

Translate subtitle blocks using the Reflection Translation Prompt from `TRANSLATION_RULES.md` (TR-IC-01) with these additional constraints in the prompt:

```
## Subtitle Rules

- Translate subtitle text only. Preserve sequence numbers and timing codes exactly.
- Match translated line length to source line length (character count +/- 20%).
  If translation is longer, rephrase more concisely. Prefer shorter synonyms.
  If translation needs two lines, keep each line under 42 characters.
- Maximum 2 lines per subtitle block.
- Preserve line breaks within subtitle blocks where the source has them.
- Reading speed: aim for 15-20 characters per second of display time.
- Do NOT merge or split subtitle blocks. Each source block = one target block.
```

Process subtitle blocks in batches of 20-30 blocks per LLM call, providing 5 preceding translated blocks as context for continuity.

Write output: `[input_folder]/[filename]_[LANG].srt`

For folder batches: translate all files to L1 first, then L2, etc. This keeps term pair context fresh per language.

## Step 5: Verify

Two-phase verification: automated structure checks, then LLM-as-judge quality evaluation per `TRANSLATION_RULES.md`.

### Phase 1: Automated Checks

Run these checks programmatically (grep, count, compare):

**All text types:**
1. Term consistency (TR-TP-03) - grep each TRANSLATION_TERM_PAIR, verify no mixed translations
2. Native characters (TR-NC-02) - grep for ASCII approximations
3. Addressing form (TR-AF-03) - consistent throughout, no mixing
4. No source language fragments remaining in translated prose (outside code/URLs)

**Document (.md, .pdf) only:**
5. Structure match (TR-SP-01..06) - heading count, list count, code block count equal to source
6. Completeness - paragraph count matches source, no missing sections
7. Untranslated items (TR-UE-01..05) - code blocks, URLs, placeholders unchanged

**Subtitle (.srt) only:**
8. Block count - same number of subtitle blocks in source and target
9. Timing preserved - all timing codes identical between source and target
10. Line length - flag lines exceeding source length by >20% or exceeding 42 characters
11. Line count per block - no block exceeds 2 lines

**CJK (JA, ZH) only (TR-CJ-06):**
12. Script consistency (ZH) - no wrong-variant characters for chosen simplified/traditional
13. Fullwidth punctuation - no halfwidth `.` `,` `?` `!` `:` `;` in prose
14. Transliteration (JA) - foreign terms in katakana, not raw English or romaji
15. Keigo consistency (JA) - no mixing of polite/plain forms

### Phase 2: LLM-as-Judge Quality Evaluation

Evaluate using the Quality Evaluation Prompt from `TRANSLATION_RULES.md` (TR-IC-02). For documents: evaluate per section (heading-delimited). For subtitles: evaluate in batches of 20-30 blocks (same batches as translation). Follow the improvement cycle (TR-IC-03, TR-IC-04): fix specific issues, re-evaluate, repeat until all 4 dimensions PASS or 3 iterations reached.

Run `/verify` after all corrections applied.

## Stuck Detection

If 3 consecutive improvement iterations fail to pass all 4 quality dimensions:
1. Accept current translation with a note of which dimensions failed
2. Document in PROBLEMS.md: file, language, failing dimensions, iteration attempts
3. Ask user: accept partial quality, retry with different approach, or translate manually

# REFERENCE

Language codes, native characters, addressing form defaults, and CJK rules: see `TRANSLATION_RULES.md` in @skills:write-documents.

## Quality Gate

- [ ] All target languages translated
- [ ] TRANSLATION_TERM_PAIRS stored in NOTES.md
- [ ] Native characters verified (no ASCII approximations)
- [ ] Structure matches source (heading, list, code block counts)
- [ ] `/verify` passed
- [ ] MUST-NOT-FORGET list checked
