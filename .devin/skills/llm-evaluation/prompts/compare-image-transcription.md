# Compare Image Transcription Semantic Capture

Evaluate how well these two transcriptions capture the **same underlying visual content**. Both are attempting to represent the same original figure - judge whether they convey equivalent semantic understanding.

## Transcription A

The following contains ASCII art and `<transcription_notes>` metadata:

{transcription_a}

## Transcription B

The following contains ASCII art and `<transcription_notes>` metadata:

{transcription_b}

## What to Compare

Each transcription contains:
- **ASCII art** (```` ```ascii ... ``` ````) - structural representation using text characters
- **transcription_notes** (`<transcription_notes>...</transcription_notes>`) - metadata including:
  - Mode (Structural/Shading)
  - Dimensions
  - What ASCII captures vs misses
  - Colors and their meanings
  - Layout description
  - Reconstruction hints

## Evaluation Criteria

**Do both transcriptions convey the same semantic understanding?**

1. **Structural Elements (35 points)**
   - Same components identified? (boxes, nodes, connections)
   - Same hierarchy or flow depicted?
   - Same labels and annotations present?

2. **Visual Information Preserved (25 points)**
   - Same colors documented?
   - Same visual details noted as missing from ASCII?
   - Same reconstruction hints provided?

3. **Relationships and Layout (25 points)**
   - Same spatial arrangement described?
   - Same directional flow captured?
   - Same groupings or regions identified?

4. **Completeness (15 points)**
   - Both capture similar level of detail?
   - Neither omits significant elements the other includes?

## Scoring Guide

- **90-100**: Both capture identical semantic content, only superficial wording differs
- **70-89**: Same core understanding, minor interpretive differences
- **50-69**: Similar overall, but one captures details the other misses
- **30-49**: Different interpretations of the same visual
- **0-29**: Fundamentally different understanding of the source image

## Output

JSON only, example format:

{{"score": 85, "differences": ["color description differs", "layout interpretation varies"]}}
