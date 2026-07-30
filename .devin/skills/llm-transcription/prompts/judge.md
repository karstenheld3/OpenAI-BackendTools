# Judge Prompt v3 - JSON Aware, optimized for Transcription Prompt v14 - Tables as Markdown

Score this JPG-to-Markdown transcription on three dimensions (1-5 each).

## 0. Format Check (Instant Fail)

**If the transcription is wrapped in a code fence, penalize heavily:**

BAD - Wrapped in code fence (score 1 for structure):
```
```markdown
# Title
content
```
```

The output should be RAW markdown, not wrapped in fences.

## 1. Text Accuracy

### Scoring Scale
- **5**: >99% accuracy, numbers exact
- **4**: 95-99%, minor typos (<5)
- **3**: 85-95%, noticeable errors (5-15)
- **2**: 70-85%, frequent errors
- **1**: <70%, major omissions

### Format Tolerances (NOT errors)
- `1,000.00` = `1.000,00` = `1000` (decimals)
- `"text"` = `'text'` = `"text"` (quotes)
- `-` = `–` = `—` (dashes)

## 2. Page Structure

### Scoring Scale
- **5**: Outline matches perfectly, sections/columns marked
- **4**: 1-2 nodes missing/misleveled
- **3**: Major sections OK, subsections wrong
- **2**: Only top-level captured
- **1**: No recognizable structure OR wrapped in ```markdown fence

### GOOD structural markers
- `<!-- Section N -->` for visual sections
- `<!-- Column N -->` for multi-column layouts
- Definition lists (`: item`) for label-value pairs

## 3. Graphics Quality

### Scoring Scale
- **5**: 100% essential DATA graphics detected (charts with ASCII + JSON, tables with markdown + JSON)
- **4**: >90% detected
- **3**: >75% detected
- **2**: 50-75% detected
- **1**: <50% detected

### Essential DATA graphics (count these)
- Charts with numeric data
- Diagrams with labeled nodes
- Flowcharts with process steps
- Tables with data values
- Infographics with statistics

### NOT essential (do NOT penalize if missing)
- Background images
- Decorative logos
- Stock photos
- UI chrome, separators
- Images without extractable data

### JSON Bonus
If image contains DATA graphics (charts, tables, diagrams with values):
- `<transcription_json>` with extracted data helps understanding
- Valid JSON with actual values from image is a plus
- Do NOT require JSON for decorative/non-data images

### Table Format
- Tables MUST use `<transcription_table>` wrapper (not `<transcription_image>`)
- Tables MUST use markdown table format (not ASCII art)
- Penalize ASCII tables - they should be markdown
- **Penalize duplicate tables** - if table appears as BOTH markdown AND ASCII, that's severe redundancy

### Penalize
- HTML tags (`<span>`, `<div>`, `&nbsp;`) - should be pure markdown
- Structural HTML tags outside of code-blocks (`<content>`, `<data>`, `<section>`) - should only be used within code blocks
- **Redundant data** - same values appearing in BOTH body text AND ASCII/JSON graphics
  - If a chart shows "Revenue: $2,450M" in ASCII art AND the surrounding text repeats "$2,450M revenue", that's redundancy
  - Data should appear in graphics OR text, not duplicated in both
  - Minor context references are OK, but full data tables repeated = penalty
- **Horizontal rules (`---`)** - do NOT use within page transcriptions
  - `---` markers are reserved for page boundaries when stitching multi-page documents
  - Use headings, blank lines, or `<!-- Section N -->` and `<!-- Column N -->` markers instead
- **Unjustified image transcriptions** - Pure text documents should not have ASCII/JSON transcriptions

## Output Format

```json
{
  "text_accuracy": {
    "score": 4,
    "justification": "Minor typos found",
    "errors_found": [],
    "tolerances_applied": []
  },
  "page_structure": {
    "score": 5,
    "justification": "All sections properly marked",
    "wrapped_in_code_fence": false,
    "missing_nodes": []
  },
  "graphics_quality": {
    "score": 4,
    "justification": "Data graphics captured with ASCII and JSON, no redundancy",
    "essential_data_graphics_in_image": 2,
    "essential_data_graphics_detected": 2,
    "json_extraction_present": true,
    "transcription_justified": true,
    "missed_graphics": [],
    "decorative_images_ignored": ["logo", "background"],
    "redundant_data_found": false,
    "horizontal_rules_found": 0
  },
  "weighted_score": 4.25
}
```

**Weights for image with graphical content:** text=0.25, structure=0.35, graphics=0.40
**Weights for text-only image (without graphical content):** text=0.75, structure=0.25, graphics=0
