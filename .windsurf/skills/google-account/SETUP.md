# Google Account Skill Setup (gogcli)

Setup guide for gogcli - Google services CLI for agent automation.

## Agent Invocation (from PowerShell)

**CRITICAL**: WSL PATH is often broken. Always use this pattern:

```powershell
wsl bash -c "export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/linuxbrew/.linuxbrew/bin'; gog <command>"
```

**Examples:**
```powershell
# Check version
wsl bash -c "export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/linuxbrew/.linuxbrew/bin'; gog --version"

# List unread emails
wsl bash -c "export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/linuxbrew/.linuxbrew/bin'; export GOG_ACCOUNT='you@gmail.com'; export GOG_KEYRING_PASSWORD='pass'; gog --json gmail search 'is:unread' --max 5"

# Download attachment
wsl bash -c "export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/linuxbrew/.linuxbrew/bin'; export GOG_ACCOUNT='you@gmail.com'; export GOG_KEYRING_PASSWORD='pass'; gog gmail thread get <threadId> --download --out-dir /mnt/e/Dev/USTVA/_Input"
```

**Current status**:
- [x] gogcli installed: v0.11.0 at `/home/linuxbrew/.linuxbrew/bin/gog`
- [ ] OAuth credentials configured
- [ ] Account authorized

## Quick OAuth Setup (Agent-Assisted via Playwright MCP)

Agent navigates Google Cloud Console, user approves OAuth. Full automation possible.

### Step 1: Create Project
```
https://console.cloud.google.com/projectcreate
```
- Set name: `gogcli-personal`
- Click Create
- Note PROJECT_ID from URL (e.g., `gogcli-personal-123456`)

### Step 2: Enable APIs
Navigate to each and click Enable:
```
https://console.cloud.google.com/apis/library/gmail.googleapis.com?project={PROJECT_ID}
https://console.cloud.google.com/apis/library/calendar-json.googleapis.com?project={PROJECT_ID}
https://console.cloud.google.com/apis/library/drive.googleapis.com?project={PROJECT_ID}
https://console.cloud.google.com/apis/library/tasks.googleapis.com?project={PROJECT_ID}
https://console.cloud.google.com/apis/library/people.googleapis.com?project={PROJECT_ID}
```

### Step 3: Configure OAuth Consent
```
https://console.cloud.google.com/apis/credentials/consent?project={PROJECT_ID}
```
- Click "Get started"
- App name: `gogcli`
- User support email: select your email
- Audience: **External**
- Developer contact: your email
- Agree to terms, Create

### Step 4: Add Test User (CRITICAL)
```
https://console.cloud.google.com/auth/audience?project={PROJECT_ID}
```
- Click "Add users"
- Enter your email address
- Save

**Without this step, OAuth will fail with "Error 403: access_denied"**

### Step 5: Create OAuth Client
```
https://console.cloud.google.com/auth/clients/create?project={PROJECT_ID}
```
- Application type: Desktop app
- Name: `gogcli-desktop`
- Create
- Download JSON (or use Playwright to capture from temp folder)

### Step 6: Store Credentials
```powershell
# If downloaded via Playwright MCP, file is in temp folder:
Copy-Item "$env:TEMP\playwright-mcp-output\*\client-secret-*.json" -Destination "$env:USERPROFILE\.gogcli\client-secret.json"

# Store in gogcli (adjust path to match where you saved the JSON)
wsl bash -c "export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/linuxbrew/.linuxbrew/bin'; gog auth credentials /mnt/c/Users/\$USER/.gogcli/client-secret.json"
```

### Step 7: Authorize Account (Agent-Assisted)

**Method A: Fully automated with Playwright MCP**

1. Start gogcli auth command (non-blocking):
```powershell
wsl bash -c "export PATH='...'; export GOG_KEYRING_PASSWORD='gogcli'; gog auth add your@gmail.com --services gmail --manual" | head -30
```

