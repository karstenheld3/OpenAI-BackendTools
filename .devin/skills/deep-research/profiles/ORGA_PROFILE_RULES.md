# Organization Profile Rules

Rules for writing and verifying organization profile INFO documents with GOOD/BAD examples.

**Inherits**: All INFO-* rules from @write-documents `INFO_RULES.md` apply in addition to OP-* rules below. Profiles are specialized INFO documents.

## Rule Index

Quality (QA) - cross-cutting, applies to ALL sections
- OP-QA-01: Every factual claim backed by source or labeled `[ASSUMED]`
- OP-QA-02: Specific over vague - quantify, name, date instead of generalizing
- OP-QA-03: Same entity = same name throughout (no synonyms, no abbreviation drift)
- OP-QA-04: One fact per bullet - no compound statements hiding multiple claims

Header (HD)
- OP-HD-01: All sections filled (standalone profiles are always FULL)
- OP-HD-02: Organization type clearly identified (university, industry body, NGO, etc.)
- OP-HD-03: Related profiles link to person/company profiles of key members

Summary (SM)
- OP-SM-01: 3-5 sentences covering type, founding, scale, mission, relevance
- OP-SM-02: Distinguish stated mission from actual focus

Data (DT)
- OP-DT-01: Legal form matches jurisdiction (e.V., Stiftung, 501(c)(3), etc.)
- OP-DT-02: Size metric appropriate to type (members, students, employees, budget)
- OP-DT-03: Rankings/accreditations sourced and dated

Governance (GV)
- OP-GV-01: Leadership entries include appointment mechanism (elected, appointed, hereditary)
- OP-GV-02: Decision-making process explicitly stated
- OP-GV-03: Accountability direction clear (to whom does leadership answer)

Membership (MB)
- OP-MB-01: Entry criteria distinguish explicit (formal) from implicit (unspoken)
- OP-MB-02: Notable members relevant to research context, not just famous names
- OP-MB-03: Membership tiers described with distinguishing privileges

Programs (PG)
- OP-PG-01: Each program entry includes audience, format, frequency, scale
- OP-PG-02: Events include date/frequency, not just name

Assessment (AS)
- OP-AS-01: Relevance assessment tied to specific research context, not generic value statements
- OP-AS-02: Influence scope quantified (reach, budget, member count) not described vaguely

Engagement (EN)
- OP-EN-01: Entry points are specific paths (application, event, committee), not vague
- OP-EN-02: Timing tied to org's calendar (membership cycles, annual events)
- OP-EN-03: At least one concrete, actionable recommendation

Research Gaps (RG)
- OP-RG-01: Each gap states what is missing AND why it matters
- OP-RG-02: Suggested next steps are actionable (specific source or action to check)

Sensitivity (SN)
- OP-SN-01: Political/ideological orientation stated only when discernible from evidence
- OP-SN-02: Criticism section balanced with source attribution

Sources (SC)
- OP-SC-01: All sources include access date
- OP-SC-02: Official org sources (website, annual report) prioritized over third-party descriptions

Cross-Reference (XR)
- OP-XR-01: Key governance members reference personal profiles when they exist
- OP-XR-02: Partner organizations reference their own profiles when they exist

## Header Rules

### OP-HD-01: Section Completeness

Standalone profiles are always FULL. All sections must be filled. When no data found, document in Research Gaps section instead of leaving empty sections.

**BAD:**
```
## Governance Structure
[empty - no data found]
## Membership and Constituency
[empty]
```

**GOOD:**
```
## Governance Structure
- No publicly available governance information identified beyond website leadership page.

## Research Gaps
- Governance: Decision-making process, appointment mechanism, and accountability unknown
- Membership: Entry criteria and member count not publicly disclosed
```

## Mission Rules

### OP-SM-02: Stated vs Actual Focus

Distinguish between official narrative and observable behavior.

**BAD:**
```
## Mission and Purpose

- **Official mission**: Advancing digital innovation in [industry]
- **Actual focus**: Same as above
```

