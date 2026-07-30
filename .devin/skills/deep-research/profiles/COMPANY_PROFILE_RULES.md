# Company Profile Rules

Rules for writing and verifying company profile INFO documents with GOOD/BAD examples.

**Inherits**: All INFO-* rules from @write-documents `INFO_RULES.md` apply in addition to CP-* rules below. Profiles are specialized INFO documents.

## Rule Index

Quality (QA) - cross-cutting, applies to ALL sections
- CP-QA-01: Every factual claim backed by source or labeled `[ASSUMED]`
- CP-QA-02: Specific over vague - quantify, name, date instead of generalizing
- CP-QA-03: Same entity = same name throughout (no synonyms, no abbreviation drift)
- CP-QA-04: One fact per bullet - no compound statements hiding multiple claims

Header (HD)
- CP-HD-01: All sections filled (standalone profiles are always FULL)
- CP-HD-02: Relation to research context states why this company matters
- CP-HD-03: Related profiles link to existing person/org profile Doc IDs

Summary (SM)
- CP-SM-01: 3-5 sentences covering activity, founding, HQ, size, position, stage
- CP-SM-02: Acronyms expanded on first use (AuM, ARR, SaaS, etc.)

Data (DT)
- CP-DT-01: Legal form and registration included when available
- CP-DT-02: Industry classification uses standard codes (NACE/SIC) when relevant
- CP-DT-03: Employee count includes date of information

Financial (FN)
- CP-FN-01: All figures include currency, fiscal year, and source
- CP-FN-02: Revenue/valuation marked `[ASSUMED]` when inferred from funding data
- CP-FN-03: Key metrics match industry (AuM for asset managers, ARR for SaaS, etc.)

Leadership (LD)
- CP-LD-01: Each person entry has name, title, tenure start, and 1-line background
- CP-LD-02: Reference personal profiles via `(see [TOPIC]-IN[NN])` when they exist

Market (MK)
- CP-MK-01: Competitor entries include basis for comparison (same segment, same geography, same customer)
- CP-MK-02: Market claims cite source - no unsourced market share percentages

Timeline (TL)
- CP-TL-01: Reverse chronological, major milestones only
- CP-TL-02: Funding rounds include amount, lead investor, and date

Risk (RK)
- CP-RK-01: Each risk factor states likelihood and potential impact, not just the risk category
- CP-RK-02: Risks derived from evidence in earlier sections, not speculative

Assessment (AS)
- CP-AS-01: SWOT entries are specific, not generic platitudes
- CP-AS-02: Outlook grounded in evidence from earlier sections

Engagement (EN)
- CP-EN-01: Key contacts include name, role, and rationale for why they are the entry point
- CP-EN-02: Conversation angles reference company's public statements or recent news
- CP-EN-03: At least one concrete, actionable recommendation in Recommended approach

Research Gaps (RG)
- CP-RG-01: Each gap states what is missing AND why it matters
- CP-RG-02: Suggested next steps are actionable (specific source or action to check)

Sensitivity (SN)
- CP-SN-01: Sensitive topics flagged with `[SENSITIVE: reason. Safe angle: ...]`
- CP-SN-02: Competitor analysis neutral in tone, no disparagement

Sources (SC)
- CP-SC-01: All sources include access date
- CP-SC-02: Financial claims require tier 1-2 sources (company register, official reports)

Cross-Reference (XR)
- CP-XR-01: Leadership entries reference personal profiles when they exist
- CP-XR-02: Competitor entries reference company profiles when they exist

## Header Rules

### CP-HD-01: Section Completeness

Standalone profiles are always FULL. All sections must be filled. When no data found, document in Research Gaps section instead of leaving empty sections.

**BAD:**
```
## Market and Competitive Landscape
[empty - no data found]
## Risk Factors
[empty]
```

**GOOD:**
```
## Market and Competitive Landscape
- No publicly available market data identified for this segment.

## Research Gaps
- Market size: No analyst reports or industry data found for [segment]
- Risk factors: Insufficient public disclosure to assess
```

