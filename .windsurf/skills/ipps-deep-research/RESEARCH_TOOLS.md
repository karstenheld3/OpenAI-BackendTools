# Research Tools Reference

**Goal**: Document available tools for research workflows

## Overview

### Source Collection Tools

- **`search_web`** (Built-in) - Web search for relevant documents. Best for initial source discovery.
- **`read_url_content`** (Built-in) - Fetch and read web page content. Best for direct URL scraping.
- **`browser_navigate`** (ms-playwright-mcp) - Navigate browser to URL. Best for dynamic sites, auth-required.
- **`browser_snapshot`** (ms-playwright-mcp) - Get accessibility tree. Best for extracting page structure.
- **`browser_screenshot`** (ms-playwright-mcp) - Capture page image. Best for visual documentation.
- **`browser_evaluate`** (ms-playwright-mcp) - Execute JavaScript. Best for extracting dynamic content.

### Document Processing Tools

- **`convert-pdf-to-jpg.py`** (pdf-tools) - PDF pages to JPG images. Best for vision analysis of PDFs.
- **`pdftotext.exe`** (pdf-tools) - Extract text from PDF. Best for searchable PDFs.
- **`pdfinfo.exe`** (pdf-tools) - Get PDF metadata. Best for checking dates, page counts.
- **`compress-pdf.py`** (pdf-tools) - Reduce PDF size. Best for archiving large docs.

### Transcription Tools

- **`transcribe-image-to-markdown.py`** (llm-transcription) - Image to structured markdown. Best for screenshots, diagrams.
- **`transcribe-audio-to-markdown.py`** (llm-transcription) - Audio to markdown transcript. Best for conference talks, podcasts.

## When to Use Each Tool

### Primary: Built-in Tools (Default)

**Start with these for all research:**

```
search_web → find sources
     ↓
read_url_content → fetch content
     ↓
Success? → Continue research
     ↓
Fail? → Escalate to Playwright
```

**Use `search_web` when:**
- Starting research, need to discover sources
- Looking for official documentation URLs
- Finding GitHub repos, blog posts, Stack Overflow

**Use `read_url_content` when:**
- URL is known and content is static
- Page doesn't require JavaScript rendering
- No authentication needed
- No cookie/consent dialogs blocking content

### Fallback: Playwright MCP (Escalation)

**Escalate to Playwright when built-in tools fail:**

#### Scenario 1: Unreadable or Unscrapable Sites

```
read_url_content fails (JavaScript-heavy, dynamic content)
     ↓
browser_navigate → browser_snapshot → browser_evaluate
```

**Signs you need Playwright:**
- `read_url_content` returns empty or garbled content
- Site requires JavaScript for content rendering
- Content loads dynamically (infinite scroll, lazy load)
- Single-page application (SPA) architecture

#### Scenario 2: Authentication or Consent Required

```
Source requires login or form submission
     ↓
browser_navigate → browser_fill → browser_click → browser_snapshot
```

**Use Playwright for:**
- Sites requiring login (use persistent profile)
- Cookie consent dialogs blocking content
- CAPTCHA or bot-detection pages
- Form submissions to access downloads
- Age verification gates

#### Scenario 3: Full-Page Documentation Capture

```
Need complete visual record of web page
     ↓
browser_navigate → browser_screenshot(fullPage: true)
     ↓
(optional) transcribe-image-to-markdown.py
```

**Use Playwright screenshots for:**
- Capturing full page context (scrollable content)
- Documenting UI layouts and dashboards
- Archiving pages that may change
- Source material for later transcription
- Evidence of current state (versioned docs)

#### Scenario 4: Document Downloads

```
PDF/file download requires interaction
     ↓
browser_navigate → browser_click(download link) → wait for download
```

**Use Playwright for:**
- Downloads behind consent dialogs
- Files requiring form submission first
- Authenticated document access
- Dynamic download links (generated per-session)

**Playwright debugging fallback:**
If Playwright commands fail or JavaScript is blocked, use desktop screenshot to diagnose:
```powershell
& "[DEVSYSTEM_FOLDER]/skills/windows-desktop-control/simple-screenshot.ps1"
```
Captures full screen to `.tools/_screenshots/` - helps identify popups, dialogs, or blockers.

**Source access failure handling:**
If both `read_url_content` and Playwright fail after 2 retries:
1. Document source as `[INACCESSIBLE]` in `__[TOPIC]_SOURCES.md`
2. Note reason: blocked, requires auth, geofenced, etc.
3. Search for alternative source (mirror, archive.org, cached version)
4. If no alternative, proceed without - document gap in research
5. Max 3 inaccessible sources per research before escalating to user

### Document Processing: PDF Tools

**Default PDF processing workflow:**

```
1. INSPECT: pdfinfo + pdfimages -list
2. Many large images? → YES: image path / NO: try pdftotext first
3. Text insufficient? → convert-pdf-to-jpg --dpi 150
4. Review 3-5 images, assess quality needed
5. BATCH: transcribe-image-to-markdown.py --workers N (start with 10, increase if stable)
6. ARCHIVE: compress-pdf.py, store .md + compressed PDF in session (preserve timestamps)
```

**Step-by-step commands:**

