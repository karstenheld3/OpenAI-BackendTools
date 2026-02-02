# Advanced Playwright MCP Workflows

Detailed workflows for cookie popups, scrolling, expanding collapsed items, full page screenshots, and link extraction.

## 1. Close Cookie Popups

Cookie consent popups block page interaction. Two strategies:

**Strategy A: Click the accept button (preferred)**
```
1. browser_snapshot()
2. // Look for cookie-related buttons: "Accept", "OK", "I agree", "Accept all"
3. browser_click(element: "Accept cookies button", ref: "e15")
4. browser_snapshot()  // Verify popup dismissed
```

**Strategy B: Remove popup via JavaScript**
```
1. browser_evaluate(expression: "(() => {
     // Common cookie popup selectors
     const selectors = [
       '#cookie-banner', '#cookieModal', '.cookie-consent',
       '[class*=\"cookie\"]', '[id*=\"cookie\"]',
       '.gdpr-banner', '#onetrust-consent-sdk'
     ];
     selectors.forEach(sel => {
       document.querySelectorAll(sel).forEach(el => el.remove());
     });
     // Remove backdrop/overlay
     document.querySelectorAll('.modal-backdrop, [class*=\"overlay\"]')
       .forEach(el => el.remove());
     // Restore scrolling
     document.body.style.overflow = 'auto';
   })()")
```

**Best practice:** Try clicking first (sets cookie to prevent reappearance), fall back to removal if button not found.

## 2. Scroll Page for Lazy-Loaded Content

Pages with lazy-loaded images or infinite scroll need scrolling before screenshot.

**Scroll to bottom (simple):**
```
1. browser_evaluate(expression: "window.scrollTo(0, document.body.scrollHeight)")
2. browser_wait_for(time: 1)  // Wait for content to load
3. browser_snapshot()
```

**Scroll incrementally (for lazy-load images):**
```
1. browser_evaluate(expression: "(async () => {
     const delay = ms => new Promise(r => setTimeout(r, ms));
     const maxScrolls = 50;
     let prevHeight = -1;
     for (let i = 0; i < maxScrolls; i++) {
       window.scrollBy(0, 400);
       await delay(200);
       if ((window.scrollY + window.innerHeight) >= document.body.scrollHeight) break;
     }
     window.scrollTo(0, 0);
   })()")
```

**Using keyboard (End key):**
```
1. browser_press_key(key: "End")
2. browser_wait_for(time: 1)
3. browser_press_key(key: "Home")  // Return to top
```

**Using mouse wheel:**
```
1. // Scroll down 400px at a time
2. browser_evaluate(expression: "window.scrollBy(0, 400)")
3. browser_wait_for(time: 0.3)
4. // Repeat until bottom reached
```

## 3. Expand Collapsed Items

Accordions, dropdowns, and collapsible sections must be expanded before capture.

**Find and click all expand buttons:**
```
1. browser_snapshot()
2. // Look for collapsed indicators: "+", "Show more", "Expand", chevron icons
3. browser_click(element: "Expand section", ref: "e20")
4. browser_snapshot()  // Get updated refs, repeat for other collapsed items
```

**Expand all via JavaScript:**
```
1. browser_evaluate(expression: "(() => {
     // Click all accordion headers/toggles
     document.querySelectorAll('[aria-expanded=\"false\"]')
       .forEach(el => el.click());
     // Click elements with expand-related classes
     document.querySelectorAll('.collapsed, .accordion-button:not(.show), [data-toggle=\"collapse\"]')
       .forEach(el => el.click());
     // Open all details elements
     document.querySelectorAll('details:not([open])')
       .forEach(el => el.setAttribute('open', ''));
   })()")
2. browser_wait_for(time: 0.5)  // Wait for animations
3. browser_snapshot()
```

**Common patterns to look for in snapshot:**
- `[aria-expanded="false"]` - Collapsed ARIA elements
- `details` without `[open]` - Native HTML collapsibles
- Buttons with "+", "Show", "Expand" text
- Elements with `collapsed` or `accordion` classes

## 4. Full Page Screenshot (Complete Workflow)

**Complete workflow (handles lazy-load + popups):**
```
1. browser_navigate(url: "https://example.com")
2. browser_wait_for(time: 2)  // Initial load
3. // Close cookie popup (see "Close Cookie Popups" section)
4. // Scroll to load lazy content
5. browser_evaluate(expression: "(async () => {
     const delay = ms => new Promise(r => setTimeout(r, ms));
     let prevHeight = -1;
     for (let i = 0; i < 30; i++) {
       window.scrollBy(0, 500);
       await delay(300);
       const newHeight = document.body.scrollHeight;
       if (newHeight === prevHeight) break;
       prevHeight = newHeight;
     }
     window.scrollTo(0, 0);
   })()")
6. browser_wait_for(time: 1)  // Final settle
7. browser_screenshot(fullPage: true)
```

**Handling fixed/sticky headers:**
To prevent fixed/sticky headers from repeating in the screenshot, remove their fixed/sticky positioning.
```
1. browser_evaluate(expression: "document.querySelectorAll('header, nav, [class*=\"sticky\"], [class*=\"fixed\"]').forEach(el => el.style.position = 'relative')")
2. browser_screenshot(fullPage: true)
```

## 5. Find and Extract Links

Extract specific link types (PDFs, videos, downloads) from complex pages.

**Find all PDFs:**
```
browser_evaluate(expression: "Array.from(document.querySelectorAll('a[href$=\".pdf\"], a[href*=\".pdf?\"]')).map(a => ({text: a.textContent.trim(), url: a.href}))")
```

**Find all videos (common formats):**
```
browser_evaluate(expression: "Array.from(document.querySelectorAll('a[href$=\".mp4\"], a[href$=\".webm\"], a[href$=\".mov\"], video source, iframe[src*=\"youtube\"], iframe[src*=\"vimeo\"]')).map(el => ({type: el.tagName, url: el.href || el.src}))")
```

**Find all downloadable files:**
```
browser_evaluate(expression: "Array.from(document.querySelectorAll('a[download], a[href$=\".pdf\"], a[href$=\".zip\"], a[href$=\".doc\"], a[href$=\".docx\"], a[href$=\".xls\"], a[href$=\".xlsx\"]')).map(a => ({text: a.textContent.trim(), url: a.href, filename: a.download || a.href.split('/').pop()}))")
```

**Find links by text pattern:**
```
browser_evaluate(expression: "Array.from(document.querySelectorAll('a')).filter(a => /download|attachment|pdf|document/i.test(a.textContent)).map(a => ({text: a.textContent.trim(), url: a.href}))")
```

**Complete workflow for finding downloads:**
```
1. browser_navigate(url: "https://example.com/resources")
2. browser_wait_for(time: 2)
3. // Dismiss cookie popup if present
4. // Scroll to load lazy content (see Section 2)
5. // Expand collapsed sections (see Section 3)
6. browser_evaluate(expression: "Array.from(document.querySelectorAll('a[href$=\".pdf\"], a[download]')).map(a => ({text: a.textContent.trim(), url: a.href}))")
7. // Returns JSON array of {text, url} objects
```

**Download a specific file:**
After finding the link, click it to download:
```
1. browser_snapshot()
2. // Find the download link in snapshot by text or ref
3. browser_click(element: "Download PDF", ref: "e25")
4. // File downloads to browser's default download folder
```
