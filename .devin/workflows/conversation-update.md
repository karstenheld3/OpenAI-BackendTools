---
description: Update an existing CONVERSATION_[COUNTERPARTY].md with new emails, messages, or attachments
---

# Update Conversation Workflow

Append new communication (emails, WhatsApp, attachments) to an existing `CONVERSATION_[COUNTERPARTY].md` file.

**Goal**: Updated conversation file with new entries in Log, History, Links, and Todos

**Why**: Conversation files grow over time. This workflow ensures consistent formatting, auto-transcription, auto-translation, and proper linking when adding new content.

Scope: Updates existing conversation files only. To create new conversations, use `/conversation-start`. To draft emails/messages as the user, use `/conversation-draft`.

## Required Skills

- @skills:write-documents for `CONVERSATION_RULES.md`

## MUST-NOT-FORGET

- Read `CONVERSATION_RULES.md` before updating any conversation file
- Filename MUST be `CONVERSATION_[COUNTERPARTY].md`, never plain `CONVERSATION.md` - CV-FL-01
- Native characters mandatory for non-English text - CV-TR-03
- Non-English/German text MUST have English translation in quote block - CV-TR-01
- Use `TRANSLATION_TERM_PAIRS` from file's Translation Settings for consistent translation - CV-TR-05
- Double language `[ENGLISH] / [LOCAL]` in log summaries, key outcomes, todos - CV-TR-06
- DATETIME FORMAT: `YYYY-MM-DD HH:MM` everywhere - CV-DT-01
- History section: newest on top (reverse chronological) - CV-DT-02
- NEVER use gogcli to send emails - Playwright Gmail UI only - CV-EM-02
- Auto-transcribe attachments when `CONVERSATION_AUTO_TRANSCRIBE_ATTACHMENTS=true` - CV-AT-03
- All attachments, transcriptions, translations in Links section - CV-LN-03

## Mandatory Re-read

Before updating, read from the conversation file:
- MUST-NOT-FORGET section (conversation-specific rules)
- Translation Settings section (variables and term pairs)
- Status section (current state, open todos)

**SESSION-MODE**: Also read NOTES.md, PROBLEMS.md in session folder

**PROJECT-MODE**: Also read NOTES.md, PROBLEMS.md in project folder

## Trigger

- `/conversation-update` - User wants to add content to an existing conversation
- `/conversation-update [counterparty]` - With explicit target

# EXECUTION

## Step 1: Locate Conversation File

Find the target `CONVERSATION_[COUNTERPARTY].md` file.

**If counterparty specified**: Search for `CONVERSATION_[COUNTERPARTY].md` in session/project folders.

**If not specified**: List all `CONVERSATION_*.md` files in current context. If multiple, ask user which one.

**If legacy `CONVERSATION.md` found**: Rename to `CONVERSATION_[COUNTERPARTY].md` first - CV-FL-01. Confirm with user.

**If not found**: Inform user to use `/conversation-start` instead. Stop workflow.

## Step 2: Read Conversation Context

From the target file, read:

1. **Translation Settings** - `CONVERSATION_AUTO_TRANSLATE`, `CONVERSATION_DO_NOT_TRANSLATE_LIST`, `TRANSLATION_TERM_PAIRS`, `CONVERSATION_AUTO_TRANSCRIBE_ATTACHMENTS`
2. **Persons Involved** - Names, emails, roles
3. **Last Log entry** - To determine chronological position
4. **Open Todos** - To check if new content resolves any

## Step 3: Identify New Content

Scan the current chat for content to add. Classify each item:

**Email**: Extract headers and body. Format per CV-EM-01.

**WhatsApp**: Extract messages with timestamps. Format per CV-WA-01.

**Attachment**: Note filename, date, topic. Plan folder per CV-AT-04.

**Decision/Action**: Extract for Log sub-items.

**Todo update**: Mark resolved todos as DONE, add new ones.

## Step 4: Process Attachments

For each new attachment:

1. Create folder: `Attachments_gitignore/YYYY-MM-DD_HH-MM_[Topic]/`
2. Download/save binary files (PDF, ZIP, images) to `Attachments_gitignore/` subfolder
3. Check downloaded images - delete email garbage per CV-AT-01
4. If `CONVERSATION_AUTO_TRANSCRIBE_ATTACHMENTS=true`:
   - Run `/transcribe` with: 1 candidate, 120 DPI, min-score=4.5
   - Output: `[filename].md` in mirrored `Attachments/YYYY-MM-DD_HH-MM_[Topic]/` folder - CV-AT-05
5. If `CONVERSATION_AUTO_TRANSLATE=true` and content language not in `CONVERSATION_DO_NOT_TRANSLATE_LIST`:
   - Produce translated version: `[filename]_en.md` in `Attachments/YYYY-MM-DD_HH-MM_[Topic]/`
   - Use `TRANSLATION_TERM_PAIRS` for consistent terms

## Step 5: Append to Conversation File

Add new content in this order:

1. **History** - Insert new entries at TOP, newest first - CV-DT-02. Use `---` separators - CV-ST-04.
2. **Log** - Insert new entries at TOP. Link to History via anchors - CV-ST-03. Use double language - CV-TR-06.
3. **Links and shared documents** - Add all new attachments, transcriptions, translations - CV-LN-03.
4. **Todos** - Update resolved items to DONE. Add new action items.
5. **Status** - Update if conversation state changed.

## Step 6: Translate Content

If `CONVERSATION_AUTO_TRANSLATE=true`:

1. Check each new History entry language
2. If language not in `CONVERSATION_DO_NOT_TRANSLATE_LIST`:
   - Add English translation in quote block - CV-TR-01, CV-TR-02
   - Use `TRANSLATION_TERM_PAIRS` for domain terms - CV-TR-05
   - Use native special characters - CV-TR-03
3. In Log entries and Todos, use double language format - CV-TR-06

# FINALIZATION

## Verification

After updating:

1. New History entries at top, reverse chronological - CV-DT-02
2. All new Log entries link to History via anchors - CV-ST-03
3. All non-English/German text has English translation - CV-TR-01
4. Term pairs used consistently - CV-TR-05
5. Double language in new log summaries and todos - CV-TR-06
6. Native special characters used - CV-TR-03
7. All dates in `YYYY-MM-DD HH:MM` format - CV-DT-01
8. All new attachments, transcriptions, translations in Links - CV-LN-03
9. Attachment folders follow `YYYY-MM-DD_HH-MM_[Topic]/` format, binaries in `Attachments_gitignore/`, text files in `Attachments/` - CV-AT-04, CV-AT-05
10. Auto-transcription completed if enabled - CV-AT-03

## Quality Gate

- [ ] `CONVERSATION_RULES.md` read before updating
- [ ] Translation Settings read from file
- [ ] Term pairs applied consistently - CV-TR-05
- [ ] Double language in new log/todo entries - CV-TR-06
- [ ] All new non-English/German text translated - CV-TR-01
- [ ] Native special characters used - CV-TR-03
- [ ] New History at top, reverse chronological - CV-DT-02
- [ ] New Log entries link to History - CV-ST-03
- [ ] All new attachments/transcriptions/translations in Links - CV-LN-03
- [ ] Auto-transcription done if enabled - CV-AT-03

## Output

`Updated: [FOLDER]/CONVERSATION_[COUNTERPARTY].md - added [N] entries ([type list])`
