# [SUBJECT] - Summary

**Doc ID**: [TOPIC]-IN01
<!-- Topic IDs: 7-14 uppercase chars. Inside T##/S## folders use nested: [TOPIC]-[SUBTOPIC]-IN01 -->
**Goal**: Cross-document synthesis and master index for [SUBJECT] research
**Version scope**: [VERSION or Documentation date YYYY-MM-DD]
**Research stats**: [pending - added in final phase]

**Depends on:**
- `_INFO_[TOPIC]-02_Sources.md [[TOPIC]-IN02]` for source references

## Goals

<!-- Conditional: insert when research request defines explicit goals, success criteria, or deliverables. Skip when Goal field in header block is sufficient. Per INFO_GUIDE.md Section 3.1 -->

- [Goal 1] → [ACHIEVED] / [PARTIAL] / [NOT ACHIEVED]
- [Goal 2] → [outcome label]

## Questions

<!-- Conditional: insert when research request poses specific questions, or research triggered by uncertainty. At least one of Goals or Questions is required. Per INFO_GUIDE.md Section 3.2 -->

Q1: [Question from user prompt]
A1: [1-3 sentence answer] [LABEL]

Q2: [Question]
A2: [Answer] [LABEL]

## Summary

[5-15 sentences of cross-document synthesis. Not a compressed table of contents but a standalone overview answering "what did we learn?" Include: purpose, key findings with confidence labels, main patterns, important limitations, actionable recommendations. Scale with complexity.]

<!-- Sections below are numbered and navigable via TOC. Sections above (Goals, Questions, Summary) are executive-level and visible without navigation. -->

## Table of Contents