```powershell
# Step 1: Inspect PDF
pdfinfo.exe "source.pdf"
pdfimages -list "source.pdf"

# Step 2a: Try text extraction first (if few/small images)
pdftotext.exe "source.pdf" "source.txt"
# Check: Is output meaningful? Has sufficient content?

# Step 2b: Convert to images (if text extraction insufficient)
python convert-pdf-to-jpg.py "source.pdf" --dpi 150 --output "[SESSION]/pdf_images/"

# Step 3: Assess quality needs
# Manually review 3-5 sample images to determine:
# - Are images clear enough for transcription?
# - What level of detail is needed?

# Step 4: Batch transcribe with parallel workers
python transcribe-image-to-markdown.py --input-folder "[SESSION]/pdf_images/" --output-folder "[SESSION]/transcribed/" --workers 60

# Step 5: Archive
python compress-pdf.py "source.pdf" --output "[SESSION]/compressed/"
# Copy with preserved timestamps:
# PowerShell: Copy-Item preserves timestamps by default
# Store: compressed PDF + all .md files in session folder
```

**Session folder structure:**

```
[SESSION]/
├── pdf_sources/
│   └── [original PDFs - reference only]
├── pdf_images/
│   └── [PDF_NAME]/
│       ├── page_001.jpg
│       ├── page_002.jpg
│       └── ...
├── transcribed/
│   └── [PDF_NAME]/
│       ├── page_001.md
│       ├── page_002.md
│       └── ...
└── compressed/
    └── [PDF_NAME]_compressed.pdf
```

**Decision criteria:**

- **`pdfimages` shows 0-5 small images** - Use text path
- **`pdfimages` shows many large images (>100KB each)** - Use image path
- **`pdftotext` output is mostly whitespace** - Use image path
- **`pdftotext` output has garbled characters** - Use image path
- **PDF is scanned document** - Use image path
- **PDF is native digital document** - Use text path (image as fallback)

### Transcription: LLM Transcription

**Use when content is visual:**

```
Visual source (screenshot, diagram, slide)
     ↓
transcribe-image-to-markdown.py
     ↓
Structured markdown with preserved layout
```

**Use `transcribe-image-to-markdown.py` for:**
- Screenshots of documentation
- Architecture diagrams
- Presentation slides
- UI mockups
- Handwritten notes (if legible)

**Use `transcribe-audio-to-markdown.py` for:**
- Conference talk recordings
- Podcast episodes discussing technology
- Video tutorials (audio track)
- Meeting recordings

## Tool Selection Flowchart

```
START: Need to collect source
│
├─> URL known? → read_url_content → Success? Done / Fail? Playwright
├─> No URL? → search_web → get URL → retry
│
├─> File (not web)?
│	├─> PDF → pdf-tools (pdftotext or jpg→transcribe)
│	├─> DOCX/PPTX → pandoc or direct read
│	├─> XLSX/CSV → pandas or direct parse
│	└─> Other → text-based? read / else convert
│
├─> Auth/consent required? → Playwright persistent profile
├─> Dynamic/JS content? → Playwright browser_snapshot
├─> Full visual capture? → Playwright screenshot(fullPage)
│
└─> Visual source?
	├─> Image → transcribe-image-to-markdown.py
	└─> Audio → transcribe-audio-to-markdown.py
```

## Common Workflows

### Workflow 1: Official Documentation Research

```powershell
# 1. Search for official docs
search_web("Microsoft Graph API documentation")

# 2. Read documentation pages
read_url_content("https://learn.microsoft.com/en-us/graph/...")

# 3. If fails, use Playwright
browser_navigate(url: "https://learn.microsoft.com/...")
browser_snapshot()
```

### Workflow 2: PDF Whitepaper Analysis

```powershell
# 1. Download PDF (if behind form)
browser_navigate(url: "https://vendor.com/whitepaper")
browser_fill(element: "Email", ref: "e5", value: "user@example.com")
browser_click(element: "Download", ref: "e8")

# 2. Analyze PDF
pdfinfo.exe whitepaper.pdf

# 3. Extract based on type
pdftotext.exe whitepaper.pdf output.txt
# OR
python convert-pdf-to-jpg.py whitepaper.pdf --dpi 150
```

### Workflow 3: Full Page Archive

```powershell
# 1. Navigate and wait for load
browser_navigate(url: "https://docs.example.com/api-reference")

# 2. Handle cookie consent if needed
browser_snapshot()  # Find consent button
browser_click(element: "Accept cookies", ref: "e12")

# 3. Capture full page
browser_screenshot(fullPage: true, filename: "api-reference-2026-01-30.png")

# 4. Transcribe to markdown
python transcribe-image-to-markdown.py --input api-reference-2026-01-30.png --output api-reference.md
```

### Workflow 4: Community Source Collection

```powershell
# 1. Search Stack Overflow
search_web("site:stackoverflow.com [subject] rate limit")

# 2. Read high-vote answers
read_url_content("https://stackoverflow.com/questions/...")

# 3. Search GitHub issues
search_web("site:github.com [repo] issue rate limit")

# 4. Read issue discussions
read_url_content("https://github.com/[org]/[repo]/issues/...")
```

## Anti-Patterns

- **Using Playwright first** - Always try built-in tools first (faster, cheaper)
- **Skipping PDF analysis** - Use `pdfinfo` before choosing extraction method
- **Screenshots without transcription** - Visual captures need markdown conversion for searchability
- **Single extraction attempt** - Retry with different tool if first fails

## Tool Locations

- **pdf-tools** - `.tools/` (binaries), `[DEVSYSTEM_FOLDER]/skills/pdf-tools/` (scripts)
- **llm-transcription** - `[DEVSYSTEM_FOLDER]/skills/llm-transcription/`
- **ms-playwright-mcp** - MCP server (configured in mcp_config.json)
