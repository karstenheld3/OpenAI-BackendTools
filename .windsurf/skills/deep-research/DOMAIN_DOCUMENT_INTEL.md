# Domain Profile: Document Intelligence

Research domain for extracting structured data, tables, and key information from previously transcribed or source documents.

## When to Use

- Research requires extracting tables, data points, or structured information from documents
- Prompt mentions: extract data, parse tables, compare documents, cross-reference, data extraction
- Source documents are contracts, reports, datasets, specifications, or technical standards
- Output will be structured data (JSON, CSV) alongside narrative analysis

## Source Tiers

- **Tier 1 (official/primary)**: Original source documents (contracts, reports, datasets, standards, specifications)
- **Tier 2 (vendor/issuer)**: Annotated/summarized versions, metadata, companion documents
- **Tier 3 (community/analyst)**: Commentary, analysis, implementation guides

## Document Handling

- **Transcribe ALL documents fully** - No partial reads, no summarization of source material
- Extract tables as structured data via `<transcription_json>` tags (produced automatically by transcription pipeline)
- For documents already transcribed: Grep `<transcription_json>` and `<transcription_table>` tags to extract all structured data
- Create cross-reference matrices when comparing multiple documents
- Store originals + transcriptions + extracted data in `_SOURCES/`:
  ```
  _SOURCES/
  \u251c\u2500\u2500 document.pdf                    # Original
  \u251c\u2500\u2500 document.md                     # Full transcription
  \u251c\u2500\u2500 document_data.jsonl             # All tables/charts as JSON
  \u251c\u2500\u2500 document_transcribed/           # Individual pages
  \u2514\u2500\u2500 cross_reference.json            # Cross-reference matrix (if applicable)
  ```
- **Model selection**: Use `gpt-5-mini` for all document transcription (accuracy critical for data extraction)

## Template Additions

Add these sections to the standard topic template:

- **Data Extraction Summary** - Overview of extracted data types and counts
- **Table Index** - List of all extracted tables with page references and JSON file locations
- **Cross-Reference Matrix** - Mapping between related data points across documents
- **Data Quality Notes** - Confidence levels, unclear values, reconciliation issues

## Quality Criteria

Additional checks for document intelligence domain quality pipeline:

- Every extracted table verified against source document (spot-check minimum 20% of tables)
- All `<transcription_json>` data parseable as valid JSON
- Cross-reference matrix complete for all overlapping data points between documents
- `[unclear]` markers from transcription documented and flagged in data quality notes
- No data points cited without page/section reference to source document
- Extracted numerical values cross-checked for unit consistency (currency, percentages, dates)
