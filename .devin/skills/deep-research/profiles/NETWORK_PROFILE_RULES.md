# Network Profile Rules

Rules for writing and verifying network profile INFO documents with GOOD/BAD examples.

**Inherits**: All INFO-* rules from @write-documents `INFO_RULES.md` apply in addition to NP-* rules below. Profiles are specialized INFO documents.

## Rule Index

Quality (QA) - cross-cutting, applies to ALL sections
- NP-QA-01: Every factual claim backed by source or labeled `[ASSUMED]`
- NP-QA-02: Specific over vague - quantify, name, date instead of generalizing
- NP-QA-03: Same entity = same name throughout (no synonyms, no abbreviation drift)
- NP-QA-04: One fact per bullet - no compound statements hiding multiple claims

Header (HD)
- NP-HD-01: All sections filled (standalone profiles are always FULL)
- NP-HD-02: Network type and formality level clearly identified
- NP-HD-03: Related profiles link to member personal profiles

Summary (SM)
- NP-SM-01: 3-5 sentences covering type, size, scope, themes, vitality
- NP-SM-02: Lifecycle stage supported by evidence

Identity (ID)
- NP-ID-01: Formality level distinguishes formal/semi-formal/informal with criteria
- NP-ID-02: Lifecycle stage matches observable indicators

Focus (FC)
- NP-FC-01: Open Value Analysis based on public claims with source citations
- NP-FC-02: Hidden Value Analysis labeled with assessment confidence (HIGH/MEDIUM/LOW)
- NP-FC-03: Evidence for hidden analysis comes from observable patterns, not speculation

Inner Circle (IC)
- NP-IC-01: Core members limited to 5-15 people with disproportionate influence
- NP-IC-02: Each member entry has day job, network role, and influence mechanism
- NP-IC-03: Succession risk assessed for central nodes

Structure (ST)
- NP-ST-01: Topology described using standard types (hub-spoke, distributed, hierarchical, clustered, chain)
- NP-ST-02: Sub-clusters have binding topic, members, and bridge persons identified
- NP-ST-03: Communication channels include frequency and rhythm

Events (EV)
- NP-EV-01: Each event includes date/frequency, format, attendance scale, and entry mechanism
- NP-EV-02: Networking value rated (who attends, what access it provides)

Entry (EN)
- NP-EN-01: Explicit and implicit barriers separated
- NP-EN-02: Recommended entry path specific to requester's position
- NP-EN-03: Entry cost quantified (financial, time, social capital)

Member Analysis (MA)
- NP-MA-01: Full format for inner circle, 1-line format for peripherals
- NP-MA-02: Contribution/extraction balance assessed per member
- NP-MA-03: Influence score relative within network (HIGH/MEDIUM/LOW)

Value Flow (VF)
- NP-VF-01: Tangible and intangible outputs separated
- NP-VF-02: Value distribution identifies asymmetries (who benefits vs contributes most)
- NP-VF-03: Free riders identified with evidence

Strategic (SA)
- NP-SA-01: Entry feasibility realistic (not aspirational)
- NP-SA-02: Alternative networks named when access is difficult
- NP-SA-03: Risks of engagement explicitly stated

Research Gaps (RG)
- NP-RG-01: Each gap states what is missing AND why it matters
- NP-RG-02: Suggested next steps are actionable (specific source or action to check)

Sensitivity (SN)
- NP-SN-01: Hidden dynamics labeled `[ASSUMED]` with confidence level
- NP-SN-02: Power dynamics described without judgmental language
- NP-SN-03: Exclusion patterns stated as observation, not accusation

Sources (SC)
- NP-SC-01: All sources include access date
- NP-SC-02: Hidden analysis sources clearly distinguished from open analysis sources

## Header Rules

### NP-HD-01: Section Completeness

Standalone profiles are always FULL. All sections must be filled. Full Member Analysis for inner circle, 1-line format for peripherals. When no data found, document in Research Gaps section instead of leaving empty sections.

**BAD:**
```
## Value Flow Analysis
[empty - no data found]
## Network Structure
### Sub-Clusters
[empty]
```

**GOOD:**
```
## Value Flow Analysis
- Insufficient data to map value flows. Network interactions not publicly observable beyond event attendance.

## Research Gaps
- Value flow: No public deal announcements or collaboration outputs traceable to network
- Sub-clusters: Member interactions not observable from public sources alone
```

## Focus Rules

### NP-FC-01: Open Value Analysis Sourced

Claims about the network's stated purpose need citations.

**BAD:**
```
### Stated Focus (Open Value Analysis)
- **Official mission**: They want to promote innovation
- **Stated goals**: Be innovative and collaborative
```

**GOOD:**
```
### Stated Focus (Open Value Analysis)
- **Official mission**: "[Actual mission statement quote]" (website header, accessed YYYY-MM-DD)
- **Stated goals**: 1) [Goal 1], 2) [Goal 2], 3) [Goal 3] (annual report [year], p.[N])
- **Key claims**:
  - "50+ deals facilitated in 2025" - Evidence: 12 verifiable from press releases, remainder [ASSUMED]
  - "Non-hierarchical peer network" - Evidence: Contradicted by inner circle analysis below
```

### NP-FC-02: Hidden Analysis Confidence

Hidden value analysis requires explicit confidence assessment.

**BAD:**
```
### Hidden Focus (Hidden Value Analysis)
- **Actual binding mechanism**: Money and power
- **Unstated value exchange**: They all get rich together
```

