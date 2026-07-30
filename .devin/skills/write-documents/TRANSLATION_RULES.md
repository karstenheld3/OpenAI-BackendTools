# Translation Rules

Rules for translating documents with consistent quality, terminology, and structure. Referenced by `/translate`, `/verify`, and `/improve`.

**Writing quality:** Apply `APAPALAN_RULES.md` to all translated content. Key rules: AP-PR-07 (be specific), AP-NM-01 (one name per concept), AP-PR-09 (consistent patterns).

## Rule Index

Quality Dimensions (QD)
- TR-QD-01: Evaluate translations across 4 dimensions (accuracy, fluency, style, terminology)
- TR-QD-02: Accuracy - no additions, mistranslations, omissions, or untranslated prose
- TR-QD-03: Fluency - correct target language grammar, spelling, punctuation
- TR-QD-04: Style - matches source register, tone, and addressing form
- TR-QD-05: Terminology - glossary terms applied consistently with correct inflection

Term Pairs (TP)
- TR-TP-01: Build TRANSLATION_TERM_PAIRS before translating
- TR-TP-02: One entry per target language, pipe-delimited format
- TR-TP-03: Apply glossary terms with grammatical inflection (case, gender, number, tense)
- TR-TP-04: Store term pairs in NOTES.md under `## Translation Settings`

Native Characters (NC)
- TR-NC-01: Use native special characters, never ASCII approximations
- TR-NC-02: Verify no ASCII approximations remain after translation

Structure Preservation (SP)
- TR-SP-01: Heading levels unchanged
- TR-SP-02: List formatting unchanged
- TR-SP-03: Code blocks untranslated (fenced and indented)
- TR-SP-04: Links: translate display text, keep URLs
- TR-SP-05: Tables: preserve column count, alignment, translate cell content
- TR-SP-06: Markdown formatting preserved (bold, italic, etc.)

