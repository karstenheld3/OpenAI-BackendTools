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
- Full natural grammar: "I", "the", "a" preserved (CV-HM-07)
- Never invent greetings/closings - use user's habitual forms (CV-HM-06)
- Structural sections (Log, Todos, Status) = zero humanizing (CV-HM-01)

## Trigger

- `/conversation-draft` - User wants a draft email or message
- `/conversation-draft [counterparty]` - With explicit target
- Implicit: User asks to "draft", "write", "reply" in conversation context

# EXECUTION

## Step 1: Read Context

1. Read target `CONVERSATION_[COUNTERPARTY].md`:
   - Humanizing Settings, Translation Settings
   - Last 3-5 History entries (voice calibration)
   - Status and open Todos (content)
2. Read `APAPALAN_RULES.md` Communication (CM) section
3. Read `CONVERSATION_HUMANIZING_RULES.md` Anti-Pattern Index

## Step 2: Extract Writing Profile

Use Humanizing Settings if populated. Otherwise extract from History:
- Greeting/closing forms (per context)
- Sentence length pattern (burstiness)
- Discourse markers and frequency
- Register (formal/informal, varies by recipient?)
- Spelling variants

## Step 3: Compose Draft

1. **Layer 1** - Write content per MECT + APAPALAN CM rules
2. **Layer 2** - Apply format per `CONVERSATION_RULES.md` (headers, datetime, translation)
3. **Layer 3** - Apply voice per `CONVERSATION_HUMANIZING_RULES.md` (CV-HM-01 through CV-HM-07)

## Step 4: Verify

Scan draft against Anti-Pattern Index in `CONVERSATION_HUMANIZING_RULES.md`. Fix all violations.

## Quality Gate

- [ ] AP-CM-01, AP-CM-02, AP-CM-03 satisfied
- [ ] Anti-Pattern Index: zero violations
- [ ] Draft marked `**STATUS: DRAFT - NOT SENT**` if email

## Output

`Draft ready: [type] to [counterparty] - [subject/topic]`
