---
description: Transcribe PDFs and web pages to complete markdown with 100% content preservation
auto_execution_mode: 1
---

# Transcribe Workflow

Convert Portable Document Format (PDF) files and web pages to complete markdown files. **Nothing may be omitted.**

**Goal**: Complete markdown transcription with 100% content preservation

**Why**: Downstream analysis requires full text access without PDF rendering dependencies

## Required Skills

- @pdf-tools for PDF to image conversion
- @ms-playwright-mcp for web page screenshots
- @llm-transcription (optional) for advanced LLM-based transcription

## MUST-NOT-FORGET

- GLOBAL-RULES apply to ALL transcription contexts
- Content Rules (Special Characters, Page Boundaries, Figure Protocol) apply to ALL output
- Ensure complete file is stitched together and file path is noted
- Keep source images for verification
- Run `/verify` after transcription complete

## Prerequisites

- @pdf-tools available for PDF to JPG conversion
- For TRANSCRIBE_SCRIPT: @llm-transcription skill + API keys file required
- For TRANSCRIBE_PROMPT: No additional prerequisites

## GLOBAL-RULES

Apply to ALL contexts before any context-specific steps.

1. **120 DPI** for PDF to JPG conversion - optimal balance of quality and processing speed
2. **Write output immediately** after each chunk - do not wait until end
3. **No omissions** - every piece of content must be transcribed
4. **Keep source images** - required for `/verify`
5. **All Content Rules apply** - Special Characters, Page Boundary Markers, Figure Transcription Protocol (see CONTENT RULES section)

## Source Types

- **Local PDF** - File path ends in `.pdf` → Convert to JPG, transcribe
- **URL to PDF** - URL ends in `.pdf` → Download first, then process
- **Web page** - URL to HTML → Screenshot, transcribe

# CONTEXT-SPECIFIC

Two dimensions determine the execution path:

**Method** (detected in Step 1):
- **TRANSCRIBE_SCRIPT** - `transcribe-image-to-markdown.py` with ensemble + judge + refinement. Requires @llm-transcription skill + API keys.
- **TRANSCRIBE_PROMPT** - Built-in transcription prompt (see Appendix). Fallback when skill or keys unavailable.

**Scope** (determined by input):
- **TRANSCRIBE_SINGLE** - One PDF or web page
- **TRANSCRIBE_MULTI** - Multiple independent PDFs

## TRANSCRIBE_SCRIPT + TRANSCRIBE_SINGLE

Prepare source first (see Source Preparation Reference), then run script. Script handles page parallelism internally via `--workers`.

```powershell
$venv = "../.tools/llm-venv/Scripts/python.exe"
$skill = ".devin/skills/llm-transcription"

# Single page transcription
& $venv "$skill/transcribe-image-to-markdown.py" `
    --input-file "../.tools/_pdf_to_jpg_converted/[NAME]/page_001.jpg" `
    --output-file "[SESSION_FOLDER]/[DocName]_page001.md" `
    --keys-file "[WORKSPACE_FOLDER]\..\.tools\.api-keys.txt" `
    --model gpt-5-mini `
    --workers 4

# Batch mode (entire folder, multiple pages)
& $venv "$skill/transcribe-image-to-markdown.py" `
    --input-folder "../.tools/_pdf_to_jpg_converted/[NAME]/" `
    --output-folder "[SESSION_FOLDER]/transcribed/" `
    --keys-file "[WORKSPACE_FOLDER]\..\.tools\.api-keys.txt" `
    --model gpt-5-mini `
    --initial-candidates 1 `
    --workers 12