**GOOD:**
```
### Hidden Focus (Hidden Value Analysis)
- **Actual binding mechanism**: Shared exit from [Company X] [year] restructuring. [N] of [M] inner circle members were [level]+ at [Company X] before [year]. Maintained deal-flow relationships post-exit.
- **Unstated value exchange**: Pre-market deal flow (members see opportunities before public announcement). Talent pipeline (junior hires rotate between member companies).
- **Common characteristics of members**: [Gender] ([ratio] inner circle), [age range], [education pattern], [language], minimum EUR [amount] personal net worth [ASSUMED]
- **Exclusion patterns**: [Observed pattern] despite [N] qualified [group] in broader network. No members from [excluded segment] despite stated "[related mission]".

**Assessment confidence**: MEDIUM - based on [N] confirmed data points ([types]) + [N] inferred patterns
```

## Inner Circle Rules

### NP-IC-02: Member Entry Completeness

Each inner circle member needs role, function, and mechanism.

**BAD:**
```
- **[Person A]** (CEO of [Company]). Important member.
- **[Person B]** (Investor). Very connected.
```

**GOOD:**
```
- **[Person A]** (CEO, [Company A]). Network role: Convener. Influence: Hosts quarterly dinners, controls guest list. Only person with direct relationships to all other inner circle members.
- **[Person B]** (Partner, [Company B]). Network role: Gatekeeper. Influence: Controls deal flow access. Their "no" excludes companies from syndicate rounds.
```

### NP-IC-03: Succession Risk

Assess what happens when key nodes depart.

**BAD:**
```
- **Succession risk**: Network would be fine without anyone.
```

**GOOD:**
```
- **Succession risk**: HIGH for [Person A] (sole convener, only full-mesh node). Network likely fragments into [N] sub-clusters without them. LOW for any single peripheral member. MEDIUM for [Person B] (deal flow would redirect to competitor syndicate within 6 months).
```

## Entry Barrier Rules

### NP-EN-01: Explicit vs Implicit Separation

Formal and informal barriers are different things.

**BAD:**
```
- **Entry barriers**: Hard to get in, need connections
```

**GOOD:**
```
- **Explicit requirements**: None formally published. Attendance at quarterly dinner requires personal invitation from inner circle member.
- **Implicit requirements**: EUR 1M+ personal investment capacity (minimum to participate in syndicate rounds). DACH-region financial services background. Male (observed, not stated). Age 40+ (youngest member is 43).
- **Introduction mechanism**: Existing member brings you as +1 to dinner. If accepted, receive direct invitations thereafter. Trial period: ~2 dinners before inclusion in deal flow communications.
```

### NP-EN-02: Requester-Specific Entry Path

Tailor the entry recommendation.

**BAD:**
```
- **Recommended entry path**: Get introduced by someone
```

**GOOD:**
```
- **Recommended entry path**: 1) Warm introduction via [Person A] (2nd-degree via shared [Company X] tenure). 2) Attend [Event Name] (November) where [N] inner circle members are confirmed. 3) Position as [expertise] expert - fills a gap in network's capability set (currently no [skill area] expertise among members).
```

## Member Analysis Rules

### NP-MA-01: Format by Importance

Inner circle gets full analysis. Peripherals get one line.

**BAD:**
```
### [Person A] (CEO)
[full analysis]

### [Peripheral Person] (Unknown)
[full analysis - wastes space for peripheral member]
```

**GOOD:**
```
### [Person A] (CEO, [Company A])
- **Network role**: Convener / Core
- **Joined/Connected since**: [year] (founding member)
- **Contributions to network**: Deal flow origination ([N] opportunities/quarter), event hosting, introductions to institutional LPs
- **Extractions from network**: Co-investment capital for [Company A] portfolio, talent referrals, board member recruitment
- **Influence score**: HIGH
- **Bridge function**: Connects to [external network] via [Person B] relationship

**Peripheral members:**
- **[Person C]** (CFO, [Company C]) - Contributes: Due diligence expertise. Extracts: Deal flow. Bridge: None.
- **[Person D]** (Partner, [Company D]) - Contributes: Legal structuring. Extracts: Client referrals. Bridge: [Adjacent network].
```

## Value Flow Rules

### NP-VF-02: Asymmetry Identification

Who gets more than they give?

**BAD:**
```
- **Who benefits most**: Everyone benefits equally
```

**GOOD:**
```
- **Who benefits most**: [Person A] ([Company A] received EUR [amount] in co-investment from network members in [period], while contributing primarily social capital/hosting). [Person B] (uses network for proprietary deal sourcing, estimated [N]% of fund pipeline originates here).
- **Who contributes most**: [Person C] (provides [N] hours/quarter of pro-bono [expertise] for network deals, extracts only [N] slots/year).
- **Free riders**: [Person D] - attended [N] of [M] events in [year], contributed 0 deals, extracted [N] client mandates. [ASSUMED - based on event attendance and no visible deal contribution]
```

## Strategic Assessment Rules

### NP-SA-01: Realistic Feasibility

Don't overstate access potential.

**BAD:**
```
- **Entry feasibility**: Easy - just attend an event
```

**GOOD:**
```
- **Entry feasibility**: MEDIUM. Path exists via [Person A] (warm 2nd-degree connection). Barrier: Current [resource] below network norm (EUR [amount]+). Mitigant: [Expertise] fills genuine gap. Timeline: [N] months from first [event type] to [inclusion milestone].
```

### NP-SA-02: Alternatives When Access is Difficult

Name backup options.

**BAD:**
```
- **Alternative networks**: Other networks exist
```

**GOOD:**
```
- **Alternative networks**:
  - [Alternative Network 1] (formal, easier entry via membership application, EUR [amount]/year, less exclusive deal flow)
  - [Alternative Network 2] (open applications quarterly, lower ticket sizes EUR [range], broader [domain] focus)
  - [Alternative Network 3] (messaging group, introduction via any existing member, purely operational/product focus, no investment component)
```
