# Minto Document Rules

Verification priority:
1. Structural completeness - AMINTON tree integrity
2. Logic soundness - MECE, no orphans, closing discipline
3. Evidence traceability - every claim backed by source

## Rule Index

Draft Structure (DS)
- MINTO-DS-01: Exactly 3 candidate arguments present
- MINTO-DS-02: One candidate marked `[RECOMMENDED]` (highest composite score)
- MINTO-DS-03: Selection criteria documented with weights and rationale
- MINTO-DS-04: Findings inventory present with source references and verification labels
- MINTO-DS-05: Source material list present and non-empty
- MINTO-DS-06: Draft follows `MINTO-DRAFT_TEMPLATE.md` structure

Argument Quality (AQ)
- MINTO-AQ-01: Each A connects to a listener motivator (Magnet Rule)
- MINTO-AQ-02: Questions follow a stated logical ordering (comparative, chronological, structural, or deductive)
- MINTO-AQ-03: One-Argument Test documented per candidate
- MINTO-AQ-04: Each answer is a single declarative sentence
- MINTO-AQ-05: Each answer captures significance, not category (Summarize Don't Label)
- MINTO-AQ-06: All items in a grouping are the same kind (Same Kind, Same Level)

Tree Integrity (TI)
- MINTO-TI-01: Every QnAn has at least one sub-question (S-node)
- MINTO-TI-02: Every sub-question has at least one evidence item (E-node)
- MINTO-TI-03: No orphan nodes (every Q has A, every A has S, every S has E)
- MINTO-TI-04: Every E-node references a source finding from the inventory
- MINTO-TI-05: 3-5 questions, max 3 answers per question, max 3 evidence per sub-question

MECE (ME)
- MINTO-ME-01: Questions under same A do not overlap
- MINTO-ME-02: Answers under same Q do not overlap
- MINTO-ME-03: Evidence items under same S do not overlap

Article Structure (AS)
- MINTO-AS-01: Doc ID assigned in format `[TOPIC]-MINTO-[NN]`
- MINTO-AS-02: Executive Summary uses SCQA and restates A (2-3 paragraphs max)
- MINTO-AS-03: One section per Q with heading derived from question text
- MINTO-AS-04: AMINTON tree appendix present and matches prose structure
- MINTO-AS-05: Prose follows top-down order (conclusion, arguments, evidence)
- MINTO-AS-06: Section headings state ideas, not categories (reading headings alone tells the story)
- MINTO-AS-07: Executive Summary uses SCQA structure (Situation → Complication → Answer)
- MINTO-AS-08: Article follows `MINTO_TEMPLATE.md` structure

Closing (CL)
- MINTO-CL-01: Closing section present with summary lines grouped by parent Q
- MINTO-CL-02: One summary line per answer
- MINTO-CL-03: Final line restates A as conclusion
- MINTO-CL-04: Closing introduces no claims absent from the tree

## MINTO-DS-01: Exactly 3 Candidates

Draft must contain exactly 3 candidate arguments, each with a complete AMINTON Root Section.

**BAD:**
```markdown
## Candidate 1 [RECOMMENDED]
### A: Our tool is better.

## Candidate 2
### A: Speed matters.
```

**GOOD:**
```markdown
## Candidate 1 [RECOMMENDED]
Score: goal_alignment=5, supportability=5, impact=5, specificity=5 (composite: 5.00)
One-Argument Test: passed
### A: Migrating to cloud now saves 40% over upgrading the existing system.
[Full AMINTON Root Section with Q1-Q3 and answers]

## Candidate 2
[Same structure]

## Candidate 3
[Same structure]
```

## MINTO-AQ-01: Magnet Rule

Every root argument must connect to a listener motivator. State the magnet explicitly.

**BAD:**
```markdown
### A: Our platform has good features.
```

**GOOD:**
```markdown
### A: Migrating to cloud now saves 40% over upgrading the existing system.
**Magnet**: Saving a resource currently wasted (infrastructure budget on declining hardware)
```

## MINTO-AQ-02: Question Ordering Must Be Logical

Questions must follow one of Minto's four orderings - there must be a stated reason why Q2 comes after Q1. Arbitrary sequence = rule violation.

Valid orderings:
- **Comparative** (most important first): Why > How > What (Sinek heuristic for persuasion)
- **Chronological** (cause-effect): What happened? > What caused it? > What should we do?
- **Structural** (parts of a whole): one Q per division, unit, or component
- **Deductive** (premise chain): rarely used at Q-level; reserved for paragraph-level

**BAD** (no discernible ordering logic):
```markdown
Q1: What features does it have?
Q2: Why does this matter?
Q3: How does it work?
```
(What-first with no stated reason; appears random)

**GOOD** (comparative - impact-first):
```markdown
Q1 (Why): Why does cloud migration save more than hardware upgrade?
Q2 (How): How do we migrate without downtime?
Q3 (What): What does the target architecture look like?
```

**GOOD** (chronological - causal chain):
```markdown
Q1: What went wrong with the IT system?
Q2: How did costs escalate undetected?
Q3: Why is recovery impossible?
```

**GOOD** (single-question - simplest structure):
```markdown
Q1: Why should we replace the current system?
  Q1A1: Upgrading costs more than replacing.
  Q1A2: The current system cannot handle projected load.
  Q1A3: Vendor support ends in 6 months.
```

## MINTO-TI-03: No Orphan Nodes

Every branch must terminate at evidence level. No intermediate nodes left without children.

**BAD:**
```markdown
Q1A1: Upgrading costs more than replacing.
  (no sub-question or evidence)
```

**GOOD:**
```markdown
Q1A1: Upgrading costs more than replacing.
  └ Q1A1-S1: "What makes upgrading more expensive?"
    ├ Q1A1-S1E1: Legacy vendor charges 3x market rate for equivalent capacity (F03)
    └ Q1A1-S1E2: Upgrade requires 6 months of parallel operation doubling infra costs (F07)
```

## MINTO-TI-04: Evidence References Source

Every E-node must reference a finding from the inventory by ID.

**BAD:**
```markdown
Q1A1-S1E1: The vendor is expensive.
```

**GOOD:**
```markdown
Q1A1-S1E1: Legacy vendor charges 3x market rate for equivalent capacity (F03)
```

## MINTO-ME-01: Questions MECE

Questions under the same argument must not overlap in scope.

**BAD:**
```markdown
Q1: Why is cost reduction important?
Q2: Why does saving money matter?
```
(Cost reduction and saving money overlap - same concern phrased differently)

**GOOD:**
```markdown
Q1: Why does cloud migration save more than upgrading?
Q2: How do we migrate without service disruption?
Q3: What does the target architecture look like?
```

## MINTO-CL-04: No New Claims in Closing

Closing summarizes proved branches only. Every statement in closing must trace back to a tree node.

**BAD:**
```markdown
## Conclusion
The market is also growing at 46% CAGR, making this an excellent investment.
```
(Market growth claim not present in the AMINTON tree)

**GOOD:**
```markdown
## Conclusion
Upgrading costs more than replacing. The current system cannot handle projected load. Vendor support ends in 6 months.
Migrating to cloud now saves 40% over upgrading the existing system.
```
(Every claim present in tree branches)

## MINTO-AQ-05: Summarize Don't Label

Every answer node must capture the *significance* of what it proves, not merely label a topic. Minto's Rule 1: summaries tell the reader something they could not infer from just seeing the list.

**BAD** (labels - intellectually blank):
```markdown
Q1A1: Cost considerations.
Q1A2: Capacity factors.
Q1A3: Support implications.
```

**GOOD** (summaries - capture significance):
```markdown
Q1A1: Upgrading costs more than replacing because the legacy vendor charges 3x market rate.
Q1A2: The current system hits capacity ceiling at 10K concurrent users - projected load is 25K.
Q1A3: Vendor support ends in 6 months, leaving critical vulnerabilities unpatched.
```

**The test**: Does the answer communicate its point without reading the evidence below? If it merely points at a topic, it fails.

## MINTO-AS-06: Headings State Ideas Not Categories

Section headings must reflect the point being made, not the type of content. Reading only headings should produce a precis of the article.

**BAD** (category labels - no scanning value):
```markdown
## Background
## Analysis
## Findings
## Recommendations
```

**GOOD** (idea-bearing headings):
```markdown
## Upgrading costs more than replacing because the legacy vendor charges 3x market rate
## The current system cannot handle projected load growth
## Vendor support ends in 6 months leaving critical vulnerabilities unpatched
```

**Verification procedure:**
1. Extract all section headings from the article
2. Read them in sequence without body text
3. If they tell a coherent story → pass
4. If they read like a table of contents of categories → fail

## MINTO-AS-07: Executive Summary Uses SCQA

The Executive Summary must ground the reader before stating the governing thought. Structure: Situation (what reader already knows) → Complication (what changed or threatens) → Answer (restate A). Total: 2-3 paragraphs max.

**BAD:**
```markdown
## Executive Summary
Migrating to cloud now saves 40% over upgrading the existing system.
```
(Bare assertion. Reader has no context for why this matters now.)

**GOOD:**
```markdown
## Executive Summary
Your infrastructure contract renews in Q1, locking in rates for 3 years. Since the original contract, cloud costs dropped 60% while your vendor raised rates to 3x market price. Migrating to cloud now saves 40% over upgrading the existing system.
```
(Situation → Complication → Answer. Reader feels the urgency before receiving the recommendation.)

## MINTO-AQ-06: Same Kind, Same Level

Every item in a grouping must be the same kind of thing. All answers under the same Q must be describable by a single plural noun (reasons, steps, problems, recommendations). Do not mix actions with observations, metrics with anecdotes, or abstraction levels.

**BAD** (mixed kinds):
```markdown
Q1A1: Migrate the database to cloud. (action)
Q1A2: The current system is slow. (observation)
Q1A3: 99.9% uptime target. (metric)
```
(Cannot label with one plural noun. Actions + observations + metrics mixed.)

**GOOD** (same kind - all reasons):
```markdown
Q1A1: Upgrading costs more than replacing.
Q1A2: The current system cannot handle projected load.
Q1A3: Vendor support ends in 6 months.
```
(All describable as "reasons to migrate.")

**The test**: Can you label all items with one plural noun? If not, restructure the grouping.

## MINTO-AS-04: Appendix Matches Prose

The AMINTON tree appendix must structurally match the prose article. Every section heading corresponds to a Q-node. Every paragraph's key claim corresponds to a QnAn-node.

**Verification procedure:**
1. Count prose sections (excluding Executive Summary and Conclusion) = number of Q-nodes
2. Count bold claims per section = number of answers per Q
3. Verify appendix tree has the same Q/A/S/E structure as prose implies
