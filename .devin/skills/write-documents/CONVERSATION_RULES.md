# Conversation Document Rules

Rules for writing and maintaining `CONVERSATION_[COUNTERPARTY].md` files with GOOD/BAD examples.

## Rule Index

Datetime (DT)
- CV-DT-01: Use `YYYY-MM-DD HH:MM` format everywhere
- CV-DT-02: History and Log in reverse chronological order (newest first)
- CV-DT-03: Attachment folders use `YYYY-MM-DD_HH-MM_[Topic]/` format
- CV-DT-04: Verify weekday-date combinations via web search before writing

Translation (TR)
- CV-TR-01: Non-English text MUST have English translation
- CV-TR-02: Translation uses quote block on next line
- CV-TR-03: Use native special characters for non-English languages, never ASCII substitutes
- CV-TR-04: Auto-translate all languages except `CONVERSATION_DO_NOT_TRANSLATE_LIST`
- CV-TR-05: `TRANSLATION_TERM_PAIRS` for consistent term translation across conversation
- CV-TR-06: Double language `[ENGLISH] / [LOCAL]` when writing documents or communicating with user

Email (EM)
- CV-EM-01: Email header format with all fields on one line
- CV-EM-02: Send via Playwright Gmail UI, never CLI tools
- CV-EM-03: Email signature included only on first occurrence per sender
- CV-EM-04: Draft emails marked with `**STATUS: DRAFT - NOT SENT**`

Effective Writing - see `APAPALAN_RULES.md` Communication (CM) section: AP-CM-01, AP-CM-02, AP-CM-03

WhatsApp (WA)
- CV-WA-01: Message format `**HH:MM Person**: message`
- CV-WA-02: Section heading includes time range and platform
- CV-WA-03: End WhatsApp sections with `**Key outcomes:**` summary

Structure (ST)
- CV-ST-01: Required sections in order: MNF, Ignore Files, Translation Settings, Humanizing Settings, Status, Links, Context, Log, History
- CV-ST-02: Persons Involved in Context section (not separate Contacts)
- CV-ST-03: Log entries link to History sections via anchor
- CV-ST-04: History entries separated by `---`

Attachments (AT)
- CV-AT-01: Check downloaded images - delete email garbage (signatures, logos, spacers)
- CV-AT-02: Ignore files pattern maintained per conversation
- CV-AT-03: Auto-transcribe attachments via `/transcribe` when `CONVERSATION_AUTO_TRANSCRIBE_ATTACHMENTS=true`
- CV-AT-04: Binary files (PDF, ZIP, images) in `[ConversationFolder]/Attachments_gitignore/YYYY-MM-DD_HH-MM_[Topic]/`
- CV-AT-05: Text files (.md, .txt, .csv, etc.) in `[ConversationFolder]/Attachments/YYYY-MM-DD_HH-MM_[Topic]/`

Todos (TD)
- CV-TD-01: Todo format with timestamp, item, deadline, status
- CV-TD-02: Status actions: `TODO:REPLY`, `TODO:REVIEW`, `TODO:PAY`, `TODO:PLAN`, `TODO:SCHEDULE_CALL`, `TODO:SCHEDULE_TRIP`, `TODO:SCHEDULE_MEETING`

File Naming (FL)
- CV-FL-01: Filename must be `CONVERSATION_[COUNTERPARTY].md`, never plain `CONVERSATION.md`

Variables (VR)
- CV-VR-01: Translation Settings section in each conversation file
- CV-VR-02: Values sourced from SESSION or WORKSPACE NOTES.md on creation
- CV-VR-03: Missing variables in NOTES.md default to `=true` and are added back

Links (LN)
- CV-LN-01: All URLs as clickable Markdown links
- CV-LN-02: Links section groups by date with description
- CV-LN-03: All attachments, transcriptions, and translations recorded in Links and shared documents
- CV-LN-04: All links absolute - full clickable paths, never relative paths or `...` abbreviations
- CV-LN-05: Explicit inline URLs when referencing sources in emails - URL at point of reference, not only in Links section

History Integrity (HY)
- CV-HY-01: Sent emails are immutable - NEVER edit, correct, or modify emails in History that have already been sent. They are a factual record of what was actually communicated. Corrections go in a NEW follow-up email/message.

