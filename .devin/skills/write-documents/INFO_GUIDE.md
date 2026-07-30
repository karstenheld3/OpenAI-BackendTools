# INFO Document Guide

Read BEFORE writing. Follow `INFO_TEMPLATE.md` for mandatory sections.

## 1. Document Purpose

Classify the INFO document to determine optional sections (see Section 3):

1. Findings report - research, options analysis, technology evaluation
2. Concept document - concept, pattern, or approach with rationale
3. How-to document - procedures, recipes, operational knowledge

## 2. Section Order

Optional sections at fixed positions:
- Goals, Questions: above TOC (unnumbered)
- Conclusions, Emergent Hypothesis: numbered content sections, before Next Steps

## 3. Optional Sections

### 3.1 Goals

Insert when: request defines explicit goals, success criteria, or deliverables.
Content: bulleted list of concrete outcomes.
Skip when: Goal field in header block is sufficient.

### 3.2 Questions

Insert when: request poses specific questions, or document triggered by uncertainty.
Format: `Q1:` question on one line, `A1:` answer on next line. Blank line between pairs.
Content: short answers (1-3 sentences) with verification labels. Detailed backing in content sections below TOC.
Skip when: no explicit questions and document is purely informational.

### 3.3 Conclusions

Insert when: research/analysis document with findings leading to actionable conclusions.
Content: derived conclusions referencing supporting sections.
Skip when: how-to or concept doc where Summary captures the takeaways.

### 3.4 Emergent Hypothesis

Insert when: research reveals patterns or theories emerging from combined evidence, not directly stated by sources.
Content: labeled hypotheses with supporting evidence and validation approaches. Mark `[ASSUMED]`.
Skip when: no hypotheses emerged, or all findings directly sourced.

## 4. Diagrams

Prefer diagrams over prose when 3+ components interact, hierarchical relationships exist, or flow has branching logic. Character rules: see `core-conventions.md`.
