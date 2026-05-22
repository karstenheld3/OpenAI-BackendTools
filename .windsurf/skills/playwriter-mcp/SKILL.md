---
name: playwriter-mcp
description: ONLY apply when user EXPLICITLY mentions "Playwriter". Default browser automation is ms-playwright-mcp.
---

# Playwriter MCP Guide

**ACTIVATION**: Only use when user explicitly says "Playwriter". Default browser MCP is `ms-playwright-mcp` by Microsoft.

Rules and usage for Playwriter - Chrome extension + CLI/MCP for real browser automation.

## Table of Contents

**Core**
- [When to Use](#when-to-use-playwriter-vs-playwright-mcp)
- [Intent Lookup](#intent-lookup)
- [MUST-NOT-FORGET](#must-not-forget)

**Workflows**
- [Quick Start](#quick-start)
- [Common Workflows](#common-workflows)
- [Screenshots](#screenshots)
- [Visual Labels](#visual-labels)
- [Screen Recording](#screen-recording-assumed)

**Reference**
- [CLI Commands](#cli-commands)
- [MCP Configuration](#mcp-configuration)
- [Troubleshooting](#troubleshooting)
- [Security](#security)
- [Setup](SETUP.md) - Installation

## When to Use Playwriter (vs Playwright MCP)

**Use Playwriter when**:
- Need existing logged-in sessions (bank, email, social media)
- Want to use your ad blockers, password managers, extensions
- Avoiding automation/bot detection
- Collaborating with AI in real-time (you see what it does)

**Use Playwright MCP when**:
- Need clean, isolated sessions
- Testing without user state
- Standard automation without auth requirements

## Intent Lookup

**User wants to...**
- **Check bank account / pay bills** -> Existing session, visual labels, `snapshot({ page })`
- **Read email / send messages** -> Existing Gmail/Outlook session, no re-auth
- **Post to social media** -> Bypass bot detection, use existing cookies
- **Fill government forms** -> Use saved passwords, extensions
- **Scrape authenticated content** -> No login needed, existing cookies
- **Debug web app** -> `getCDPSession`, `createDebugger`, breakpoints
- **Record demo/tutorial** -> `startRecording` / `stopRecording`
- **Collaborate with AI** -> Real-time visibility, can intervene

**Technical tasks...**
- **Get element refs** -> `snapshot({ page })` or `screenshotWithAccessibilityLabels({ page })`
- **Take screenshot** -> `page.screenshot({ path: '...', type: 'jpeg' })`
- **Click by ref** -> `page.locator('aria-ref=e5').click()`
- **Persist data** -> `state.varName = ...`
- **Intercept API** -> `page.on('response', ...)`
- **Record session** -> `startRecording` / `stopRecording`

## MUST-NOT-FORGET

- Install Chrome extension FIRST (from Chrome Web Store)
- Click extension icon on tab to enable control (icon turns green)
- Use single quotes for `-e` to prevent bash interpretation
- Never call `browser.close()` - it closes YOUR Chrome
- Use `state.varName` to persist data between calls
- Green icon = connected, gray = not controlled
- **TIMEOUTS**: ALWAYS pass timeout (default 20000ms is too long!). Use `1500` for simple ops, `3000` for screenshots.
- **NO waitForTimeout inside code** - causes stalls. Use proper waits like `waitForSelector` instead.
- **goto() stalls on SPAs** - default `waitUntil: 'load'` never fires on SharePoint/dynamic sites. Use `{ waitUntil: 'domcontentloaded' }`.
- **click() can stall** - if element triggers animation/loading that blocks. Don't click multiple elements in one call.
- **After any cancellation** - always check connection before proceeding with more operations.
- **If stalled, reset won't work** - user must restart Chrome or click extension icon again.

## Quick Start

```bash
# 1. Install CLI
npm i -g playwriter

# 2. Create session
playwriter session new  # outputs ID (e.g., 1)

# 3. Navigate
playwriter -s 1 -e 'await page.goto("https://example.com")'

# 4. Get accessibility snapshot
playwriter -s 1 -e 'console.log(await snapshot({ page }))'

# 5. Click element by ref
playwriter -s 1 -e 'await page.locator("aria-ref=e5").click()'
```

## CLI Commands

### Session Management

```bash
playwriter session new          # Create sandbox, get ID
playwriter session list         # Show sessions + state keys
playwriter session reset <id>   # Fix connection issues
```

### Execute Code

```bash
playwriter -s <id> -e '<code>'  # Run Playwright code in session
```

**Variables in scope**: `page`, `context`, `state`, `require`

## Common Workflows

### Navigate and Screenshot

```bash
playwriter -s 1 -e 'await page.goto("https://example.com")'
playwriter -s 1 -e 'await page.screenshot({ path: "screenshot.png" })'
```

### Screenshot with Visual Labels

```bash
playwriter -s 1 -e 'await screenshotWithAccessibilityLabels({ page })'
# Returns screenshot with Vimium-style labels (aria-ref=e1, e2, etc.)
playwriter -s 1 -e 'await page.locator("aria-ref=e5").click()'
```

### Persist Data Between Calls

```bash
playwriter -s 1 -e "state.users = await page.$$eval('.user', els => els.map(e => e.textContent))"
playwriter -s 1 -e "console.log(state.users)"
```

### Create Isolated Page

```bash
playwriter -s 1 -e 'state.myPage = await context.newPage(); await state.myPage.goto("https://example.com")'
```

### Intercept Network Requests

```bash
playwriter -s 1 -e "state.requests = []; page.on('response', r => { if (r.url().includes('/api/')) state.requests.push(r.url()) })"
playwriter -s 1 -e "await Promise.all([page.waitForResponse(r => r.url().includes('/api/')), page.click('button')])"
playwriter -s 1 -e "console.log(state.requests)"
```

## Screenshots

```bash
# Basic screenshot
playwriter -s 1 -e 'await page.screenshot({ path: "screenshot.png" })'

# Full page
playwriter -s 1 -e 'await page.screenshot({ path: "full.png", fullPage: true })'

# JPEG (smaller)
playwriter -s 1 -e 'await page.screenshot({ path: "shot.jpg", type: "jpeg", quality: 80 })'
```

## Visual Labels

Vimium-style labels for AI element identification:

```bash
playwriter -s 1 -e 'await screenshotWithAccessibilityLabels({ page })'
playwriter -s 1 -e 'await page.locator("aria-ref=e5").click()'
```

**Color coding**:
- Yellow = links
- Orange = buttons
- Coral = inputs
- Pink = checkboxes
- Peach = sliders
- Salmon = menus
- Amber = tabs

## Accessibility Snapshot (No Screenshot)

```bash
playwriter -s 1 -e 'console.log(await snapshot({ page }))'
# Returns accessibility tree with aria-ref selectors
```

## Screen Recording [ASSUMED]

```bash
# Start recording
playwriter -s 1 -e 'await startRecording({ page, outputPath: "./recording.mp4", frameRate: 30 })'

# Navigate, interact...
playwriter -s 1 -e 'await page.click("a")'

# Stop and save
playwriter -s 1 -e 'await stopRecording({ page })'
```

Recording survives page navigation (uses `chrome.tabCapture`).

## MCP Configuration

**Skill-based (recommended)**:
```bash
npx -y skills add remorses/playwriter
```

**Direct MCP config**:
```json
{
  "mcpServers": {
    "playwriter": {
      "command": "npx",
      "args": ["playwriter@latest"]
    }
  }
}
```

## Troubleshooting

### View Logs

```bash
playwriter logfile  # Shows path to ~/.playwriter/relay-server.log
```

### All Pages Return about:blank

Restart Chrome (known Chrome bug in `chrome.debugger` API).

### Extension Icon Not Turning Green

1. Ensure extension installed from Chrome Web Store
2. Click directly on extension icon (not right-click menu)
3. Try `playwriter session reset <id>`

### Connection Issues

```bash
playwriter session reset <id>
```

## Security

- WebSocket binds to `localhost:19988` only (any local process can connect; use `--token` for auth)
- Only tabs where you clicked extension icon are controlled
- Chrome shows automation banner on controlled tabs
- Malicious websites cannot connect

## Requirements

- Chrome/Chromium browser
- Node.js 18+ with npm
- Playwriter Chrome extension (from Chrome Web Store)

See [SETUP.md](SETUP.md) for installation details.
