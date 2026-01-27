# Transcription Prompt v1B

Transcribe this document page image to Markdown. **Accuracy over speed.**

## Key Areas

1. **Graphics** - Essential graphics with labeled ASCII art and data extraction
2. **Structure** - Semantic hierarchy matching visual document outline
3. **Text** - Character-level accuracy

All three matter equally. Do each one correctly.

---

## CRITICAL RULES

**DO:**
- Label every node in diagrams: `[DATABASE]`, `[PROCESS]`, `(pending)`
- Extract ALL data values from charts (numbers > visual fidelity)
- Match header levels to visual hierarchy (H1=title, H2=sections, H3=subsections)
- Use `[unclear]` for text you cannot read with confidence

**DON'T:**
- Don't transcribe UI chrome (toolbars, ribbons, browser elements)
- Don't count decorative logos/separators as missed graphics
- Don't use headers for formatting convenience - only for real sections
- Don't guess numbers - mark as `[unclear: ~value?]` if uncertain

---

## 1. Graphics (Highest Priority)

### Essential vs Decorative

**TRANSCRIBE (essential):** Charts, diagrams, flowcharts, infographics, data visualizations, maps, technical illustrations

**SKIP (decorative):** UI chrome, toolbars, logos, watermarks, separators, backgrounds → add only: `<!-- Decorative: [list] -->`

### ASCII Art Requirements

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

### Chart Data Extraction

**DATA > VISUALS.** A bar chart transcription must include:
```ascii
REVENUE FY2024 ($M)
North America: ████████ 2,450 (52%)
Europe:        █████ 1,180 (25%)
APAC:          ███ 890 (19%)
Other:         █ 180 (4%)
Total: $4,700M | YoY: +12%
```

If you can read the numbers, include them. ASCII proportions are secondary.

---

## 2. Structure

### Semantic Hierarchy

Headers must match the VISUAL document structure, not Markdown convenience:
- H1 = Document title (one per page max)
- H2 = Major sections visible in document
- H3 = Subsections within sections

**Verify:** Extract your headers → compare to visible document outline → fix mismatches.

### Multi-Column Layouts

Read top-to-bottom within each column, then next column. Mark column breaks:
```markdown
<!-- Column 1 -->
[Content...]

<!-- Column 2 -->
[Content...]
```

### Sidebars and Callouts

Clearly separate from main content:
```markdown
> **Sidebar: [Title]**
> [Sidebar content...]
```

### Page Boundaries

```markdown
<transcription_page_footer> Page X | Company </transcription_page_footer>

---

<transcription_page_header> Title | Section </transcription_page_header>
```

---

## 3. Text Accuracy

### Precision

- Every word exactly as shown
- Numbers must match exactly (0.89 ≠ 0.69)
- Proper nouns match case and spelling
- Mark unclear text: `[unclear]` or `[unclear: best guess?]`

### Special Characters

- Superscripts: ¹ ² ³ (not ^1 ^2 ^3)
- Greek: α β γ δ (actual Unicode)
- Math: `$E = mc^2$` (LaTeX syntax)
- Symbols: © ® ™ § † ‡ °

### Acceptable Variations

These are equivalent (don't worry about matching exactly):
- Decimals: 1,000.00 = 1.000,00 = 1000.00
- Quotes: " = ' = " = '
- Dashes: - = – = —

---

## 4. Tables

Use Markdown tables for tabular data:
```markdown
| Column A | Column B | Column C |
|----------|----------|----------|
| Value 1  | Value 2  | Value 3  |
```

For complex tables that break in Markdown, use ASCII:
```ascii
+----------+----------+----------+
| Col A    | Col B    | Col C    |
+----------+----------+----------+
| Val 1    | Val 2    | Val 3    |
+----------+----------+----------+
```

---

## Output Structure

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