Untranslatable Elements (UE)
- TR-UE-01: Code blocks (fenced ``` and indented) stay in source language
- TR-UE-02: URLs, file paths stay unchanged
- TR-UE-03: Placeholders `[LIKE_THIS]` stay unchanged
- TR-UE-04: HTML/XML tags stay unchanged
- TR-UE-05: Variable names, command names stay unchanged

Addressing Form (AF)
- TR-AF-01: Document addressing form decision before translating
- TR-AF-02: Default to formal when user does not specify
- TR-AF-03: Addressing form must be consistent throughout document (no mixing)

CJK Languages (CJ)
- TR-CJ-01: ZH requires script decision: simplified or traditional
- TR-CJ-02: JA honorifics use keigo system (teineigo default for technical, sonkeigo for formal)
- TR-CJ-03: JA/ZH use fullwidth punctuation, not halfwidth
- TR-CJ-04: JA foreign terms transliterated to katakana with source term in parentheses on first use
- TR-CJ-05: ZH loanwords follow target region conventions (mainland vs Taiwan vs HK)
- TR-CJ-06: Verify correct script, punctuation width, and transliteration after translation

Improvement Cycle (IC)
- TR-IC-01: Translation uses single-roundtrip reflection (translate, self-review, output improved)
- TR-IC-02: Verification uses LLM-as-judge with 4 quality dimensions
- TR-IC-03: Failed dimensions trigger targeted fix and re-evaluation
- TR-IC-04: Improvement cycle repeats until all 4 dimensions PASS

## Table of Contents

- [Quality Dimensions](#quality-dimensions)
- [Term Pairs](#term-pairs)
- [Native Characters](#native-characters)
- [Structure Preservation](#structure-preservation)
- [Untranslatable Elements](#untranslatable-elements)
- [Addressing Form](#addressing-form)
- [CJK Languages](#cjk-languages)
- [Improvement Cycle](#improvement-cycle)
- [Prompt Templates](#prompt-templates)

## Quality Dimensions

Every translation must be evaluated across 4 dimensions. These apply during translation (self-review), verification (LLM-as-judge), and improvement (targeted fixes).

### TR-QD-01: 4-Dimension Evaluation

All translation quality checks use these 4 dimensions consistently:

1. Accuracy - source meaning preserved without additions, omissions, or mistranslations
2. Fluency - natural target language with correct grammar, spelling, punctuation
3. Style - source register, tone, and cultural appropriateness maintained
4. Terminology - glossary terms applied consistently with correct grammatical inflection

### TR-QD-02: Accuracy

No content added, removed, or changed in meaning.

**BAD:**
```
Source: "The system retries 3 times with exponential backoff."
Translation: "Das System versucht es erneut."
(omits "3 times" and "exponential backoff")
```

**GOOD:**
```
Source: "The system retries 3 times with exponential backoff."
Translation: "Das System wiederholt den Versuch 3-mal mit exponentiellem Backoff."
```

### TR-QD-03: Fluency

Correct target language grammar, no calques (word-by-word translations that sound unnatural).

**BAD:**
```
Source: "This makes sense."
Translation (DE): "Das macht Sinn."
(calque from English; German: "Sinn ergeben" or "Sinn haben")
```

**GOOD:**
```
Source: "This makes sense."
Translation (DE): "Das ergibt Sinn."
```

### TR-QD-04: Style

Register (formal/informal), tone (technical/casual), and cultural context preserved.

**BAD:**
```
Source (technical): "Configure the endpoint."
Translation (DE, formal): "Konfiguriere den Endpunkt."
(informal imperative "Konfiguriere" in formal document)
```

**GOOD:**
```
Source (technical): "Configure the endpoint."
Translation (DE, formal): "Konfigurieren Sie den Endpunkt."
```

### TR-QD-05: Terminology

Glossary terms used consistently, with correct grammatical inflection.

**BAD:**
```
Glossary: workflow -> Arbeitsablauf
Paragraph 1: "Der Arbeitsablauf wird gestartet."
Paragraph 5: "Der Workflow wird beendet."
(inconsistent: "Arbeitsablauf" in P1, "Workflow" in P5)
```

**GOOD:**
```
Glossary: workflow -> Arbeitsablauf
Paragraph 1: "Der Arbeitsablauf wird gestartet."
Paragraph 5: "Der Arbeitsablauf wird beendet."
```

## Term Pairs

### TR-TP-01: Build Before Translating

Term pairs must exist before Step 4 (Translate). Translating without term pairs produces inconsistent terminology.

### TR-TP-02: Format

One entry per target language. Pipe-delimited. Arrow separates source from target.

**BAD:**
```
Terms: workflow = Arbeitsablauf, deployment = Bereitstellung
```

**GOOD:**
```
TRANSLATION_TERM_PAIRS_DE: workflow -> Arbeitsablauf | deployment -> Bereitstellung | repository -> Repository
TRANSLATION_TERM_PAIRS_HU: workflow -> munkafolyamat | deployment -> telepites | repository -> tarolo
```

### TR-TP-03: Grammatical Inflection

Glossary terms are base forms. Apply correct inflection in context.

**BAD:**
```
Glossary: Arbeitsablauf (workflow)
"Die Arbeitsablauf wurde gestartet."
(wrong article: "Arbeitsablauf" is masculine -> "Der")
```

**GOOD:**
```
Glossary: Arbeitsablauf (workflow)
"Der Arbeitsablauf wurde gestartet."
"Die Arbeitsabläufe wurden gestartet." (plural inflected correctly)
```

### TR-TP-04: Storage Location

- SESSION-MODE: session `NOTES.md` under `## Translation Settings ([FILENAME])`
- PROJECT-MODE: workspace `NOTES.md` under `## Translation Settings ([FILENAME])`

Reuse existing term pairs across files in a batch. Grow term pairs over multiple translation runs.

## Native Characters

### TR-NC-01: Use Native Characters

Every target language has characters that must never be replaced with ASCII approximations.

**BAD:**
```
"Vielen Dank fuer die Rueckmeldung" (DE)
"Koszonom szepen" (HU)
```

**GOOD:**
```
"Vielen Dank für die Rückmeldung" (DE)
"Köszönöm szépen" (HU)
```

Per-language reference:
- DE: ä Ä ö Ö ü Ü ß
- HU: á Á é É í Í ó Ó ö Ö ő Ő ú Ú ü Ü ű Ű
- FR: à â ç é è ê ë î ï ô ù û ü ÿ (+ uppercase)
- ES: á é í ó ú ñ ü ¿ ¡ (+ uppercase)
- PL: ą ć ę ł ń ó ś ź ż (+ uppercase)
- CS: á č ď é ě í ň ó ř š ť ú ů ý ž (+ uppercase)

### TR-NC-02: Verification Pattern

Grep for common ASCII approximations after translation:
- DE: `ae`, `oe`, `ue`, `ss` (for ß) in positions where Umlaut or ß is expected
- HU: missing accents on common words (`a` where `á` expected, `o` where `ö`/`ő` expected)
- FR: missing accents (`e` where `é`/`è`/`ê` expected)

## Structure Preservation

### TR-SP-01 through TR-SP-06

Source and target document must have identical markdown structure.

**BAD:**
```
Source:                          Translation:
## 1. Overview                   ## 1. Überblick
- Item A                         Punkt A
- Item B                         Punkt B
```
(list formatting lost)

**GOOD:**
```
Source:                          Translation:
## 1. Overview                   ## 1. Überblick
- Item A                         - Punkt A
- Item B                         - Punkt B
```

Automated verification: count headings, lists, code blocks, tables, links in source and target. Counts must match.

## Untranslatable Elements

### TR-UE-01 through TR-UE-05

Elements that must remain in source language or unchanged.

**BAD:**
```
Source: "Run `git commit -m "fix"` to save."
Translation (DE): "Führen Sie `git übertragen -m "Korrektur"` aus, um zu speichern."
(code block content translated)
```

**GOOD:**
```
Source: "Run `git commit -m "fix"` to save."
Translation (DE): "Führen Sie `git commit -m "fix"` aus, um zu speichern."
```

**BAD:**
```
Source: "See [Documentation](https://docs.example.com) for details."
Translation (DE): "Siehe [Dokumentation](https://docs.beispiel.com) für Details."
(URL translated)
```

**GOOD:**
```
Source: "See [Documentation](https://docs.example.com) for details."
Translation (DE): "Siehe [Dokumentation](https://docs.example.com) für Details."
```

## Addressing Form

### TR-AF-01: Document Decision

Before translating, determine addressing form per target language. Record in Translation MNF.

### TR-AF-02: Default to Formal

When user does not specify:
- DE: Sie (formal)
- FR: vous (formal)
- HU: Ön (formal)
- ES: usted (formal)
- IT: Lei (formal)
- PL: Pan/Pani (formal)
- JA: teineigo/desu-masu (polite) for technical; sonkeigo (honorific) for business/formal
- ZH: formal register (no pronoun-level distinction, formality expressed through word choice)

### TR-AF-03: No Mixing

**BAD (DE):**
```
"Konfigurieren Sie den Endpunkt. Dann kannst du den Service starten."
(Sie in first sentence, du in second)
```

**GOOD (DE):**
```
"Konfigurieren Sie den Endpunkt. Dann können Sie den Service starten."
```

## CJK Languages

Rules specific to Japanese (JA) and Chinese (ZH) translations. These supplement the general rules above.

### TR-CJ-01: Chinese Script Decision

Before translating to ZH, determine script variant. Record in Translation MNF.

- ZH simplified - mainland China, Singapore
- ZH traditional - Taiwan, Hong Kong, Macau

This decision affects vocabulary, not just character forms. Example: "software" = simplified: "软件", traditional: "軟體" (different words, not just character variants).

### TR-CJ-02: Japanese Honorific System

JA has three keigo levels. Select based on document register:

- **Teineigo** (desu/masu) - default for technical documentation
- **Sonkeigo** (respectful) - business correspondence, formal reports
- **Kenjougo** (humble) - rarely needed in documentation

Do not mix keigo levels within a document. Equivalent to TR-AF-03 for European languages.

### TR-CJ-03: Fullwidth Punctuation

JA and ZH use fullwidth punctuation characters. Never substitute halfwidth equivalents.

**BAD (JA):**
```
"設定を確認してください."
(halfwidth period)
```

**GOOD (JA):**
```
"設定を確認してください。"
(fullwidth period)
```

Fullwidth punctuation reference:
- Period: JA `。` ZH `。`
- Comma: JA `、` ZH `，`
- Quotation marks: JA `「」`(single) `『』`(double) / ZH `""` (simplified) `「」` (traditional)
- Parentheses: `（）`
- Exclamation: `！`
- Question: `？`
- Colon: `：`
- Semicolon: `；`

### TR-CJ-04: Japanese Transliteration

Foreign terms (loanwords, technical terms) in JA: transliterate to katakana. On first occurrence, add source term in parentheses.

**BAD:**
```
"workflowを開始します。"
(English left untranslated)
```

**GOOD:**
```
"ワークフロー（workflow）を開始します。"
(katakana transliteration with source in parentheses on first use)
```

After first occurrence, use katakana only without parenthetical source.

Terms already established in Japanese IT vocabulary (e.g., サーバー, データベース, ファイル) do not need parenthetical source.

### TR-CJ-05: Chinese Loanword Conventions

ZH loanword treatment varies by region. Follow the script decision from TR-CJ-01:

- ZH simplified (mainland): prefer translated terms over transliterations. Example: "server" = "服务器" not "伺服器"
- ZH traditional (Taiwan): may differ. Example: "server" = "伺服器" not "服务器"

When glossary has no entry for a technical term, research the standard translation for the target region.

### TR-CJ-06: CJK Verification Patterns

After translation, verify:

1. **Script consistency** (ZH) - no simplified characters in traditional output, no traditional in simplified
2. **Punctuation width** - grep for halfwidth `.` `,` `?` `!` `:` `;` in JA/ZH prose (outside code blocks). All must be fullwidth
3. **Untranslated fragments** - grep for Latin-script words in JA/ZH prose that are not in code blocks, URLs, or glossary-approved English terms
4. **Transliteration** (JA) - foreign terms use katakana, not romaji or raw English
5. **Keigo consistency** (JA) - no mixing of desu/masu with plain form (da/dearu) in same document

## Improvement Cycle

### TR-IC-01: Single-Roundtrip Reflection

Translation uses one LLM call that internally: 1) translates, 2) self-reviews across 4 dimensions, 3) outputs improved translation. See Reflection Translation Prompt Template below.

