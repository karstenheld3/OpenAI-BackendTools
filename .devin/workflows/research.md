---
description: Structured research with verification labels and source retention
auto_execution_mode: 1
---

# Research Workflow

Structured research about a topic with step-by-step findings and source documentation.

**Goal**: Verified INFO document with labeled findings, sources retained, summary at top

**Why**: Lightweight alternative to `/deep-research` - single-document output, no multi-file set, no STRUT

Scope: Single-topic research producing one `_INFO_*.md`. Use `/deep-research` for multi-topic exhaustive research (MCPI).

## Required Skills

Read before proceeding:
- `[AGENT_FOLDER]/rules/research-and-report-writing-rules.md` for Most Executable Point of Information (MEPI) / Most Complete Point of Information (MCPI) research depth
- @write-documents `INFO_GUIDE.md` and `INFO_RULES.md` for INFO document structure
- @write-documents `APAPALAN_RULES.md` for writing quality

## MUST-NOT-FORGET

- Evaluate sources with Signs of Confusion and Sloppiness (SOCAS) - apply @write-documents `SOCAS_RULES.md` Source Evaluation subset
- Summary section mandatory - copy/paste ready list at document top
- Label ALL findings: `[ASSUMED]`, `[VERIFIED]`, `[TESTED]`, `[PROVEN]`
- MEPI by default (2-3 curated options); MCPI only when completeness explicitly needed
- Deep beats wide - tokens on 2-3 well-researched options over 10+ superficial ones
- Document exclusions - what was NOT considered and why
- Keep ALL sources - even if findings were minimal
- Site exceptions - use Playwright browser (NOT `search_web`/`read_url_content`) for: `gesetze-im-internet.de`

## Output

```
_INFO_[TOPIC]-IN[NN]_[Title].md
├── Summary (copy/paste ready list)
├── Sections (step-by-step findings, labeled)
└── Sources (all URLs, even if minimal findings)
```

## Quality Gate

- [ ] Summary at document top
- [ ] ALL findings labeled (`[ASSUMED]`/`[VERIFIED]`/`[TESTED]`/`[PROVEN]`)
- [ ] ALL sources retained with URLs
- [ ] Exclusions documented
- [ ] No unverified contradictions remaining
- [ ] SOCAS applied to source evaluation

**Source Retention Rule:** ALL sources must be kept. Never discard - even if findings were minimal or contradictory, document what was checked to prevent re-checking.

## GLOBAL-RULES

Apply to ALL branches below (profiles and general topics alike):

1. All INFO-* rules from @write-documents `INFO_RULES.md` apply to every output document (profiles are specialized INFO documents)
2. All APAPALAN rules from @write-documents `APAPALAN_RULES.md` apply to all written content
3. Verification labels (`[ASSUMED]`/`[VERIFIED]`/`[TESTED]`/`[PROVEN]`) required on factual claims
4. Inline source links at first mention per INFO-SC-05

# CONTEXT-SPECIFIC

## Personal Profile

Detect by: research subject is a **person** (name, email address, contact).

1. Read @deep-research `profiles/PERSONAL_PROFILE_TEMPLATE.md` for document structure
2. Read @deep-research `profiles/PERSONAL_PROFILE_RULES.md` for quality rules (PP-* rules)
3. Follow template section by section, applying all PP-* rules
4. Skip sections with no findings (PP-AC-02) but fill all others (PP-HD-01)
5. Apply MUST-NOT-FORGET items (verification labels, source retention, SOCAS)

## Organization Profile

Detect by: research subject is a **non-commercial organization** (university, association, NGO, government agency, foundation, standards body, research institute, professional network).

1. Read @deep-research `profiles/ORGA_PROFILE_TEMPLATE.md` for document structure
2. Read @deep-research `profiles/ORGA_PROFILE_RULES.md` for quality rules (OP-* rules)
3. Follow template section by section, applying all OP-* rules
4. Skip sections with no findings but fill all others
5. Apply MUST-NOT-FORGET items (verification labels, source retention, SOCAS)

## Company Profile

Detect by: research subject is a **commercial company** (startup, corporation, GmbH, LLC, AG, Ltd, SaaS vendor, consultancy, agency).

1. Read @deep-research `profiles/COMPANY_PROFILE_TEMPLATE.md` for document structure
2. Read @deep-research `profiles/COMPANY_PROFILE_RULES.md` for quality rules (CP-* rules)
3. Follow template section by section, applying all CP-* rules
4. Skip sections with no findings but fill all others
5. Apply MUST-NOT-FORGET items (verification labels, source retention, SOCAS)

## General Topic (default)

Detect by: research subject is NOT a person, organization, or company.

1. Make research plan - identify 2-5 key questions to answer
2. Research step by step, adding sections to INFO document
3. After each section, self-check:
   - Do I need to verify these findings further?
   - Can I remove duplicates or contradictions?
   - Is this information actionable? If not, cut it.
4. Review each new section against existing ones - remove redundancies, ambiguities, unverified claims
5. If no verified solution exists: think outside the box - missing perspectives? Clever alternatives?
6. Write sources section (all URLs with primary findings)
7. Write summary section at document top (copy/paste ready)

