---
description: Create a new CONVERSATION_[COUNTERPARTY].md file from chat context
---

# Start Conversation Workflow

Create a new `CONVERSATION_[COUNTERPARTY].md` by extracting conversation partner data and communication history from the current chat.

**Goal**: Populated `CONVERSATION_[COUNTERPARTY].md` with contacts, context, log entries, full history, and translation settings

**Why**: Manual creation of conversation files is tedious and error-prone. This workflow extracts all data from the chat context and structures it according to `CONVERSATION_TEMPLATE.md`.

Scope: Creates conversation files only. To update existing conversations, use `/conversation-update`. To draft emails/messages as the user, use `/conversation-draft`. Use `/transcribe` for PDF attachments, Playwright Gmail UI for sending emails.

## Required Skills

- @skills:write-documents for `CONVERSATION_TEMPLATE.md` and `CONVERSATION_RULES.md`

## MUST-NOT-FORGET

- Read `CONVERSATION_RULES.md` before creating any conversation file
- Read `CONVERSATION_TEMPLATE.md` before creating any conversation file
- Filename MUST be `CONVERSATION_[COUNTERPARTY].md`, never plain `CONVERSATION.md` - CV-FL-01
- Read translation variables from NOTES.md; add missing ones with `=true` - CV-VR-02
- Native characters mandatory for non-English text (e.g., ä, ö, ü, ß for German) - CV-TR-03
- Non-English/German text MUST have English translation in quote block - CV-TR-01
- Double language `[ENGLISH] / [LOCAL]` in log summaries, key outcomes, todos - CV-TR-06
- DATETIME FORMAT: `YYYY-MM-DD HH:MM` everywhere - CV-DT-01
- NEVER use gogcli to send emails - Playwright Gmail UI only - CV-EM-02
- History section: newest on top (reverse chronological) - CV-DT-02
- All URLs as clickable Markdown links - CV-LN-01
- All attachments, transcriptions, translations in Links section - CV-LN-03

## Mandatory Re-read

**SESSION-MODE**: NOTES.md, PROBLEMS.md, PROGRESS.md in session folder

**PROJECT-MODE**: NOTES.md, PROBLEMS.md in project folder

## Trigger

- `/conversation-start` - User wants to track a new or ongoing conversation
- `/conversation-start [person/company]` - With explicit conversation partner

# EXECUTION

## Step 1: Detect Mode

Determine where the conversation file will live.

**PROJECT-MODE** (persistent conversation tracking):
- Active session is `_!EmailConversations` or similar dedicated conversation project
- Or user explicitly requests project-level tracking
- Output path: `[PROJECT_FOLDER]/[SubfolderName]/CONVERSATION_[COUNTERPARTY].md`
- Subfolder naming: `FirstnameLastname-Description/` (e.g., `JoaoEstevao-FaroLandlordAppartment/`)

**SESSION-MODE** (conversation as part of broader work):
- Active session is any other session (e.g., `_!EmigrationGermanyToPortugal`)
- Conversations live in **topic subfolders** within the session (e.g., `Faro-Wohnung/`)
- Output path: `[SESSION_FOLDER]/[TopicSubfolder]/CONVERSATION_[COUNTERPARTY].md`
- If subfolder already exists, place file there. If not, ask user for subfolder name.

**Filename rules** (both modes):
- Always `CONVERSATION_[COUNTERPARTY].md` - CV-FL-01
- `[COUNTERPARTY]`: short identifier for partner/provider (e.g., `JoaoEstevao`, `FAGAR`, `MEO`)
- Never use plain `CONVERSATION.md`

**No Context Match**: Ask user to specify mode and target folder.

## Step 2: Scan Chat for Conversation Partner

Extract from previous messages in the current chat:

- **Person/Company name**
- **Email address(es)**
- **Phone number(s)**
- **Role/relationship** (e.g., landlord, provider, coach)
- **Address** (if mentioned)
- **Website** (if mentioned)
- **Reference numbers** (contract IDs, user numbers, NIF, etc.)
- **Language** used in communication

Proceed directly to file creation. User can review and edit after.

## Step 3: Check for Existing Conversation Files

List all `CONVERSATION_*.md` files in the target folder.

**Case A - Same partner already tracked:**
- A `CONVERSATION_[COUNTERPARTY].md` file for the same partner already exists
- Do NOT create a new file. Inform user to use `/conversation-update` instead
- Stop workflow

**Case B - Legacy `CONVERSATION.md` exists:**
- Rename to `CONVERSATION_[COUNTERPARTY].md` using the partner from that file
- Confirm rename with user before executing
- Then create new file as `CONVERSATION_[NEW_COUNTERPARTY].md`

**Case C - Other conversation files exist (different partner):**
- Create new file as `CONVERSATION_[COUNTERPARTY].md`

**Case D - Empty folder or folder does not exist:**
- PROJECT-MODE: create subfolder if needed
- Create `CONVERSATION_[COUNTERPARTY].md`

