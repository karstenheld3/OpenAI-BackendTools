# Research Summary Depth Rules

Rules for verifying content depth and completeness of `_INFO_[TOPIC]-01_Summary.md` files. Referenced by `/verify` and `/improve` workflows after structural checks (SM-01 through SM-11 in `RESEARCH_RULES.md`) pass.

**Scope**: Summary files only. Prerequisites: SM-* rules in `RESEARCH_RULES.md` verified first. These rules check whether the summary captures enough of the underlying research to serve as the primary reading artifact (80% coverage target - reader rarely needs to open topic files).

## Detection

Apply these rules when scope is a `_INFO_[TOPIC]-01_Summary.md` file or a research output folder that contains one.

## Rule Index

Content Depth (CD) - mandatory quality thresholds
- SD-CD-01: Per-Topic Summaries are 5-15 sentences with Key Findings and quantitative facts
- SD-CD-02: Source references include actual URLs, not just source IDs
- SD-CD-03: Key entities have condensed inline profiles
- SD-CD-04: Quantitative evidence chains preserved from topic files
- SD-CD-05: Scoring and ranking tables surfaced with methodology
- SD-CD-06: 3-5 impactful source quotes preserved with attribution
- SD-CD-07: All applicable template sections present and populated

Enrichment Sections (ES) - conditional, present when applicable
- SD-ES-01: Cross-Research References section when entity appears in 2+ sibling research sets
- SD-ES-02: Entity Index section when 5+ named entities across topic files
- SD-ES-03: Contradictions and Tensions section when competing forces or paradoxes found
- SD-ES-04: Open Questions and Research Gaps section aggregated from topic files
- SD-ES-05: Unicode diagrams for complex structures (market maps, regulatory layers, timelines)
- SD-ES-06: Reading Guide section when 3+ audience types benefit from different reading orders
- SD-ES-07: Problem -> Solution Lookup when research evaluates multiple options for distinct needs
- SD-ES-08: Recommendations section when research produces actionable advice beyond conclusions
- SD-ES-09: Risk Assessment section when evaluated options carry categorized risks

## SD-CD-01: Per-Topic Summary Data Density

Each Per-Topic Summary must contain 5-15 sentences (scale with topic complexity) plus a Key Findings list. Sentences must include the top 3-5 quantitative facts from the topic file. Verification labels must be preserved on key claims.

**BAD:**
```
### IN05: Adoption Barriers

Organizations face scaling barriers and skill gaps. Error rates in automated processes
are very high. These create opportunities for better solutions.

**Key Findings:**
- Scaling difficulty is a major barrier
- Skill gaps exist
```

**GOOD:**
```
### IN05: Adoption Barriers and Failure Modes

Organizations face interconnected barriers creating a "scaling trap" from pilots to enterprise
deployment. The barriers cluster into four categories: organizational (92% cite skill gaps),
technical (data quality is most-cited barrier), operational (55% cannot measure impact), and
structural (85-95% false positive rates in automated monitoring). The false positive crisis
consumes operational capacity: 50,000 daily alerts at major enterprises, 47,500 false positives,
2-5 hours investigation per alert, 90%+ analyst time on non-actionable cases, 25-40% annual
staff turnover. Teams spending 90% of capacity on alert investigation have near-zero bandwidth
for strategic analysis and research. [VERIFIED] (TOPIC-SC-SRCA-DOCREF, TOPIC-SC-SRCB-DOCREF)

**Key Findings:**
- 92% cite employee skill gaps as barrier (Industry Survey Q1 2026) [VERIFIED]
- False positive rates: 85-95% in automated monitoring [VERIFIED]
- $XXB annual industry compliance cost, rising 15%/year [VERIFIED]
- Strategic analysis gap caused by alert overload, not alert quality [VERIFIED]
```

## SD-CD-02: Source URL Inlining

When the summary references source IDs (e.g., `TOPIC-SC-SRCID-DOCREF`), the actual URL must be included at least once per entity or source. Read `_INFO_[TOPIC]-02_Sources.md` to resolve IDs to URLs.

**BAD:**
```
VendorA dominates with 1,000+ customers [VERIFIED] (TOPIC-SC-VNDA-MKTPOS)
```

**GOOD:**
```
VendorA dominates with 1,000+ customers [VERIFIED] (TOPIC-SC-VNDA-MKTPOS | vendora.com)
```

