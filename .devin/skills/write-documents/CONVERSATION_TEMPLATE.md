# Conversation: [Name or Description]

**Filename**: `CONVERSATION_[COUNTERPARTY].md` - CV-FL-01

## MUST-NOT-FORGET

- DATETIME FORMAT: Use `YYYY-MM-DD HH:MM` everywhere (logs, todos, headings, attachments) - CV-DT-01
- CHRONOLOGICAL ORDER: History section = newest on top, oldest at bottom (reverse chronological) - CV-DT-02
- TRANSLATION FORMAT: All non-English text MUST be followed by English translation in quote block - CV-TR-01, CV-TR-02
  - Format: `**Person (HH:MM)**: Original text here.`
  - Next line: `> English translation here.`
  - Example:
    ```
    **Person (11:49)**: Non-English text here.
    > English translation here.
    ```
- NATIVE CHARACTERS: When writing in non-English languages, use native special characters (e.g., German Umlaute: ae → ä, oe → ö, ue → ü, ss → ß). Never substitute with ASCII approximations - CV-TR-03
- AUTO-TRANSLATE: Translate all languages except `CONVERSATION_DO_NOT_TRANSLATE_LIST` - CV-TR-04
- TERM PAIRS: Use `TRANSLATION_TERM_PAIRS` for consistent translation - CV-TR-05
- DOUBLE LANGUAGE: Use `[ENGLISH] / [LOCAL]` in log summaries, key outcomes, status, todos - CV-TR-06
- WEEKDAY VERIFICATION: When writing any weekday-date combination, ALWAYS verify via web search first. Never calculate mentally. Never contradict user's weekday without search proof - CV-DT-04
- SEND EMAILS VIA PLAYWRIGHT GMAIL UI - NEVER use CLI tools to send (body encoding fails) - CV-EM-02
- Email header format: `From: | To: | CC: | BCC: | Subject: | Reply-To: | Thread: | Message-ID:` - CV-EM-01
- History heading format: `### YYYY-MM-DD HH:MM - Summary` - CV-ST-04
- Log entry format: `- **YYYY-MM-DD HH:MM** - Main topic` with anchor to History - CV-ST-03
- Todo format: `- **YYYY-MM-DD HH:MM** - Item - Deadline: YYYY-MM-DD, Status: TODO:[ACTION]/DONE` - CV-TD-01
- Todo actions: `TODO:REPLY`, `TODO:REVIEW`, `TODO:PAY`, `TODO:PLAN`, `TODO:SCHEDULE_CALL` (web), `TODO:SCHEDULE_TRIP`, `TODO:SCHEDULE_MEETING` (in person) - CV-TD-02
- Attachment folders: binaries in `Attachments_gitignore/YYYY-MM-DD_HH-MM_[Topic]/`, text files in `Attachments/YYYY-MM-DD_HH-MM_[Topic]/` - CV-AT-04, CV-AT-05
- AUTO-TRANSCRIBE: When enabled, transcribe attachments via `/transcribe` (1 candidate, 120dpi, min-score=4.5) - CV-AT-03
- All URLs as Markdown clickable links: `[Title](https://...)` - CV-LN-01
- ALL LINKS ABSOLUTE: File paths, attachment references, and source links MUST be full absolute clickable paths. Never use relative paths or `...` abbreviations - CV-LN-04
- LINKS COMPLETENESS: All attachments, transcriptions, translations recorded in Links section - CV-LN-03
- CHECK DOWNLOADED IMAGES - After downloading, review each image. Delete signature icons, logos, spacers, and other email template garbage. Keep only real attachments - CV-AT-01
- No markdown tables except when sent in emails
- HUMANIZING: When drafting AS user, apply MECT/APAPALAN as baseline + 1-5% humanizing (CV-HM-*). Humanizing adds texture, not imprecision - CV-HM-01
- CONSISTENCY ANCHORING: Analyze user's prior messages before first draft. Extract greeting/closing, sentence length, punctuation, discourse markers - CV-HM-02
- SPELLING VARIANTS: Same word = same spelling every time. Track in SPELLING_VARIANTS - CV-HM-03
- SENTENCE RHYTHM: Vary sentence length. No 3+ consecutive sentences of similar word count - CV-HM-05
- QUESTIONS/CTA IN OWN PARAGRAPH: Every question and call-to-action in its own paragraph, separated by blank lines, labeled (Question:/Request:), fully self-contained - AP-CM-02
- ACCOUNTABLE COMMITMENTS: Every commitment states action, deliverable, and timing - AP-CM-01
- TIME PRECISION: Weekday + ISO date, HH:MM with timezone when scheduling; periods include year - AP-CM-03

## Ignore Files

Files matching these patterns should NOT be downloaded. If downloaded, delete them.

