---
name: google-account
description: Apply when interacting with Google services (Gmail, Calendar, Drive, Tasks) via gogcli CLI
---

# Google Account Skill (gogcli)

Interact with Google services using the `gogcli` CLI tool.

## Table of Contents

- [Prerequisites Check](#prerequisites-check-run-first)
- [MUST-NOT-FORGET](#must-not-forget)
- [Intent Lookup](#intent-lookup)
- [Tool: gogcli](#tool-gogcli)
- [Gmail Operations](#gmail-operations)
- [Calendar Operations](#calendar-operations)
- [Tasks Operations](#tasks-operations)
- [Drive Operations](#drive-operations)
- [Configuration](#configuration)
- [Limitations](#limitations)
- [Token Expiry Re-Auth Flow](#token-expiry-re-auth-flow)
- [Common Mistakes](#common-mistakes-lessons-learned)
- [Setup](SETUP.md)
- [Uninstall](UNINSTALL.md)

## Prerequisites Check (RUN FIRST)

Before using this skill, verify `gog` is installed:

```powershell
wsl bash -c "export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/linuxbrew/.linuxbrew/bin'; gog --version"
```

**If command fails or `gog` not found**: Stop and follow [SETUP.md](SETUP.md) workflow completely. Do NOT improvise installation steps.

**If `gog` found but auth fails**: Follow [Token Expiry Re-Auth Flow](#token-expiry-re-auth-flow) below.

## MUST-NOT-FORGET

- Tool is `gog` (from gogcli package), NOT `gop`
- **WSL PATH is broken by default** - Always include full PATH export (see command template below)
- **If `gog` not installed**: Follow SETUP.md, do NOT improvise installation
- **If token expired**: Follow [Token Expiry Re-Auth Flow](#token-expiry-re-auth-flow)
- Use `--json` flag for all commands to enable parsing
- Set `GOG_ACCOUNT` environment variable for non-interactive use
- Use `GOG_KEYRING_PASSWORD` with file backend for automation
- Google Meet links cannot be created via CLI (API limitation)
- Attachments download to specified `--out-dir`, default is current directory

### Command Template (ALWAYS USE)

```powershell
wsl bash -c "export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/linuxbrew/.linuxbrew/bin'; export GOG_KEYRING_PASSWORD='<PASSWORD>'; export GOG_ACCOUNT='<EMAIL>'; gog <command>"
```

**Get config from `[WORKSPACE_FOLDER]/!NOTES.md`** - Look for "gogcli" section with account and keyring password.

## Intent Lookup

User wants to...
- **Check unread emails** -> `gog gmail search 'is:unread' --max 20`
- **Read specific email** -> `gog gmail thread get <threadId>`
- **Download attachments** -> `gog gmail thread get <threadId> --download --out-dir ./attachments`
- **Send email** -> `gog gmail send --to <email> --subject "..." --body "..."`
- **Create draft** -> `gog gmail drafts create --to <email> --subject "..." --body "..."`
- **See today's calendar** -> `gog calendar events primary --today`
- **Create calendar event** -> `gog calendar create primary --summary "..." --from <datetime> --to <datetime>`
- **Add attendees** -> Include `--attendees "email1,email2" --send-updates all`
- **Check availability** -> `gog calendar freebusy --calendars "primary" --from <start> --to <end>`
- **List tasks** -> `gog tasks lists` then `gog tasks list <tasklistId>`
- **Add task** -> `gog tasks add <tasklistId> --title "..." --due <date>`
- **Mark task done** -> `gog tasks done <tasklistId> <taskId>`
- **Download from Drive** -> `gog drive download <fileId> --out ./file.bin`
- **Search Drive** -> `gog drive search "query" --max 20`

## Tool: gogcli

Repository: https://github.com/steipete/gogcli
Website: https://gogcli.sh/

Unified CLI for Google services:
- Gmail: Search, read, send, drafts, labels, attachments, filters
- Calendar: Events CRUD, free/busy, reminders, recurrence
- Drive: Upload, download, organize, share
- Tasks: Tasklists, tasks CRUD, due dates, recurring
- Contacts: Personal contacts, directory search
- Sheets/Docs/Slides: Read, write, export
- Additional: Forms, Apps Script, People, Chat (Workspace-only), Groups (Workspace-only)

### Command Structure

```
gog [--json] [--account <email>] <service> <command> [options]
```

Global flags:
- `--json` - Output in JSON format (recommended for parsing)
- `--account <email>` - Use specific account (or set `GOG_ACCOUNT` env var)

## Gmail Operations

### Search and Read

```bash
# Search recent
gog --json gmail search 'newer_than:7d' --max 10

# Search unread
gog --json gmail search 'is:unread' --max 20

# Search by sender
gog --json gmail search 'from:someone@example.com' --max 10

# Get thread details
gog --json gmail thread get <threadId>
```

### Download Attachments

```bash
# Download all attachments from thread
gog gmail thread get <threadId> --download --out-dir [TOOLS_FOLDER]/_downloaded_attachments

# Single attachment
gog gmail attachment <messageId> <attachmentId> --out ./file.bin
```

### Send Email

```bash
# Plain text
gog gmail send --to recipient@example.com --subject "Subject" --body "Body text"

# HTML body
gog gmail send --to recipient@example.com --subject "Subject" --body-html "<p>HTML content</p>"

# Reply with quote
gog gmail send --reply-to-message-id <messageId> --quote --to recipient@example.com --subject "Re: ..." --body "Reply"
```

### Drafts

```bash
# Create
gog gmail drafts create --to recipient@example.com --subject "Draft" --body "Content"

# List
gog gmail drafts list

# Send draft
gog gmail drafts send <draftId>
```

### Labels

```bash
# List
gog gmail labels list

# Modify thread
gog gmail thread modify <threadId> --add STARRED --remove INBOX
```

## Calendar Operations

### List Events

```bash
# Today
gog --json calendar events primary --today

# This week
gog --json calendar events primary --week

# Next N days
gog --json calendar events primary --days 7

# Date range
gog --json calendar events primary --from 2025-01-15T00:00:00Z --to 2025-01-22T00:00:00Z
```

### Create Events

```bash
# Basic event
gog calendar create primary \
  --summary "Meeting" \
  --from 2025-01-15T10:00:00Z \
  --to 2025-01-15T11:00:00Z

# With attendees
gog calendar create primary \
  --summary "Team Sync" \
  --from 2025-01-15T14:00:00Z \
  --to 2025-01-15T15:00:00Z \
  --attendees "alice@example.com,bob@example.com" \
  --send-updates all

# Recurring
gog calendar create primary \
  --summary "Weekly Standup" \
  --from 2025-01-15T09:00:00Z \
  --to 2025-01-15T09:30:00Z \
  --rrule "RRULE:FREQ=WEEKLY;BYDAY=MO"

# With reminder
gog calendar create primary \
  --summary "Payment" \
  --from 2025-02-11T09:00:00Z \
  --to 2025-02-11T09:15:00Z \
  --reminder "email:1d" \
  --reminder "popup:30m"
```

### Update and Delete

```bash
# Update
gog calendar update primary <eventId> --summary "Updated Title"

# Delete
gog calendar delete primary <eventId>
```

### Free/Busy Check

```bash
gog --json calendar freebusy --calendars "primary" \
  --from 2025-01-15T00:00:00Z \
  --to 2025-01-16T00:00:00Z
```

## Tasks Operations

```bash
# List tasklists
gog --json tasks lists

# List tasks
gog --json tasks list <tasklistId>

# Add task
gog tasks add <tasklistId> --title "Task title" --due 2025-02-01

# Add recurring
gog tasks add <tasklistId> --title "Daily review" --due 2025-02-01 --repeat daily

# Mark complete
gog tasks done <tasklistId> <taskId>

# Undo
gog tasks undo <tasklistId> <taskId>
```

## Drive Operations

```bash
# List files
gog --json drive ls --max 20

# Search
gog --json drive search "invoice" --max 20

# Download
gog drive download <fileId> --out ./downloaded-file.bin

# Upload
gog drive upload ./path/to/file --parent <folderId>
```

## Configuration

### Environment Variables (Required for Automation)

```bash
export GOG_ACCOUNT='you@gmail.com'
export GOG_KEYRING_BACKEND='file'
export GOG_KEYRING_PASSWORD='secure-password'

# Optional: Restrict commands (sandboxing)
export GOG_ENABLE_COMMANDS='gmail,calendar,tasks,drive'
```

### Config File Location

- Linux/WSL: `~/.config/gogcli/config.json`
- Windows: `%AppData%\gogcli\config.json`
- macOS: `~/Library/Application Support/gogcli/config.json`

### WSL Invocation (from PowerShell)

```powershell
# CORRECT - with full PATH (get EMAIL and PASSWORD from [WORKSPACE_FOLDER]/!NOTES.md)
wsl bash -c "export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/linuxbrew/.linuxbrew/bin'; export GOG_ACCOUNT='<EMAIL>'; export GOG_KEYRING_PASSWORD='<PASSWORD>'; gog --json gmail search 'is:unread' --max 5"

# WRONG - PATH not set, will fail with 'gog: command not found'
wsl bash -c 'export GOG_ACCOUNT="you@gmail.com" && gog gmail search "is:unread" --max 5'
```

## Limitations

1. Google Meet links - Cannot be created via CLI (API limitation)
2. Workspace-only features - Chat, Keep, Groups require Google Workspace
3. OAuth consent - User must manually complete initial OAuth flow in browser
4. Token refresh - Tokens auto-refresh, but initial auth requires browser
5. Headless auth - Use `--manual` flag for servers without browser

## Token Expiry Re-Auth Flow

When you see `"invalid_grant" "Token has been expired or revoked"`, follow this flow:

### Step 1: Start Auth (Non-Blocking)

```powershell
wsl bash -c "export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/linuxbrew/.linuxbrew/bin'; export GOG_KEYRING_PASSWORD='<PASSWORD>'; gog auth add <EMAIL> --manual --force" 2>&1 | Select-String -Pattern 'state=' | ForEach-Object { $_.Line }
```

This outputs an OAuth URL. Note the `state=` parameter value.

### Step 2: Navigate with Playwright MCP

```js
// Navigate to the OAuth URL from Step 1
await page.goto('<OAUTH_URL_FROM_STEP_1>');
```

### Step 3: Click Through Consent

1. Click your account
2. If "Google hasn't verified this app" appears, click "Continue"
3. Click "Continue" on consent screen
4. Browser redirects to localhost (shows ERR_CONNECTION_REFUSED - this is expected)

### Step 4: Capture Redirect URL

```js
// Get redirect URL from network requests
await mcp1_browser_network_requests({ includeStatic: false })
// Look for: http://127.0.0.1:<PORT>/oauth2/callback?state=...&code=...
```

### Step 5: Complete Auth

```powershell
# Pipe the redirect URL to gogcli (must match state from Step 1)
wsl bash -c "export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/linuxbrew/.linuxbrew/bin'; export GOG_KEYRING_PASSWORD='<PASSWORD>'; echo '<REDIRECT_URL>' | gog auth add <EMAIL> --manual --force"
```

### Step 6: Verify

```powershell
wsl bash -c "export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/linuxbrew/.linuxbrew/bin'; export GOG_KEYRING_PASSWORD='<PASSWORD>'; export GOG_ACCOUNT='<EMAIL>'; gog --json gmail search 'is:unread' --max 3"
```

## Common Mistakes (Lessons Learned)

### 1. WSL PATH Not Set
**Symptom**: `gog: command not found`
**Fix**: Always use full PATH export in command:
```bash
export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/linuxbrew/.linuxbrew/bin'
```

### 2. State Mismatch
**Symptom**: `state mismatch` error when pasting redirect URL
**Cause**: Using redirect URL from a different auth session
**Fix**: The `state=` parameter in redirect URL must match the auth session. Start fresh auth and use that session's redirect URL.

### 3. Invalid Client ID
**Symptom**: `Error 401: invalid_client` / "The OAuth client was not found"
**Cause**: Using wrong client_id in OAuth URL
**Fix**: Get correct client_id from your client secret file:
```powershell
Get-Content "<CLIENT_SECRET_PATH>" | ConvertFrom-Json | Select-Object -ExpandProperty installed | Select-Object client_id
# Client secret path is in [WORKSPACE_FOLDER]/!NOTES.md under "gogcli" section
```

### 4. Terminal Truncates OAuth URL
**Symptom**: Cannot copy full OAuth URL from terminal
**Fix**: Use Playwright MCP to navigate directly - read client_id from JSON, construct URL with correct scopes.

### 5. Port Mismatch in Redirect URI
**Symptom**: Auth fails silently
**Cause**: gogcli uses random port each session (e.g., 8085, 45111)
**Fix**: Always capture redirect URL from same auth session via `mcp1_browser_network_requests`.

## Sources

- GitHub: https://github.com/steipete/gogcli
- Website: https://gogcli.sh/