Format: `(SOURCE_ID | domain-or-short-url)`. Full URL not required - domain or short path sufficient for follow-up. Each source URL appears once on first reference; subsequent references use source ID only.

## SD-CD-03: Entity Profiles Inlined

For each entity classified as COMPETE, PARTNER, or MONITOR that appears in 2+ topic files or is central to conclusions, include a condensed 1-line profile in the summary. Profile fields: funding/revenue, headcount, key product, URL, classification.

**BAD:**
```
VendorA is a major competitor in the target market segment.
```

**GOOD:**
```
VendorA (PE-backed, 800+ employees, 20 countries, 1,000+ customers, PlatformX + EngineY,
vendora.com) [COMPETE] - dominant in target segment, acquired StartupB (agentic AI)
and StartupC (obligation mapping) in 2025-2026.
```

Profile placement: either inline on first mention, or in a dedicated Entity Index section (SD-ES-02). Not both.

## SD-CD-04: Quantitative Evidence Chains

When topic files contain linked quantitative facts forming a causal chain, the summary must preserve the chain, not just the headline number.

**BAD:**
```
Compliance costs are high and false positive rates exceed 85%.
```

**GOOD:**
```
False positive rates of 85-95% generate 47,500 false alerts daily at major enterprises,
each requiring 2-5 hours investigation, consuming 90%+ of analyst time, driving 25-40%
annual staff turnover, costing $XXB annually industry-wide. [VERIFIED]
```

A chain is: input fact -> consequence -> consequence -> impact metric. Preserve at least 3 links.

## SD-CD-05: Scoring and Ranking Tables

When topic files contain scoring models, ranked comparisons, or multi-criteria evaluations, the summary must surface the complete scoring methodology and top results.

**BAD:**
```
We evaluated several arenas and recommend Arena A.
```

**GOOD:**
```
Arena ranking by Pain (1-5) x WTP (1-5) x Margin (score):
1. Arena A (target segment): Pain 5, WTP 5, Margin HIGH (70-85%)
2. Arena B (adjacent segment): Pain 4, WTP 4, Margin HIGH
3. Arena C (expansion segment): Pain 4, WTP 4, Margin MEDIUM-HIGH
[... top 5 minimum]
```

## SD-CD-06: Key Source Quotes

Preserve 3-5 direct quotes from sources that are particularly impactful, quotable, or capture a market dynamic concisely. Include attribution.

**BAD:**
```
Enterprises prefer solutions that minimize risk.
```

**GOOD:**
```
"Enterprises don't want innovation. They want solutions that don't create problems." - (industry
observation, TOPIC-SC-SRCID-DOCREF)
```

Selection criteria: quote captures insight that paraphrasing would dilute, or quote is reusable in presentations or decision-making materials.

## SD-CD-07: Template Section Completeness

All sections from `RESEARCH_SUMMARY_TEMPLATE.md` must be present and populated when applicable. "When applicable" conditions:

- Goals/Questions: always required (SM-08 prerequisite)
- Summary: always required (SM-01 prerequisite)
- Topic Files: always required (SM-02 prerequisite)
- Conclusions: required when research produces actionable conclusions derived from cross-topic analysis
- Emergent Hypotheses: required when research reveals patterns not directly stated by any single source
- Per-Topic Summaries: always required (SM-09 prerequisite)
- Limitations: always required

When a conditional section is omitted, no marker needed - absence means "not applicable." When present, section must contain substantive content (not placeholder text).

**BAD:**
```
## 2. Conclusions

[To be added]
```

**GOOD:**
```
## 2. Conclusions

1. VendorA is the primary competitive threat in the target segment, but their enterprise
   pricing (EUR 500K+) leaves the mid-market underserved (IN04, IN06)
2. Operations teams spending 90% of capacity on alert investigation have near-zero bandwidth
   for strategic analysis - the product fills this gap, not the alert quality gap (IN05, IN07)
```

## SD-ES-01: Cross-Research References

When an entity (company, product, framework, regulation) appears in 2+ sibling research sets within the same parent folder, add a Cross-Research References section linking to the other summary with a brief finding delta.

Condition: parent folder contains 2+ research subfolders, and entity name grep yields matches in multiple subfolders.

