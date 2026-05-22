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
- NATIVE CHARACTERS: Non-English text must use native special characters (e.g., ä, ö, ü, ß for German). Never substitute with ASCII approximations (ae, oe, ue, ss) - CV-TR-03
- AUTO-TRANSLATE: Translate all languages except `CONVERSATION_DO_NOT_TRANSLATE_LIST` - CV-TR-04
- TERM PAIRS: Use `TRANSLATION_TERM_PAIRS` for consistent translation - CV-TR-05
- DOUBLE LANGUAGE: Use `[ENGLISH] / [LOCAL]` in log summaries, key outcomes, status, todos - CV-TR-06
- SEND EMAILS VIA PLAYWRIGHT GMAIL UI - NEVER use CLI tools to send (body encoding fails) - CV-EM-02
- Email header format: `From: | To: | CC: | BCC: | Subject: | Reply-To: | Thread: | Message-ID:` - CV-EM-01
- History heading format: `### YYYY-MM-DD HH:MM - Summary` - CV-ST-04
- Log entry format: `- **YYYY-MM-DD HH:MM** - Main topic` with anchor to History - CV-ST-03
- Todo format: `- **YYYY-MM-DD HH:MM** - Item - Deadline: YYYY-MM-DD, Status: TODO:[ACTION]/DONE` - CV-TD-01
- Todo actions: `TODO:REPLY`, `TODO:REVIEW`, `TODO:PAY`, `TODO:PLAN`, `TODO:SCHEDULE_CALL` (web), `TODO:SCHEDULE_TRIP`, `TODO:SCHEDULE_MEETING` (in person) - CV-TD-02
- Attachment folder format: `Attachments/YYYY-MM-DD_HH-MM_[Topic]/` - CV-AT-04
- AUTO-TRANSCRIBE: When enabled, transcribe attachments via `/transcribe` (1 candidate, 120dpi, min-score=4.5) - CV-AT-03
- All URLs as Markdown clickable links: `[Title](https://...)` - CV-LN-01
- LINKS COMPLETENESS: All attachments, transcriptions, translations recorded in Links section - CV-LN-03
- CHECK DOWNLOADED IMAGES - After downloading, review each image. Delete signature icons, logos, spacers, and other email template garbage. Keep only real attachments - CV-AT-01
- No markdown tables except when sent in emails

## Ignore Files

Files matching these patterns should NOT be downloaded. If downloaded, delete them.

`line.png` | `space.png` | `*-logo*.png` | `i-facebook*.png` | `i-instagram*.png` | `i-link*.png` | `image-horizontal*.png` | `Outlook-*.png`

## Translation Settings

- **CONVERSATION_AUTO_TRANSCRIBE_ATTACHMENTS**=true
- **CONVERSATION_AUTO_TRANSLATE**=true
- **CONVERSATION_DO_NOT_TRANSLATE_LIST**: English, ...
- **TRANSLATION_TERM_PAIRS**: [TERM1_LOCAL] -> [TERM1_ENGLISH] | [TERM2_LOCAL] -> [TERM2_ENGLISH] | ...

## Status

**Current**: [ACTIVE / AWAITING_RESPONSE / ON_HOLD / COMPLETED]

### Todos and Deliverables

- **2026-03-15 09:15** - Send proposal draft - Deadline: 2026-03-20, Status: TODO:REPLY
- **2026-03-17 14:30** - Review contract terms - Status: DONE

## Links and shared documents

- **2026-03-15 09:15** - Some websites to check
  - [Website Title](https://example.com)
- **2026-03-17 14:30** - Document title
  - [Document.pdf](Attachments/2026-03-17_14-30_Topic/Document.pdf)
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
  - Attachment: [Doc.pdf](Attachments/2026-03-17_14-30_Topic/Doc.pdf)
  - [Email](#2026-03-17-1430---q2-timeline-discussion)
- **2026-03-15 09:15** - Initial project kickoff
  - Decision: Use agile methodology
  - [Email](#2026-03-15-0915---project-kickoff)

## History

### 2026-03-17 14:30 - Q2 Timeline Discussion

From: contact@example.com | To: your@email.com | CC: second@example.com | BCC: -
Subject: Re: Q2 Timeline | Reply-To: - | Thread: Q2 Planning | Message-ID: abc123

Email body here.

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