Proceed to Step 4 for variable reading, then Step 5 for file creation.

## Step 4: Read Translation Variables from NOTES.md

Read SESSION NOTES.md (if SESSION-MODE) or WORKSPACE NOTES.md (if PROJECT-MODE). Look for these variables:

- `CONVERSATION_AUTO_TRANSCRIBE_ATTACHMENTS`
- `CONVERSATION_AUTO_TRANSLATE`
- `CONVERSATION_DO_NOT_TRANSLATE_LIST`
- `TRANSLATION_TERM_PAIRS`

If any variable is missing from NOTES.md, add it with default `=true` (for booleans) or empty (for lists).

These values populate the Translation Settings section in the new conversation file.

## Step 5: Create Conversation File

1. Read `CONVERSATION_TEMPLATE.md` from @skills:write-documents
2. Read `CONVERSATION_RULES.md` from @skills:write-documents
3. Fill template sections:

**MUST-NOT-FORGET**:
- Copy from template
- Adapt translation rule to conversation language (e.g., "All Portuguese text" instead of generic)

**Ignore Files**:
- Start with default patterns from template
- Adjust per conversation partner if known

**Translation Settings**:
- Populate from NOTES.md values (Step 4)
- Add conversation-specific term pairs if known from chat context

**Status**:
- Set to `ACTIVE`
- Add any reference numbers, contract IDs

**Todos and Deliverables**:
- Extract any pending actions from chat

**Links and shared documents**:
- Extract any URLs or documents mentioned
- Include transcription and translation files per CV-LN-03

**Conversation Context / Persons Involved**:
- Full contact details for each person
- Role, timezone, communication preferences

**Topics**:
- Extract discussion topics from chat

**Log**:
- One entry per communication event (email, WhatsApp, form submission, call)
- Reverse chronological (newest first)
- Include Decision/Action/Attachment sub-items
- Use double language format per CV-TR-06

**History**:
- Full text of each communication
- Reverse chronological (newest first)
- Email header format: `From: | To: | CC: | BCC: - | Subject: | Reply-To: - | Thread: | Message-ID:`
- Non-English/German text followed by English translation in quote block
- Entries separated by `---`

## Step 6: Populate from Chat Context

Scan the entire current chat for:

1. **Emails** (quoted text, forwarded messages, Gmail content)
   - Extract full headers and body
   - Add to History with proper formatting
   - Create Log entry for each email

2. **WhatsApp messages** (if present)
   - Format: `**HH:MM Person**: message`
   - Add translation quote blocks for non-English/German
   - End section with `**Key outcomes:**`

3. **Form submissions** (if present)
   - Document submitted data
   - Note which platform/URL

4. **Attachments mentioned**
   - Create `Attachments_gitignore/YYYY-MM-DD_HH-MM_[Topic]/` structure entries
   - Link in Log and History

5. **Decisions and actions**
   - Extract to Log sub-items (Decision:, Action:, Attachment:)
   - Create Todo entries for pending items

# FINALIZATION

## Verification

After creating the file:

1. Filename is `CONVERSATION_[COUNTERPARTY].md` - CV-FL-01
2. Translation Settings populated from NOTES.md - CV-VR-01, CV-VR-02
3. All contacts have email addresses
4. Log entries link to History sections via anchors - CV-ST-03
5. History in reverse chronological order - CV-DT-02
6. All non-English/German text has English translation - CV-TR-01
7. Native special characters used - CV-TR-03
8. All dates in `YYYY-MM-DD HH:MM` format - CV-DT-01
9. All URLs are clickable Markdown links - CV-LN-01
10. All attachments, transcriptions, translations in Links section - CV-LN-03
11. Double language format in log summaries and todos - CV-TR-06

## Quality Gate

- [ ] `CONVERSATION_RULES.md` read before creating file
- [ ] `CONVERSATION_TEMPLATE.md` read before creating file
- [ ] Filename is `CONVERSATION_[COUNTERPARTY].md` - CV-FL-01
- [ ] Translation variables read from NOTES.md - CV-VR-02
- [ ] Translation Settings section populated - CV-VR-01
- [ ] Native special characters used - CV-TR-03
- [ ] Non-English/German text has English translation - CV-TR-01
- [ ] Double language in log summaries and todos - CV-TR-06
- [ ] All dates in `YYYY-MM-DD HH:MM` format - CV-DT-01
- [ ] History in reverse chronological order - CV-DT-02
- [ ] Log entries link to History sections via anchors - CV-ST-03
- [ ] All attachments, transcriptions, translations in Links - CV-LN-03

## Output

**New**: `Created: [FOLDER]/CONVERSATION_[COUNTERPARTY].md`

**Legacy rename + new**: `Renamed: CONVERSATION.md -> CONVERSATION_[EXISTING].md | Created: CONVERSATION_[NEW].md`