**GOOD:**
```
## Cross-Research References

- VendorA: Market dominance (this research, IN04) + technology ecosystem participant
  (TECHLANDSCAPE, IN08). Delta: TECHLANDSCAPE focuses on VendorA's architecture;
  this research focuses on market position and acquisition strategy.
- VendorB: Competitor profile (TECHLANDSCAPE, IN07) + business model case study
  (BIZMODELS, IN14). Delta: BIZMODELS analyzes pricing; TECHLANDSCAPE analyzes positioning.
```

## SD-ES-02: Entity Index

When 5+ named entities appear across topic files with classifications, add an Entity Index section listing all entities with classification, primary topic file reference, and condensed profile. Adapt classification scheme to domain: COMPETE/PARTNER/MONITOR for market research, license type for software, risk level for compliance.

**GOOD (market research):**
```
## Entity Index

- VendorA (COMPETE) - PE-backed, 800+ employees, PlatformX, vendora.com → IN04
- VendorB (COMPETE) - EUR 6.1B revenue, ProductY + ProductZ → IN04
- VendorC (COMPETE) - $130M Series B, $700M valuation, PlatformW → IN07
- VendorD (MONITOR) - API-native monitoring, 550 items/day → IN04
- PartnerE (PARTNER) - IT provider for target customer segment → IN06
```

**GOOD (software evaluation):**
```
## Library Index

- libraryA (MIT) - async HTTP client, HTTP/2 support, 12K stars → IN05
- libraryB (BSD-3) - HTML parser, C-backed, handles malformed HTML → IN08
- libraryC (AGPL-3.0) - PDF extraction, 180 pages/sec, license risk → IN10
- toolD (MIT) - document conversion, single API, 169K stars → IN43
```

## SD-ES-03: Contradictions and Tensions

When research findings pull in opposite directions or reveal paradoxes, add a Contradictions and Tensions section. Each item states both sides with source references.

Condition: cross-topic analysis reveals conflicting data, competing market forces, or paradoxes.

**GOOD:**
```
## Contradictions and Tensions

1. Adoption vs. Impact: 81% of organizations report AI adoption, but only 14% see AI as
   transformational (IN03 vs IN05). High adoption rate masks shallow integration.
2. Sensitivity vs. Blindness: Monitoring systems simultaneously produce 85-95% false positives
   AND detect less than 1% of actual issues (IN05). System is both too sensitive and too blind.
```

## SD-ES-04: Open Questions and Research Gaps

Aggregate unanswered questions and "Extend This Segment" prompts from topic files into a single section. Each item references the source topic file.

Condition: topic files contain "Extend This Segment" sections, or key questions remain unanswered.

**GOOD:**
```
## Open Questions and Research Gaps

- What would mid-market firms pay for tools in the target segment? (IN04)
- Does PartnerE plan to add AI-powered capabilities for their customer base? (IN04)
- VendorC regional expansion timeline and market penetration status? (IN07)
- Actual adoption rates of VendorA at mid-market firms? (IN04)
```

## SD-ES-05: Unicode Diagrams

When the summary describes complex hierarchical, layered, or sequential structures, represent them as Unicode box-drawing diagrams instead of (or in addition to) prose.

Condition: structure has 3+ levels, 3+ parallel elements, or describes a flow/timeline.

**GOOD:**
```
Market Structure (3 tiers):
┌─ Tier 1: Enterprise ────────────────────────────────────┐
│  VendorA (dominant)  │  VendorB (incumbent)  │  VendorC │
├─ Tier 2: Mid-Market ────────────────────────────────────┤
│  VendorD             │  VendorE              │  (gap)   │
├─ Tier 3: SME / Manual ──────────────────────────────────┤
│  Spreadsheets        │  Newsletters          │  Manual  │
└─────────────────────────────────────────────────────────┘
```

## SD-ES-06: Reading Guide

When the summary serves 3+ distinct audience types who benefit from different reading orders, add a Reading Guide section with role-based navigation paths.

Condition: research covers strategic, technical, legal, and/or financial dimensions simultaneously.

**GOOD:**
```
## Reading Guide

- Product Manager: Summary → IN05 (Pain Points) → IN10 (Implications) → Conclusions
- Legal/Compliance: IN03 (Requirements) → IN04 (Regulatory Detail) → Limitations
- CTO/Architect: IN07 (Competitive Landscape) → IN06 (Technology) → IN10
- Investor: Summary → Conclusions → IN03 (Market Sizing) → Emergent Hypotheses
```

## SD-ES-07: Problem -> Solution Lookup