**GOOD:**
```
## Mission and Purpose

- **Official mission**: "[Actual mission statement quote]" (charter, [year])
- **Actual focus**: Lobbying platform for [incumbent segment] against [disruptor] regulation. 80% of published position papers defend existing [industry] regulations. [ASSUMED - based on publication analysis]
- **Target constituency**: C-level executives at [member type] with >[threshold]
- **Value proposition**: [Core service 1] and peer networking among non-competing institutions
```

## Governance Rules

### OP-GV-01: Appointment Mechanism

How leaders got there matters for understanding power dynamics.

**BAD:**
```
### Leadership
- **[Person A]** - President (since 2021)
```

**GOOD:**
```
### Leadership
- **[Person A]** - President (since 2021). Elected by general assembly for 3-year term. Previously board member (2018-2021). CEO of [Company X].
```

### OP-GV-02: Decision-Making Clarity

Specify how decisions flow.

**BAD:**
```
- **Decision-making**: Board decides things
```

**GOOD:**
```
- **Decision-making**: 7-member executive board (majority vote). Strategic decisions require supervisory board approval (15 members, rotating industry representatives). Budget >EUR 500K requires general assembly ratification.
```

## Membership Rules

### OP-MB-01: Explicit vs Implicit Criteria

Separate formal requirements from unspoken ones.

**BAD:**
```
- **Membership criteria**: Companies in [industry] can join
```

**GOOD:**
```
- **Membership criteria**: Formal: registered [institution type] in [region], annual revenue >EUR [amount], nomination by existing member. Implicit: [established segment] background preferred - [disruptor segment] applications reportedly deprioritized [ASSUMED - based on member composition analysis showing 0 [disruptor type] among [N] members]
```

## Program Rules

### OP-PG-01: Program Entry Completeness

Each program needs enough detail to evaluate attendance value.

**BAD:**
```
- **Annual Conference**: Big event, many attendees
- **Working Groups**: Members collaborate
```

**GOOD:**
```
- **[Annual Event Name]**: Purpose: Peer networking and [domain] briefing. Audience: C-level from member institutions (120-150 attendees). Format: 2-day conference, invitation-only dinners. Frequency: Annual (November). Scale: EUR 800K budget, 30 speakers.
- **[Working Group Name]**: Purpose: Joint position papers on [topic]. Audience: [Role] heads and legal counsel. Format: Monthly virtual meetings + quarterly in-person. Frequency: 12x/year. Scale: 25 active participants from 18 institutions.
```

## Engagement Rules

### OP-EN-01: Specific Entry Points

Name the actual path in, not categories.

**BAD:**
```
- **Entry points**: Membership, events, partnerships
```

**GOOD:**
```
- **Entry points**:
  - Guest attendance at [Annual Event] (apply via website by [month], EUR [amount] non-member fee, requires member recommendation)
  - [Working Group] observer status (request via [contact], no fee, 3-month trial)
  - Associate membership (EUR [amount]/year, simplified application for technology vendors, limited voting rights)
```

### OP-EN-02: Calendar-Aligned Timing

Tie recommendations to the org's actual schedule.

**BAD:**
```
- **Timing considerations**: Apply when ready
```

**GOOD:**
```
- **Timing considerations**:
  - Membership applications reviewed in Q1 (January-March) for April intake
  - Annual Summit registration opens August, fills by September
  - Working Group new observer slots available after annual restructuring (January)
  - Board election year 2027 - turnover creates openness to new relationships
```

## Sensitivity Rules

### OP-SN-01: Political Orientation from Evidence

Only state when supported by observable indicators.

**BAD:**
```
- **Political/ideological orientation**: Conservative, anti-innovation
```

**GOOD:**
```
- **Political/ideological orientation**: Pro-[incumbent segment] regulation. Evidence: [N] of [M] recent position papers oppose [reform type]. Board composition 100% [established segment]. No [disruptor segment] representation despite stated "innovation" mission. [ASSUMED - inferred from publication and membership patterns]
```