```

After script completes, proceed to Step 3 (Stitch).

## TRANSCRIBE_SCRIPT + TRANSCRIBE_MULTI

Process multiple independent PDFs in parallel across Cascade terminals.

**Limits**: Max 4 concurrent Cascade terminals. Each runs `--workers 30`.

### Process

1. Convert ALL PDFs to JPG first (single terminal, sequential - fast I/O-bound step)
2. Count pages per PDF. Sort by page count descending.
3. Launch first 4 PDFs in 4 terminals (`run_command`, `Blocking: false`, `WaitMsBeforeAsync: 2000`)
4. Monitor with `command_status`. When a terminal finishes:
   - Stitch that PDF's pages into final .md file (Step 3)
   - If unprocessed PDFs remain, launch the next one in that terminal
5. Repeat until all PDFs are transcribed and stitched

### Rules

- One PDF per terminal at a time (script handles page parallelism internally)
- Start with the largest PDFs first so small ones fill gaps at the end
- No aggregation scripts - each `run_command` processes exactly one PDF
- Monitor and react: stitch immediately, then reuse freed terminal
- All 4 initial `run_command` calls in one tool call block (parallel launch)

## TRANSCRIBE_PROMPT + TRANSCRIBE_SINGLE

Prepare source first (see Source Preparation Reference), then process in 4-page chunks. **Maximum 4 pages per transcription call.**

### Create Output File

```markdown
# [Document Title]

<!-- TRANSCRIPTION PROGRESS
Chunk: 1 of [total_chunks]
Pages completed: 0 of [total]
-->

## Table of Contents
[Generate after first pass or from PDF Table of Contents (TOC)]
```

### For Each Chunk (pages 1-4, 5-8, 9-12, etc.)

1. Read up to 4 page images:
```
read_file(file_path: "[path]_page001.jpg")
read_file(file_path: "[path]_page002.jpg")
read_file(file_path: "[path]_page003.jpg")
read_file(file_path: "[path]_page004.jpg")
```

2. Extract ALL content from these pages:
   - Every heading, paragraph, list, footnote
   - Every figure → See **Figure Transcription Protocol** in CONTENT RULES
   - Every table → Markdown table
   - Every caption, label, reference

3. Append to output file IMMEDIATELY - do not wait until end

4. Update progress marker:
```markdown
<!-- TRANSCRIPTION PROGRESS
Chunk: 2 of 5
Pages completed: 4 of 20
-->
```

5. Continue with next chunk until all pages processed

After all chunks complete, proceed to Step 3 (Stitch).

## TRANSCRIBE_PROMPT + TRANSCRIBE_MULTI

Process each PDF sequentially using the TRANSCRIBE_PROMPT + TRANSCRIBE_SINGLE process above. No terminal parallelism (agent transcribes inline).

## No Context Match

If method or scope is unclear, ask user:
1. Is `transcribe-image-to-markdown.py` available with API keys?
2. How many documents need transcription?

# EXECUTION

## Step 1: Detect Method and Scope

### Method Detection

```powershell
# Check for llm-transcription skill
$skillPath = ".devin/skills/llm-transcription/transcribe-image-to-markdown.py"
$keysFile = "[WORKSPACE_FOLDER]\..\.tools\.api-keys.txt"
$hasSkill = Test-Path $skillPath
$hasKeys = Test-Path $keysFile

if ($hasSkill -and $hasKeys) {
    Write-Host "METHOD: TRANSCRIBE_SCRIPT (llm-transcription skill)"
} else {
    Write-Host "METHOD: TRANSCRIBE_PROMPT (built-in)"
    if (-not $hasSkill) { Write-Host "  - Missing: $skillPath" }
    if (-not $hasKeys) { Write-Host "  - Missing: $keysFile" }
}
```

### Scope Detection

- **TRANSCRIBE_SINGLE**: User provides one PDF or web page
- **TRANSCRIBE_MULTI**: User provides multiple PDFs or a folder of PDFs

## Step 2: Route to Context-Specific Process

**STOP - Do NOT prepare sources or convert PDFs here.** Each context-specific section handles its own preparation, conversion, counting, and transcription.

Based on method and scope detected in Step 1, jump to:
- **TRANSCRIBE_SCRIPT + TRANSCRIBE_SINGLE** - Single PDF, script handles page parallelism
- **TRANSCRIBE_SCRIPT + TRANSCRIBE_MULTI** - Multiple PDFs, 4 parallel terminals
- **TRANSCRIBE_PROMPT + TRANSCRIBE_SINGLE** - Single PDF, manual 4-page chunks
- **TRANSCRIBE_PROMPT + TRANSCRIBE_MULTI** - Multiple PDFs, sequential inline

After the context-specific process completes, return here and continue with Step 3 (Stitch).

## Step 3: Stitch Transcribed Pages

After batch transcription completes, merge individual page files into single output.

For TRANSCRIBE_SCRIPT + TRANSCRIBE_MULTI, stitching happens inline during the context-specific process.

```powershell
$folder = "[OUTPUT_FOLDER]/02_transcribed_pages"
$output = "[OUTPUT_FOLDER]/[DocName].md"  # No suffix like _COMPLETE
$files = Get-ChildItem $folder -Filter "*.md" | Where-Object { $_.Name -notlike "_*" } | Sort-Object Name
$content = @()
$pageNum = 1
foreach ($file in $files) {
    # Page marker BEFORE content (first page gets marker too)
    if ($pageNum -eq 1) {
        $content += "<!-- Page {0:D3} -->`n`n" -f $pageNum
    } else {
        $content += "`n---`n<!-- Page {0:D3} -->`n`n" -f $pageNum
    }
    $content += (Get-Content $file.FullName -Raw).TrimEnd()
    $pageNum++
}
$finalContent = ($content -join "").TrimEnd()
$finalContent | Out-File $output -Encoding UTF8
Write-Output "Merged $($files.Count) files to $output"
```

**Page marker format:**
```markdown
<!-- Page 001 -->