When research evaluates multiple options (libraries, vendors, tools, strategies, approaches) for distinct problems or needs, add a Problem -> Solution Lookup section. Each entry maps a specific problem to the recommended solution with alternatives. Adapt heading to domain.

Condition: research covers 5+ distinct options across 3+ problem categories.

**GOOD:**
```
## Problem → Solution Lookup

### [Category 1]

- **[Problem statement]** → OptionA (IN-XX, license). Alt: OptionB (IN-YY) if [condition]
- **[Problem statement]** → OptionC (IN-XX, license)

### [Category 2]

- **[Problem statement]** → OptionD (IN-XX). Alt: OptionE (IN-YY) for [different tradeoff]
```

## SD-ES-08: Recommendations

When research produces actionable advice beyond analytical conclusions, add a Recommendations section grouped by use case, audience, or scenario. Distinct from Conclusions (what we learned) - Recommendations say what to do.

Condition: research covers options where different contexts lead to different choices.

**GOOD:**
```
## Recommendations

### [Use Case / Audience 1]

- Start with OptionA + OptionB for baseline coverage (IN-XX, IN-YY)
- Add OptionC only when [specific trigger] (IN-ZZ)

### [Use Case / Audience 2]

- Prefer OptionD over OptionA due to [tradeoff] (IN-XX)
```

## SD-ES-09: Risk Assessment

When evaluated options carry categorized risks (legal, technical, operational, financial), add a Risk Assessment section. Adapt categories to domain: license risks for software, vendor lock-in for SaaS, regulatory exposure for compliance, technical debt for architecture.

Condition: 3+ options have non-trivial risks that affect the recommendation.

**GOOD:**
```
## Risk Assessment

### [Risk Category 1]

- OptionA: [Risk description with specifics] → [Mitigation or decision] (IN-XX)
- OptionB: [Risk description] → [Mitigation] (IN-YY)

### [Risk Category 2]

- OptionC: [Risk description] → [Mitigation] (IN-XX)
```

## Verification Procedure

Execute after SM-* structural checks (from `RESEARCH_RULES.md`) pass. Order:

1. Open summary file and `_INFO_[TOPIC]-02_Sources.md` side by side
2. Check SD-CD-07: scan for all template sections, verify each is present and populated (or correctly omitted with justification)
3. Check SD-CD-01: for each Per-Topic Summary, count sentences and verify Key Findings list with [LABEL]s and quantitative facts
4. Check SD-CD-02: grep for source IDs without URLs. Cross-reference against Sources file. Flag any source ID appearing 3+ times without URL resolution
5. Check SD-CD-03: identify entities mentioned 2+ times. Verify each has a condensed profile (inline or in Entity Index)
6. Check SD-CD-04: identify quantitative claims. Verify chains are preserved (3+ linked facts), not just headline numbers
7. Check SD-CD-05: check topic files for scoring/ranking tables. Verify top results surfaced in summary
8. Check SD-CD-06: verify 3-5 impactful quotes present with attribution
9. Check SD-ES-* conditionals: for each, evaluate whether the condition applies. If yes, verify section present and populated

Severity levels:
- SD-CD-01 through SD-CD-04 violations: HIGH (directly reduce coverage below 80% target)
- SD-CD-05 through SD-CD-07 violations: MEDIUM
- SD-ES-* violations: LOW (conditional sections, omission acceptable when condition not met)

## Improvement Procedure (`/improve`)

When `/improve` targets a summary file, apply these enrichment techniques. Each technique maps to one SD-* rule and constitutes one Phase 3 improvement candidate. Execute in priority order.

### Priority 1: Data Density (HIGHEST impact)

**Technique: Per-Topic Data Densification** (serves SD-CD-01)

1. Read each `_INFO_[TOPIC]-[NN]_*.md` topic file (skip Summary and Sources)
2. For each topic file, extract: all quantitative facts, all [VERIFIED] and [PROVEN] claims, all entity profiles, key conclusions
3. Expand Per-Topic Summary from current length to 5-15 sentences
4. Add Key Findings list with [LABEL]s if missing
5. Preserve data chains: input fact -> consequence -> consequence -> impact metric (minimum 3 links)
6. Verify: after densification, reader understands topic file's main contribution without opening it

**Technique: Template Section Population** (serves SD-CD-07)

