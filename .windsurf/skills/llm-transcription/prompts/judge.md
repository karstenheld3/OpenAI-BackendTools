# Judge Prompt v1d

Score this JPG-to-Markdown transcription on three dimensions (1-5 each).

## 1. Text Accuracy

### Scoring Scale
- **5**: >99% accuracy, numbers exact
- **4**: 95-99%, minor typos (<5)
- **3**: 85-95%, noticeable errors (5-15)
- **2**: 70-85%, frequent errors
- **1**: <70%, major omissions

### BAD (penalize)
```
Image: "Revenue was $2,450M"
Transcription: "Revenue was $2,540M"  ← Wrong number
```

### GOOD (no penalty)
```
Image: "Revenue was $2,450.00"
Transcription: "Revenue was $2,450"  ← Format variation OK
```

### Format Tolerances (NOT errors)
- `1,000.00` = `1.000,00` = `1000` (decimals)
- `"text"` = `'text'` = `"text"` (quotes)
- `-` = `–` = `—` (dashes)

---

## 2. Page Structure

### Scoring Scale
- **5**: Outline matches perfectly
- **4**: 1-2 nodes missing/misleveled
- **3**: Major sections OK, subsections wrong
- **2**: Only top-level captured
- **1**: No recognizable structure

### BAD (penalize)
```
Image shows: Title → Section A → Subsection A.1
Transcription: # Title ## Subsection A.1  ← Missing Section A
```

### GOOD (correct)
```
Image shows: Title → Section A → Subsection A.1
Transcription: # Title ## Section A ### Subsection A.1
```

---

## 3. Graphics Quality

### Scoring Scale
- **5**: 100% essential graphics detected
- **4**: >90% detected
- **3**: >75% detected
- **2**: 50-75% detected
- **1**: <50% detected

### Essential (count these)
- Charts, diagrams, flowcharts
- Infographics, data visualizations
- Meaningful icons (warning, status)
- Figures referenced in text

### Decorative (ignore these)
- UI chrome (toolbars, ribbons, menus)
- Backgrounds, separators, shadows
- Repeated identical icons
- Window frames, browser elements

### BAD (wrong counting)
```
Image: Word document with Copilot popup
Judge counts: "34 graphics (toolbar icons)" ← Wrong, those are UI chrome
```

### GOOD (correct counting)
```
Image: Word document with Copilot popup
Judge counts: "1 essential graphic (Copilot popup)" ← Correct
```

---

## Output Format

```json
{
  "text_accuracy": {
    "score": 4,
    "justification": "Two typos found, format variations tolerated",
    "errors_found": ["$2,540M should be $2,450M", "'imports' typo"],
    "tolerances_applied": ["decimal separator"]
  },
  "page_structure": {
    "score": 5,
    "justification": "All 12 outline nodes correctly captured",
    "image_outline": ["Title", "Section A", "A.1", "Section B"],
    "transcription_outline": ["Title", "Section A", "A.1", "Section B"],
    "missing_nodes": [],
    "misleveled_nodes": []
  },
  "graphics_quality": {
    "score": 4,
    "justification": "24 of 25 essential graphics detected",
    "essential_graphics_in_image": 25,
    "essential_graphics_detected": 24,
    "missed_essential_graphics": ["company logo top-right"],
    "ignored_decorative_elements": 8
  },
  "weighted_score": 4.25
}
```

**Weights:** text=0.25, structure=0.35, graphics=0.40
