# Playwright MCP Tools Reference

Complete tool catalog for `@playwright/mcp` v0.0.70 (21 core + 40 opt-in). Tool parameters delivered via MCP `tools/list` handshake.

## Core Tools (21, always available)

**Navigation:**
- `browser_navigate` - Navigate to URL
- `browser_navigate_back` - Go back in history

**Element Interaction:**
- `browser_click` - Click element (supports `ref`, `selector`, `doubleClick`, `button`, `modifiers`)
- `browser_type` - Type text into element (supports `submit` to press Enter after, `slowly` for key-by-key)
- `browser_fill_form` - Fill multiple form fields at once. Takes `fields` array of `{ref, name, type, value}`. Field types: textbox, checkbox, radio, combobox, slider
- `browser_hover` - Hover over element
- `browser_drag` - Drag and drop between two elements
- `browser_select_option` - Select dropdown option(s) by value text
- `browser_press_key` - Press keyboard key (e.g., "Enter", "Control+A", "End")
- `browser_file_upload` - Upload files by path
- `browser_handle_dialog` - Accept/dismiss alert, confirm, or prompt dialogs

**Inspection (read-only):**
- `browser_snapshot` - Accessibility tree with element refs. Primary inspection tool. Supports partial snapshots via `ref`, `selector`, or `depth`
- `browser_take_screenshot` - Visual capture. Use `type: "jpeg"` to reduce size. Supports `fullPage`, element-specific via `ref`/`selector`
- `browser_console_messages` - Browser console logs. Filter by `level`: error, warning, info, debug
- `browser_network_requests` - Network request listing (read-only, no `--caps` needed). Filter with `filter` regex param

**JavaScript Execution:**
- `browser_evaluate` - Run JS in browser context. No Node.js APIs. Return value must be serializable
- `browser_run_code` - Run Playwright code snippet server-side with `page` object available

**Timing:**
- `browser_wait_for` - Wait for time (seconds), text to appear, or text to disappear

**Viewport:**
- `browser_resize` - Set browser window dimensions

**Session:**
- `browser_close` - Close page

**Tab Management:**
- `browser_tabs` - List, create, close, or select tabs. Actions: "list", "new", "close", "select"

## Opt-In Tools by Capability

Enabled via `--caps <category>` flag. Multiple: `--caps vision,network,storage`.

### Network (`--caps=network`)

Note: `browser_network_requests` (read-only listing) is a core tool above.

- `browser_network_state_set` - Toggle offline/online mode
- `browser_route` - Mock HTTP requests by URL pattern (set status, body, headers)
- `browser_route_list` - List active route mocks
- `browser_unroute` - Remove route mocks (by pattern, or all)

### Storage (`--caps=storage`)

**Cookies:** `browser_cookie_list`, `browser_cookie_get`, `browser_cookie_set`, `browser_cookie_delete`, `browser_cookie_clear`

**LocalStorage:** `browser_localstorage_list`, `browser_localstorage_get`, `browser_localstorage_set`, `browser_localstorage_delete`, `browser_localstorage_clear`

**SessionStorage:** `browser_sessionstorage_list`, `browser_sessionstorage_get`, `browser_sessionstorage_set`, `browser_sessionstorage_delete`, `browser_sessionstorage_clear`

**Storage State:**
- `browser_storage_state` - Save cookies + localStorage to file
- `browser_set_storage_state` - Restore from file (clears existing first)

### DevTools (`--caps=devtools`)

- `browser_resume` - Resume paused script execution (step over, step into, by location)
- `browser_start_tracing` / `browser_stop_tracing` - Record Chromium trace
- `browser_start_video` / `browser_stop_video` - Record video of page
- `browser_video_chapter` - Add chapter marker to recording

### Vision (`--caps=vision`)

Coordinate-based interactions for canvas, maps, custom widgets. Use `browser_take_screenshot` first to determine x,y positions.

- `browser_mouse_click_xy` - Click at coordinates (button, clickCount, delay)
- `browser_mouse_down` / `browser_mouse_up` - Press/release mouse button at position
- `browser_mouse_move_xy` - Move mouse to coordinates
- `browser_mouse_drag_xy` - Drag from start to end coordinates
- `browser_mouse_wheel` - Scroll by delta (deltaX, deltaY)

### PDF (`--caps=pdf`)

- `browser_pdf_save` - Save current page as PDF file

### Testing (`--caps=testing`)

- `browser_generate_locator` - Generate stable Playwright locator for element
- `browser_verify_element_visible` - Assert element is visible (by role and name)
- `browser_verify_text_visible` - Assert text is visible on page
- `browser_verify_list_visible` - Assert list items visible
- `browser_verify_value` - Assert element has expected value

### Config (`--caps=config`)

- `browser_get_config` - Get resolved server configuration (merged CLI + env + config file)

## Element Targeting

All interaction tools support two targeting methods (v0.0.69+):

1. **`ref`** - Element reference from latest `browser_snapshot`. Most reliable. Ephemeral: invalidated by any page change
2. **`selector`** - CSS or role-based selector. Stable across page changes. Priority:
   - `[data-testid="submit"]` - Test IDs (most stable)
   - `role=button[name="Save"]` - Semantic role selectors
   - `text=Sign in` - Visible text matching
   - `input[name="email"]` - HTML attribute selectors