`line.png` | `space.png` | `*-logo*.png` | `i-facebook*.png` | `i-instagram*.png` | `i-link*.png` | `image-horizontal*.png` | `Outlook-*.png`

## Translation Settings

- **CONVERSATION_AUTO_TRANSCRIBE_ATTACHMENTS**=true
- **CONVERSATION_AUTO_TRANSLATE**=true
- **CONVERSATION_DO_NOT_TRANSLATE_LIST**: English, ...
- **TRANSLATION_TERM_PAIRS**: [TERM1_LOCAL] -> [TERM1_ENGLISH] | [TERM2_LOCAL] -> [TERM2_ENGLISH] | ...

## Humanizing Settings

- **SPELLING_VARIANTS**: [standard orthography]
- **DISCOURSE_MARKERS**: [use language defaults, 1-2 per message]
- **GREETING_VARIANTS**: [extract from first user message]
- **CLOSING_VARIANTS**: [extract from first user message]
- **SENTENCE_LENGTH_PROFILE**: [short: 30%, medium: 40%, long: 30%]
- **ANCHORING**: INSUFFICIENT_HISTORY

## Status

**Current**: [ACTIVE / AWAITING_RESPONSE / ON_HOLD / COMPLETED]

### Todos and Deliverables

- **2026-03-16 10:30** - DRAFT: Follow-up proposal to Jane - Status: TODO:REPLY
- **2026-03-15 09:15** - Send proposal draft - Deadline: 2026-03-20, Status: TODO:REPLY
- **2026-03-17 14:30** - Review contract terms - Status: DONE

## Links and shared documents

- **2026-03-15 09:15** - Some websites to check
  - [Website Title](https://example.com)
- **2026-03-17 14:30** - Document title
  - [Document.pdf](Attachments_gitignore/2026-03-17_14-30_Topic/Document.pdf)
  - [Document.md](Attachments/2026-03-17_14-30_Topic/Document.md) (transcription)
  - [Document_en.md](Attachments/2026-03-17_14-30_Topic/Document_en.md) (translation)

## Conversation Context

### Persons Involved

**[Contact Name]** (contact@example.com)
- Role: [Role at Organization]
- Phone: [+XX XXX XXX XXXX]
- Timezone: [TZ]
- Notes: [Communication preferences]

**[Second Contact]** (second@example.com)
- Role: [Role]
- Notes: [Relevant notes]

**[Your Name]** (your@email.com)
- Role: Me

### Topics

- **Topic 1** - Brief description
- **Topic 2** - Brief description

## Log

- **2026-03-17 14:30** - Discussed Q2 timeline adjustments
  - Decision: Move milestone 2 to April 15
  - Action: Send updated document by Friday
  - Attachment: [Doc.pdf](Attachments_gitignore/2026-03-17_14-30_Topic/Doc.pdf) | [Doc.md](Attachments/2026-03-17_14-30_Topic/Doc.md)
  - [Email](#2026-03-17-1430---q2-timeline-discussion)
- **2026-03-16 10:30** - DRAFT: Follow-up proposal to Jane
  - [Draft](#2026-03-16-1030---draft-follow-up-proposal-to-jane)
- **2026-03-15 09:15** - Initial project kickoff
  - Decision: Use agile methodology
  - [Email](#2026-03-15-0915---project-kickoff)

## History

### 2026-03-17 14:30 - Q2 Timeline Discussion

From: contact@example.com | To: your@email.com | CC: second@example.com | BCC: -
Subject: Re: Q2 Timeline | Reply-To: - | Thread: Q2 Planning | Message-ID: abc123

Email body here.

---

### 2026-03-16 10:30 - DRAFT: Follow-up proposal to Jane

From: your@email.com | To: contact@example.com | CC: - | BCC: -
Subject: Proposal for Q2 collaboration | Reply-To: - | Thread: Q2 Planning | Message-ID: -

**STATUS: DRAFT - NOT SENT**

Hi Jane,

following up on our call on Friday (2026-03-14) - I think we should move forward with the joint proposal.

Question: Can you review the attached outline and send feedback by Wednesday, 2026-03-18?

Best,
Max

---

### 2026-03-15 09:15 - Project Kickoff

From: your@email.com | To: contact@example.com | CC: - | BCC: -
Subject: Project Alpha - Kickoff | Reply-To: - | Thread: Project Alpha | Message-ID: def456

Email body here.

---

### 2026-03-14 WhatsApp - Topic Name

Platform: WhatsApp | Participants: [Your Name], [Contact Name]

**14:30 [You]**: Message text here.

**14:45 [Contact]**: Reply text here.
> English translation here.

**Key outcomes:**
- Outcome 1
- Outcome 2