[Page 1 content...]

---
<!-- Page 002 -->

[Page 2 content...]
```

**Filename convention:** Use original document name without suffixes:
- Correct: `Enel-Integrated-Annual-Report-2023.md`
- Wrong: `Enel-Integrated-Annual-Report-2023_COMPLETE.md`

## Step 4: Finalize

1. Remove progress markers
2. Generate/verify Table of Contents
3. Log metadata to session NOTES.md (source, pages, figures, date) per core-conventions.md

## Stuck Detection

If 3 consecutive attempts fail on a page or chunk:
1. Document in PROBLEMS.md with page number and error
2. Mark page as `[TRANSCRIPTION FAILED: page N]` in output
3. Ask user for guidance

# FINALIZATION

## Verification

Run `/verify` to check:
1. Compare page count
2. Check all sections present
3. Verify all figures have BOTH:
   - ASCII art block (` ```ascii `)
   - XML description block (`<transcription_notes>`)
4. Verify page boundary markers:
   - `<transcription_page_header>` after each `---` (if header exists in source)
   - `<transcription_page_footer>` before each `---` (if footer exists in source)
5. Cross-check text accuracy
6. Validate XML tags are well-formed

## Output

- Converted images: `../.tools/_pdf_to_jpg_converted/[NAME]/` (default from convert-pdf-to-jpg.py, do NOT override)
- Transcribed pages: `[SESSION_FOLDER]/02_transcribed_pages/`
- Final merged output: `[SESSION_FOLDER]/[DocName].md`
- Web screenshots: `../.tools/_web_screenshots/[DOMAIN]/`

# CONTENT RULES

Apply to ALL transcription output regardless of method or scope.

## Special Characters for Accurate Transcription

- **Superscripts/subscripts**: Use Unicode (¹ ² ³, ₁ ₂ ₃) not ASCII (^1 ^2 ^3)
- **Greek letters**: Use actual Unicode characters (α β γ)
- **Math formulas**: Use LaTeX syntax (`$E = mc^2$`) not Unicode operators
- **Symbols**: Use proper Unicode (© ® ™ § † ‡ °)

## Page Boundary Markers

Preserve exact page structure with headers and footers from original document.

**Page Footer** - Place BEFORE `---` page separator:
```markdown
<transcription_page_footer> Page 5 | Company Name | Confidential </transcription_page_footer>

---
```

**Page Header** - Place IMMEDIATELY AFTER `---` page separator:
```markdown
---

<transcription_page_header> Annual Report 2024 | Section 3: Financials </transcription_page_header>
```

**Formatting Rules:**
- **Single-line**: Tags and content on one line
  ```markdown
  <transcription_page_footer> 12 | FY 2023 | Vestas. </transcription_page_footer>
  ```
- **Multi-line**: Tags on separate lines, content indented
  ```markdown
  <transcription_page_header>
  Annual Report 2024
  Section 3: Financial Statements
  Classification: Public
  </transcription_page_header>
  ```

