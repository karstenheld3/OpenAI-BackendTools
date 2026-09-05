---
description: Draft emails, WhatsApp messages, or other text AS the user
---

# Draft Conversation Workflow

Draft outbound text AS the user - matching their voice while maintaining precision.

**Goal**: Draft ready for user review that sounds like them and contains zero precision gaps

**Why**: Three rule layers must compose correctly. Missing any layer produces either generic text (missing humanizing) or imprecise text (missing APAPALAN Communication rules).

Scope: Drafts only. Use `/conversation-start` to create, `/conversation-update` to append.

## Required Skills

- @skills:write-documents for `CONVERSATION_HUMANIZING_RULES.md`, `CONVERSATION_RULES.md`, `APAPALAN_RULES.md`, `MECT_WRITING_RULES.md`

## Rule Layers (Priority Order)

Three layers compose every draft. Higher priority wins on conflict:

```
Layer 1 - MECT + APAPALAN Communication (precision, clarity)
├─ MECT baseline: explicit terminology, deliberate redundancy for concept matching
├─ AP-CM-01: Accountable commitments
├─ AP-CM-02: Labeled questions/requests
└─ AP-CM-03: Time precision

Layer 2 - CONVERSATION_RULES.md (format)
└─ CV-EM-*, CV-WA-*, CV-DT-*, CV-TR-*

Layer 3 - CONVERSATION_HUMANIZING_RULES.md (voice)
└─ CV-HM-01 through CV-HM-07
```

**Conflict resolution**: Precision (Layer 1) always wins. Humanizing (Layer 3) never weakens precision or clarity.

**AP-BR-02 exception**: "Sacrifice grammar for brevity" applies to agent documents, NEVER to user-voice drafts. Keep full natural grammar (CV-HM-07).

## MUST-NOT-FORGET

- Read `CONVERSATION_HUMANIZING_RULES.md` Anti-Pattern Index before finalizing
- Read `APAPALAN_RULES.md` Communication (CM) section
- AP-CM-01, AP-CM-02, AP-CM-03 apply to every draft in every language
- WEEKDAY VERIFICATION: When writing any weekday-date combination, ALWAYS verify via web search first. Never calculate mentally. Never contradict user's weekday without search proof (CV-DT-04, GLOB-FL-0051)
- TIMEZONE VERIFICATION: Use the timezone stated in Persons Involved. CET = Oct-Mar (UTC+1), CEST = Mar-Oct (UTC+2). Never default to "CET" without checking season (GLOB-FL-0054)
- QUESTION LABEL: Every sentence ending in `?` MUST have `Question:` or `Frage:` prefix (AP-CM-02, GLOB-FL-0053)
- Full natural grammar: "I", "the", "a" preserved (CV-HM-07)
- Never invent greetings/closings - use user's habitual forms (CV-HM-06)
- Structural sections (Log, Todos, Status) = zero humanizing (CV-HM-01)
- When a CONVERSATION file is referenced or loaded, ALWAYS write draft to that file (Step 6)

## Trigger

- `/conversation-draft` - User wants a draft email or message
- `/conversation-draft [counterparty]` - With explicit target
- Implicit: User asks to "draft", "write", "reply" in conversation context

# EXECUTION

## Step 1: Determine Context and Target

Identify counterparty and output target before reading anything:

1. **Counterparty** - From `/conversation-draft [counterparty]`, loaded session, referenced file, or conversation context
2. **Conversation file** - Locate `CONVERSATION_[COUNTERPARTY].md`. Sources: explicit reference, `/session-load`, open IDE files, conversation folder
3. **Output target**:
   - **File + chat** (default): Conversation file exists or is identifiable. Draft written to file AND presented in chat for review
   - **Chat-only** (fallback): No conversation file exists or identifiable. Draft presented in chat only. Note: `ANCHORING: INSUFFICIENT_HISTORY`

## Step 2: Read Context

1. Read target `CONVERSATION_[COUNTERPARTY].md` (when target = file):
   - Humanizing Settings, Translation Settings
   - Last 3-5 History entries (voice calibration)
   - Status and open Todos (content)
2. Read `APAPALAN_RULES.md` Communication (CM) section
3. Read `CONVERSATION_HUMANIZING_RULES.md` Anti-Pattern Index

## Step 3: Extract Writing Profile

Use Humanizing Settings if populated. Otherwise extract from History:
- Greeting/closing forms (per context)
- Sentence length pattern (burstiness)
- Discourse markers and frequency
- Register (formal/informal, varies by recipient?)
- Spelling variants

## Step 4: Compose Draft

1. **Layer 1** - Write content per MECT + APAPALAN CM rules
2. **Layer 2** - Apply format per `CONVERSATION_RULES.md` (headers, datetime, translation)
3. **Layer 3** - Apply voice per `CONVERSATION_HUMANIZING_RULES.md` (CV-HM-01 through CV-HM-07)

## Step 5: Verify

Scan draft against Anti-Pattern Index in `CONVERSATION_HUMANIZING_RULES.md`. Fix all violations.

**AP-CM-02 checklist** (every `?` sentence):
1. Own paragraph (blank-line separated)
2. Labeled with `Question:`/`Request:` (or language equivalent)
3. Self-contained (counterpart understands without re-reading)

**AP-CM-03 timezone check**:
- Read timezone from Persons Involved section
- Verify abbreviation matches season of scheduled date (CET Oct-Mar, CEST Mar-Oct)

## Step 6: Write to Conversation File

When target = file (determined in Step 1), write the draft to `CONVERSATION_[COUNTERPARTY].md`:

1. **History** - Add entry at top with `STATUS: DRAFT - NOT SENT`, email header (CV-EM-01), and full draft body
2. **Log** - Add entry linking to History anchor
3. **Todos** - Add entry with `TODO:REPLY` status

Present draft in chat for user review AND persist to file. The chat output is for review; the file write is the conversation record (CV-EM-04).

## Quality Gate

- [ ] AP-CM-01, AP-CM-02, AP-CM-03 satisfied
- [ ] AP-CM-02: every question labeled with `Question:`/`Frage:`/`Request:`
- [ ] AP-CM-03: timezone matches season (CET Oct-Mar, CEST Mar-Oct)
- [ ] Anti-Pattern Index: zero violations
- [ ] Draft marked `**STATUS: DRAFT - NOT SENT**` if email
- [ ] Draft written to CONVERSATION file (History, Log, Todo) when conversation is referenced

## Output

`Draft ready: [type] to [counterparty] - [subject/topic]`
