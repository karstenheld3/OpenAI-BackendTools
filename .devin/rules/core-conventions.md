---
trigger: always_on
---

# Core Conventions

Universal formatting and writing conventions for all documents.

## Text Style (Exception: transcribed or external documents)

- Use ASCII "double quotes" or 'single quotes'. Never use Non-ASCII quotes unless explicitly asked.
- No emojis in documentation (see Document Rule Exceptions below)
- Avoid Markdown tables; use unnumbered lists with indented properties (see Document Rule Exceptions below)
- Use Unicode box-drawing characters for structures:
  - Trees and flows: `├─>` `└─>` `│` (2-space indentation compatible)
  - Boxes and diagrams (non-UI): `┌─` `├─` `└─` `│` `─` `┐` `┤` `┘`
  - UI mockups: Same Unicode characters (SPEC-DG-06), not ASCII `+` `-` `|`
- Arrow symbol `→` must have spaces around it: `A → B` not `A→B`
- Never use `▼` (U+25BC); use `v` instead
- Try to fit single statements/decisions/objects on a single line
- Format workflow references as inline code: `/verify`, `/go`, `/implement`
- Inline enumerations use `N)` format, not `(N)`: `1) first, 2) second, 3) third`
- URLs must always include the scheme (`https://` or `http://`). Never write bare domains: `msn.com` → `https://msn.com`

## Encoding

- Always assume UTF-8 encoding.
- When writing in non-English languages, use native special characters (e.g., German Umlaute: ae → ä, oe → ö, ue → ü, ss → ß). Never substitute with ASCII approximations.
- When non-UTF-8 encoding is detected, document in workspace or session NOTES.md:
  1. File path
  2. Detected encoding (e.g., ISO-8859-1, Windows-1252)
  3. How to preserve encoding (e.g., which PowerShell `[System.IO.File]::` encoding parameters)
- Test and verify PowerShell snippets to correctly read and write file (use copy of file for testing) before recording 3. in NOTES.md.

## Authoritative Literals

Some values are **lexical, not semantic** - every character matters. Addresses, IBANs, reference numbers, registration codes, and official names must be reproduced exactly as recorded. GenAI systematically introduces format drift on these values (Unicode normalization, abbreviation, punctuation changes).

**Rules:**
- Values marked `[LITERAL]` MUST be copied character-for-character
- No Unicode substitution: `o` stays `o` (not `º`), `.` stays `.` (not `ª`), comma stays comma (not dash)
- No abbreviation or expansion of any part of the literal value
- No reformatting: punctuation, spacing, and casing exactly as recorded
- Source of truth for new literals: official documents (government registrations, contracts, bank confirmations) - never from secondary documents
- When a literal is used in outbound communication (emails, letters, forms), copy from the `[LITERAL]`-marked source

**Marking format** - tag values in-place where they are already defined (no separate section, no duplication):
```
- **Street**: Rua da Liberdade, 42, 3.o Esq. [LITERAL: registration certificate 2026-01-15]
- **IBAN**: DE89370400440532013000 [LITERAL]
- **Tax ID**: 123456789 (obtained 2026-03-10) [LITERAL]
```

`[LITERAL]` = copy character-for-character, AP-PR-13 applies. Optional source after colon.

**Known GenAI corruption categories** (why this rule exists):
- **Unicode normalization**: `o` → `º`, `.` → `ª`, straight quotes → curly quotes, half-width → full-width (CJK)
- **Punctuation drift**: commas → dashes, spaces inserted/removed in IBANs, slash direction changed
- **Abbreviation/expansion**: "Dto." → "D", "Apt." → "Apartment", "S/O" → "Son of"
- **Sub-premise loss**: Floor/unit/door numbers dropped or merged into building number (critical for Indian, Portuguese, Japanese addresses where "Flat 4B, 3rd Floor" or "1.o Dto." determines deliverability)
- **Identifier transposition**: LLM token prediction silently swaps digits in similar IDs sharing a prefix (`acct_7H9j2` → `acct_7H9j3`). Corrupted ID still parses, routes to wrong record
- **Script/romanization mixing**: Kanji address rewritten in romaji, Devanagari transliterated, Arabic addresses reversed (RTL)
- **Postal code reformatting**: spaces added/removed (`1000-001` → `1000001`), country-specific formats broken (UK: `SW1A 1AA`, India 6-digit PIN, Japan `〒100-0000`)
- **"Looks right" hallucination**: Model fills gaps with plausible-but-wrong values (invents house numbers, "corrects" postal codes to nearby valid ones)

## Date and Time Format

- **In documents**: `YYYY-MM-DD HH:MM` - Example: `2026-03-19 14:30`
- **In logging**: `YYYY-MM-DD HH:MM:SS` - Example: `2026-03-19 14:30:23`
- **In filenames**: `YYYY-MM-DD` prefix - Example: `2026-03-19_ServerMigration.md`, `2026-03-19_14-30_MeetingNotes.md`
- **In session folders**: `YYYY-MM-DD` prefix - Example: `_2026-03-19_FixAuthBug/`
- **In Document History**: `[YYYY-MM-DD HH:MM]` - Example: `**[2026-03-19 14:30]**`
- **For months**: `YYYY-MM` - Example: `2026-03`

Never use locale-dependent formats (`03/19/2026`, `19.03.2026`, `March 19, 2026`).

## Document Structure