**Content to capture:**
- Page numbers (any format: "5", "Page 5", "5 of 20", "v")
- Document title / section name
- Company name / logo text
- Classification labels (Public, Confidential, etc.)
- Version / date stamps
- Navigation text (e.g., "Introduction | Get ready | Onboard and engage")

**Omit if absent:** If a page has no header or footer, omit the corresponding tag entirely.

## Figure Transcription Protocol

**MANDATORY**: Every figure MUST have BOTH ASCII art AND XML description.

### Step F0: Analyze Before Drawing (Required)

Before creating ASCII art, describe the image:
1. **Subject**: What is this? (diagram type, subject matter)
2. **Elements**: What are the key parts? (list 3-7 main components)
3. **Relationships**: How do elements connect? (spatial, logical, flow)
4. **Priority**: What matters most for understanding?

### Step F1: Create ASCII Art (Required)

**CHOOSE MODE** based on figure type:

**Mode A: Structural** (flowcharts, diagrams, architecture, UI)
```
Box/lines:  + - | / \ _ [ ] ( ) { } < >
Arrows:     -> <- v ^ >> <<
Labels:     A-Z a-z 0-9
Connectors: --- ||| === ...
```

**Mode B: Shading** (photographs, complex graphics, gradients)
```
Density ramp (dark to light): @#%&8BWM*oahkbd=+-:. 
Or simplified:                 @%#*+=-:.
```

**MAXIMIZE SEMANTICS** - Pack as much meaning into ASCII art as possible:
- **Title header**: Start with `[DIAGRAM TITLE - WHAT IT SHOWS]`
- **Inline legends**: Embed symbol meanings directly (`[S] = Server`, `[C] = Client`)
- **Semantic labels**: Label every node, region, and outcome (`[DATABASE]`, `(pending)`, `RETRY LOOP`)
- **State annotations**: Mark states explicitly (`(inactive)` vs `(ACTIVE)`)
- **Result summaries**: Include outcome text where applicable (`Result: Request completed`)

LLMs understand explicit labels better than visual patterns. Inline semantics beat cross-referencing metadata.

**LAYOUT RULES**:
- **Width**: 80-120 characters (max 180 for very complex diagrams)
- **Aspect ratio**: Characters are ~2:1 (taller than wide) - compensate by doubling horizontal spacing
- **Whitespace**: Use blank lines to separate logical sections

**PURE ASCII ONLY** - No Unicode box-drawing, arrows, or shading blocks. Unicode adds no LLM value and risks alignment issues.

````
<transcription_image>
**Figure [N]: [Caption from original]**

```ascii
[ASCII art representation here]
```

<transcription_notes>
- Mode: Structural | Shading
- Dimensions: [width]x[height] characters
- ASCII captures: What the ASCII diagram successfully represents
- ASCII misses: Visual elements that cannot be shown in ASCII
- Colors:
  - [color name] - what it represents (e.g., "Blue - input nodes")
  - [color name] - what it represents
- Layout: Spatial arrangement, panels, relative positions
- Details: Fine details, textures, gradients, 3D effects, icons
- Data: Specific values, measurements, labels, or quantities visible
- Reconstruction hint: Key detail needed to imagine original
</transcription_notes>
</transcription_image>
````

### Step F2: Compare and Describe (Required)

After creating ASCII, compare with original image and add `<transcription_notes>` inside the same `<transcription_image>` wrapper:

### Step F2b: Self-Verify (Required)

Before proceeding, verify ASCII art quality:
- [ ] All labeled elements from original present?
- [ ] Spatial relationships preserved (left/right, above/below)?
- [ ] Flow or hierarchy clear (if applicable)?
- [ ] Readable without seeing original?

If any check fails, revise ASCII art before continuing.

### Step F3: Example

Original: A flowchart with colored boxes showing data flow

**Step F0 Analysis**:
- Subject: Data processing pipeline flowchart
- Elements: Input box, Process box, Output box, 3 log boxes, arrows
- Relationships: Linear flow left-to-right, each stage logs downward
- Priority: Flow direction and logging hierarchy