### TR-IC-02: LLM-as-Judge Verification

After translation, evaluate quality with a separate LLM call using the Quality Evaluation Prompt Template. Traditional metrics (BLEU, COMET) correlate poorly with human judgment for LLM translations. LLM-as-judge on the 4 quality dimensions is the recommended method (see `_INFO_TRANSLATION_QUALITY.md [XLATE-IN01]`).

### TR-IC-03: Targeted Fix

When a dimension rates FAIL, fix only the specific issues cited. Do not re-translate the entire section.

**BAD:**
```
Fluency FAIL: "Das System macht Sinn."
Action: Re-translate entire paragraph from scratch.
```

**GOOD:**
```
Fluency FAIL: "Das System macht Sinn."
Action: Replace "macht Sinn" with "ergibt Sinn". Keep rest of paragraph.
```

### TR-IC-04: Repeat Until PASS

```
translate (TR-IC-01)
  -> evaluate (TR-IC-02)
    -> all PASS? -> done
    -> any FAIL? -> fix specific issues (TR-IC-03)
      -> re-evaluate (TR-IC-02)
        -> repeat until all PASS or 3 iterations reached
          -> after 3 iterations: flag for human review
```

Maximum 3 improvement iterations per section. If issues persist after 3 iterations, mark section with `<!-- TRANSLATION_REVIEW_NEEDED: [dimension] -->` and continue.