- Place Table of Contents after header block (or after MUST-NOT-FORGET if present)
- No `---` markers between sections
- One empty line between sections
- Most recent changes at top in changelog sections

## Header Block

All documents start with:

```
# [Document Type]: [Title]

**Doc ID**: [TOPIC]-[TYPE][NN]
**Goal**: Single sentence describing purpose
**Target file**: `/path/to/file.py` (or list for multiple)

**Depends on:**
- `_SPEC_[X].md [TOPIC-SP01]` for [what it provides]

**Does not depend on:**
- `_SPEC_[Y].md [TOPIC-SP02]` (explicitly exclude if might seem related)
```

- Doc ID is required for all documents
- Reference other docs by filename AND Doc ID: `_SPEC_CRAWLER.md [CRWL-SP01]`
- Omit optional fields if not applicable: Target file, Depends on, Does not depend on

## Document History Section

Always at document end, reverse chronological order:

```
## Document History

**[2026-01-12 14:30]**
- Added: "Scenario" section with Problem/Solution/What we don't want
- Changed: Placeholder standardized to `{itemId}` (camelCase)
- Fixed: Modal OK button signature

**[2026-01-12 10:00]**
- Initial specification created
```

**Action prefixes:** Added, Changed, Fixed, Removed, Moved

## Document Rule Exceptions

Documents may opt-in to use Markdown tables or emojis by adding a DevSystem tag as the **first line** of the document (before the title).

**Syntax:**
```html
<DevSystem MarkdownTablesAllowed=true EmojisAllowed=true APAPALAN=true MECT=true />
```

**Attributes:**
- `MarkdownTablesAllowed=true` - Allow Markdown tables in this document
- `EmojisAllowed=true` - Allow emojis in this document
- `APAPALAN=true` - APAPALAN rules apply ("As Precise As Possible, As Little As Necessary"). Defined in `@skills:write-documents` and `@skills:coding-conventions`
- `MECT=true` - MECT rules apply ("Minimal Explicit Consistent Terminology"). Defined in `@skills:write-documents` and `@skills:coding-conventions`

**Table formatting rule:** When tables are allowed, format with aligned columns using spaces for human readability. No bold, italic, or other formatting inside table cells.
```markdown
| Model           | Workers | TPM   |
|-----------------|---------|-------|
| gpt-5-nano      | 120+    | ~402K |
| claude-4-5-opus | 60+     | ~473K |
```
- BAD: `|Model|Workers|TPM|` (no spacing)
- BAD: `| **Model** | Workers |` (bold in cells)

**Allowed emojis (when enabled):**
- ✅ - Yes, supported, pass, enabled
- ❌ - No, unsupported, fail, disabled
- ⚠️ - Warning, partial, caution
- ★ - Filled star (rating)
- ☆ - Outlined star (rating)
- ⯪ - Half-filled star (rating)

**Usage pattern:** Emoji first, then textual equivalent
```markdown
- **MCP** - ✅ Yes
- **Hooks** - ❌ No
- **Data** - ⚠️ Partial (read-only)
- **Quality** - ★★★☆☆ (3)
- **Docs** - ★★★★⯪ (4.5)
```

**When to use exceptions:**
- Comparison documents where tables improve readability
- Feature matrices and compatibility charts
- Status dashboards

## Skill References

Reference skills using `@skills:skill-name` format. The skill name must match a folder in `[AGENT_FOLDER]/skills/`.

- `@skills:write-documents` - Document writing skill
- `@skills:coding-conventions` - Coding conventions skill
- `@skills:deep-research` - Deep research skill

**BAD:** `(write-documents skill)`, `write-documents skill`, `the writing skill`
**GOOD:** `@skills:write-documents`

## APAPALAN Writing Principle

**APAPALAN** = As Precise As Possible (Priority 1), As Little As Necessary (Priority 2)

All written output - documents, code comments, log messages, commit messages, communications - follows this principle. Full rules in `APAPALAN_RULES.md` (@skills:write-documents skill).

**Why:** Imprecise writing causes wrong assumptions. Verbose writing wastes attention. Precision prevents misunderstanding; brevity respects the reader's time. Precision always wins when the two conflict.

**Minimal subset (always apply):**
- **AP-PR-07**: Be specific - no "handles errors appropriately", say "retry 3 times with exponential backoff"
- **AP-PR-09**: Consistent patterns - same concept = same format everywhere
- **AP-BR-02**: Sacrifice grammar for brevity - drop articles, filler, verbose constructions
- **AP-NM-01**: One name per concept - no synonyms, no polysemy
- **AP-NM-05**: Use standard terms - don't invent new names for known concepts
- **AP-ST-01**: Goal first - reader knows WHY before HOW

## Transcription Output

Transcribed content MUST contain only the original document's content. No processing metadata, agent annotations, or workflow artifacts.

**IMPORTANT: Text Style rules do NOT apply to transcribed content.**
Transcriptions preserve the original exactly - including curly quotes, typos, unusual punctuation, and formatting choices. Only markdown structural elements (headers, lists, emphasis) are agent-created.

**Prohibited in transcription output:**
- Source filename, path, or URL
- Page counts, figure counts, or statistics
- Transcription date or processing timestamps
- Verification status or progress markers
- Agent notes or processing comments

**Store metadata separately:** If tracking is needed, create a companion `[FILENAME]_meta.json` or add to session NOTES.md.
