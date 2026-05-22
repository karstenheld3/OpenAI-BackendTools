# Playwright MCP Troubleshooting

Common issues ordered by frequency.

## "Unsupported command-line flag: --no-sandbox" warning

**Cause:** `--no-sandbox` in config or `PLAYWRIGHT_MCP_NO_SANDBOX` env var set.
**Fix (if not needed):** Remove flag from config, unset env var.
**Fix (if needed - Docker/WSL2):** Keep it. Warning is cosmetic, browser works correctly.

## Element not found / stale reference

**Cause:** Page changed since last snapshot - refs are ephemeral.
**Fix:** Take fresh `browser_snapshot()` before interacting. This is the most common error.

## Chrome crashes with SIGTRAP in WSL2

**Cause:** Chromium sandbox requires kernel features unavailable in some WSL2 configurations.
**Fix:** Add `--no-sandbox` to MCP config args.

## npx not found

**Fix:** Install Node.js 18+, verify `npx --version`. On Windows, may need full path: `C:\Program Files\nodejs\npx.cmd`.

## Profile lock error

**Cause:** Previous Chrome instance didn't shut down cleanly.
**Fix:** Close running Chrome instances using same profile. Delete lock file in profile directory: `%LOCALAPPDATA%\ms-playwright\mcp-{channel}-{workspace-hash}`.

## Extension not connecting

**Checklist:**
1. "Playwright MCP Bridge" installed and enabled in Chrome/Edge
2. Chrome or Edge running (Firefox/WebKit not supported in extension mode)
3. Auth token matches (copy from extension icon popup)
4. No other debugger attached to the target tab
5. Try: re-install extension, restart Chrome

## Headed browser not visible (IDE worker process)

**Cause:** IDE runs MCP server in a background process without display access.
**Fix:** Use HTTP server mode:
1. Run `npx @playwright/mcp@latest --port 8931` from a terminal with display
2. Configure client with `"url": "http://localhost:8931/mcp"`

## Cookie popup keeps reappearing

**Cause:** Isolated mode (`--isolated`) clears all state between sessions.
**Fix:** Use persistent profile (default, remove `--isolated`) so cookie consent is remembered.

## Tools missing (e.g., cookie operations, route mocking)

**Cause:** Opt-in tools need `--caps` flag.
**Fix:** Add required capability: `--caps storage` for cookie tools, `--caps network` for route mocking, `--caps vision` for coordinate-based interactions.

## Automation detected by website

**Mitigations:**
- `--user-agent <standard-ua>` to set normal user agent
- Extension mode (real browser, no automation flags)
- `--init-script` to override `navigator.webdriver`