```markdown
<transcription_image>
**Figure 3: Data Processing Pipeline**

```ascii
DATA PROCESSING PIPELINE - 3 STAGE FLOW WITH LOGGING

STAGE 1: INPUT        STAGE 2: PROCESS       STAGE 3: OUTPUT
+===========+         +===========+          +===========+
|   INPUT   |-------->|  PROCESS  |--------->|  OUTPUT   |
|   (data)  |         |   [gear]  |          |  (result) |
+===========+         +===========+          +===========+
      |                     |                      |
      v                     v                      v
+-----------+         +-----------+          +-----------+
|   Log A   |         |   Log B   |          |   Log C   |
| (received)|         |(processed)|          |  (sent)   |
+-----------+         +-----------+          +-----------+

Legend: === main flow  --- log output  [gear] = processing icon
```

<transcription_notes>
- Mode: Structural
- Dimensions: 70x14 characters
- ASCII captures: Box structure, flow direction (arrows), hierarchical logging, all labels, stage numbers, inline annotations
- ASCII misses: Rounded corners, shadow effects, actual gear icon graphic
- Colors:
  - Blue - input/output stages (INPUT, OUTPUT boxes)
  - Green - processing stage (PROCESS box)
  - Gray - logging components (Log A, B, C)
- Layout: Horizontal flow left-to-right, vertical drops to log boxes below each stage
- Details: Process box contains gear icon; arrows have gradient fill; boxes have subtle shadows
- Data: None
- Reconstruction hint: Main boxes are larger with double borders; log boxes are smaller with single borders
</transcription_notes>
</transcription_image>
```

### Figure Protocol Rules

1. **WRAPPER TAG**: Every figure MUST be wrapped in `<transcription_image>...</transcription_image>`
2. **NO EXCEPTIONS**: Every figure gets ASCII + notes, even photographs
3. **Photographs**: ASCII shows composition/layout; notes describe subject matter
4. **Graphs/Charts**: ASCII shows axes and trend; notes provide data points
5. **Network Diagrams**: ASCII shows topology; notes describe node colors and link types
6. **3D Visualizations**: ASCII shows 2D projection; notes describe depth and perspective

**Why wrapper tag?** Enables hybrid comparison: Levenshtein for text, LLM-as-a-judge for graphics.

# REFERENCE

## Source Preparation Reference

Conversion and download commands used by context-specific sections.

### For Local PDF
```powershell
python .devin/skills/pdf-tools/convert-pdf-to-jpg.py "path/to/document.pdf" --dpi 120  # 120 DPI - optimal for transcription
```

### For URL to PDF
```powershell
$url = "https://example.com/document.pdf"
$filename = [System.IO.Path]::GetFileName($url)
# Download to _DOWNLOADS_gitignore (not checked in)
New-Item -ItemType Directory -Path "[SESSION_FOLDER]/_DOWNLOADS_gitignore" -Force | Out-Null
Invoke-WebRequest -Uri $url -OutFile "[SESSION_FOLDER]/_DOWNLOADS_gitignore/$filename"
# Then convert to JPG
python .devin/skills/pdf-tools/convert-pdf-to-jpg.py "[SESSION_FOLDER]/_DOWNLOADS_gitignore/$filename" --dpi 120
```

### For Web Page
```
mcp0_browser_navigate(url: "https://example.com/page")
mcp0_browser_evaluate(function: "window.scrollTo(0, document.body.scrollHeight)")
mcp0_browser_wait_for(time: 2)
mcp0_browser_evaluate(function: "window.scrollTo(0, 0)")
mcp0_browser_take_screenshot(fullPage: true, filename: "../.tools/_web_screenshots/[domain]/page-001.png")
```

### Count and Plan

```powershell
$images = Get-ChildItem "../.tools/_pdf_to_jpg_converted/[NAME]/" -Filter "*.jpg"
$totalPages = $images.Count
$chunks = [math]::Ceiling($totalPages / 2)
Write-Host "Total pages: $totalPages, Chunks needed: $chunks"
```

### Output Strategy (page count)

- **1-20 pages** - Single markdown file
- **21-50 pages** - Single file, write after each 4-page chunk
- **51-100 pages** - Multiple section files + index, merge optional
- **100+ pages** - Multiple chapter files + index

