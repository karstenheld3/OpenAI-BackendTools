# Personal Profile Rules

Rules for writing and verifying personal profile INFO documents with GOOD/BAD examples.

**Inherits**: All INFO-* rules from @write-documents `INFO_RULES.md` apply in addition to PP-* rules below. Profiles are specialized INFO documents.

## Rule Index

Quality (QA) - cross-cutting, applies to ALL sections
- PP-QA-01: Every factual claim backed by source or labeled `[ASSUMED]`
- PP-QA-02: Specific over vague - quantify, name, date instead of generalizing
- PP-QA-03: Same entity = same name throughout (no synonyms, no abbreviation drift)
- PP-QA-04: One fact per bullet - no compound statements hiding multiple claims

Header (HD)
- PP-HD-01: All sections filled (standalone profiles are always FULL)
- PP-HD-02: Related profiles field links to existing profile Doc IDs
- PP-HD-03: Connection to requester states relationship type and evidence

Summary (SM)
- PP-SM-01: 3-5 sentences covering role, location, arc, distinguishing feature, relevance
- PP-SM-02: No claims without source backing in body sections

Personal Data (PD)
- PP-PD-01: Inferred fields marked `[ASSUMED]` with reasoning
- PP-PD-02: Connection count includes date (decays rapidly)

Current Occupation (OC)
- PP-OC-01: Key figures quantified (team size, revenue, portfolio) not described vaguely
- PP-OC-02: Activity timeline contains at least 2 dated milestones

Timeline (TL)
- PP-TL-01: Career timeline reverse chronological, no gaps >2 years without explanation
- PP-TL-02: Dates consistent across Career Timeline, Current Occupation, and Company Factsheets
- PP-TL-03: Education timeline includes institution, degree, field, years

Topics (TP)
- PP-TP-01: Each topic has status and qualifier in heading
- PP-TP-02: Conversation angle ends each topic with a concrete question

Additional Activities (AC)
- PP-AC-01: Each entry dated - no undated items
- PP-AC-02: Omit subsections with no findings (do not leave empty subsections)

Social Media (MA)
- PP-MA-01: Capture date stated in section heading
- PP-MA-02: Pattern summary distinguishes original content from reposts/reactions

Character (CH)
- PP-CH-01: Self-description uses actual quotes from LinkedIn/bio
- PP-CH-02: Career pattern uses arrow notation with spaces
- PP-CH-03: Assessments distinguish observation from inference - label inferences `[ASSUMED]`

Networking (NW)
- PP-NW-01: Engagement Strategy has at least one concrete, actionable recommendation
- PP-NW-02: Touchpoints reference specific events, not vague categories

Research Gaps (RG)
- PP-RG-01: Each gap states what is missing AND why it matters
- PP-RG-02: Suggested next steps are actionable (specific source, person, or event to check)

Sensitivity (SN)
- PP-SN-01: Sensitive topics flagged with `[SENSITIVE: reason. Safe angle: ...]`
- PP-SN-02: No private data beyond what is publicly available

Sources (SC)
- PP-SC-01: All sources include access date
- PP-SC-02: Source recency - flag if all sources older than 12 months

Cross-Reference (XR)
- PP-XR-01: Referenced persons/companies use `(see [TOPIC]-IN[NN])` when profile exists
- PP-XR-02: Company Factsheets kept minimal when company profile exists separately

## Header Rules

### PP-HD-01: Section Completeness

Standalone profiles are always FULL. All sections must be filled. When no data found, document in Research Gaps section instead of leaving empty sections.

**BAD:**
```
## Education Timeline
[empty - no data found]
## Additional Activities
### Publications
[empty]
### Speaking Engagements
[empty]
```

**GOOD:**
```
## Education Timeline
- No public education data found. [ASSUMED - profile may predate LinkedIn education fields]

## Research Gaps
- Education history: No university or degree information found across LinkedIn, company bio, or press mentions
- Publications: No academic or industry publications identified
```

### PP-HD-03: Connection Statement

Connection must state relationship type and basis.

**BAD:**
```
**Connection to [Requester Name]**: Connected on LinkedIn.
```

**GOOD:**
```
**Connection to [Requester Name]**: 2nd-degree via [Person B] (shared tenure at [Company X] 2015-2018). Overlapping interest in [shared domain].
```

## Timeline Rules

### PP-TL-01: Career Timeline Completeness

Reverse chronological. Gaps >2 years require explanation.

**BAD:**
```
## Career Timeline

- **2020-present**: CEO at [Company B], [City]
- **2012-2015**: VP Engineering at [Company A], [City]
```

