---
description: Transcribe PDFs and web pages to complete markdown with 100% content preservation
auto_execution_mode: 1
---

# Transcribe Workflow

Convert Portable Document Format (PDF) files and web pages to complete markdown files. **Nothing may be omitted.**

## Required Skills

- @pdf-tools for PDF to image conversion
- @ms-playwright-mcp for web page screenshots

## Core Principle

**Maximum 4 pages per transcription call.** Write output to file immediately after each chunk.

## Source Types

| Source | Detection | Processing |
|--------|-----------|------------|
| Local PDF | File path ends in `.pdf` | Convert to JPG, transcribe |
| URL to PDF | URL ends in `.pdf` | Download first, then process |
| Web page | URL to HTML | Screenshot, transcribe |

## Step 1: Prepare Source

### For Local PDF
```powershell
python .windsurf/skills/pdf-tools/convert-pdf-to-jpg.py "path/to/document.pdf" --dpi 300  # 300 DPI (Dots Per Inch)
```

### For URL to PDF
```powershell
$url = "https://example.com/document.pdf"
$filename = [System.IO.Path]::GetFileName($url)
# Download to: [SESSION_FOLDER] > [WORKSPACE_FOLDER]
Invoke-WebRequest -Uri $url -OutFile "[SESSION_FOLDER]/$filename"
# Then convert to JPG
python .windsurf/skills/pdf-tools/convert-pdf-to-jpg.py "[SESSION_FOLDER]/$filename" --dpi 300
```

### For Web Page
```
mcp0_browser_navigate(url: "https://example.com/page")
mcp0_browser_evaluate(function: "window.scrollTo(0, document.body.scrollHeight)")
mcp0_browser_wait_for(time: 2)
mcp0_browser_evaluate(function: "window.scrollTo(0, 0)")
mcp0_browser_take_screenshot(fullPage: true, filename: ".tools/_web_screenshots/[domain]/page-001.png")
```

## Step 2: Count and Plan

```powershell
$images = Get-ChildItem ".tools/_pdf_to_jpg_converted/[NAME]/" -Filter "*.jpg"
$totalPages = $images.Count
$chunks = [math]::Ceiling($totalPages / 2)
Write-Host "Total pages: $totalPages, Chunks needed: $chunks"
```

## Step 3: Determine Output Strategy

| Total Pages | Output Strategy |
|-------------|-----------------|
| 1-20 | Single markdown file |
| 21-50 | Single file, write after each 4-page chunk |
| 51-100 | Multiple section files + index, merge optional |
| 100+ | Multiple chapter files + index |

## Step 4: Create Output File with Header

```markdown
# [Document Title]

<!-- TRANSCRIPTION PROGRESS
Chunk: 1 of [total_chunks]
Pages completed: 0 of [total]
-->

## Table of Contents
[Generate after first pass or from PDF Table of Contents (TOC)]
```

## Step 5: Transcribe in 4-Page Chunks

For each chunk (pages 1-4, 5-8, 9-12, etc.):

### 5a. Read exactly 4 page images (or fewer for final chunk)
```
read_file(file_path: "[path]_page001.jpg")
read_file(file_path: "[path]_page002.jpg")
read_file(file_path: "[path]_page003.jpg")
read_file(file_path: "[path]_page004.jpg")
```

### 5b. Extract ALL content from these pages
- Every heading, paragraph, list, footnote
- Every figure → See **Figure Transcription Protocol** below
- Every table → Markdown table
- Every caption, label, reference

### Special Characters for Accurate Transcription

- **Superscripts/subscripts**: Use Unicode (¹ ² ³, ₁ ₂ ₃) not ASCII (^1 ^2 ^3)
- **Greek letters**: Use actual Unicode characters (α β γ)
- **Math formulas**: Use LaTeX syntax (`$E = mc^2$`) not Unicode operators
- **Symbols**: Use proper Unicode (© ® ™ § † ‡ °)

### Page Boundary Markers

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

### 5c. Append to output file IMMEDIATELY
Do not wait until end. Write after each chunk.

### 5d. Update progress marker
```markdown
<!-- TRANSCRIPTION PROGRESS
Chunk: 2 of 5
Pages completed: 4 of 20
-->
```

### 5e. Continue with next chunk
Repeat until all pages processed.

## Step 6: Finalize

1. Remove progress markers
2. Generate/verify Table of Contents
3. Log metadata to session NOTES.md (source, pages, figures, date) per core-conventions.md

## Output Locations

- Converted images: `.tools/_pdf_to_jpg_converted/[PDF_FILENAME]/`
- Web screenshots: `.tools/_web_screenshots/[DOMAIN]/`
- Markdown output: `[SESSION_FOLDER]/` or user-specified location

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

## Verification

After transcription, run `/verify` to:
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

## Best Practices

1. **4 pages max per call** - Prevents context overflow and ensures quality
2. **Write immediately** - Append to file after each chunk
3. **Track progress** - Use progress markers for resumability
4. **300 DPI for PDFs** - Higher quality for accurate transcription
5. **Keep source images** - Required for `/verify`
6. **No omissions** - Every piece of content must be transcribed
7. **ASCII + XML for figures** - Every figure requires both ASCII art and `<transcription_notes>` XML block
8. **Page boundaries** - Preserve headers/footers with `<transcription_page_header>` and `<transcription_page_footer>` tags