## Prompt Templates

### Reflection Translation Prompt

Single LLM roundtrip for translate + self-review + improve.

**System message:**

```
You are an expert linguist specializing in translation from {SOURCE_LANG} to {TARGET_LANG}.
You produce translations that are accurate, fluent, stylistically appropriate, and terminologically consistent.
```

**User message:**

````
Translate the source text from {SOURCE_LANG} to {TARGET_LANG}.

Follow this process internally before producing output:
1. Translate the full source text.
2. Review your translation for issues in these 4 dimensions:
   (i) Accuracy - no additions, mistranslations, omissions, or untranslated text
   (ii) Fluency - correct {TARGET_LANG} grammar, spelling, punctuation; no unnecessary repetitions
   (iii) Style - matches source text register and tone; culturally appropriate for {TARGET_LANG}
   (iv) Terminology - consistent use of glossary terms; domain-appropriate; equivalent idioms
3. Fix all issues found, then output ONLY the final improved translation.

## Translation Parameters

- Addressing form: {ADDRESSING_FORM}
- Tonality: {TONALITY}
- Regional variant: {REGIONAL_VARIANT}

## Glossary (mandatory term translations)

{TRANSLATION_TERM_PAIRS}

Apply glossary terms with correct grammatical inflection (case, gender, number, tense).

