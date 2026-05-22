# Domain Profile: DEFAULT

Generic research domain profile. Use when no specific domain profile matches (SOFTWARE, MARKET_INTEL, LEGAL).

## When to Use

- Research topic doesn't fit existing domain profiles
- Multi-domain research spanning several categories
- Personal/lifestyle topics (recreation, vacation, health, psychology, relocation, life decisions)
- General knowledge synthesis
- Open-ended exploratory research

## Source Tiers

1. **Tier 1 - Official/Authoritative**: Government sources, legislation, official publications, academic papers
2. **Tier 2 - Professional**: Industry reports, established news outlets, professional associations
3. **Tier 3 - Expert**: Technical blogs by recognized experts, conference talks, official developer advocates
4. **Tier 4 - Community Quality**: Stack Overflow (high votes), GitHub issues (many reactions), Reddit (top posts)
5. **Tier 5 - Community General**: Forums, Discord, personal blogs, social media

**Source Priority**: Always verify Tier 4-5 claims against Tier 1-3 sources when possible. Label Tier 4-5 sources with `[COMMUNITY]` verification label.

## Document Handling

- **PDFs**: Full transcription via `@skills:pdf-tools` + `@skills:llm-transcription` pipeline
- **Web pages**: Full read via `read_url_content` or Playwright MCP
- **Media**: Podcast/video transcription when relevant
- **Large documents**: Process completely (no agent-selected chunks)

## Available QA Tools

### Source Collection
- `search_web` - Initial source discovery
- `read_url_content` - Full web page content extraction
- `Playwright MCP` - Interactive web reading, JavaScript rendering, screenshots
- `Playwriter MCP` - Authenticated sessions, complex interactions

### Document Processing
- `@skills:pdf-tools` - PDF to JPG conversion (`convert-pdf-to-jpg.py`)
- `@skills:llm-transcription` - Image/PDF to markdown with structured data extraction
- Full transcription required - every page, not agent-selected chunks

### Media Processing
- Podcast download via web tools or direct URL
- Video transcription for YouTube, Vimeo via transcription APIs
- Audio transcription via Whisper or similar

### Source Handling
- **Primary sources**: Download to `_DOWNLOADS_gitignore/`, transcribe to `_SOURCES/`
- **Source IDs**: Assign in format `[TOPIC]-SC-[SOURCE]-[DOCNAME]`
- **Secondary sources**: Cite with `[COMMUNITY]` label and access date
- **Access dates**: All sources MUST include `Accessed: YYYY-MM-DD`

## Template Additions

Add these sections to research output template:
- **Limitations and Known Issues** - What we couldn't verify, caveats
- **Recommendations** - Clear actionable guidance (even if brief)
- **Source Access Dates** - When each source was accessed

## Quality Criteria

Additional checks for DEFAULT domain quality pipeline:

- All critical claims have inline citations with verification labels
- Legal/financial/medical claims MUST have Tier 1-2 source citations
- All sources have access dates logged
- Limitations section populated with honest assessment
- Recommendations section exists (even if brief)
- Tier 4-5 sources labeled with `[COMMUNITY]` and limitations noted

## Effort Validation

- Decomposition MUST estimate minimum research hours
- If actual time < 50% of estimate, agent MUST justify or expand research
- Goal: outperform 2 days (16 hours) of human research for EXPLORATORY scope

## VCRIV Pipeline

Quality assurance cycle (runs per scope-based granularity):

- `V` - Verify: Run `/verify` workflow - formal and rule-based correctness
- `C` - Critique: Run `/critique` workflow - find gaps, produces `_REVIEW.md`
- `R` - Reconcile: Run `/reconcile` workflow - prioritize findings
- `I` - Implement: Apply findings, delete `_REVIEW.md`
- `V` - Verify (final): Confirm corrections complete

## MUST-NOT-FORGET

- Run full VCRIV pipeline: `/verify` -> `/critique` -> `/reconcile` -> implement -> `/verify`

**Granularity:**
- NARROW (1 dimension): VCRIV per topic file
- FOCUSED/EXPLORATORY (2+ dimensions): VCRIV per dimension
- Final VCRIV on synthesis document