### CP-HD-02: Research Context Relation

Must explain WHY this company is being researched.

**BAD:**
```
**Relation to research context**: Part of the network.
```

**GOOD:**
```
**Relation to research context**: Portfolio company of [Person A] ([TOPIC]-IN[NN]). Primary revenue generator for network's deal flow. Potential partnership target for [collaboration area].
```

## Financial Rules

### CP-FN-01: Financial Figures with Context

Every number needs currency, period, and source attribution.

**BAD:**
```
- **Revenue**: 15M
- **Valuation**: High
```

**GOOD:**
```
- **Revenue**: EUR 15M (FY2025, company website investor page)
- **Valuation**: EUR 120M post-money (Series B, 2024-09, [publication] report)
```

### CP-FN-02: Inferred Financials Labeled

When financial data is estimated from indirect signals, mark clearly.

**BAD:**
```
- **Revenue**: EUR 8-12M (based on employee count)
```

**GOOD:**
```
- **Revenue**: EUR 8-12M [ASSUMED - estimated from 85 employees x EUR 100-140K revenue per employee for [industry segment]]
```

## Leadership Rules

### CP-LD-01: Person Entry Format

Name, title, tenure, and context in one structured entry.

**BAD:**
```
- [Person A] - CEO
- [Person B] - runs marketing
```

**GOOD:**
```
- **[Person A]** - CEO (since 2019). Previously VP Product at [Company X]. Founded two prior startups.
- **[Person B]** - CMO (since 2022). Ex-[Company Y], 15 years [industry] marketing.
```

### CP-LD-02: Cross-Reference to Person Profile

When a personal profile exists, reference instead of duplicating bio.

**BAD:**
```
- **[Person A]** - CEO (since 2019). Born in [City], studied at [University], worked at [Company X] 2005-2010, then [Company Y] 2010-2018, VP Product...
  [full career history duplicated here]
```

**GOOD:**
```
- **[Person A]** - CEO (since 2019). (see [TOPIC]-IN[NN] for full profile)
```

## Assessment Rules

### CP-AS-01: Specific SWOT Entries

Generic statements add no value. Be precise.

**BAD:**
```
- **Strengths**: Good team, innovative product, growing market
- **Weaknesses**: Limited resources
```

**GOOD:**
```
- **Strengths**: Patent-pending [technology] for [market niche] (only [language]-language [product category]). Team combines [domain] (ex-[regulator]) and tech (ex-[Company X]) expertise.
- **Weaknesses**: Single-market dependency ([country] only). No [expansion market] product roadmap visible. Key-person risk on CTO (sole architect of [core system]).
```

## Engagement Rules

### CP-EN-01: Contact Rationale

Name who to contact AND why they are the right person.

**BAD:**
```
- **Key people to contact**: CEO, Head of Sales
```

**GOOD:**
```
- **Key people to contact**:
  - [Person B] (CMO) - Owns partnership decisions. Publicly stated interest in channel partners at [Event Name] [year].
  - [Person C] (Board) - Warm path via shared [Company X] alumni network.
```

### CP-EN-02: Evidence-Based Conversation Angles

Reference actual public statements or events.

**BAD:**
```
- **Conversation angles**: AI, innovation, growth
```

**GOOD:**
```
- **Conversation angles**:
  - Their CEO's keynote at [Event Name] (YYYY-MM) focused on "[topic]" - align with your [related thesis]
  - Recent [funding round] press release mentions expansion to [region] - offer local network introductions
```

## Sensitivity Rules

### CP-SN-01: Sensitive Topic Flagging

Mark and provide safe alternative.

**BAD:**
```
Company faced a data breach in 2023 affecting 50,000 customers.
```

**GOOD:**
```
Company experienced a security incident in 2023. [SENSITIVE: Data breach with regulatory consequences. Safe angle: Ask about their security improvements and SOC 2 certification achieved in 2024 - positions as learning/growth story.]
```