2. Agent navigates to auth URL via Playwright MCP
3. Agent clicks through account selection and consent screens
4. Browser redirects to localhost (fails with ERR_CONNECTION_REFUSED)
5. Agent captures redirect URL from `mcp1_browser_network_requests`
6. Pipe redirect URL to new gogcli command:
```powershell
echo "http://127.0.0.1:PORT/oauth2/callback?state=...&code=..." | wsl bash -c "export PATH='...'; export GOG_KEYRING_PASSWORD='gogcli'; gog auth add your@gmail.com --services gmail --manual"
```

**Method B: Manual in WSL terminal**
```bash
export PATH='/home/linuxbrew/.linuxbrew/bin:$PATH'
export GOG_KEYRING_PASSWORD='gogcli'
gog auth add your@gmail.com --manual
# Visit URL, approve, paste redirect URL back
```

### Verify Authorization
```powershell
wsl bash -c "export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/linuxbrew/.linuxbrew/bin'; export GOG_KEYRING_PASSWORD='gogcli'; gog auth status"
```

Expected output includes:
```
account your@gmail.com
credentials_exists      true
```

## Pre-Installation Verification

Complete ALL verification steps before modifying your system.
If any step fails, fix it before proceeding to installation.

### 1. Check WSL (Windows only)

```powershell
wsl --version
```

Expected: WSL version info (e.g., `WSL version: 2.0.9.0`)

If not installed:
1. Open PowerShell as Administrator
2. Run: `wsl --install`
3. Restart computer
4. Run `wsl` to complete Ubuntu setup

### 2. Check Homebrew in WSL

```bash
# In WSL terminal
brew --version
```

Expected: `Homebrew 4.x.x` or similar

If not installed:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> ~/.bashrc
```

### 3. Check Go (only if building from source)

```powershell
# Windows
go version
```

```bash
# WSL
go version
```

Expected: `go version go1.21` or higher

If not installed: https://go.dev/dl/

### Pre-Installation Checklist

- [ ] WSL installed and working (Option A/C)
- [ ] Homebrew installed in WSL (Option A)
- [ ] Go 1.21+ installed (Option B/C only)

**If all checks pass, proceed to installation.**

---

## Installation

### Step 1: Install gogcli

#### Option A: WSL with Homebrew (Recommended)

```bash
# In WSL terminal
brew install steipete/tap/gogcli
```

Expected: Installation completes without errors

```bash
# Verify
gog --version
```

Expected: `gogcli version 1.x.x` or similar

#### Option B: Build from Source (Windows Native)

```powershell
git clone https://github.com/steipete/gogcli.git
cd gogcli
go build -o bin/gog.exe ./cmd/gog
```

Expected: `bin/gog.exe` created

```powershell
# Add to PATH
$env:Path += ";$PWD\bin"

# Verify
gog.exe --version
```

Expected: `gogcli version 1.x.x`

#### Option C: Build from Source (WSL)

```bash
git clone https://github.com/steipete/gogcli.git
cd gogcli
make
```

Expected: Build completes, `bin/gog` created

```bash
# Add to PATH
export PATH="$PATH:$PWD/bin"
echo 'export PATH="$PATH:~/gogcli/bin"' >> ~/.bashrc