**GOOD:**
```
## Career Timeline

- **Since 2020**: CEO at [Company B], [City] ([1-line product description])
- **2015-2020**: Sabbatical and angel investing [ASSUMED - no public role found]
- **2012-2015**: VP Engineering at [Company A], [City] (led team of 45)
```

### PP-TL-02: Date Consistency

Dates must match across sections.

**BAD:**
```
## Career Timeline
- **Since 2019**: CEO at [Company]

## Current Occupation
### [Company] (CEO, since 2020)
```

**GOOD:**
```
## Career Timeline
- **Since 2019**: CEO at [Company], [City] ([industry])

## Current Occupation
### [Company] (CEO, since 2019)
```

## Topic Rules

### PP-TP-01: Status and Qualifier

Every topic heading needs status and qualifier.

**BAD:**
```
### Artificial Intelligence
```

**GOOD:**
```
### [Topic Name] (primary, via [Company] product)
```

### PP-TP-02: Conversation Angle

Each topic ends with a specific, askable question.

**BAD:**
```
Conversation angle: "Ask about AI"
```

**GOOD:**
```
Conversation angle: "How did you decide to [specific technical/strategic choice they made]?"
```

## Character Assessment Rules

### PP-CH-01: Self-Description from Source

Use actual quotes, not paraphrases.

**BAD:**
```
- **Self-description**: She describes herself as a technology leader.
```

**GOOD:**
```
- **Self-description**: "[Actual LinkedIn headline or bio quote from the subject's profile]"
```

### PP-CH-02: Career Pattern Arrow Notation

Use `->` arrows with spaces for career arc.

**BAD:**
```
- **Career pattern**: Consulting to product to founder
```

**GOOD:**
```
- **Career pattern**: [Phase 1 descriptor] ([Company A]) -> [Phase 2 descriptor] ([Company B]) -> [Phase 3 descriptor] ([Company C])
```

## Networking Rules

### PP-NW-01: Actionable Engagement

Recommendations must be specific enough to execute.

**BAD:**
```
- **Recommended approach**: Reach out via LinkedIn
```

**GOOD:**
```
- **Recommended approach**: Request introduction via [Person B] (shared [Company X] tenure). Reference the [Event Name] panel on [topic] (YYYY-MM-DD) where they spoke. Opening angle: [specific shared interest].
```

### PP-NW-02: Specific Touchpoints

Reference actual events, publications, or shared connections.

**BAD:**
```
- **Potential touchpoints for reconnection**:
  - Industry events: Attend conferences she goes to
  - Shared interests: Talk about AI
```

**GOOD:**
```
- **Potential touchpoints for reconnection**:
  - [Event Name] (YYYY-MM, [City]): Confirmed speaker on "[talk topic]"
  - [Person B] introduction: Shared [N]-year tenure at [Company X] ([year range])
```

## Sensitivity Rules

### PP-SN-01: Sensitive Topic Flagging

Mark with reason AND safe alternative angle.

**BAD:**
```
- Was terminated from previous role at [Company] in [year].
```

**GOOD:**
```
- Left [Company] in [year] under unclear circumstances. [SENSITIVE: Possible involuntary departure. Safe angle: Ask about the transition to entrepreneurship and what motivated the career change.]
```

## Cross-Reference Rules

### PP-XR-01: Profile Reference Format

When a separate profile exists, reference it. Do not duplicate content.

**BAD:**
```
### [Company]
- **Description**: [Company] is a [City]-based [industry] company founded in [year]...
  [200 words of company description]
```

**GOOD:**
```
### [Company]
- **Description**: [Industry] company, [City] (see [TOPIC]-IN[NN])
- **Person's role**: [Title] and co-founder since [year]
- **Key projects**: [Project 1], [Project 2]
```

## Quality Rules (Cross-Cutting)

### PP-QA-01: Evidence Backing

Every factual claim must cite a source or be labeled `[ASSUMED]`.

**BAD:**
```
- **Domain expertise**: Expert in digital transformation
- **Core thesis**: Believes in AI-first approaches
```

**GOOD:**
```
- **Domain expertise**: Digital transformation strategy (keynote at [Event], [year]; 3 publications on topic)
- **Core thesis**: "AI will replace 80% of routine compliance work within 5 years" (LinkedIn post, [date]) [VERIFIED]
```

### PP-QA-02: Specific Over Vague

Quantify, name, date. Never generalize when specifics are available.

**BAD:**
```
- **Key figures**: Large team, significant revenue
- **Role scope**: Responsible for strategy and operations
```

**GOOD:**
```
- **Key figures**: 45 employees, EUR 8.2M ARR (2024)
- **Role scope**: Leads product strategy for B2B segment (3 product lines, 12 enterprise clients)
```

