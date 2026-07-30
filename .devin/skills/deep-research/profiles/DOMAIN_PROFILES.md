# Domain Profiles: Profile Research

Research domain for people, companies, organizations, and networks. Produces structured intelligence for relationship building, networking strategy, and due diligence.

## When to Use

- Research subject is a person, company, organization, or professional network
- Prompt mentions: profile, background check, network analysis, who is, inner circle, career history, relationship mapping
- Output will be consumed by someone preparing for networking, partnership evaluation, hiring, or relationship strategy
- Use PROFILE instead of MARKET_INTEL when the focus is people/relationships rather than financials/markets

## Source Tiers

- **Tier 1 (identity/official)**: LinkedIn profile, company website "About/Team" page, official bio, university directory, organization member list
- **Tier 2 (public record)**: Company register (Handelsregister, Companies House), patent databases, published papers (Google Scholar), conference speaker lists, board appointment announcements
- **Tier 3 (media/community)**: News articles, press releases, podcast appearances, event photos, social media posts, Glassdoor/Kununu reviews, community forums
- **Tier 4 (inferred)**: Patterns from career moves, network connections, timing correlations, absence of information

**Tier 4 special rule**: All tier 4 findings MUST be labeled `[ASSUMED]`. Never present inferred information as fact.

## Gotchas

Common failures a fresh agent will encounter:

1. **LinkedIn requires authentication** - `@skills:ms-playwright-mcp` must use a logged-in browser session. Anonymous scraping returns partial data or login walls. Always verify profile access before starting extraction.
2. **Common name disambiguation** - "Thomas Mueller" returns hundreds of profiles. Use company + location + tenure dates to confirm identity. When uncertain, mark `[ASSUMED - based on company match]`.
3. **Source decay** - Social media posts, company pages, and news articles disappear. Screenshot critical sources immediately. Store in `_SOURCES/` with access date.
4. **Research order for multi-profile sets** - Research companies/organizations BEFORE people. Company context helps interpret career moves, role significance, and reporting structures.
5. **Standalone decision** - Decide during Preflight (Phase 1): only primary research subjects get standalone FULL profiles. All other entities (connections, employers, organizations) are inlined in the parent profile.
6. **GDPR for EU subjects** - Only use publicly available information. Do not attempt to access private databases, leaked data, or non-public social media content.
7. **Profile information half-life** - Career data decays within months (job changes, title changes). Always note data capture date. Flag any profile where newest source is >6 months old.

## Document Handling

- **LinkedIn**: Primary source for personal profiles. Use `@skills:ms-playwright-mcp` to capture full profile (requires login). Store screenshot + extracted text in `_SOURCES/`
- **Company websites**: Capture "About", "Team", "Leadership" pages via browser automation or `read_url_content`
- **News/media**: `read_url_content` for articles. Note publication date - profile information decays rapidly
- **Academic sources**: Google Scholar for publications. University websites for academic roles
- **No PDF pipeline required**: Profile research is primarily web-based, not document-based

## Output Templates (Shared Module)

This folder is a shared module used by ANY domain when researching entities (people, companies, organizations, networks). Select template based on subject type:
- Person → [PERSONAL_PROFILE_TEMPLATE.md](PERSONAL_PROFILE_TEMPLATE.md)
- Company → [COMPANY_PROFILE_TEMPLATE.md](COMPANY_PROFILE_TEMPLATE.md)
- Organization → [ORGA_PROFILE_TEMPLATE.md](ORGA_PROFILE_TEMPLATE.md)
- Network → [NETWORK_PROFILE_TEMPLATE.md](NETWORK_PROFILE_TEMPLATE.md)

**Cross-domain usage**: MARKET_INTEL researching a company, DEFAULT researching a person, LEGAL researching a regulatory body - all use these templates for entity-focused output.

## Rules

Each profile type has a rules file with GOOD/BAD examples. Read the applicable rules file during `/verify` and `/improve`:
- Person → [PERSONAL_PROFILE_RULES.md](PERSONAL_PROFILE_RULES.md)
- Company → [COMPANY_PROFILE_RULES.md](COMPANY_PROFILE_RULES.md)
- Organization → [ORGA_PROFILE_RULES.md](ORGA_PROFILE_RULES.md)
- Network → [NETWORK_PROFILE_RULES.md](NETWORK_PROFILE_RULES.md)

**Standalone vs inlined**: Only FULL profiles become standalone documents. Supporting entities (relevant connections, past employers, peripheral mentions) are inlined within the parent profile's sections (e.g., Related Company Factsheets, Inner Circle, Career Timeline). Never create a standalone document for an entity that is not the primary research subject.

## Quality Criteria

Additional checks for profile domain quality pipeline:

- All career dates verified against at least 2 sources (LinkedIn + company website or news)
- Sensitive topics flagged with `[SENSITIVE: reason. Safe angle: ...]`
- Source recency noted - profiles older than 12 months flagged for refresh
- Cross-references between profiles use `(see [TOPIC]-IN[NN])` format
- Hidden value analysis (network profiles) clearly labeled with assessment confidence level
- No personal data beyond what is publicly available (General Data Protection Regulation (GDPR) consideration for European subjects)
- Engagement Strategy section includes at least one concrete, actionable recommendation

## Process Requirements

Profile research follows the same STRUT + VCRIV discipline as all deep-research:

- **STRUT required**: Always create `__STRUT_[TOPIC].md`. For single profiles this is lightweight (1 phase, 1 deliverable) but ensures planning and time tracking.
- **VCRIV required**: Run on every standalone profile document. For single profiles, VCRIV can be executed in 1 consolidated step (verify + critique + reconcile + implement + verify in one pass). For multi-profile sets, run VCRIV per profile.

## Decomposition Rules

Profile research follows SKILL.md Output Rules:

- **Single profile** (single-file output): No numbered scheme. Filename from context: `_INFO_[TOPIC]_[SubjectName].md`. Each profile template has its own Sources section inline.
- **Network analysis** (multi-file output): Mandatory `_INFO_[TOPIC]-01_Summary.md` + `_INFO_[TOPIC]-02_Sources.md` + numbered profiles starting at 03. Example: 1 network profile + N personal profiles + M company/org profiles.
- **Company set** (multi-file output): Mandatory `_INFO_[TOPIC]-01_Summary.md` + `_INFO_[TOPIC]-02_Sources.md` + 1 company profile per entity starting at 03, cross-referenced.

## Enrichment

Profile enrichment techniques are defined in the `/improve` workflow (Research Output → Profile-specific enrichment section). Run `/improve` on profile documents to apply them.