## Long Document Strategy (50+ pages)

For documents over 50 pages, create multiple files:

```
[SESSION_FOLDER]/
├── [DocName]_INDEX.md      # TOC and metadata
├── [DocName]_Part01.md     # Pages 1-20
├── [DocName]_Part02.md     # Pages 21-40
├── [DocName]_Part03.md     # Pages 41-60
└── ...
```

Index file format:
```markdown
# [Document Title] - Index

## Parts

1. [Part01](./[DocName]_Part01.md) - Pages 1-20: [Chapter names]
2. [Part02](./[DocName]_Part02.md) - Pages 21-40: [Chapter names]
...
```

## Best Practices

1. **4 pages max per call** - Prevents context overflow and ensures quality (TRANSCRIBE_PROMPT)
2. **Write immediately** - Append to file after each chunk
3. **Track progress** - Use progress markers for resumability (TRANSCRIBE_PROMPT)
4. **120 DPI for PDFs** - Optimal balance of quality and processing speed for transcription
5. **Keep source images** - Required for `/verify`
6. **No omissions** - Every piece of content must be transcribed
7. **ASCII + XML for figures** - Every figure requires both ASCII art and `<transcription_notes>` XML block
8. **Page boundaries** - Preserve headers/footers with `<transcription_page_header>` and `<transcription_page_footer>` tags

# APPENDIX

## Built-in Transcription Prompt (TRANSCRIBE_PROMPT)

Use this prompt when llm-transcription skill is not available:

---

**Transcription Prompt v1B**

Transcribe this document page image to Markdown. **Accuracy over speed.**

**Key Areas:**
1. Graphics - Essential graphics with labeled ASCII art and data extraction
2. Structure - Semantic hierarchy matching visual document outline
3. Text - Character-level accuracy

**CRITICAL RULES:**

DO:
- Label every node in diagrams: `[DATABASE]`, `[PROCESS]`, `(pending)`
- Extract ALL data values from charts (numbers > visual fidelity)
- Match header levels to visual hierarchy (H1=title, H2=sections, H3=subsections)
- Use `[unclear]` for text you cannot read with confidence

DON'T:
- Don't transcribe UI chrome (toolbars, ribbons, browser elements)
- Don't count decorative logos/separators as missed graphics
- Don't use headers for formatting convenience - only for real sections
- Don't guess numbers - mark as `[unclear: ~value?]` if uncertain

**Graphics:**

TRANSCRIBE (essential): Charts, diagrams, flowcharts, infographics, data visualizations, maps, technical illustrations

SKIP (decorative): UI chrome, toolbars, logos, watermarks, separators, backgrounds - add only: `<!-- Decorative: [list] -->`

Every essential graphic MUST have:

```markdown
<transcription_image>
**Figure N: [Caption]**

```ascii
[TITLE - WHAT THIS SHOWS]
[Visual with INLINE labels - every node named]
Legend: [A]=Item1 [B]=Item2
```

<transcription_notes>
- Data: [all numbers, percentages, values]
- Colors: [color] = [meaning]
- ASCII misses: [what couldn't be shown]
</transcription_notes>
</transcription_image>
```

**Structure:**

Headers must match the VISUAL document structure:
- H1 = Document title (one per page max)
- H2 = Major sections visible in document
- H3 = Subsections within sections

Multi-column: Read top-to-bottom within each column, mark with `<!-- Column N -->`.

**Text Accuracy:**

- Every word exactly as shown
- Numbers must match exactly
- Mark unclear text: `[unclear]` or `[unclear: best guess?]`

Special Characters:
- Superscripts: use actual Unicode (not ^1 ^2 ^3)
- Greek: use actual Unicode characters
- Math: use LaTeX syntax
- Symbols: use proper Unicode

**Output Structure:**

```markdown
# [Document Title]

<transcription_page_header> [if present] </transcription_page_header>

## [Section]

[Content...]

<transcription_image>
**Figure 1: [Caption]**
[ASCII with inline labels]
<transcription_notes>[Data, colors, misses]</transcription_notes>
</transcription_image>

<transcription_page_footer> [if present] </transcription_page_footer>
```