### PP-QA-03: Naming Consistency

Same entity = same name throughout the document.

**BAD:**
```
## Career Timeline
- **Since 2020**: CEO at TechCorp Solutions GmbH

## Current Occupation
### TCS (CEO, since 2020)
```

**GOOD:**
```
## Career Timeline
- **Since 2020**: CEO at TechCorp Solutions GmbH, [City]

## Current Occupation
### TechCorp Solutions GmbH (CEO, since 2020)
```

### PP-QA-04: One Fact Per Bullet

No compound statements. Each bullet = one verifiable claim.

**BAD:**
```
- **2018-2020**: VP Product at [Company A] where she led the platform rebuild and also served on the board of [Association] and published a book on API design
```

**GOOD:**
```
- **2018-2020**: VP Product at [Company A], [City] (led platform rebuild, team of 30)
```

## Personal Data Rules

### PP-PD-01: Inferred Fields Labeled

Mark inferred data explicitly with reasoning.

**BAD:**
```
- **Nationality**: German
- **Languages**: German, English
```

**GOOD:**
```
- **Nationality**: German [ASSUMED - LinkedIn location and education both in Germany]
- **Languages**: German (native) [ASSUMED], English (professional) [VERIFIED - LinkedIn set to English, English-language posts]
```

## Current Occupation Rules

### PP-OC-01: Quantified Key Figures

Key figures must be numbers, not adjectives.

**BAD:**
```
- **Key figures**: Growing team, strong revenue
```

**GOOD:**
```
- **Key figures**: 120 employees (LinkedIn, [date]), Series B funded (EUR 15M, [year])
```

### PP-OC-02: Activity Timeline Depth

At least 2 dated milestones per active role.

**BAD:**
```
- **Activity timeline**:
  - Founded the company
```

**GOOD:**
```
- **Activity timeline**:
  - 2023-06: Closed Series A (EUR 5M, led by [Investor])
  - 2024-01: Launched product in [market] (press release [date])
  - 2024-09: Expanded to 3 new markets (LinkedIn announcement)
```

## Additional Activities Rules

### PP-AC-01: Dated Entries

Every entry must have a date or date range.

**BAD:**
```
### Board Memberships and Advisory Roles
- Advisory Board, [Industry Association]
- Mentor at [Accelerator]
```

**GOOD:**
```
### Board Memberships and Advisory Roles
- **2021-present**: Advisory Board, [Industry Association] (invited member)
- **2023-present**: Mentor, [Accelerator] (2 cohorts per year)
```

## Social Media Rules

### PP-MA-01: Capture Date Required

Section heading must state when social media was captured.

**BAD:**
```
## Latest Social Media Activity
```

**GOOD:**
```
## Latest Social Media Activity (as of 2025-01-15)
```

### PP-MA-02: Original vs Repost

Pattern summary must distinguish content creation from curation.

**BAD:**
```
**Pattern**: Active on LinkedIn, posts about technology.
```

**GOOD:**
```
**Pattern**: Posts 2-3x/week. ~60% reposts of industry news with brief commentary, ~40% original thought leadership (long-form, English). Topics: AI regulation, enterprise adoption. Engagement: 50-200 reactions on original posts.
```

## Character Assessment Rules

### PP-CH-03: Observation vs Inference

Distinguish what is observed from what is interpreted.

**BAD:**
```
- **Values indicators**: She values innovation and disruption
```

**GOOD:**
```
- **Values indicators**: Left established consulting career for early-stage startup (risk tolerance) [ASSUMED]. Publicly advocates for open-source contributions (3 LinkedIn posts in 2024) [VERIFIED].
```

## Research Gaps Rules

### PP-RG-01: Gap Impact Stated

Each gap explains what is missing AND why it matters for the profile's purpose.

**BAD:**
```
- Education details unknown
- No information about hobbies
```

**GOOD:**
```
- Education history: No university or degree information found. Matters: Cannot assess academic network, alumni connections, or domain training depth.
- Pre-2015 career: No public data before current company. Matters: Career pattern and industry experience unclear.
```

### PP-RG-02: Actionable Next Steps

Suggested steps must name a specific action, not a category.

**BAD:**
```
- **Suggested next steps**: Research more about education. Check social media.
```

**GOOD:**
```
- **Suggested next steps**:
  - Check XING profile (often contains education data not on LinkedIn)
  - Ask [Mutual Connection] about shared tenure at [Company] (2015-2018)
  - Monitor [Event Name] speaker list ([month] [year]) - confirmed attendee
```
