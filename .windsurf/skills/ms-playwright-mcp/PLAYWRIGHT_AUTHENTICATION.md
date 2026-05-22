# Playwright MCP Authentication Reference

How to handle authenticated sessions and persistent logins.

## How to Maintain Logged-In Sessions

### 1. Persistent Profile (Default)

Browser state (cookies, localStorage, sessions) persists between MCP sessions automatically. No special configuration needed.

**How it works:**
- First session: log in manually or via automation
- Subsequent sessions: already logged in (cookies preserved)
- Profile location: `%LOCALAPPDATA%\ms-playwright\mcp-{channel}-{workspace-hash}` (Windows)

**Custom profile location:**
```json
{"args": ["@playwright/mcp@latest", "--user-data-dir", "C:/path/to/my-profile"]}
```

**Clear auth state:** Delete the profile directory.

### 2. Extension Mode (Existing Browser)

Connect to user's already-logged-in Chrome/Edge browser. Best for sites with complex auth (SSO, MFA, hardware keys).

**Setup:**
1. Install "Playwright MCP Bridge" from Chrome Web Store: https://chromewebstore.google.com/detail/playwright-mcp-bridge/mmlmfjhmonkocbjadbfplnigmagldckm
2. Add `--extension` to MCP config args
3. (Optional) Set `PLAYWRIGHT_MCP_EXTENSION_TOKEN` env var for auto-approval

**Config:**
```json
{
  "mcpServers": {
    "playwright-extension": {
      "command": "npx",
      "args": ["@playwright/mcp@latest", "--extension"],
      "env": {
        "PLAYWRIGHT_MCP_EXTENSION_TOKEN": "your-token-here"
      }
    }
  }
}
```

**Workflow:**
1. Agent sends first browser command
2. Tab selection UI appears - user picks which tab to control
3. Agent interacts with selected tab using all standard tools
4. User's existing cookies, sessions, extensions all available

**Key facts:**
- Uses `chrome.debugger` API internally (NOT `--remote-debugging-port`)
- Chrome/Edge only (Firefox/WebKit not supported)
- Auth token copied from extension icon popup in browser toolbar
- Ignores `browser` config (browser already running)

### 3. Isolated Mode with Storage State

Start clean but inject saved auth state:

**Save auth state** (requires `--caps=storage`):
```
browser_storage_state(filename: "auth-state.json")
```

**Load auth state on startup:**
```json
{"args": ["@playwright/mcp@latest", "--isolated", "--storage-state", "auth-state.json"]}
```

### 4. Initial State Injection

**`--init-page` (TypeScript)** - Set permissions, geolocation, viewport before automation:
```typescript
export default async ({ page }) => {
  await page.context().grantPermissions(['geolocation']);
  await page.context().setGeolocation({ latitude: 37.7749, longitude: -122.4194 });
};
```

**`--init-script` (JavaScript)** - Inject JS before page scripts (e.g., override navigator.webdriver):
```javascript
Object.defineProperty(navigator, 'webdriver', { get: () => false });
```

## Automation Detection Mitigations

- `--user-agent <ua>` - Set standard user agent string
- Extension mode uses real browser profile (no automation flags)
- `--init-script` to override `navigator.webdriver` and other detection signals