1. Compare summary against `RESEARCH_SUMMARY_TEMPLATE.md` section list
2. For each missing section: read all topic files, extract cross-topic patterns
3. Write Conclusions (cross-topic, reference IN-numbers), Emergent Hypotheses (patterns from combined evidence, all [ASSUMED]), Limitations (scope boundaries, source freshness)

### Priority 2: Self-Containment (HIGH impact)

**Technique: Source URL Inlining** (serves SD-CD-02)

1. Open `_INFO_[TOPIC]-02_Sources.md`
2. For each source ID referenced in the summary, find the corresponding URL in the Sources file
3. On the first reference to each source, append `| domain-or-short-url` inside the parentheses
4. Subsequent references keep source ID only

**Technique: Entity Profile Extraction** (serves SD-CD-03)

1. Grep all topic files for entities with classifications (COMPETE, PARTNER, MONITOR)
2. For each entity appearing 2+ times or central to conclusions, read the most detailed topic file mention
3. Create condensed 1-line profile: Name (funding/revenue, headcount, key product, URL) [CLASSIFICATION]
4. Place profile inline on first mention or collect in Entity Index (SD-ES-02)

### Priority 3: Cross-Research Integration (HIGH impact)

**Technique: Cross-Research Comparison** (serves SD-ES-01)

1. Identify the parent folder containing sibling research subfolders
2. For each entity named in this summary, grep entity name across all sibling research folders
3. For each entity appearing in 2+ sets, read both summaries and extract finding delta
4. Add Cross-Research References section with entity, folder, and delta

**Technique: Entity Index Construction** (serves SD-ES-02)

1. Read all topic files, collect every named entity with classification
2. Deduplicate and sort by classification (domain-appropriate grouping)
3. Add condensed profile and primary topic file reference for each

**Technique: Problem-Solution Mapping** (serves SD-ES-07)

1. Read all topic files, identify distinct problems/needs that the research addresses
2. For each problem, identify the recommended solution and alternatives from the topic files
3. Group by category, format as problem -> solution with IN-references and key attributes

**Technique: Recommendation Synthesis** (serves SD-ES-08)

1. Read Conclusions and Per-Topic Summaries for actionable advice
2. Group recommendations by use case, audience, or scenario
3. For each group: state what to do, with rationale and IN-references
4. Distinct from Conclusions: Conclusions = findings, Recommendations = actions

**Technique: Risk Cataloging** (serves SD-ES-09)

1. Read all topic files for risk indicators (license issues, stability concerns, vendor dependencies, operational risks)
2. Categorize risks by type (legal, technical, operational, financial)
3. For each risk: state the option, the risk, and the mitigation or decision

### Priority 4: Visual Comprehension (MEDIUM impact)

**Technique: Structure Diagramming** (serves SD-ES-05)

1. Scan summary for hierarchical, layered, or sequential structures described in prose
2. For structures with 3+ levels or parallel elements, create Unicode box-drawing diagram
3. Place diagram adjacent to the prose description (complement, not replace)

**Technique: Evidence Chain Preservation** (serves SD-CD-04)

1. Read topic files for linked quantitative facts (A causes B causes C, with numbers at each step)
2. Verify the full chain appears in the summary, not just endpoint numbers
3. If chain is broken, reconstruct from topic file data

### Priority 5: Nuance and Completeness (MEDIUM impact)

**Technique: Contradiction Extraction** (serves SD-ES-03)

1. Read all topic files looking for findings that pull in opposite directions
2. For each tension: state both sides with source references
3. Add Contradictions and Tensions section

**Technique: Open Question Aggregation** (serves SD-ES-04)

1. Read all topic files for "Extend This Segment" sections and unanswered questions
2. Collect and deduplicate
3. Add Open Questions and Research Gaps section with topic file references

**Technique: Quote Preservation** (serves SD-CD-06)

1. Read all topic files for direct quotes from sources
2. Select 3-5 most impactful (captures insight that paraphrasing would dilute)
3. Add with attribution and source reference

### Priority 6: Navigation (LOW impact)

**Technique: Reading Guide Construction** (serves SD-ES-06)

1. Identify 3+ distinct audience types (product, technical, legal, financial, investor)
2. For each audience, define optimal reading path through summary sections and topic files
3. Add Reading Guide section

**Technique: Scoring Table Surfacing** (serves SD-CD-05)

1. Grep topic files for scoring models, ranked lists, multi-criteria evaluations
2. Surface complete methodology and top 5 results in summary
3. Reference source topic file
