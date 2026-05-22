# SOCAS Evaluation Rules

Rules for applying Signs of Confusion and Sloppiness (SOCAS) criteria during quality evaluation.

Use during `/verify`, `/critique`, `/improve`, and `/research` workflows.

## Rule Index

Criteria (CR)
- SOCAS-01: Inconsistencies
- SOCAS-02: Ambiguous Naming and Wording
- SOCAS-03: Overlapping Concerns
- SOCAS-04: Undisclosed Contact Information
- SOCAS-05: Ineffective Communication
- SOCAS-06: Incomplete Specifications
- SOCAS-07: Confusing Elements
- SOCAS-08: Information vs Noise Imbalance
- SOCAS-09: Lack of Structure
- SOCAS-10: Gaps in Reasoning
- SOCAS-11: Unnecessary Complexity
- SOCAS-12: Presentation Sloppiness
- SOCAS-13: Empty Structure
- SOCAS-14: Arbitrary Sequencing
- SOCAS-15: Net-Negative Adoption

Application (AP)
- SOCAS-AP-01: Cite criterion ID with quoted evidence
- SOCAS-AP-02: 3+ criteria violated triggers rework recommendation
- SOCAS-AP-03: Apply context-appropriate subset
- SOCAS-AP-04: UX-specific criteria for interface review

Reporting (RP)
- SOCAS-RP-01: Finding format - ID, evidence, severity
- SOCAS-RP-02: Summary format - criteria count and verdict

## Table of Contents