## Structure Rules

- Preserve all markdown formatting exactly (headings, lists, bold, italic, links, tables)
- Do NOT translate: code blocks (fenced ``` and indented), URLs, file paths, placeholders [LIKE_THIS], HTML/XML tags
- Links: translate display text, keep URLs unchanged
- Tables: preserve column count and alignment, translate cell content
- Use native {TARGET_LANG} characters (never ASCII approximations)

## Source Text

<SOURCE_TEXT>
{SOURCE_TEXT}
</SOURCE_TEXT>

Output ONLY the final {TARGET_LANG} translation. No explanations, no notes, no markup around the translation.
````

For chunked translation, add before `## Source Text`:

```
## Previously Translated Text (for context only, do NOT re-translate)

<CONTEXT>
{PREVIOUS_TRANSLATED_CHUNKS}
</CONTEXT>
```

### Quality Evaluation Prompt

LLM-as-judge for translation quality. Used in `/verify` and `/improve`.

**System message:**

```
You are an expert translation quality evaluator for {SOURCE_LANG} to {TARGET_LANG} translations.
You evaluate with precision and flag only genuine issues.
```

**User message:**

````
Evaluate this translation across 4 quality dimensions. For each dimension, rate PASS or FAIL and cite the specific issue if FAIL.

## Dimensions

1. **Accuracy** - Are all source concepts present? Any additions, omissions, mistranslations?
2. **Fluency** - Natural {TARGET_LANG}? Grammar, spelling, punctuation correct?
3. **Style** - Matches source register? Addressing form ({ADDRESSING_FORM}) consistent?
4. **Terminology** - Glossary terms applied correctly and consistently?

## Glossary

{TRANSLATION_TERM_PAIRS}

## Source Text

<SOURCE_TEXT>
{SOURCE_SECTION}
</SOURCE_TEXT>

## Translation

<TRANSLATION>
{TRANSLATED_SECTION}
</TRANSLATION>

Output a JSON object:
```json
{
  "accuracy": {"rating": "PASS|FAIL", "issues": []},
  "fluency": {"rating": "PASS|FAIL", "issues": []},
  "style": {"rating": "PASS|FAIL", "issues": []},
  "terminology": {"rating": "PASS|FAIL", "issues": []},
  "overall": "PASS|FAIL"
}
```
Each issue: `{"text": "quoted problematic text", "suggestion": "corrected text", "reason": "why"}`
````
