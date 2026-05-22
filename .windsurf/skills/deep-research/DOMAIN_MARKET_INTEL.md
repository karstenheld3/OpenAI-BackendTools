# Domain Profile: Market Intelligence

Research domain for companies, financial reports, competitive analysis, market trends, and business intelligence.

## When to Use

- Research subject is a company, market segment, product category, or competitive landscape
- Prompt mentions: revenue, market share, quarterly results, annual report, SEC filing, earnings, competitor, press release
- Output will be consumed by business analysts, investors, or strategy teams

## Source Tiers

- **Tier 1 (official/primary)**: SEC filings (10-K, 10-Q, 8-K), annual reports, investor presentations, official press releases
- **Tier 2 (vendor/issuer)**: Earnings call transcripts, company blog, official product pages, regulatory filings
- **Tier 3 (community/analyst)**: Analyst reports, industry publications, news articles, financial databases

## Document Handling

- **Mandatory PDF download**: Quarterly and annual reports MUST be downloaded and transcribed via source processing pipeline
- For reports >50 pages: Transcribe fully via `@skills:llm-transcription` (batch mode, 12 workers). Use `<transcription_json>` tags to extract all financial tables without additional LLM calls.
- Extract key data as structured JSON via grep of `<transcription_json>` tags: revenue, margins, guidance, segment breakdown
- Download reports to `_DOWNLOADS_gitignore/`, store transcriptions (`report.md`) in `_SOURCES/`
- For press releases and news: `read_url_content` or `@skills:ms-playwright-mcp` screenshot + transcribe

## Template Additions

Add these sections to the standard topic template:

- **Financial Summary** - Key metrics (revenue, margins, growth rates, guidance)
- **Competitive Position** - Market share, key competitors, differentiation
- **Key Metrics** - KPIs specific to the industry/company
- **Risk Factors** - From official filings and analyst reports
- **Timeline** - Key dates (earnings, product launches, regulatory milestones)

## Quality Criteria

Additional checks for market intelligence domain quality pipeline:

- All numerical claims traced to specific report page/section with inline citation
- Financial data cross-referenced between multiple sources (e.g., 10-K vs earnings call)
- Currency and fiscal year clearly stated for all financial figures
- Time period explicitly stated for all metrics (Q1 2025, FY2024, TTM, etc.)
- At least one primary source (annual report or SEC filing) fully transcribed per company
- Analyst opinions clearly labeled as `[COMMUNITY]`, not presented as fact
