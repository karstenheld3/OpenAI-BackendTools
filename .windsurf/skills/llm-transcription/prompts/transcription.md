# Transcription Prompt v14 - Tables as Markdown

Transcribe this document page image to Markdown. **Accuracy over speed.**

**CRITICAL: Output raw markdown directly. Do NOT wrap your entire output in ```markdown code fences.**

## Key Areas

1. **Graphics** - Essential graphics with labeled ASCII art and data extraction
2. **Structure** - Semantic hierarchy matching visual document outline
3. **Text** - Character-level accuracy

All three matter equally.

---

## CRITICAL RULES

**DO:**
- Label every node in diagrams: `[DATABASE]`, `[PROCESS]`, `(pending)`
- Extract ALL data values from charts (numbers > visual fidelity)
- Match header levels to visual hierarchy (H1=title, H2=sections, H3=subsections)
- Use `[unclear]` for text you cannot read with confidence
- Use `<!-- Section N -->` and nested `<!-- Column N -->` for multi-column text-only layouts (no transcriptions, minimal markdown)
- For graphical or colorized layouts, figures and tables, keep detailed `<transcription_notes>` with colors, visual details, and context
- **Figures/charts**: use `<transcription_image>` with ````ascii` + `<transcription_json>`
- **Tables**: use `<transcription_table>` with markdown table + `<transcription_json>`

**DON'T:**
- **Don't wrap your entire output in ```markdown code fences**
- **Don't use HTML tags** (`<span>`, `<div>`, `&nbsp;`, etc.) - pure markdown only
- Don't use ````ascii` or `<transcription_json>` for text-only pages.
- Don't transcribe UI chrome (toolbars, ribbons, browser elements)
- Don't count decorative logos/separators as missed graphics
- Don't use headers for formatting convenience - only for real sections
- Don't guess numbers - mark as `[unclear: ~value?]` if uncertain
- **Don't duplicate data** - if a chart's data appears in surrounding text, don't repeat it in both places
- **Don't skip ASCII art** - every chart/graph needs BOTH ASCII representation AND JSON data
- **Don't use ASCII for tables** - tables use markdown format, not ASCII

**FORBIDDEN TAGS (break markdown rendering):**
- Never use `<content>`, `<data>`, `<section>` or similar custom tags outside code blocks
- Only allowed tags: `<transcription_image>`, `<transcription_table>`, `<transcription_json>`, `<transcription_notes>`, `<transcription_page_header>`, `<transcription_page_footer>`

---

## 1. Graphics

### Essential vs Decorative

**TRANSCRIBE:** Charts, diagrams, flowcharts, infographics, data visualizations

**SKIP:** UI chrome, toolbars, logos, watermarks → `<!-- Decorative: [list] -->`

### ASCII Art Format

<transcription_image>
**Figure N: [Caption]**

```ascii
[CHART TYPE - TITLE]
Category A: ████████ 2,450.75 (52.3%)
Category B: █████ 1,180.50 (25.1%)
Category C: ███ 890.25 (19.0%)
Total: $4,700.50M | YoY: +12.5%
```

<transcription_json>
{"chart_type": "bar_chart", "title": "Revenue by Category", "data": [{"category": "A", "value": 2450.75, "percent": 52.3}, {"category": "B", "value": 1180.50, "percent": 25.1}, {"category": "C", "value": 890.25, "percent": 19.0}], "total": 4700.50, "unit": "$M", "change": "+12.5% YoY"}
</transcription_json>

<transcription_notes>
- Type: Horizontal bar chart
- Colors: blue=A, green=B, grey=C
- ASCII misses: gradients, exact proportions, 3D effects
</transcription_notes>
</transcription_image>

### Data Extraction Tag

**BOTH ASCII AND JSON are MANDATORY** for all figures and tables:
- ````ascii` block for visual representation
- `<transcription_json>` for structured data extraction

JSON contains:
- chart_type or table_type
- title
- data array with all values
- totals, units, changes where applicable

### Table Example

<transcription_table>
**Table 1: Quarterly Revenue**

| Region | Q1 | Q2 | Q3 | Q4 |
|--------|---------|---------|---------|----------|
| North | 1,120.50 | 1,235.75 | 1,342.25 | 1,458.00 |
| South | 890.25 | 945.50 | 1,012.75 | 1,125.00 |
| East | 765.00 | 824.50 | 888.25 | 956.75 |

<transcription_json>
{"table_type": "data_table", "title": "Quarterly Revenue", "columns": ["Region", "Q1", "Q2", "Q3", "Q4"], "data": [{"Region": "North", "Q1": 1120.50, "Q2": 1235.75, "Q3": 1342.25, "Q4": 1458.00}, {"Region": "South", "Q1": 890.25, "Q2": 945.50, "Q3": 1012.75, "Q4": 1125.00}, {"Region": "East", "Q1": 765.00, "Q2": 824.50, "Q3": 888.25, "Q4": 956.75}], "unit": "millions USD"}
</transcription_json>

<transcription_notes>
- Source: Financial Report 2023
- Units: millions USD
</transcription_notes>
</transcription_table>

### ANTI-DUPLICATION RULE

**Only suppress data that appears BOTH in surrounding text AND in graphics.**

If the page text says "Revenue was $4,700M" AND there's a chart showing the same value:
- Include the value in ASCII art (primary source)
- Include the value in notes (to capture additional information like colors or icons assiciated with exact value)
- DON'T repeat "Revenue was $4,700M" in plain text transcription if it's just restating the chart

If data appears ONLY in graphics (not in text), include it fully in both ASCII and notes.

---

## 2. Structure

### Headers
- H1 = Document title (one per page max)
- H2 = Major sections
- H3 = Subsections

### Multi-Column Layouts

<!-- Column 1 -->
[Content...]

<!-- Column 2 -->
[Content...]

### Sidebars

> **Sidebar: [Title]**
> [Content...]

### Sections and Columns

Use `<!-- Section N -->` to mark visual sections, with nested `<!-- Column N -->` for multi-column layouts:

<!-- Section 1 -->
<!-- Column 1 -->
**Title or Label**

Label items:
: Item A
: Item B
: Item C

<!-- Column 2 -->
Main content text that appears alongside the label column...

<!-- Section 2 -->
Single-column content continues here...

### Structured Text (Definition Lists)

For label-value pairs and categorized lists, use definition list format:

**Category Title**

Label:
: **Item 1**
: **Item 2**
: **Item 3**

Nested content under items:
: **Main Item**
  - Sub-point A
  - Sub-point B

### Page Boundaries

<transcription_page_header> Title | Section </transcription_page_header>

<transcription_page_footer> Page X | Company </transcription_page_footer>

---

## 3. Text Accuracy

- Every word exactly as shown
- Numbers must match exactly
- Mark unclear: `[unclear]` or `[unclear: best guess?]`

### Special Characters
- Superscripts: ¹ ² ³
- Greek: α β γ δ
- Math: `$E = mc^2$`
- Symbols: © ® ™ § † ‡ °

---

## 4. Tables

**Always use markdown tables** (never ASCII) wrapped in `<transcription_table>`:

<transcription_table>
**Table N: [Title]**

| Column A | Column B |
|----------|----------|
| Value 1  | Value 2  |

<transcription_json>
{"table_type": "...", "data": [...]}
</transcription_json>

<transcription_notes>
- [visual details, colors, source]
</transcription_notes>
</transcription_table>
