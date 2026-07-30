---
name: ms-playwright-mcp
description: Automates browser interactions via Microsoft Playwright MCP server (@playwright/mcp). Use when navigating websites, filling forms, taking screenshots, scraping web data, testing web UI, or automating any browser-based task. Covers persistent sessions, extension mode for existing browser tabs, and 40+ browser automation tools.
compatibility: Requires Node.js 18+ and @playwright/mcp package via npx
---

# Playwright MCP Skill

Workflow guidance for Microsoft Playwright MCP server. Tool parameters are delivered by MCP `tools/list` handshake - this skill provides procedures, gotchas, and decision logic.

**References** (loaded on demand):
- [PLAYWRIGHT_TOOLS.md](PLAYWRIGHT_TOOLS.md) - Complete tool catalog (21 core + 40 opt-in)
- [PLAYWRIGHT_CONFIG.md](PLAYWRIGHT_CONFIG.md) - All CLI flags, env vars, JSON config
- [PLAYWRIGHT_AUTHENTICATION.md](PLAYWRIGHT_AUTHENTICATION.md) - Extension mode, persistent profiles
- [PLAYWRIGHT_TROUBLESHOOTING.md](PLAYWRIGHT_TROUBLESHOOTING.md) - Common issues with fixes
- [SETUP.md](SETUP.md) - Installation
- [UNINSTALL.md](UNINSTALL.md) - Uninstallation

## MUST-NOT-FORGET

1. Use `browser_snapshot` (accessibility tree) for element discovery, not screenshots
2. Element refs are ephemeral - ALWAYS re-snapshot before clicking after any navigation or page change
3. Reference elements via `ref` from snapshot (e.g., `ref: "e5"`) or `selector` (e.g., `[data-testid="submit"]`)
4. Use `type: "jpeg"` for all screenshots (default PNG produces unnecessarily large files)
5. NEVER auto-close browser - only user may close. Sessions preserve authentication state
6. `browser_fill_form` takes `fields` array (NOT `browser_fill`). `browser_take_screenshot` (NOT `browser_screenshot`)
7. Opt-in tools need `--caps` flag. Cookie read needs `--caps=storage`. Route mocking needs `--caps=network`
8. `browser_evaluate` runs in browser (no Node.js APIs). `browser_run_code` runs server-side with Playwright `page` object
9. Downloads go to `--output-dir` path. Default: `.playwright-mcp/` under the IDE user data folder (NOT the system Downloads folder). Use `find_by_name` in the IDE data dir to locate downloaded files if path unknown
10. Extension mode: Chrome/Edge only, uses Chrome Web Store extension, NOT `--remote-debugging-port`

## Intent Lookup