1. [Topic Files](#1-topic-files)
2. [Reading Guide](#2-reading-guide)
3. [Conclusions](#3-conclusions)
4. [Emergent Hypotheses](#4-emergent-hypotheses)
5. [Topic Count](#5-topic-count)
6. [Per-Topic Summaries](#6-per-topic-summaries)
7. [Problem → Solution Lookup](#7-problem--solution-lookup)
8. [Recommendations](#8-recommendations)
9. [Risk Assessment](#9-risk-assessment)
10. [Limitations](#10-limitations)
11. [Contradictions and Tensions](#11-contradictions-and-tensions)
12. [Cross-Research References](#12-cross-research-references)
13. [Entity Index](#13-entity-index)
14. [Open Questions and Research Gaps](#14-open-questions-and-research-gaps)
15. [Document History](#15-document-history)

## 1. Topic Files

### [Category 1] (X files)

- [`_INFO_[TOPIC]-03_[Name1].md`](./_INFO_[TOPIC]-03_[Name1].md) [[TOPIC]-IN03]
  - Brief description of contents
- [`_INFO_[TOPIC]-04_[Name2].md`](./_INFO_[TOPIC]-04_[Name2].md) [[TOPIC]-IN04]
  - Brief description of contents

### [Category 2] (X files)

- [`_INFO_[TOPIC]-05_[Name3].md`](./_INFO_[TOPIC]-05_[Name3].md) [[TOPIC]-IN05]
  - Brief description of contents

### [Category N] (X files)

- [`_INFO_[TOPIC]-[NN]_[Name].md`](./_INFO_[TOPIC]-[NN]_[Name].md) [[TOPIC]-IN[NN]]
  - Brief description of contents

## 2. Reading Guide

<!-- Conditional: insert when 3+ distinct audience types benefit from different reading orders. Per RESEARCH_SUMMARY_RULES.md SD-ES-06 -->

- [Role 1]: Summary → IN-XX ([topic]) → IN-YY ([topic]) → Conclusions
- [Role 2]: IN-XX ([topic]) → IN-YY ([topic]) → Limitations

## 3. Conclusions

<!-- Conditional: insert when research produces actionable conclusions derived from cross-topic analysis. Reference supporting topics by IN-number. Per INFO_GUIDE.md Section 3.3 -->

1. [Conclusion derived from findings] (IN-XX, IN-YY)
2. [Conclusion] (IN-XX)

## 4. Emergent Hypotheses

<!-- Conditional: insert when research reveals patterns or theories emerging from combined evidence, not directly stated by any single source. All items [ASSUMED]. Per INFO_GUIDE.md Section 3.4 -->

1. **[Hypothesis name]**: [Description with supporting evidence and validation approach]. [ASSUMED]

## 5. Topic Count

- **Total Topics**: XX
- **[Category 1]**: X
- **[Category 2]**: X
- **[Category N]**: X

## 6. Per-Topic Summaries

[For each topic file: summary (3-20 sentences, scale with complexity) + key findings. Goal: reader understands overall summary and conclusions without opening the file.]

### IN03: [Name1]

[3-20 sentence summary derived from the topic file's content. Cover scope, main findings, and significance to the overall research.]

**Key Findings:**
- [Finding 1] [LABEL]
- [Finding 2] [LABEL]
- [Finding 3] [LABEL]

### IN04: [Name2]

[3-20 sentence summary]

**Key Findings:**
- [Finding 1] [LABEL]
- [Finding 2] [LABEL]

## 7. Problem → Solution Lookup

<!-- Conditional: insert when research evaluates multiple options (libraries, vendors, tools, strategies) for distinct problems or needs. Format: problem statement → recommended solution + alternatives. Adapt heading to domain: "Problem → Solution Lookup", "Requirement → Library", "Need → Vendor". Per RESEARCH_SUMMARY_RULES.md SD-ES-07 -->

### [Category 1]

- **[Problem/need statement]** → [Recommended solution] (IN-XX). Alt: [alternative] (IN-YY) if [condition]
- **[Problem/need statement]** → [Recommended solution] (IN-XX)

## 8. Recommendations

<!-- Conditional: insert when research produces actionable advice beyond analytical conclusions. Group by use case, audience, or scenario. Distinct from Conclusions (what we learned) - Recommendations say what to do. Per RESEARCH_SUMMARY_RULES.md SD-ES-08 -->

### [Use Case / Audience 1]

- [Actionable recommendation with rationale] (IN-XX, IN-YY)
- [Recommendation] (IN-XX)

### [Use Case / Audience 2]

- [Recommendation] (IN-XX)

## 9. Risk Assessment

<!-- Conditional: insert when evaluated options carry categorized risks (legal, technical, operational, financial). Adapt categories to domain: license risks, vendor lock-in, regulatory exposure, technical debt. Per RESEARCH_SUMMARY_RULES.md SD-ES-09 -->

### [Risk Category 1]

- [Option/entity]: [Risk description] → [Mitigation or decision] (IN-XX)

### [Risk Category 2]

- [Option/entity]: [Risk description] → [Mitigation or decision] (IN-XX)

## 10. Limitations

[Known limitations, data quality caveats, scope boundaries, source freshness notes]

## 11. Contradictions and Tensions

<!-- Conditional: insert when research findings pull in opposite directions or reveal paradoxes. State both sides with IN-references. Per RESEARCH_SUMMARY_RULES.md SD-ES-03 -->

1. [Tension name]: [Side A with data] vs [Side B with data] (IN-XX vs IN-YY)
2. [Tension name]: [Description of paradox] (IN-XX)

## 12. Cross-Research References

<!-- Conditional: insert when entity appears in 2+ sibling research sets within the same parent folder. List entity, both research folders, and finding delta. Per RESEARCH_SUMMARY_RULES.md SD-ES-01 -->

- [Entity]: [Finding in this research] (IN-XX) + [Finding in other research] (OTHER_TOPIC, IN-YY). Delta: [what differs].

## 13. Entity Index

<!-- Conditional: insert when 5+ named entities with classifications appear across topic files. Adapt classification scheme to domain: COMPETE/PARTNER/MONITOR for market research, license type for software, risk level for compliance. Per RESEARCH_SUMMARY_RULES.md SD-ES-02 -->

- [Entity] ([classification]) - [key attributes relevant to domain] -> IN-XX

## 14. Open Questions and Research Gaps

<!-- Conditional: insert when topic files contain unanswered questions or "Extend This Segment" prompts. Aggregate and deduplicate. Per RESEARCH_SUMMARY_RULES.md SD-ES-04 -->

- [Unanswered question]? (IN-XX)
- [Research extension prompt] (IN-YY)

<!-- Content depth improvements (SD-CD-*) - apply to existing sections above:
- SD-CD-01: Per-Topic Summaries -> 5-15 sentences + Key Findings with [LABEL]s + top 3-5 quantitative facts
- SD-CD-02: Source URL Inlining -> append `| domain` on first source ID reference. Resolve from Sources file.
- SD-CD-03: Entity Profiles -> inline 1-line profiles for COMPETE/PARTNER/MONITOR entities
- SD-CD-04: Evidence Chains -> preserve linked quantitative facts (min 3 links, not just endpoints)
- SD-CD-05: Scoring Tables -> surface methodology + top 5 results from topic files
- SD-CD-06: Key Quotes -> 3-5 impactful direct source quotes with attribution
See RESEARCH_SUMMARY_RULES.md for full rules and BAD/GOOD examples.
-->

## 15. Document History

**[YYYY-MM-DD HH:MM]**
- Initial Summary created with XX topics

<!-- Template Instructions (delete when using):
1. Replace all [PLACEHOLDERS] with actual values
2. [TOPIC] = 7-14 char uppercase identifier (e.g., OAIAPIS, MSGRAPH, AUTHSYST)
3. [SUBJECT] = Full name (e.g., "OpenAI API", "Microsoft Graph API")
4. File numbering: 01=Summary, 02=Sources, 03+=topic files
5. Goals and/or Questions: at least one required. Derive from prompt decomposition (Q1).
6. Questions use `Q1:`/`A1:` format (question on one line, answer on next, blank line between pairs)
7. Conclusions: derived from cross-topic analysis, reference IN-numbers
8. Emergent Hypotheses: patterns from combined evidence, all [ASSUMED]
9. Per-Topic Summaries: 3-20 sentences + Key Findings per topic (scale with complexity)
10. Research stats added in final phase from STRUT
11. NO Progress Tracking - that goes in STRUT/TASKS
12. Summary must be cross-document synthesis, not a table of contents
13. Limitations: data quality, scope boundaries, source freshness
14. Sections 2, 3-4, 7-14 are conditional: keep when condition is met, delete entire section + TOC entry when not.
15. Adapt conditional section headings to domain (e.g., "Problem → Solution" → "Requirement → Library")
16. Content depth improvements (SD-CD-*): see HTML comment before Document History.
    Apply during finalization or `/improve`. See RESEARCH_SUMMARY_RULES.md for BAD/GOOD examples.
-->