# Verify
gog --version
```

Expected: `gogcli version 1.x.x`

### Step 2: Create Google Cloud Project

1. Open: https://console.cloud.google.com/projectcreate
2. Enter project name (e.g., "gogcli-personal")
3. Click Create
4. Note the Project ID

### Step 3: Enable APIs

Enable each API for your project:

- Gmail API: https://console.cloud.google.com/apis/api/gmail.googleapis.com
- Calendar API: https://console.cloud.google.com/apis/api/calendar-json.googleapis.com
- Drive API: https://console.cloud.google.com/apis/api/drive.googleapis.com
- Tasks API: https://console.cloud.google.com/apis/api/tasks.googleapis.com
- People API: https://console.cloud.google.com/apis/api/people.googleapis.com

For each: Click "Enable" button.

Expected: Each API shows "API enabled" status.

### Step 4: Configure OAuth Consent Screen

1. Open: https://console.cloud.google.com/auth/branding
2. User Type: External (or Internal for Workspace)
3. App name: "gogcli"
4. User support email: Your email
5. Developer contact: Your email
6. Save and Continue
7. Scopes: Skip (gogcli requests scopes at runtime)
8. Test users: Add your Google account email
9. Save

Expected: Consent screen shows "Publishing status: Testing"

### Step 5: Create OAuth Client

1. Open: https://console.cloud.google.com/auth/clients
2. Click "Create Client"
3. Application type: Desktop app
4. Name: "gogcli-desktop"
5. Click Create
6. Download JSON (button: "Download JSON")
7. Save as `client_secret.json` to `[WORKSPACE_FOLDER]/../.tools/gogcli-client-secret.json`

Expected: JSON file downloaded (contains `client_id` and `client_secret`)

### Step 6: Store Credentials

```bash
# Store OAuth client credentials (from shared .tools folder)
gog auth credentials ~/.tools/gogcli-client-secret.json
```

Expected: `Credentials stored successfully`

```bash
# Verify stored
gog auth credentials list
```

Expected: Shows your client ID

### Step 7: Authorize Account

#### Interactive (with browser)

```bash
gog auth add you@gmail.com
```

Browser opens for OAuth consent. Approve all requested permissions.

#### Headless (WSL/server without browser)

```bash
gog auth add you@gmail.com --services user --manual
```

1. Copy the printed URL
2. Open in browser on another machine
3. Approve permissions
4. Copy the full redirect URL from browser address bar
5. Paste back into terminal

Expected: `Account added successfully` or similar

### Step 8: Configure for Agent Automation

#### Set Keyring Backend

```bash
# Use file backend (no OS keychain dependency)
gog auth keyring file

# Set password for non-interactive access
export GOG_KEYRING_PASSWORD='your-secure-password'
```

#### Persist Environment Variables

Add to `~/.bashrc` or `~/.profile`:

```bash
export GOG_ACCOUNT='you@gmail.com'
export GOG_KEYRING_BACKEND='file'
export GOG_KEYRING_PASSWORD='your-secure-password'

# Optional: Restrict commands for security
export GOG_ENABLE_COMMANDS='gmail,calendar,tasks,drive'
```

Reload:
```bash
source ~/.bashrc
```

Expected: No output (variables set silently)

### Step 9: Verify Setup

```bash
# Check auth status
gog auth status

# Test Gmail
gog gmail labels list

# Test Calendar
gog calendar events primary --today

# Test with JSON output
gog --json gmail search 'is:unread' --max 5
```

Expected: Commands return data without prompts or errors.

### Step 10: Create Attachments Directory

```bash
# Create directory for downloaded attachments
mkdir -p [TOOLS_FOLDER]/_downloaded_attachments
```

Replace `[TOOLS_FOLDER]` with your actual tools directory path.

## Troubleshooting

### "No credentials found"

```bash
gog auth credentials ~/path/to/client_secret.json
```

### "Token expired" or "Invalid grant"

```bash
gog auth add you@gmail.com --force-consent
```

### "Keyring password required"

Set environment variable:
```bash
export GOG_KEYRING_PASSWORD='your-password'
```

### WSL: "gog: command not found"

Add to PATH:
```bash
# If installed via Homebrew
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"

# If built from source
export PATH="$PATH:~/gogcli/bin"
```

### Permission denied errors

Ensure APIs are enabled in Google Cloud Console (Step 3).

### Rate limiting

gogcli respects Google API quotas. For high-volume use, request quota increase in Cloud Console.

## Security Notes

- Store `client_secret.json` outside workspace (not in git)
- Use environment variables for `GOG_KEYRING_PASSWORD`
- Never commit credentials or tokens
- Use `GOG_ENABLE_COMMANDS` to restrict available commands
- Consider separate OAuth client for each environment

## Completion Checklist

- [ ] gogcli installed and in PATH
- [ ] Google Cloud Project created
- [ ] APIs enabled (Gmail, Calendar, Drive, Tasks, People)
- [ ] OAuth consent screen configured
- [ ] OAuth Desktop client created and JSON downloaded
- [ ] Credentials stored: `gog auth credentials`
- [ ] Account authorized: `gog auth add`
- [ ] Keyring backend set to file
- [ ] Environment variables configured
- [ ] Test commands work without prompts
- [ ] Attachments directory created