**User wants to...**
- **Read a webpage / research a topic** → Navigate, snapshot, dismiss cookie popup, scroll for lazy content
- **Fill out a form** → Snapshot to get refs, `browser_fill_form` with fields array, click submit
- **Take a screenshot** → `browser_take_screenshot(type: "jpeg")`, or `fullPage: true` for complete page
- **Log into a site** → Fill credentials + submit, or use persistent profile. See [PLAYWRIGHT_AUTHENTICATION.md](PLAYWRIGHT_AUTHENTICATION.md)
- **Use an already logged-in browser** → Extension mode (`--extension`). See [PLAYWRIGHT_AUTHENTICATION.md](PLAYWRIGHT_AUTHENTICATION.md)
- **Scrape data** → `browser_evaluate` with JS to extract DOM content, or `browser_snapshot` for structured text
- **Test a web UI** → Navigate, snapshot, assert elements present, use `--caps=testing` for verification tools
- **Download a file** → Find link with snapshot, click to download, check output dir
- **Interact with a map / canvas / custom widget** → Need `--caps=vision` for coordinate-based click/drag
- **Mock API responses** → Need `--caps=network`, use `browser_route` with URL pattern
- **Handle cookie/General Data Protection Regulation (GDPR) popups** → Snapshot, find accept/reject button, click it. See [Dismiss Cookie Popup](#5-dismiss-cookiegdpr-popup)
- **Debug browser issues** → See [PLAYWRIGHT_TROUBLESHOOTING.md](PLAYWRIGHT_TROUBLESHOOTING.md)

## Core Procedures

### 1. Navigate and Interact

```
1. browser_navigate(url: "https://example.com")
2. browser_snapshot()                              # Get element refs
3. # If cookie popup visible: find accept button, click it, re-snapshot
4. browser_click(ref: "e12", element: "Target button")
5. browser_snapshot()                              # Verify result, get new refs
```

After EVERY navigation or click that changes the page: re-snapshot. Refs from previous snapshot are invalid.

### 2. Fill a Form

```
1. browser_snapshot()                              # Find form fields
2. browser_fill_form(fields: [
     {ref: "e3", name: "Email", type: "textbox", value: "user@example.com"},
     {ref: "e5", name: "Password", type: "textbox", value: "password123"}
   ])
3. browser_click(ref: "e8", element: "Submit button")
4. browser_snapshot()                              # Verify submission result
```

Field types: `textbox`, `checkbox` (value: "true"/"false"), `radio`, `combobox` (value: option text), `slider`.

### 3. Full Page Screenshot

```
1. browser_navigate(url: "https://example.com")
2. browser_snapshot()                              # Check for cookie popups
3. # Dismiss cookie popup if present
4. # Scroll down to trigger lazy-loaded content:
   browser_press_key(key: "End")
   browser_wait_for(time: 2)
   browser_press_key(key: "Home")
5. browser_take_screenshot(fullPage: true, type: "jpeg")
```

### 4. Extract Data with JavaScript

```
1. browser_navigate(url: "https://example.com")
2. browser_evaluate(function: "document.querySelectorAll('h2').length")
3. browser_evaluate(function: "JSON.stringify([...document.querySelectorAll('tr')].map(r => r.textContent))")
```

`browser_evaluate` runs in browser context. No Node.js APIs. Return values must be serializable.
For Playwright API access (e.g., `page.locator()`), use `browser_run_code` instead.

### 5. Dismiss Cookie/GDPR Popup

```
1. browser_snapshot()
2. # Look for buttons with text: Accept, Agree, OK, Got it, Allow, Consent
3. browser_click(ref: "<popup-button-ref>", element: "Accept cookies")
4. browser_snapshot()                              # Verify popup dismissed
```

If popup uses iframe: snapshot may show it nested. Try clicking by text selector: `selector: "text=Accept"`.

### 6. Scroll and Load Lazy Content

```
1. browser_press_key(key: "End")                   # Scroll to bottom
2. browser_wait_for(time: 2)                        # Wait for lazy load
3. browser_snapshot()                              # Check if new content appeared
4. # Repeat if more content expected
```

For infinite scroll: repeat scroll+wait+snapshot in a loop until content stops changing.

## Element Targeting

Two methods (v0.0.69+):

1. **`ref` from snapshot** (preferred) - `ref: "e5"` from latest `browser_snapshot`
2. **`selector`** (when refs unavailable) - priority order:
   - `[data-testid="submit"]` - Test IDs (most stable)
   - `role=button[name="Save"]` - Semantic roles
   - `text=Sign in` - Visible text
   - `input[name="email"]` - HTML attributes

All interaction tools (`browser_click`, `browser_type`, `browser_hover`, etc.) accept both `ref` and `selector`.

## Capabilities Quick Reference

Core 21 tools always available. Opt-in categories enabled via `--caps`:

- **network** - Route mocking, offline toggle
- **storage** - Cookie/localStorage/sessionStorage Create/Read/Update/Delete (CRUD)
- **devtools** - Tracing, video recording, debugger
- **vision** - Coordinate-based mouse (for canvas/maps)
- **pdf** - Save page as PDF
- **testing** - Element/text/value verification, locator generation
- **config** - Read resolved server configuration

Enable all: `--caps vision,pdf,devtools,network,storage,testing,config`. Tool details: [PLAYWRIGHT_TOOLS.md](PLAYWRIGHT_TOOLS.md)

## Gotchas

- **Refs invalidated by any page change** - navigation, DOM mutation, dynamic content. Always re-snapshot before interacting
- **`browser_fill_form` not `browser_fill`** - Old name deprecated. New API takes `fields` array, not single field
- **`browser_take_screenshot` not `browser_screenshot`** - Old name deprecated
- **`browser_evaluate` runs in BROWSER** - No Node.js. Use `browser_run_code` for server-side Playwright API
- **Cookie read needs `--caps=storage`** - Even basic `browser_cookie_list` is gated
- **`browser_network_requests` is core** - Read-only request listing. Route mocking needs `--caps=network`
- **Extension mode is Chrome/Edge only** - Firefox/WebKit not supported
- **`--no-sandbox` warning is cosmetic** - Browser works correctly. Required in Docker/WSL2
- **Default screenshot format is PNG** - Always specify `type: "jpeg"` for smaller files
- **Profile lock error** - Previous Chrome didn't shut down cleanly. Close Chrome instances or delete lock file

## Quick Config

**Basic (persistent profile, default):**
```json
{"mcpServers": {"playwright": {"command": "npx", "args": ["@playwright/mcp@latest"]}}}
```

**Persistent profile with all capabilities:**
```json
{"mcpServers": {"playwright": {"command": "npx", "args": ["@playwright/mcp@latest", "--caps", "vision,pdf,devtools,network,storage,testing,config"]}}}
```

**Extension mode (existing browser):**
```json
{"mcpServers": {"playwright": {"command": "npx", "args": ["@playwright/mcp@latest", "--extension"]}}}
```

Full config reference: [PLAYWRIGHT_CONFIG.md](PLAYWRIGHT_CONFIG.md)
