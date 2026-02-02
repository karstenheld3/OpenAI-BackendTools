# Troubleshooting

Common issues and solutions for Playwright MCP.

## npx not found

Use full path to npx:
```json
{
  "command": "[NPX_FULL_PATH]"
}
```

## Profile lock errors

Reset profile lock:
```powershell
Remove-Item "[USER_PROFILE_PATH]\.ms-playwright-mcp-profile\SingletonLock" -Force -ErrorAction SilentlyContinue
```

## Extension mode not connecting

Known issue (GitHub #921): `--extension` flag may launch new Chrome.
Workaround: Ensure Chrome is running with `--remote-debugging-port=9222` before starting MCP.

## Element not found

1. Call `browser_snapshot()` to refresh refs
2. Wait for page to fully load
3. Check if element is in iframe (use `browser_evaluate` to access)

## Automation detection

If site blocks automation:
1. Use `--user-data-dir` with existing browser profile
2. Use headed mode instead of headless
3. Try `--extension` mode with real browser

## Flaky Test Prevention

**Common causes:**
- Race conditions: Tests proceed before app ready
- Unstable selectors: IDs change between renders
- Network unpredictability: API response time varies
- State contamination: Tests share state

**Solutions:**
- Always call `browser_snapshot()` before interacting
- Use stable selectors (data-testid, roles, labels)
- Wait for specific elements, not arbitrary timeouts
- Isolate tests with fresh browser contexts