- [The 15 Criteria](#the-15-criteria)
- [Application Rules](#application-rules)
- [Context-Appropriate Subsets](#context-appropriate-subsets)
- [UX-Specific Criteria](#ux-specific-criteria)
- [Reporting Format](#reporting-format)

## The 15 Criteria

### SOCAS-01: Inconsistencies

Any type of inconsistency signals confusion:
- Same concept named multiple ways
- Same word used for different things
- Contradicting statements within same document
- Format/style inconsistencies without reason

### SOCAS-02: Ambiguous Naming and Wording

Lack of clear naming scheme:
- Undefined or hand-wavy concepts
- Key nouns without clear definition or boundaries
- Names that could mean multiple things
- Missing glossary for domain terms

### SOCAS-03: Overlapping Concerns

Redundancy with deviation indicates poor design:
- Two components doing the same job differently
- Concept overlap without clear boundaries
- Responsibilities split inconsistently
- Duplicate mechanisms with slight variations
- Items in same grouping at wildly different levels of detail ("Revenue trends" next to "Johnson account")

### SOCAS-04: Undisclosed Contact Information

Organizational red flag:
- Generic email addresses only (info@, contact@)
- No named contacts for specific concerns
- Hidden or hard-to-find contact details
- No escalation path documented

### SOCAS-05: Ineffective Communication

Forces unnecessary communication loops:
- Information scattered across multiple documents
- Critical details buried in noise
- Missing context requiring follow-up questions
- No clear owner or decision maker identified

### SOCAS-06: Incomplete Specifications

Mixing suggestions with requirements:
- No clear distinction between MUST, SHOULD, MAY
- Underspecified behavior for edge cases
- Implicit assumptions left unstated
- Conclusions not supported by evidence

### SOCAS-07: Confusing Elements

Funny but confusing additions:
- Jokes or humor that obscures meaning
- Creative naming that sacrifices clarity
- Excessive metaphors or analogies
- Easter eggs in serious documentation

### SOCAS-08: Information vs Noise Imbalance

Poor signal-to-noise ratio:
- Relevant details buried in irrelevant additions
- Verbose explanations of obvious things
- Missing explanations of complex things
- Filler content without substance

### SOCAS-09: Lack of Structure

Unstructured writing:
- No clear headings or sections
- Missing enumerations for lists
- No identifiers for referenceable content
- Wall-of-text formatting
- No table of contents for long documents

### SOCAS-10: Gaps in Reasoning

Logical inconsistencies:
- Conclusions not supported by evidence
- Missing steps in explanations
- Assumptions presented as facts
- No explicit tradeoffs or alternatives discussed
- Selection not justified ("Three problems..." - why these three and no others?)

### SOCAS-11: Unnecessary Complexity

Abstractions that don't earn their cost:
- Over-engineered solutions for simple problems
- Jargon where plain language works
- Deep nesting without clear benefit
- Indirection without purpose

### SOCAS-12: Presentation Sloppiness

Surface-level quality issues:
- Typos and grammatical errors
- Stale or broken references
- Inconsistent formatting
- Outdated information mixed with current
- Outdated, abandoned, or unsupported code (stale repos, unresolved issues, no recent commits)

### SOCAS-13: Empty Structure

Structure present but hollow - author organized without synthesizing:
- Headings label categories instead of stating ideas ("Background", "Analysis", "Results")
- Main point buried at end or absent entirely
- Section summaries describe what the section covers, not what was found
- No stated purpose - reader cannot tell why the document exists

### SOCAS-14: Arbitrary Sequencing

Items dumped without analyzing relationships:
- Items in lists appear in no discernible order
- No logical, chronological, structural, or importance-based sequence
- Reader cannot determine why item 2 follows item 1

### SOCAS-15: Net-Negative Adoption

Solution introduces more problems than it solves - detectable through community research:
- GitHub issues dominated by workarounds for the tool's own limitations
- Community forums show recurring migration-away discussions
- Known problems acknowledged by maintainers but unresolved across major versions
- Adopters report increased complexity, debugging time, or breaking changes disproportionate to value gained

## Application Rules

### SOCAS-AP-01: Cite Criterion ID with Quoted Evidence

Every finding must reference the criterion ID and quote the specific evidence.

**BAD:**
```
The document has naming issues and some inconsistencies.
```

**GOOD:**
```
SOCAS-01: "retry mechanism" in section 2, "reconnection logic" in section 4 - same concept, different names
SOCAS-02: "handler" used without definition - could mean error handler, event handler, or request handler
```

### SOCAS-AP-02: Rework Threshold

3+ criteria violated in one artifact = recommend rework. Below 3 = flag findings, no rework recommendation.

**BAD:**
```
Found 1 minor inconsistency. Recommend complete rework of the specification.
```

**GOOD:**
```
SOCAS violations: 5 of 15 (SOCAS-01, SOCAS-03, SOCAS-06, SOCAS-09, SOCAS-10)
Verdict: REWORK - exceeds 3-criterion threshold
```

### SOCAS-AP-03: Context-Appropriate Subsets

Not all 15 criteria apply to every context. Apply only the relevant subset.

**BAD:** Flagging SOCAS-04 (Undisclosed Contact Information) on a code module.

**GOOD:** See [Context-Appropriate Subsets](#context-appropriate-subsets) for which criteria apply where.

## Context-Appropriate Subsets

### Agent Output Review (`/verify`, `/critique`, `/improve`)

Apply when reviewing agent-generated specs, research, code, plans:
- SOCAS-01 (Inconsistencies)
- SOCAS-02 (Ambiguous Naming)
- SOCAS-03 (Overlapping Concerns)
- SOCAS-06 (Incomplete Specifications)
- SOCAS-08 (Noise Imbalance)
- SOCAS-09 (Lack of Structure)
- SOCAS-10 (Gaps in Reasoning)
- SOCAS-11 (Unnecessary Complexity)
- SOCAS-12 (Presentation Sloppiness)
- SOCAS-13 (Empty Structure)
- SOCAS-14 (Arbitrary Sequencing)

### Document Review

Apply when reviewing human-authored technical specifications, API docs, process descriptions, requirements:
- All 14 criteria applicable

### Source Evaluation (`/research`)

Apply when ranking external sources for reliability:
- SOCAS-01 (Inconsistencies)
- SOCAS-02 (Ambiguous Naming)
- SOCAS-04 (Undisclosed Contact Information)
- SOCAS-05 (Ineffective Communication)
- SOCAS-06 (Incomplete Specifications)
- SOCAS-08 (Noise Imbalance)
- SOCAS-09 (Lack of Structure)
- SOCAS-10 (Gaps in Reasoning)
- SOCAS-12 (Presentation Sloppiness)
- SOCAS-13 (Empty Structure)
- SOCAS-15 (Net-Negative Adoption)

High SOCAS count = unreliable source. Prefer sources with low SOCAS indicators. Document findings in source notes.

Also evaluate community and repo health signals:
- High ratio of open issues with no maintainer response
- Recurring community complaints about same problems
- Archived/abandoned repos still referenced as active
- Declared end-of-life or deprecated with no successor

### Organizational Assessment

Evaluate organizations by their public outputs (website, docs, communications):
- All 14 criteria applicable

## UX-Specific Criteria

### SOCAS-AP-04: UX Design Review

Apply these additional indicators when evaluating user interfaces. Each maps to a parent SOCAS criterion.

- Breaking established patterns without substantial gain (SOCAS-01)
- Broken proximity of related UX elements (SOCAS-03)
- No tab order and keyboard support for users without mouse (SOCAS-06)
- No copy functionality for relevant textual information (SOCAS-06)
- Unclear visual hierarchy (SOCAS-09)
- Unestablished commands for standard operations - instead of OK, Cancel, Save, Load (SOCAS-02)
- Application deletes or loses data without user confirmation (SOCAS-06)
- Users can accidentally close dialogs with entered data by clicking outside (SOCAS-06)

## Reporting Format

### SOCAS-RP-01: Finding Format

Each finding: criterion ID, quoted evidence, severity (LOW, MEDIUM, HIGH).

**BAD:**
```
- The document is inconsistent
- Naming could be better
- Some parts are unclear
```

**GOOD:**
```
- SOCAS-01 HIGH: "fetch handler" (line 12) vs "request processor" (line 45) - same component, different names
- SOCAS-06 MEDIUM: Edge case unspecified - what happens when input list is empty?
- SOCAS-10 LOW: "Best approach selected" - no alternatives discussed, no selection criteria stated
```

### SOCAS-RP-02: Summary Format

After findings, provide summary with violation count and verdict.

**BAD:**
```
Overall the document has some issues that should be addressed.
```

**GOOD:**
```
SOCAS: 4/15 violated (SOCAS-01 HIGH, SOCAS-06 MEDIUM, SOCAS-10 LOW, SOCAS-12 LOW)
Verdict: REWORK - exceeds 3-criterion threshold
```

Verdict values:
- `PASS` - 0 criteria violated
- `ACCEPTABLE` - 1-2 criteria violated (flag findings, no rework)
- `REWORK` - 3+ criteria violated
