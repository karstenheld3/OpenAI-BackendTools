# APAPALAN Writing Rules

Concrete enforceable rules for applying the APAPALAN principle across all document types, code, logging, and communication. Origin: `_INFO_APAPALAN_PRINCIPLE.md [APAPALAN-IN01]` (Karsten Held, 2017).

**APAPALAN** = As Precise As Possible (Priority 1), As Little As Necessary (Priority 2)

**Abstraction levels:**
- **MECT** = General principles that guide judgment. Answers: "What makes good writing?"
- **APAPALAN** (this file) = Concrete enforceable rules with measurable criteria. Answers: "How do I check compliance?" BAD/GOOD examples define the exact pattern to follow.

## Rule Index

Precision (PR) - Priority 1
- AP-PR-01: Standardized datetime format
- AP-PR-02: Standardized attribute/property format
- AP-PR-03: Standardized contact information format
- AP-PR-04: Standardized link and reference format
- AP-PR-05: Referenceable IDs on all trackable items
- AP-PR-06: Write out acronyms on first use
- AP-PR-07: Be specific - no generic or abstract writing
- AP-PR-08: Every non-obvious rule or format needs examples
- AP-PR-09: Consistent patterns (repeat established structures)
- AP-PR-10: Never abbreviate keys and references (use single quotes for literals)
- AP-PR-11: Labels decodable at point of use (full word, legend, or mnemonic)
- AP-PR-12: Explain domain jargon and idioms on first use
- AP-PR-13: Authoritative literals reproduced character-for-character (no Unicode normalization, no abbreviation, no reformatting)

Brevity (BR) - Priority 2
- AP-BR-01: Single line for single statements
- AP-BR-02: Sacrifice grammar for brevity
- AP-BR-03: DRY within same document scope
- AP-BR-04: Compact object and list definitions
- AP-BR-05: Show format over describing format
- AP-BR-06: Pipe-delimited property lines for multi-attribute items
- AP-BR-07: No redundant bold in structured lists

Structure (ST)
- AP-ST-01: Goal or intention captured first
- AP-ST-02: Subjects direct and actionable
- AP-ST-03: Self-contained units
- AP-ST-04: Anti-DRY for delegation (inline 100% for action requests)
- AP-ST-05: Hierarchical information ordering (general to specific)
- AP-ST-06: Visual thought grouping (cluster related, separate distinct)
- AP-ST-07: Cognitive load limit (max 7 ungrouped items)

Communication (CM) - outbound text to counterparts (emails, messages, replies)
- AP-CM-01: Accountable commitments - every commitment states action, deliverable, and timing
- AP-CM-02: Labeled questions and requests - own paragraph, blank-line separated, labeled (Question:/Request:), fully self-contained
- AP-CM-03: Time precision in communication - weekday + ISO date, timezone when scheduling, periods include year

Naming (NM)
- AP-NM-01: One name per concept (no polysemy, no synonyms)
- AP-NM-02: Unambiguous compound names (word order determines meaning)
- AP-NM-03: Avoid dangerous meta-words (Module, Service, Check, etc.)
- AP-NM-04: Word pairs must form intuitive opposites
- AP-NM-05: Use and keep standard terms (association field principle)

## Table of Contents

