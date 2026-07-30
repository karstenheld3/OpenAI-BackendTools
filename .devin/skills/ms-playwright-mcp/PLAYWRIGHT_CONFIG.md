# Playwright MCP Configuration Reference

Package: `@playwright/mcp` | Repo: github.com/microsoft/playwright-mcp | Latest: v0.0.70

## Configuration Precedence

CLI flags > environment variables > JSON config file

## Environment Variables

Every CLI flag has a `PLAYWRIGHT_MCP_` env var equivalent. Uppercase, hyphens become underscores:
- `--no-sandbox` = `PLAYWRIGHT_MCP_NO_SANDBOX`
- `--user-data-dir` = `PLAYWRIGHT_MCP_USER_DATA_DIR`
- `--caps` = `PLAYWRIGHT_MCP_CAPS`

## CLI Flags Reference

**Browser Selection and Launch:**
- `--browser <browser>` - chromium (default), chrome, firefox, webkit, msedge
- `--executable-path <path>` - Custom browser binary
- `--headless` - Headless mode (headed by default)
- `--device <device>` - Device emulation, e.g., "iPhone 15"
- `--viewport-size <size>` - Viewport, e.g., "1280x720"
- `--user-agent <ua>` - Custom user agent string

**Profile and Session:**
- `--user-data-dir <path>` - Custom profile directory (overrides default workspace-scoped location)
- `--isolated` - In-memory profile, nothing persists
- `--storage-state <path>` - Load cookies/localStorage from JSON file
- `--save-session` - Save session to output directory

**Initialization:**
- `--init-page <path...>` - TypeScript file evaluated on Playwright page object before automation
- `--init-script <path...>` - JavaScript injected before page scripts (multiple files allowed)

**Capabilities:**
- `--caps <caps>` - Comma-separated opt-in categories: vision, pdf, devtools, network, storage, testing, config

**Connection:**
- `--extension` - Connect via "Playwright MCP Bridge" Chrome extension
- `--cdp-endpoint <endpoint>` - Chrome DevTools Protocol endpoint
- `--cdp-header <headers...>` - CDP headers
- `--cdp-timeout <timeout>` - CDP connect timeout (default 30000ms)
- `--endpoint <endpoint>` - Bound browser endpoint

**Server (HTTP/Server-Sent Events (SSE) mode):**
- `--port <port>` - Enable HTTP/SSE transport
- `--host <host>` - Bind address (default localhost, use 0.0.0.0 for all interfaces)
- `--allowed-hosts <hosts...>` - Allowed hosts ('*' disables check)
- `--shared-browser-context` - Share browser context between HTTP clients

**Network:**
- `--allowed-origins <origins>` - Semicolon-separated trusted origins (NOT a security boundary, NOT affecting redirects)
- `--blocked-origins <origins>` - Semicolon-separated blocked origins (evaluated before allowlist)
- `--block-service-workers` - Block service workers
- `--proxy-server <proxy>` - HTTP proxy, e.g., "http://myproxy:3128"
- `--proxy-bypass <bypass>` - Domains to bypass proxy
- `--ignore-https-errors` - Ignore HTTPS certificate errors

**Security:**
- `--no-sandbox` - Disable Chromium sandbox (required for Docker/WSL2, cosmetic warning elsewhere)
- `--sandbox` - Enable extra sandbox for normally non-sandboxed processes
- `--secrets <path>` - Dotenv file; matching text in responses is replaced (convenience, not secure)
- `--allow-unrestricted-file-access` - Allow file access outside workspace roots
- `--grant-permissions <perms...>` - Browser permissions: geolocation, clipboard-read, clipboard-write

**Output:**
- `--output-dir <path>` - Directory for output files (screenshots, PDFs, videos)
- `--output-mode <mode>` - "file" or "stdout" (default)
- `--image-responses <mode>` - "allow", "omit", or "auto" (default)
- `--snapshot-mode <mode>` - "full" (default) or "none"
- `--console-level <level>` - Console level: error, warning, info, debug

**Code Generation:**
- `--codegen <lang>` - "typescript" (default) or "none"

**Testing:**
- `--test-id-attribute <attr>` - Test ID attribute (default "data-testid")

**Timeouts:**
- `--timeout-action <ms>` - Action timeout (default 5000ms)
- `--timeout-navigation <ms>` - Navigation timeout (default 60000ms)

## JSON Config File

Activated with `--config path/to/config.json`:

```json
{
  "browser": {
    "browserName": "chromium",
    "isolated": false,
    "userDataDir": "/path/to/profile",
    "launchOptions": {},
    "contextOptions": {},
    "cdpEndpoint": "ws://...",
    "cdpHeaders": {},
    "cdpTimeout": 30000,
    "remoteEndpoint": "ws://...",
    "initPage": ["init-page.ts"],
    "initScript": ["init-script.js"]
  },
  "extension": false,
  "server": {
    "port": 8931,
    "host": "localhost",
    "allowedHosts": ["*"]
  },
  "capabilities": ["core", "vision", "pdf", "devtools", "network", "storage", "testing", "config"],
  "saveSession": false,
  "sharedBrowserContext": false,
  "secrets": { "API_KEY": "sk-..." },
  "outputDir": "./output",
  "console": { "level": "info" },
  "network": {
    "allowedOrigins": ["https://example.com:*"],
    "blockedOrigins": ["https://ads.example.com:*"]
  },
  "testIdAttribute": "data-testid",
  "timeouts": { "action": 5000, "navigation": 60000, "expect": 5000 },
  "imageResponses": "auto",
  "snapshot": { "mode": "full" },
  "allowUnrestrictedFileAccess": false,
  "codegen": "typescript"
}
```

## Default Profile Locations

Workspace-scoped persistent profiles (default, not isolated):

- **Windows**: `%LOCALAPPDATA%\ms-playwright\mcp-{channel}-{workspace-hash}`
- **macOS**: `~/Library/Caches/ms-playwright/mcp-{channel}-{workspace-hash}`
- **Linux**: `~/.cache/ms-playwright/mcp-{channel}-{workspace-hash}`

Workspace hash derived from MCP client's workspace root - different projects get separate profiles. Override with `--user-data-dir <path>`. Delete profile directory to clear all state.

## Deployment Modes

**Stdio (default)** - MCP client spawns server:
```json
{"mcpServers": {"playwright": {"command": "npx", "args": ["@playwright/mcp@latest"]}}}
```

**HTTP/SSE** - Standalone server (for headed browser on headless systems):
```bash
npx @playwright/mcp@latest --port 8931
```
Client: `{"mcpServers": {"playwright": {"url": "http://localhost:8931/mcp"}}}`

**Docker** - Headless Chromium, `--no-sandbox` required:
```json
{"mcpServers": {"playwright": {"command": "docker", "args": ["run", "-i", "--rm", "--init", "--pull=always", "mcr.microsoft.com/playwright/mcp"]}}}
```

## Requirements

- Node.js 18+ with npx in PATH
- Chrome/Chromium for headed mode
- For extension mode: Chrome or Edge with "Playwright MCP Bridge" extension from Chrome Web Store