Literals (LT)
- CV-LT-01: Addresses, IBANs, reference numbers, and identifiers in outbound communication (drafts, emails, letters) MUST be copied from `[LITERAL]`-marked values or verified against official source documents (government registration, contract, bank confirmation). Never type from memory or copy from secondary documents. See `core-conventions.md` "Authoritative Literals" and AP-PR-13.

Humanizing (HM) - see [CONVERSATION_HUMANIZING_RULES.md](CONVERSATION_HUMANIZING_RULES.md)
- CV-HM-01: Override Scope - MECT/APAPALAN baseline + 1-5% humanizing for user-voice drafts
- CV-HM-02: Consistency Anchoring - extract and replicate user's writing profile from History
- CV-HM-03: Orthographic Consistency - per-conversation SPELLING_VARIANTS, same word = same spelling
- CV-HM-04: Discourse Markers - include user's discourse markers at observed frequency
- CV-HM-05: Sentence Rhythm - vary sentence length (burstiness), no 3+ similar-length consecutive sentences
- CV-HM-06: Opening/Closing Repertoire - use user's habitual greeting/closing per context, never invent or mechanically rotate
- CV-HM-07: Native Naturalness - drafts in any language read as written by a native speaker, never as translated English

## Table of Contents

- [Datetime Format](#datetime-format)
- [Reverse Chronological Order](#reverse-chronological-order)
- [Translation Format](#translation-format)
- [Native Characters](#native-characters)
- [Email Header Format](#email-header-format)
- [Email Sending](#email-sending)
- [Draft Emails](#draft-emails)
- [WhatsApp Message Format](#whatsapp-message-format)
- [WhatsApp Section Heading](#whatsapp-section-heading)
- [WhatsApp Key Outcomes](#whatsapp-key-outcomes)
- [Log Entry Format](#log-entry-format)
- [Log Anchors](#log-anchors)
- [History Heading Format](#history-heading-format)
- [Todo Format](#todo-format)
- [Attachment Folder Format](#attachment-folder-format)
- [Image Cleanup](#image-cleanup)
- [URL Format](#url-format)
- [Absolute Links](#absolute-links)
- [Source References](#source-references)
- [File Naming](#file-naming)
- [Translation Settings Variables](#translation-settings-variables)
- [Auto-Translate](#auto-translate)
- [Term Pairs](#term-pairs)
- [Double Language](#double-language)
- [Auto-Transcribe Attachments](#auto-transcribe-attachments)
- [Attachment Folder Location](#attachment-folder-location)
- [Links Completeness](#links-completeness)

## Datetime Format

Use `YYYY-MM-DD HH:MM` in all timestamps: headings, log entries, todos, attachment folders.

**BAD:**
```
### March 17, 2026 2:30 PM - Timeline Discussion
- Mar 17 - Discussed timeline
- 17.03.2026 14:30 - Send proposal
```

**GOOD:**
```
### 2026-03-17 14:30 - Timeline Discussion
- **2026-03-17 14:30** - Discussed timeline
- **2026-03-17 14:30** - Send proposal - Deadline: 2026-03-20, Status: TODO:REPLY
```

## Weekday Verification

When writing any weekday-date combination (e.g. "Friday, 2026-07-24"), ALWAYS verify via web search first. Never calculate mentally - mental calendar math is systematically unreliable.

**BAD:**
```
Deadline: Thursday, 2026-07-24
(written without verification - actually Friday)
```

**GOOD:**
```
[verify via web search: "what day is July 24 2026" → Friday]
Deadline: Friday, 2026-07-24
```

## Reverse Chronological Order

History and Log: newest entry on top, oldest at bottom.

**BAD:**
```
## History

### 2026-03-15 09:15 - First Email
...
### 2026-03-17 14:30 - Second Email
```

**GOOD:**
```
## History

### 2026-03-17 14:30 - Second Email
...
### 2026-03-15 09:15 - First Email
```

## Translation Format

Non-English text: original first, English translation in quote block on next line.

**BAD:**
```
Person said: "Aqui vai a última fatura." (Here is the last invoice.)
```

**BAD:**
```
Person: Here is the last invoice.
(Original: Aqui vai a última fatura.)
```

**GOOD:**
```
**Person (11:49)**: Aqui vai a última fatura.
> Here is the last invoice.
```

## Native Characters

Non-English text must use native special characters. Never substitute with ASCII approximations.

**BAD:**
```
**14:30 Contact**: Vielen Dank fuer die Rueckmeldung, wir koennen das Gespraech morgen fuehren.
> Thanks for the response, we can have the conversation tomorrow.
```

**GOOD:**
```
**14:30 Contact**: Vielen Dank für die Rückmeldung, wir können das Gespräch morgen führen.
> Thanks for the response, we can have the conversation tomorrow.
```

## Email Header Format

All fields on one pipe-separated line. Use `-` for empty fields, never omit fields.

**BAD:**
```
From: john@example.com
To: me@example.com
Subject: Meeting
```

**BAD:**
```
From: john@example.com | To: me@example.com | Subject: Meeting
```

**GOOD:**
```
From: john@example.com | To: me@example.com | CC: - | BCC: -
Subject: Re: Meeting | Reply-To: - | Thread: Project Alpha | Message-ID: abc123
```

## Email Sending

Always use Playwright Gmail UI. CLI send tools have body encoding failures.

**BAD:** `cli-tool send --to "contact@example.com" --subject "Re: Meeting" --body "..."`

**GOOD:** Open Gmail in Playwright, compose and send via UI.

## Draft Emails

Mark unsent drafts clearly at top of entry.

**BAD:**
```
### 2026-03-18 13:52 - Electricity Inquiry

From: me@example.com | To: admin@company.com ...

Draft email body...
```

**GOOD:**
```
### 2026-03-18 13:52 - DRAFT Electricity Inquiry

**STATUS: DRAFT - NOT SENT**

From: me@example.com | To: admin@company.com ...

Draft email body...
```


## WhatsApp Message Format

Timestamp before person name, person in bold.

**BAD:**
```
Alice: Hi Bob, message here.
Bob replied: Ok no problem.
```

**GOOD:**
```
**13:44 Sender**: Message text here.

**15:11 Recipient**: Obrigado, irei mandar limpar de imediato o apartamento
> Thanks, I will have the apartment cleaned immediately
```

## WhatsApp Section Heading

Include date, platform, and topic. Add time range in body.

**BAD:**
```
### 2026-03-17 - WhatsApp Messages
```

**GOOD:**
```
### 2026-03-17 WhatsApp - Payment Confirmation

Platform: WhatsApp | Participants: [Your Name], [Contact Name]
```

## WhatsApp Key Outcomes

End WhatsApp sections with structured summary of decisions and next steps.

**BAD:**
```
**19:56 Sender**: No problem, tomorrow is fine.

---
```

**GOOD:**
```
**19:56 Sender**: No problem, tomorrow is fine.

**Key outcomes:**
- Contact confirmed: free to choose any provider
- Reference code pending confirmation tomorrow
- Key detail documented

---
```

## Log Entry Format

Bold timestamp, main topic on same line. Sub-items indented with Decision/Action/Attachment.

**BAD:**
```
- Discussed timeline on March 17. Decided to move milestone. Need to send chart.
```

**GOOD:**
```
- **2026-03-17 14:30** - Discussed Q2 timeline adjustments
  - Decision: Move milestone 2 to April 15
  - Action: Send updated Gantt chart by Friday
  - Attachment: [Q2_Timeline.pdf](Attachments_gitignore/2026-03-17_14-30_Q2Timeline/Q2_Timeline.pdf)
  - [Email](#2026-03-17-1430---q2-timeline-discussion)
```

## Log Anchors

Every log entry links to its History section via Markdown anchor.

**BAD:**
```
- **2026-03-17 14:30** - Discussed timeline
```

**GOOD:**
```
- **2026-03-17 14:30** - Discussed timeline
  - [Email](#2026-03-17-1430---q2-timeline-discussion)
```

For WhatsApp:
```
  - [WhatsApp](#2026-03-17-whatsapp---payment-confirmation)
```

## History Heading Format

Email: `### YYYY-MM-DD HH:MM - Summary`
WhatsApp: `### YYYY-MM-DD WhatsApp - Topic`

**BAD:**
```
### Email from John about timeline
### WhatsApp chat 17 March
```

**GOOD:**
```
### 2026-03-17 14:30 - Q2 Timeline Discussion
### 2026-03-17 WhatsApp - Payment Confirmation
```

## Todo Format

Timestamp, item, optional deadline, status with action type.

**BAD:**
```
- [ ] Reply to John
- [ ] Pay invoice (due March 20)
```

**GOOD:**
```
- **2026-03-15 09:15** - Reply to John with proposal - Deadline: 2026-03-20, Status: TODO:REPLY
- **2026-03-17 11:03** - Pay deposit to landlord - Status: DONE
```

## Attachment Folder Format

Two mirrored folder trees per conversation:
- `Attachments_gitignore/YYYY-MM-DD_HH-MM_[Topic]/` - binary files (PDF, ZIP, images) - excluded from git
- `Attachments/YYYY-MM-DD_HH-MM_[Topic]/` - text files (.md, .txt, .csv, etc.) - tracked in git

**BAD:**
```
Attachments_gitignore/contract.pdf
Attachments_gitignore/March2026/contract.pdf
Attachments_gitignore/2026-03-16_16-50_Contract/contract.md
```

**GOOD:**
```
Attachments_gitignore/2026-03-16_16-50_RentalContract/CT_Arrendamento.pdf
Attachments/2026-03-16_16-50_RentalContract/CT_Arrendamento.md
Attachments/2026-03-16_16-50_RentalContract/CT_Arrendamento_en.md
```

## Image Cleanup

After downloading email attachments, review each image. Delete email template garbage.

Delete: signature icons, company logos, social media icons, spacer images, horizontal lines.
Keep: real attachments (documents, photos, screenshots).

Maintain per-conversation Ignore Files pattern list for recurring garbage.

## URL Format

All URLs as clickable Markdown links with descriptive title.

**BAD:**
```
Check https://www.company.com for details.
See provider.com/services/energy/
```

**GOOD:**
```
Check [Company Name](https://www.company.com) for details.
See [Provider Energy](https://provider.com/services/energy/)
```

## Absolute Links

File paths, attachment references, and source links must be full absolute clickable paths. Never use relative paths or `...` abbreviations.

**BAD:**
```
See Attachments/.../contract.md
Transcription: ../2026-03-16_RentalContract/contract.md
```

**GOOD:**
```
See [contract.md](e:/Conversations/MariaSilva-Landlord/Attachments/2026-03-16_16-50_RentalContract/contract.md)
```

## Source References

When referencing a source (article, website, document, regulation), include the explicit URL inline at the point of reference. A name alone is not verifiable; the reader must not need to search the Links section or the web.

**BAD** (source named without URL):
```
- **2026-03-17 14:30** - Landlord cited the rental law amendment from the government portal
- According to the provider's cancellation policy, 30 days notice is required
```

**GOOD** (explicit inline URL at point of reference):
```
- **2026-03-17 14:30** - Landlord cited the [rental law amendment](https://dre.pt/dre/detalhe/lei/56-2023-XXXXXX) from the government portal
- According to the [provider's cancellation policy](https://provider.com/terms/cancellation), 30 days notice is required
```

## File Naming

Filename must always include counterparty identifier. Never use plain `CONVERSATION.md`.

**BAD:**
```
MariaSilva-Landlord/CONVERSATION.md
ClientFolder/CONVERSATION.md
```

**GOOD:**
```
MariaSilva-Landlord/CONVERSATION_MariaSilva.md
ClientFolder/CONVERSATION_ClientName.md
```

## Translation Settings Variables

Each conversation file has a Translation Settings section. Values are read from SESSION or WORKSPACE NOTES.md when the conversation is created. If a variable is missing from NOTES.md, add it with `=true`.

**Variables:**
- `CONVERSATION_AUTO_TRANSCRIBE_ATTACHMENTS` - Auto-transcribe PDF/image attachments via `/transcribe`
- `CONVERSATION_AUTO_TRANSLATE` - Auto-translate content not in do-not-translate list
- `CONVERSATION_DO_NOT_TRANSLATE_LIST` - Comma-separated languages to skip translation
- `TRANSLATION_TERM_PAIRS` - Pipe-separated term pairs for consistent translation

**BAD:**
```
## Translation Settings
(empty - no settings)
```

**BAD:**
```
Translate everything to English.
```

**GOOD:**
```
## Translation Settings
- **CONVERSATION_AUTO_TRANSCRIBE_ATTACHMENTS**=true
- **CONVERSATION_AUTO_TRANSLATE**=true
- **CONVERSATION_DO_NOT_TRANSLATE_LIST**: English, German
- **TRANSLATION_TERM_PAIRS**: Caução -> Deposit | Renda -> Rent | Arrendamento -> Rental Contract
```

## Auto-Translate

When `CONVERSATION_AUTO_TRANSLATE=true`, translate all conversation text and attachment content to English. Skip languages listed in `CONVERSATION_DO_NOT_TRANSLATE_LIST`.

**BAD:**
```
**João (11:49)**: Aqui vai a última fatura.
```

**GOOD:**
```
**João (11:49)**: Aqui vai a última fatura.
> Here is the last invoice.
```

## Term Pairs

Use `TRANSLATION_TERM_PAIRS` for consistent translation of domain terms. Same source term must always produce same English term.

**BAD** (inconsistent translation):
```
> Here is the rental deposit.
...
> The security deposit was transferred.
...
> The caution payment is confirmed.
```

**GOOD** (term pair: Caução -> Deposit):
```
> Here is the deposit (Caução).
...
> The deposit (Caução) was transferred.
...
> The deposit (Caução) payment is confirmed.
```

## Double Language

When writing documents or communicating with the user, use double language format to ensure term pairing is visible and consistent.

**BAD:**
```
The landlord confirmed the deposit was received.
```

**GOOD:**
```
The landlord (senhorio) confirmed the deposit (caução) was received.
```

Applies to: Log summaries, Key outcomes, Status updates, Todo items. Does NOT apply to: verbatim History entries (those use translation quote blocks).

## Auto-Transcribe Attachments

When `CONVERSATION_AUTO_TRANSCRIBE_ATTACHMENTS=true`, transcribe PDF and image attachments using `/transcribe` workflow with: 1 candidate, 120 DPI, min-score=4.5. Output `.md` file in mirrored `Attachments/` folder (same subfolder name).

**BAD** (transcription in same folder as binary):
```
Attachments_gitignore/2026-03-16_16-50_Contract/
├── contract.pdf
└── contract.md
```

**GOOD** (binary and transcription separated):
```
Attachments_gitignore/2026-03-16_16-50_Contract/
└── contract.pdf
Attachments/2026-03-16_16-50_Contract/
└── contract.md
```

If `CONVERSATION_AUTO_TRANSLATE=true` and transcribed content is not in `CONVERSATION_DO_NOT_TRANSLATE_LIST`, also produce translated version in `Attachments/`: `contract_en.md`.

## Attachment Folder Location

Attachments live inside the conversation folder with two sibling trees:
- `Attachments_gitignore/YYYY-MM-DD_HH-MM_[Topic]/` - binaries (git-excluded)
- `Attachments/YYYY-MM-DD_HH-MM_[Topic]/` - text files (git-tracked)

**BAD:**
```
_!EmailConversations/Attachments_gitignore/2026-03-16_Contract/file.pdf
SharedAttachments/file.pdf
```

**GOOD:**
```
MariaSilva-Landlord/Attachments_gitignore/2026-03-16_16-50_RentalContract/contract.pdf
MariaSilva-Landlord/Attachments/2026-03-16_16-50_RentalContract/contract.md
```

## Links Completeness

All attachments, transcriptions, and translations must be recorded in the Links and shared documents section with date, description, and relative path.

**BAD:**
```
## Links and shared documents
- **2026-03-16 16:50** - Rental Contract
  - [contract.pdf](Attachments_gitignore/2026-03-16_16-50_RentalContract/contract.pdf)
```

**GOOD:**
```
## Links and shared documents
- **2026-03-16 16:50** - Rental Contract
  - [contract.pdf](Attachments_gitignore/2026-03-16_16-50_RentalContract/contract.pdf)
  - [contract.md](Attachments/2026-03-16_16-50_RentalContract/contract.md) (transcription)
  - [contract_en.md](Attachments/2026-03-16_16-50_RentalContract/contract_en.md) (translation)
```