- [Core Principle](#core-principle)
- [Precision Rules (PR)](#precision-rules-pr)
- [Brevity Rules (BR)](#brevity-rules-br)
- [Structure Rules (ST)](#structure-rules-st)
- [Communication Rules (CM)](#communication-rules-cm)
- [Naming Rules (NM)](#naming-rules-nm)

## Core Principle

**Priority 1: Precision** - Never sacrifice clarity for brevity. Every statement must be unambiguous. A reader must understand exactly what is meant without guessing.

**Priority 2: Brevity** - After precision is guaranteed, remove every unnecessary word. Sacrifice grammar, filler, and noise repetition. But never sacrifice a word that carries meaning.

**Critical boundary - noise vs signal redundancy:** Brevity rules (AP-BR-*) cut NOISE words (filler, structural repetition that adds zero information). They NEVER cut SIGNAL redundancy (restated referents, concept anchors, disambiguation words that prevent the reader from guessing). A word is signal redundancy when removing it forces the reader to interpolate from memory or context. "The authentication retry handles transient network errors" repeats "authentication" and specifies "transient network" - both are signal redundancy that a brevity pass must preserve.

**Anti-pattern**: Cryptic abbreviations sacrifice precision for brevity.
- BAD: `P=1`, `F1=1` - unclear type, unclear meaning
- GOOD: `Precision=1.00`, `F1-Score=1.00` - full name, 2 decimals indicate float

**Anti-pattern**: Verbose writing sacrifices brevity without adding precision. (See AP-BR-02 for full examples.)

**Signal vs Noise:** Every design choice is either **Signal** (purposeful, carries information) or **Noise** (arbitrary, the reader interprets as meaningful when it isn't). Precision strengthens signals. Brevity eliminates noise. All APAPALAN rules serve one of these two goals.

## Precision Rules (PR)

### AP-PR-01: Standardized Datetime Format

Use `YYYY-MM-DD HH:MM` everywhere. Context-specific variations:

- In documents: `YYYY-MM-DD HH:MM` - Example: `2026-03-19 14:30`
- In logging: `YYYY-MM-DD HH:MM:SS` - Example: `2026-03-19 14:30:23`
- In filenames: `YYYY-MM-DD` prefix - Example: `2026-03-19_ServerMigration.md`, `2026-03-19_14-30_MeetingNotes.md`
- In session folders: `YYYY-MM-DD` prefix - Example: `_2026-03-19_FixAuthBug/`
- In Document History: `[YYYY-MM-DD HH:MM]` - Example: `**[2026-03-19 14:30]**`

Never use locale-dependent formats (`03/19/2026`, `19.03.2026`, `March 19, 2026`).

**BAD:**
```
March 17, 2026 2:30 PM
17.03.2026 14:30
3/17/26
last Tuesday
```

**GOOD:**
```
2026-03-17 14:30
[2026-03-17 14:30:23]  (logging only)
2026-03-17_StatusReport.md  (filename)
```

### AP-PR-02: Standardized Attribute/Property Format

Context determines format. Consistency within each context is mandatory.

**Logs**: `key='value'` with additional properties in parentheses
```
Processing library 'Documents' (id='045229b3', size=342)...
```

Documents: `Key: Value` or `- Key: Value`
```
- Started: 2026-03-17
- Goal: Fix authentication
```

**Code**: Follow language conventions (Python: snake_case, JS: camelCase)

**BAD** (mixing formats):
```
Processing file report.csv
Site URL: https://example.com
Library: Documents (id: 045229b3)
```

**GOOD** (consistent):
```
Processing file='report.csv'...
  Site: url='https://example.com'
  Library: title='Documents' (id='045229b3')
```

### AP-PR-03: Standardized Contact Information Format

Structured contact blocks with all relevant fields.

**BAD:**
```
John from Acme Corp, email john@acme.com, call him at +1 555 1234
```

**GOOD:**
```
**John Smith** (john@acme.com)
- Role: Project Manager at Acme Corp
- Phone: +1 555 1234
- Timezone: EST
```

### AP-PR-05: Referenceable IDs on All Trackable Items

**Prerequisite for AP-PR-04.** You cannot reference what has no ID. Create IDs FIRST, then reference.

**What needs IDs:**
- Requirements (FR), decisions (DD), guarantees (IG), criteria (AC)
- Problems (PR), bugs (BG), fixes (FX), failures (FL)
- Tasks (TK), steps (IS), test cases (TC)
- Sections (numbered headings: `## 1.`, `### 1.1`)
- Plan nodes (P1, P1-S1, P1-D1)

**ID formats by scope:**
- Document-scoped (2-digit): `CRAWLENG-FR-01`, `AUTHSYST-DD-03`
- Tracking (4-digit): `AUTHSYST-PR-0001`, `GLOB-BG-0002`
- Plan-scoped (ephemeral): `P1-S1`, `P2-D1`
- Headings (implicit): `## 3. Implementation` → "section 3"

**Valid ID systems:**
- Document IDs: `[TOPIC]-[TYPE][NN]` (e.g., `CRAWLENG-SP01`)
- Numbered headings: `## 1. Section` → reference as "section 1"
- Item IDs: `FR-01`, `DD-03`, `P1-S2`, `BG-0001`
- Line numbers in code: `file.py:42`

**BAD:**
```
- Toast notifications should support info, success, error types
- We decided to use localStorage
- There's a race condition in the auth flow
```

**GOOD:**
```
- **UI-FR-01**: Toast notifications support info, success, error, warning types
- **AUTH-DD-01**: Use localStorage for token storage
- **AUTH-PR-0001**: Race condition on simultaneous token refresh
```

**Document with numbered headings (implicit ID system):**
```
## 1. Overview
## 2. Requirements
### 2.1 Functional
### 2.2 Non-Functional
## 3. Design
```
Now "section 2.1" is a valid reference target.

### AP-PR-04: Standardized Link and Reference Format

**Depends on AP-PR-05.** A reference is only as good as the ID system it points to. Three steps:
1. Define a consistent ID system (AP-PR-05)
2. Apply IDs to all information that should be referenced
3. Use the IDs to reference within and across documents

**Reference formats:**
- Document: `_SPEC_CRAWLENG.md [CRAWLENG-SP01]` (filename AND Doc ID)
- Section: `section 3.2` or `CRAWLENG-FR-01`
- URL: `[Example Site](https://example.com)` (clickable Markdown)
- Cross-doc: `See CRAWLENG-FR-01 in _SPEC_CRAWLENG.md [CRAWLENG-SP01]`

**BAD:**
```
Check https://example.com for details.
See the crawler spec for requirements.
As mentioned above...
```

**GOOD:**
```
Check [Example Site](https://example.com) for details.
See `_SPEC_CRAWLER.md [CRWL-SP01]` for requirements.
Per CRWL-FR-01, the crawler must...
```

### AP-PR-06: Write Out Acronyms on First Use

Format: `Full Term (ACRONYM)`. After first use, acronym alone is acceptable within same document.

**BAD:**
```
Use OBO for SPO authentication via MI.
Check the MNF list before completing.
```

**GOOD:**
```
Use On Behalf Of (OBO) for SharePoint Online (SPO) authentication via Managed Identity (MI).
Check the MUST-NOT-FORGET (MNF) list before completing.
```

### AP-PR-07: Be Specific

No generic or abstract writing. Every statement must contain concrete, verifiable information.

**BAD:**
```
The system handles errors appropriately.
Performance should be acceptable.
The feature works as expected.
```

**GOOD:**
```
Retry 3 times with exponential backoff (1s, 2s, 4s), then fail with ERROR status.
Response time < 200ms for 95th percentile under 100 concurrent users.
Toast auto-dismisses after 5000ms, supports info/success/error/warning types.
```

### AP-PR-08: Every Non-Obvious Rule Needs Examples

Rules without examples are ambiguous. Show BAD/GOOD pairs for every format rule, naming convention, and structural pattern.

**BAD:**
```
## File Naming
Use descriptive names with proper prefixes.
```

**GOOD:**
```
## File Naming
- `_INFO_[TOPIC].md` - Research documents. Example: `_INFO_AUTHENTICATION.md`
- `_SPEC_[COMPONENT].md` - Specifications. Example: `_SPEC_CRAWLER.md`
```

### AP-PR-09: Consistent Patterns

Repeat established structures. Do not invent new forms for similar content.

**Why:** Inconsistency signals confusion or sloppiness. Same concept named multiple ways, same structure expressed differently = unclear thinking. Fix the inconsistency = fix the confusion.

**Action:** Before writing, identify the established patterns from existing documents and rules. Match it exactly.

**Detects:**
- Same concept with multiple names
- Same structure expressed differently without reason
- Overlapping forms for same purpose

**BAD/GOOD:**
- List markers: `- * +` mixed → `- - -` one form
- Headings: `## 1.` `## Design` `## IV.` → `## 1.` `## 2.` `## 3.`
- Inline enumerations: `(1) first, (2) second` → `1) first, 2) second`
- Properties: `Key:` `**Key** -` `Key =` → `Key:` throughout
- Functions: `get_` `fetch_` `load_` (same purpose) → `get_` everywhere

### AP-PR-10: Never Abbreviate Keys and References

Keys, variable names, file paths, and other referenceable identifiers must appear in full. Use single quotes to mark literal strings that can be copied or searched.

**Why:** Abbreviations force readers to mentally expand them, risking misinterpretation. Single quotes signal "this is a literal value you can copy/paste or grep for."

**Applies to:**
- Environment variable names
- Configuration keys
- File paths and filenames
- Function/method names when referenced in prose
- Database / CSV column names and JSON properties
- Any identifier the reader might need to find elsewhere

**BAD:**
```
Priority: Checked when KEY_AUTH is false.
Used when both flags above are false.
See the auth config for details.
```

**GOOD:**
```
Priority: Checked when 'AZURE_OPENAI_USE_KEY_AUTHENTICATION' is false.
Used when 'AZURE_OPENAI_USE_KEY_AUTHENTICATION'=false
and 'AZURE_OPENAI_USE_MANAGED_IDENTITY'=false.
See 'config/auth.yaml' for details.
```

**Exception:** Code blocks and monospace formatting (`backticks`) already signal literal values - single quotes are not needed inside code blocks.

### AP-PR-11: Labels Decodable at Point of Use

Every label, marker, and status indicator must be decodable where it appears - without scrolling to a definition elsewhere in the document.

**Strategies (pick one per label set):**
- **Full word** - `[SUPPORTED]`, `[ASSUMED]`, `(PASS)`. Always works.
- **Legend** - Define all short labels in a legend visible at every usage point (no scrolling). Short labels permitted under legend.
- **Mnemonic** - Designed short form where the full term is recoverable: `CMDTY` → Commodity. No legend needed.

**BAD** (opaque, no legend, no mnemonic):
```
1. [S] Team has React experience
2. [C] Dashboard is read-heavy
```

**GOOD** (full word):
```
1. [SUPPORTED] Team has React experience
2. [CAVEATED] Dashboard is read-heavy
```

**GOOD** (legend in sight):
```
S=Supported | C=Caveated | U=Unsupported
1. [S] Team has React experience - confirmed
2. [C] Dashboard is read-heavy - Q3 will shift
```

**Legend limit:** If content under one legend exceeds ~20 items or spans multiple screens, switch to full words. A legend the reader cannot see is not a legend.

**Reconstruction Test** (for mnemonics): Can the reader recover the full term from the short form alone? `CMDTY` → yes. `[S]` → no.

**Does NOT apply to:**
- Established system labels: `[ASSUMED]`, `[VERIFIED]`, `[TESTED]`, `[PROVEN]`
- Plan node IDs: `P1-S1`, `P2-D1` (positional, not classification)
- Checkbox states: `[x]`, `[ ]`, `[N]` (STRUT system)

### AP-PR-12: Explain Domain Jargon and Idioms on First Use

Like AP-PR-06 for acronyms, but for meaning: domain jargon, idioms, and figurative language must be explained or replaced on first use.

Either **replace** (jargon adds no value) or **keep + explain** in parentheses (term carries domain authority or is a citation).

**BAD:**
```
Price: FAIR TO RICH depending on execution.
Claude Code is the dark horse in this market.
```

**GOOD:**
```
Price: FAIR TO RICH (Mergers & Acquisitions valuation term: reasonably priced to slightly overpriced) depending on execution.
Claude Code is the dark horse (unexpected strong competitor) in this market.
```

**Test:** "Would a reader outside this domain understand this without looking it up?"

**Does NOT apply to:** Terms covered by AP-PR-06, terms defined earlier in same document, terms clear from immediate context.

### AP-PR-13: Authoritative Literals Reproduced Character-for-Character

Values marked `[LITERAL]` or stored in an "Authoritative Literals" section are lexical, not semantic. Every character matters. GenAI systematically introduces format drift: Unicode normalization (`º` for `o`), punctuation changes (dashes for commas), abbreviation, expansion.

**Applies to:** Addresses, IBANs, reference numbers, registration codes, certificate numbers, official names, tax IDs.

**Source of truth:** Official documents (government registrations, contracts, bank confirmations). Never copy from secondary documents without cross-referencing the authoritative source.

**BAD** (GenAI reformats IBAN - spaces, dashes, digit transposition):
```
DE89 3704 0044 0532 0130 00     (spaces inserted)
DE89-3704-0044-0532-0130-00    (dashes inserted)
DE89370400440532013000          (last 2 digits swapped - still valid MOD-97!)
```

**GOOD**: `DE89370400440532013000`

**BAD** (sub-premise loss - floor/unit dropped, address undeliverable):
```
Rua da Liberdade 42-E           (floor "3.o" lost, "Esq." → "E")
Flat 453, Tagore Road, 118923   ("Hostel" building name dropped)
港区六本木6-10-1                  (building name + floor stripped)
```

**BAD** (Unicode normalization + expansion):
```
R.ª da Liberdade, 42 - 3.º Esq.    (ª and º introduced)
Rua da Liberdade, n.º 42, 3.º Esquerdo  (abbreviation expanded)
```

**BAD** (postal code reformatting):
```
1000001         (hyphen removed from 1000-001)
SW1A1AA         (space removed from UK SW1A 1AA)
〒 100-0000     (space after 〒 symbol, Japan)
```

Full corruption categories in `core-conventions.md` "Authoritative Literals" section.

## Brevity Rules (BR)

### AP-BR-01: Single Line for Single Statements

If a statement, decision, or object fits on one line, keep it on one line.

**BAD:**
```
**Pause Button**
(requests job pause):
<button class="btn-small"
  onclick="controlJob(42, 'pause')">
  Pause
</button>
```

**GOOD:**
```
**Pause Button** (requests job pause):
<button class="btn-small" onclick="controlJob(42, 'pause')"> Pause </button>
```

### AP-BR-02: Sacrifice Grammar for Brevity

Drop articles (a, the, an), filler words (basically, actually, just), and verbose constructions when meaning is preserved.

**BAD:**
```
The system should automatically process the incoming files on a regular basis.
Before starting, you should read the relevant documents based on the current mode.
```

**GOOD:**
```
Auto-process incoming files on schedule.
SESSION-MODE: Read NOTES.md, PROBLEMS.md, PROGRESS.md, FAILS.md
```

**Exception**: User-facing text, error messages, and external communication preserve full grammar for professionalism.

### AP-BR-03: DRY Within Same Document Scope

Never repeat the same information within one document. Reference instead of restating. (For action requests to others, see AP-ST-04 which overrides this.)

**Does NOT apply to:** Concept anchors and disambiguation words that reinforce the reader's mental model. Restating a referent ("the authentication retry" instead of "it") is signal redundancy, not DRY violation. DRY targets identical BLOCKS of information, not individual words that anchor concepts.

**BAD:**
```
## Section A
Use `YYYY-MM-DD HH:MM` format for all timestamps.

## Section B
Remember to use `YYYY-MM-DD HH:MM` format for timestamps here too.
```

**GOOD:**
```
## Section A
Use `YYYY-MM-DD HH:MM` format for all timestamps.

## Section B
Timestamps follow AP-PR-01.
```

### AP-BR-04: Compact Object and List Definitions

Use lists. No empty lines between properties. No Markdown tables (unless opted-in).

**BAD:**
```
### EXPLORE

**Purpose**: Understand the situation before acting

**BUILD focus**: What feature? What constraints?

**Entry**: Start of workflow
```

**GOOD:**
```
### EXPLORE

- Purpose: Understand the situation before acting
- BUILD: What feature? What constraints?
- Entry: Start of workflow
```

### AP-BR-05: Show Format Over Describing Format

A format example communicates more precisely and more briefly than a description.

**BAD:**
```
## Todo Format
Todos should start with a bold timestamp in YYYY-MM-DD HH:MM format,
followed by a dash, then the item description, then optionally a deadline
in the same format preceded by "Deadline:", then a status field.
```

**GOOD:**
```
## Todo Format
`- **YYYY-MM-DD HH:MM** - Item description - Deadline: YYYY-MM-DD, Status: TODO:ACTION`

Example:
- **2026-03-15 09:15** - Reply to John with proposal - Deadline: 2026-03-20, Status: TODO:REPLY
```

### AP-BR-06: Pipe-Delimited Property Lines for Multi-Attribute Items

For items with many properties, use ` | ` (pipe with spaces) to separate values on a single line.

**Format:** `Key: value | Key: value | ...` - always use `Key: Value` pairs separated by ` | `. Bold ID starts the first line. Group related properties per line.

**When to use:** 4+ properties, catalog items, metadata headers, anything where vertical lists waste space.
**When NOT to use:** Long values, nested data, fewer than 4 properties.

**BAD** (12 lines for one item):
```
### SRV-042
- **Region**: eu-west-1
- **Type**: m5.xlarge
- **CPU**: 4 vCPU
- **RAM**: 16 GB
- **Storage**: 200 GB SSD
- **Status**: running
- **Uptime**: 45 days
```

**BAD** (pipe-delimited but bare values - reader must guess what each field means):
```
**SRV-042** eu-west-1 | m5.xlarge | 4 vCPU | 16 GB | 200 GB SSD
running | 45 days
```

**GOOD** (same data, every value labeled):
```
**SRV-042** Region: eu-west-1 | Type: m5.xlarge | CPU: 4 vCPU | RAM: 16 GB | Storage: 200 GB SSD
- Status: running | Uptime: 45 days
```

**BAD** (missing fields, partial metadata):
```
From: john@example.com
To: me@example.com
Subject: Re: Q2 Timeline
```

**GOOD** (all fields present, `-` for empty):
```
From: john@example.com | To: me@example.com | CC: team@example.com | BCC: -
- Subject: Re: Q2 Timeline | Reply-To: - | Thread: Q2 Planning | Message-ID: abc123
- Date: 2026-03-17 14:30 | Attachments: Q2_Timeline.pdf (1.2MB)
```

**BAD** (mixed formats, inconsistent labels):
```
PRD-007 - Widget Pro v2.1, costs $49.99, in stock
12x8x4 cm, 250g, available in black and silver, made of aluminum
```

**GOOD** (consistent Key: Value, grouped by concern):
```
**PRD-007** Name: Widget Pro | Version: 2.1 | Price: $49.99 | Stock: yes
- Dimensions: 12x8x4 cm | Weight: 250g | Color: black, silver | Material: aluminum
- Link: https://example.com/products/widget-pro
- Status: DISCONTINUED (replaced by PRD-012)
```

**Conventions:**
- Always `Key: Value` format - no bare values without labels
- Bold ID on header line
- `?` for unknown values in documents (`[UNKNOWN]` is for logs)
- Group by concern: identity/metrics, physical attributes, terms/status

### AP-BR-07: No Redundant Bold in Structured Lists

Implements MECT principle MW-LT-04 (every formatting signal must carry information).

Bold is a signal. It must introduce something the reader encounters for the first time or mark a context switch. When structure (indent, dash, colon) already provides visual distinction, bold on labels is noise.

**Decision: bold or not?**

```
Is the label a NEW CONCEPT being defined here for the first time?
├─ Yes -> Bold. Reader must notice and remember this term.
└─ No
   Is the label a CONTEXT SWITCH (BAD/GOOD, "In code:", "In email:")?
   ├─ Yes -> Bold. Reader must notice the boundary.
   └─ No
      Is the label an ACTION STEP in a procedure (the bold IS the instruction)?
      ├─ Yes -> Bold. Reader must know what to DO.
      └─ No -> No bold. Structure provides distinction.
```

**Examples where bold IS appropriate:**
- Concept definitions: `- **Intentional** - WHY it was introduced`
- Context switches: `**BAD:**`, `**In code:**`, `**In email:**`
- Procedure steps: `1. **Start with most explicit name**: ...`
- Rule indexes and section labels

**Examples where bold is NOT appropriate:**
- Uniform key-value lists: `- In documents: ...`, `- In logging: ...`
- Classification lists: `- Stakeholders need ...`, `- Developers need ...`
- Dictionary entries: `- must - obligation`, `- should - recommendation`
- Examples applying an already-defined concept: `Intentional: "Prevents..."`

**BAD** (redundant bold on every label):
```
**Contacts:**
- **South Office**: 289 897 380 (Mon-Fri 9-13h, 14-17h)
- **Head Office**: +351 21 842 53 00 (Mon-Fri 9-18h)
- **Contact Person**: Maria Silva (Customer Service)
```

**GOOD** (structure provides distinction):
```
**Contacts:**
- South Office: 289 897 380 (Mon-Fri 9-13h, 14-17h)
- Head Office: +351 21 842 53 00 (Mon-Fri 9-18h)
- Contact Person: Maria Silva (Customer Service)
```

## Structure Rules (ST)

### AP-ST-01: Goal or Intention Captured First

Every document, section, and communication starts with purpose. Reader knows WHY before HOW.

**BAD:**
```
# Verify Workflow

## Required Skills
...

## Steps
1. Read documents
2. Check rules
```

**GOOD:**
```
# Verify Workflow

Goal: Validated work with all issues identified and labeled
Why: Prevents shipping bugs, spec violations, and rule breaks

## Required Skills
...
```

### AP-ST-02: Subjects Direct and Actionable

Email subjects, headings, and labels state the action or outcome, not the topic.

**BAD:**
```
Subject: Meeting
Subject: Update
Subject: Question about the project
### Authentication Section
```

**GOOD:**
```
Subject: ACTION: Review contract by 2026-03-20
Subject: FYI: Q2 timeline moved to April 15
Subject: DECISION NEEDED: Choose auth provider by Friday
### AUTH-DD-01: Use JWT with httpOnly Cookie Storage
```

### AP-ST-03: Self-Contained Units

Each log line, document section, email, or message must be understandable without reading other materials. Ask: "Can the reader act on this without seeking additional information?"

**BAD:**
```
As discussed, please proceed with option 2.
See previous email for details.
```

**GOOD:**
```
Please proceed with Option 2: JWT tokens stored in httpOnly cookies
with 15-minute expiry and silent refresh. Implementation guide
attached (auth_impl_v2.pdf).
```

**In logs** (Full Disclosure principle):
```
BAD:  [ 1 / 2 ] LLM extraction run 1...
GOOD: [ 1 / 2 ] Calling gpt-5-mini to extract 5 records from 20 rows...
```

### AP-ST-04: Anti-DRY for Delegation (overrides AP-BR-03)

When requesting action from others, inline ALL needed information. Do NOT reference threads or external docs as the only source. People do not read referenced sources. This overrides AP-BR-03 (DRY) because the audience is different: BR-03 avoids self-repetition for a reader who has the full document; ST-04 ensures a recipient can act without seeking additional sources.

**BAD:**
```
Hi John,

As per our discussion and the attached spec (see section 3.2),
please implement the changes we agreed on.

Thanks
```

**GOOD:**
```
Hi John,

Please implement these 3 changes to the auth module by 2026-03-25:

1. Replace localStorage token storage with httpOnly cookies
   - Set SameSite=Strict, Secure=true
   - Implementation: src/auth/tokenStore.js

2. Add silent token refresh 5 minutes before expiry
   - Use /api/auth/refresh endpoint
   - Retry 3 times with 2s backoff

3. Add mutex lock for concurrent refresh requests
   - Only one refresh request at a time
   - Queue subsequent requests until first completes

Full spec: _SPEC_AUTH.md [AUTH-SP01] section 3.2
Previous discussion: [Email 2026-03-15](#2026-03-15-1430---auth-design-review)
```

### AP-ST-05: Hierarchical Information Ordering

Order information from general to specific. Most important first, details follow.

**BAD:**
```
The button uses a 4px border radius with #0078d4 color and sends a POST
request to /api/jobs/start which creates a new crawl job for the site.
It's the main action button on the dashboard.
```

**GOOD:**
```
[Start Job] - Creates new crawl job via POST /api/jobs/start.
Dashboard main action. Style: #0078d4, 4px border-radius.
```

### AP-ST-06: Visual Thought Grouping

Related content clusters together (no empty lines); distinct thoughts separate by one empty line. Applies to specs, emails, code, logs.

**Principle:** Whitespace creates visual paragraphs. Items that form one logical unit have no empty lines between them. Distinct units separate by exactly one empty line.

**BAD** (scattered - each line isolated):
```
- **Started**: 2026-03-17

- **Goal**: Fix authentication

- **Status**: In Progress


## Next Section
```

**GOOD** (grouped by concern):
```
- **Started**: 2026-03-17
- **Goal**: Fix authentication
- **Status**: In Progress

## Next Section
```

**In logs** (from LOGGING-RULES.md - Announce/Track/Report pattern):
```
Connecting to 'https://contoso.sharepoint.com/sites/ProjectA'...
  OK. Connected in 1.2 secs.
Processing 3 libraries...
  [ 1 / 3 ] Processing library 'Documents'...
    342 files retrieved.
    OK.
  [ 2 / 3 ] Processing library 'Reports'...
    ERROR: Access denied -> (403) Forbidden
  [ 3 / 3 ] Processing library 'Archive'...
    SKIP: Library empty.
  FAIL: 2 libraries processed, 1 failed.
```
No empty lines within one activity; indentation shows nesting; activities separate naturally.

**In code:**
```python
# BAD - scattered related statements
user = get_user(id)

token = generate_token(user)

response = send_auth(token)


# GOOD - grouped by concern
user = get_user(id)
token = generate_token(user)
response = send_auth(token)

log_success(user, response)
notify_admin(response)
```

**In email:**
```
# BAD - wall of separated lines
Hi John,

Please review the attached.

Deadline is Friday.

Let me know if questions.

Thanks


# GOOD - grouped by purpose
Hi John,

Please review the attached contract by Friday.
Let me know if you have questions.

Thanks
```

### AP-ST-07: Cognitive Load Limit

People can hold roughly 5 to 7 separate items in working memory at once (Miller's Law). Lists, parameters, or sections that exceed this limit without grouping cause readers to skip, re-read, or abandon the content.

**Rule:** When a flat list exceeds 7 items, group into named clusters. When a section addresses more than 5 distinct concerns, split into subsections.

**BAD** (9 ungrouped action points - reader stops after 5):
```
Hi John,

Before the release on Friday, please:
- Update the API documentation for the new endpoints
- Run the integration tests on staging
- Fix the failing auth test in CI
- Review Maria's PR for the rate limiter
- Notify the QA team that staging is ready
- Update the changelog with all merged PRs
- Check that SSL certificates are renewed before April
- Send the release notes draft to stakeholders
- Schedule the deployment window with ops
```

**GOOD** (grouped by concern - reader processes 3 clusters of 3):
```
Hi John,

Before the release on Friday, please:

Code:
- Fix the failing auth test in CI
- Review Maria's PR for the rate limiter
- Run the integration tests on staging

Documentation:
- Update the API documentation for the new endpoints
- Update the changelog with all merged PRs
- Send the release notes draft to stakeholders

Coordination:
- Notify the QA team that staging is ready
- Check that SSL certificates are renewed before April
- Schedule the deployment window with ops
```

**Applies to:**
- Document lists and bullet points
- Email action items (>5 points = readers stop reading)
- Function parameters (>5 = use options object or config struct)
- Menu items, navigation tabs, dashboard panels
- Spec requirements per section

**When grouping is not needed:**
- Ordered steps (sequence provides structure: step 1, 2, 3... up to ~10)
- Exhaustive lookup lists where completeness is key (e.g., all country codes, all error codes, all supported file types). Grouping these adds noise because the reader needs to scan quickly, not memorize. Keep existing sequence or topology if one exists; if none, sort alphabetically.
- Rule indexes (this document - grouped by category)

## Communication Rules (CM)

Rules for outbound text to counterparts: emails, WhatsApp messages, replies, meeting requests. These apply when writing TO another person, not when writing documents, code, or logs.

**Scope distinction**: PR/BR/ST/NM rules apply to all text (documents, code, logs, communication). CM rules apply ONLY to outbound communication where a counterpart reads and acts.

### AP-CM-01: Accountable Commitments

Every commitment in outbound communication states WHAT the counterpart receives and WHEN: action, deliverable, weekday + ISO date + time. Vague actions leave the counterpart guessing and force follow-up questions.

**BAD** (counterpart does not know what to expect):
```
I'll sign tomorrow.
We'll take care of the heating issue soon.
I'll look into the invoice.
```

**GOOD** (action, deliverable, timing explicit):
```
I'll send the signed contract back tomorrow (Friday, 2026-07-17) by 12:00 CET.
The plumber comes Friday, 2026-07-17, 09:00-12:00. I'll confirm by email once the heating works.
I'll check the invoice and send you the payment confirmation by tomorrow evening (Friday, 2026-07-17, 18:00 CET).
```

**Relates to** AP-PR-07 (Be Specific) and AP-ST-03 (Self-Contained Units): a commitment is a promise - it must be precise enough that the counterpart can hold you to it without asking clarifying questions.

### AP-CM-02: Labeled Questions and Requests

Every question and call-to-action stands in its own paragraph, separated by blank lines, labeled and fully self-contained. Label questions with "Question:" and action requests with "Request:" (DE: Frage/Bitte, FR: Question/Demande, ES: Pregunta/Solicitud). The ask carries its own context - the counterpart understands it without re-reading.

**BAD** (ask buried in paragraph, unlabeled, not self-contained):
```
I reviewed the contract and the terms look fine to me and I was wondering
if we could maybe also talk about the timeline. Agreed?
```

**GOOD** (labeled, self-contained question in own paragraph):
```
I reviewed the contract - the terms look fine to me.

Question: Can we discuss the project timeline in our meeting on Tuesday, 2026-03-24?
```

**GOOD** (labeled request with explicit timing):
```
I've prepared the updated proposal with the Q2 2026 numbers.

Request: Can you please review the attached proposal and send your feedback by Friday, 2026-07-17 18:00 CET?
```

**Relates to** AP-ST-04 (Anti-DRY for Delegation): ST-04 says inline 100% for action requests. CM-02 adds the structural requirement: own paragraph, blank-line separation, label prefix, and self-containment test ("Can the counterpart answer/act without re-reading?").

### AP-CM-03: Time Precision in Communication

State dates as weekday + ISO date, times as `HH:MM` with timezone when scheduling across locations. Periods include the year. The weekday adds disambiguation in the reader's mind.

**BAD:**
```
Let's meet Tuesday at 2pm.
The Q2 numbers look good.
The first installment is due next month.
```

**GOOD:**
```
Let's meet Tuesday, 2026-03-24 14:00 CET.
The Q2 2026 numbers look good.
The first installment is due next month (August, 2026-08).
```

**Language equivalents** (weekday in target language):
- DE: "Freitag, 2026-07-17"
- FR: "vendredi 2026-07-17"
- ES: "viernes, 2026-07-17"

**Seasonal timezone rule** (Europe/Berlin): CET (UTC+1) applies last Sunday of October through last Sunday of March. CEST (UTC+2) applies last Sunday of March through last Sunday of October. Never use "CET" as generic catch-all. Check the scheduled date's season and use the correct abbreviation. If the conversation file states a timezone explicitly, use that exact abbreviation.

**BAD:**
```
Let's meet Wednesday, 2026-08-19 11:00 CET.
```
August = summer = CEST, not CET.

**GOOD:**
```
Let's meet Wednesday, 2026-08-19 11:00 CEST.
```

**Relates to** AP-PR-01: PR-01 defines the format (`YYYY-MM-DD HH:MM`). CM-03 adds the disambiguation requirements for communication: weekday prefix, timezone when cross-location, year on period references.

## Naming Rules (NM)

### AP-NM-01: One Name Per Concept

One concept = one name, used everywhere. No synonyms, no polysemy.

**Why:** Synonyms cause search failures. Polysemy causes silent misunderstandings - people THINK they agree when they don't.

**BAD:**
```
"garage" / "service" / "workshop"  (3 names for same concept)
"car tickets" (UI) vs "service events" (internal) vs "service tickets" (nested)
```

**GOOD:**
```
"workshop" everywhere - UI, API, database, documentation, conversations
```

**BAD** (polysemy):
```
"Meter" = connection point AND physical device AND customer relationship
```

**GOOD:**
```
"MeterPoint" (connection), "MeterDevice" (physical), "MeterContract" (customer)
```

### AP-NM-02: Unambiguous Compound Names

Word order determines meaning. If a compound name has multiple readings, restructure it.

**BAD:**
```
EmptyCollectionKey    → Is the collection empty, or is the key empty?
InvalidUserInput      → Is the user invalid, or is the input invalid?
```

**GOOD:**
```
KeyOfEmptyCollection  → Unambiguous: the collection is empty
InputFromInvalidUser  → Unambiguous: the user is invalid
```

### AP-NM-03: Avoid Dangerous Meta-Words

Words that seem specific but hide ambiguity. When you must use them, qualify them.

**Dangerous words:** Module, Service, Generation, Check, Payload, Workload, Cargo, Network, Monitor, View, Console, Facade, Provider, Asset

**BAD:**
```
ProductModule         → Does Product contain Module or Module contain Product?
UserService           → Named after consumer, provider, or product?
Check                 → Result yes/no ("check if") or always yes ("perform check")?
```

**GOOD:**
```
ProductCatalog        → Clear what it is
UserAuthProvider      → Clear role
ValidateUserExists    → Clear: returns yes/no
RunDataCleanup        → Clear: performs action
```

### AP-NM-04: Intuitive Word Pairs

Opposites must form intuitive pairs. Users predict the counterpart from the first name.

**BAD:**
```
ReferenceObject / DifferenceObject   → Users expect Current/Target or Before/After
EncodeUrl() / PlainText()            → Users search for DecodeUrl(), fail to find it
Concat() (joins rows) / join() (joins strings)  → Swapped from every other platform
```

**GOOD:**
```
CurrentObject / TargetObject
EncodeUrl() / DecodeUrl()
JoinRows() / ConcatStrings()
```

### AP-NM-05: Use and Keep Standard Terms

Use established terminology. When deviating intentionally, state the deviation and reason. If a name worked for years, don't rename it - even if it became a misnomer. People predict behavior by the evoked association field, not the literal name.

**BAD:**
```
The data holder sends info to the checker which puts it in the box.
Renamed login() → authenticate()  because system no longer requires credentials
Renamed save() → persist()        because it now writes to cloud, not disk
```

**GOOD:**
```
The API client sends the payload to the validator which persists it to the message queue.
Keep login()   → "Login" already means "authenticate" in users' minds
Keep save()    → "Save" already means "persist my work" regardless of storage
Build new API if behavior actually changes: login() stays, add sso_connect() for new flow
```

**Intentional deviation:**
```
"Activity" (not "task") - we use "task" for TASKS documents, so "activity" avoids term collision.
```

Like "horsepower" doesn't mean horses powering a car - it's the association field, not the name.
