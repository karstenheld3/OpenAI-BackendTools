# INFO Document Rules

Verification priority:
1. Factuality and misinterpretation prevention - verify against `APAPALAN_RULES.md`, `MECT_WRITING_RULES.md`, `SOCAS_RULES.md`
2. Document structure - verify against rules below

## Rule Index

Header (HD)
- INFO-HD-01: Header block with Doc ID, Goal, Timeline (all three required)
- INFO-HD-02: Doc ID format `[TOPIC]-IN[NN]`
- INFO-HD-03: Timeline format `Created YYYY-MM-DD, Updated N times (YYYY-MM-DD - YYYY-MM-DD)`

Summary (SM)
- INFO-SM-01: Summary section mandatory, positioned immediately after header block
- INFO-SM-02: Summary items use verification labels

Table of Contents (TC)
- INFO-TC-01: TOC entries are clickable markdown links
- INFO-TC-02: TOC numbering matches actual section numbering
- INFO-TC-03: Every numbered section appears in TOC and vice versa

Sections (SN)
- INFO-SN-01: Content sections use numbered H2 headings
- INFO-SN-02: Subsections use decimal notation
- INFO-SN-03: Optional sections positioned per `INFO_GUIDE.md`

Sources (SC)
- INFO-SC-01: Source ID format `[TOPIC]-[DOC]-SC-[SOURCE_ID]-[SOURCE_REF]`
- INFO-SC-02: Each source entry has URL or file reference AND primary finding
- INFO-SC-03: Sources section lists only findable/verifiable sources
- INFO-SC-04: URLs start with `https://` (clickable in editors and terminals)
- INFO-SC-05: Inline source links in content sections at first mention of each online source, app, or tool

Format (FT)
- INFO-FT-01: Standard section order per `INFO_GUIDE.md` Section 2
- INFO-FT-02: Document History present, reverse chronological, with action prefixes
- INFO-FT-03: Diagrams use Unicode box-drawing characters per `core-conventions.md`
- INFO-FT-04: Foreign terms always translated into document language at point of use

## INFO-HD-01: Header Block

All three fields required in every INFO document.

**BAD:**
```markdown
# INFO: Authentication

Some notes about auth.
```

**GOOD:**
```markdown
# INFO: Authentication

**Doc ID**: AUTHSYST-IN01
**Goal**: Evaluate OAuth2 vs API key authentication for the REST API
**Timeline**: Created 2026-06-20, Updated 2 times (2026-06-20 - 2026-06-24)
```

## INFO-HD-02: Doc ID Format

Must follow `[TOPIC]-IN[NN]` pattern. TOPIC is 7-14 uppercase letters, registered in `ID-REGISTRY.md`. Inside `T##_`/`S##_` folders, use nested format `[TOPIC]-[SUBTOPIC]-IN[NN]`.

**BAD:** `AUTH-01`, `Info-Authentication`, `AUTHSYST-INFO-01`

**GOOD:** `AUTHSYST-IN01`, `AIDETECT-STYLMTRY-IN01`

## INFO-HD-03: Timeline Format

**BAD:** `Created: June 20, 2026`, `Last updated 2026-06-24`

**GOOD:** `Created 2026-06-20, Updated 2 times (2026-06-20 - 2026-06-24)`

For new documents with no updates: `Created 2026-06-20, Updated 0 times`

For living/catalog documents that accumulate entries over time, Timeline may be omitted when Document History provides equivalent chronology.

## INFO-SM-01: Summary Section

Summary is mandatory and positioned immediately after the header block. Contains copy-paste-ready key findings.

**BAD:**
```markdown
## Table of Contents
1. [Overview](#1-overview)
```
(Summary missing entirely)

**GOOD:**
```markdown
## Summary

- OAuth2 is required for multi-tenant scenarios [VERIFIED]
- API key auth sufficient for single-tenant internal tools [ASSUMED]
- Token refresh adds ~200ms latency per request [TESTED]
```

## INFO-SM-02: Verification Labels

Summary items use `[VERIFIED]`, `[UNVERIFIED]`, `[ASSUMED]`, `[TESTED]`, or `[PROVEN]` labels. Not every item requires a label, but key claims must have one.

These are *research confidence labels* applied during writing. They are distinct from `ID-REGISTRY.md` *retrospective assumption labels* (`[CONTRADICTS]`, `[OUTDATED]`, `[INCOMPLETE]`) which are applied in FAILS/LEARNINGS after assumptions proved wrong.

Labels are applied by writing and verification workflows, never pre-filled in templates. Templates use `[LABEL]` as placeholder.

**BAD:**
```markdown
- OAuth2 is the industry standard
- API keys are simpler
```

**GOOD:**
```markdown
- OAuth2 is the industry standard for multi-tenant SaaS [VERIFIED]
- API keys are simpler but lack token rotation [ASSUMED]
```

## INFO-TC-01: Clickable TOC Links

Every TOC entry must be a clickable markdown link with anchor slug matching the section heading.

**BAD:**
```markdown
## Table of Contents

1. Overview
2. Architecture
3. Sources
```

**GOOD:**
```markdown
## Table of Contents

1. [Overview](#1-overview)
2. [Architecture](#2-architecture)
3. [Sources](#3-sources)
```

## INFO-TC-02: TOC Numbering Matches Sections

TOC numbers must match the actual `## N.` numbering in the document.

**BAD:** `2. [Sources](#3-sources)` ← TOC entry 2 links to section 3

**GOOD:** `2. [Architecture](#2-architecture)` ← TOC and section numbers match

## INFO-TC-03: TOC Completeness

Every numbered section appears in TOC and every TOC entry has a corresponding section. No orphans in either direction.

**BAD:** TOC lists 4 sections but document has 5 numbered sections (one missing from TOC).

**GOOD:** TOC and document sections are 1:1.

## INFO-SN-01: Numbered H2 Headings

Content sections use `## N. Title` format.

**BAD:** `## Overview`, `## 1) Overview`, `## Section 1: Overview`

**GOOD:** `## 1. Overview`, `## 2. Architecture`

## INFO-SN-02: Subsection Notation

Subsections use `### N.M Subtitle` decimal notation.

**BAD:** `### Overview Details`, `### 1a. Details`

**GOOD:** `### 1.1 Authentication Flow`, `### 2.3 Error Handling`

## INFO-SN-03: Optional Section Positioning

Optional sections must be positioned per `INFO_GUIDE.md`:
- Goals, Questions: above TOC, unnumbered
- Conclusions, Emergent Hypothesis: numbered, before Next Steps

**BAD:** Conclusions section placed after Sources.

**GOOD:** Conclusions as last numbered content section before Next Steps.

## INFO-SC-01: Source ID Format

**BAD:** `Source: https://docs.example.com`, `[1] https://...`

**GOOD:** `AUTHSYST-IN01-SC-MSFT-OAUTH`: https://learn.microsoft.com/oauth - OAuth2 implementation guide [VERIFIED]

## INFO-SC-02: Source Entries

Each source needs both a reference (URL or filename) AND a primary finding describing what it contributed.

**BAD:**
```markdown
- `AUTHSYST-IN01-SC-MSFT-OAUTH`: https://learn.microsoft.com/oauth
```

**GOOD:**
```markdown
- `AUTHSYST-IN01-SC-MSFT-OAUTH`: https://learn.microsoft.com/oauth - Token refresh requires client_secret for confidential apps [VERIFIED]
```

## INFO-SC-03: Source Verifiability

Only list sources that can be accessed and verified. Drop dead links, paywalled content without summary, or hallucinated references.

## INFO-SC-04: Clickable URLs

All URLs in source entries must start with `https://` (or `http://` if HTTPS unavailable). Never use bare domains or omit the scheme.

**BAD:** `docs.example.com/oauth`, `www.microsoft.com/learn`

**GOOD:** `https://docs.example.com/oauth`, `https://learn.microsoft.com/oauth`

## INFO-SC-05: Inline Source Links

When a content section discusses information from an online source, app, tool, or entity with a website, include the URL as a markdown link at first mention in that section. The centralized Sources section remains as the reference with source IDs and primary findings. Inline links provide immediate access without scrolling.

**BAD** (URL only in Sources section, no inline link):
```markdown
## 2. Token Refresh

Token refresh requires client_secret for confidential apps.
```

**BAD** (entity discussed without linking its website, acronym not spelled out):
```markdown
## Summary

She is VP of Engineering at Acme Corp (enterprise analytics platform).
```

**GOOD** (inline link at first mention):
```markdown
## 2. Token Refresh

Token refresh requires client_secret for confidential apps ([Microsoft OAuth docs](https://learn.microsoft.com/oauth)).
```

**GOOD** (entity linked at first mention):
```markdown
## Summary

She is Vice President of Engineering at [Acme Corp](https://www.acmecorp.example.com) (enterprise analytics platform).
```

**Also acceptable** (link text describes the source):
```markdown
## 2. Token Refresh

According to the [Microsoft OAuth documentation](https://learn.microsoft.com/oauth), token refresh requires client_secret for confidential apps.
```

**When to apply:** Online sources, apps, tools, and entities (companies, organizations, products, profiles) that have a URL. Link at first mention in each section. Local file references (`filename.py`) do not need inline links.

**Summary sections are high-priority.** Readers expect to click immediately on every important entity mentioned there. The subject's profile, their company, connected people, and referenced communities must all be linked in the Summary.

## INFO-FT-04: Foreign Term Translation

When a document uses terms from another language, each term MUST be translated or explained in the document's primary language at point of use. Never create hybrid compounds mixing languages without translation.

**BAD:**
```markdown
- API requires authentification-Berechtigung before access
- The Endpunkt has rate-Begrenzung enabled
- Submit demande for acceso-Nachweis
```

**GOOD:**
```markdown
- API requires authentification (= Berechtigung/authorization) before access
- Endpoint: "punto de acceso" (access point) has rate limiting enabled
- Demarche administrative: "demande de titre" (application for certificate)
```

**Rule**: Foreign terms appear as-is (e.g., official API names, legal terms, form field labels) followed by translation in parentheses or after `=`. Never fuse a foreign word with a native suffix into an undefined hybrid (e.g., "acceso-Nachweis", "demande-Antrag").

## INFO-FT-02: Document History

Present at document end, reverse chronological order. Use action prefixes: Added, Changed, Fixed, Removed, Moved.

**BAD:**
```markdown
## Document History
Created the document. Updated sources.
```

**GOOD:**
```markdown
## Document History

**[2026-06-24 14:30]**
- Added: Section 3 with token refresh analysis
- Changed: Summary updated with latency findings

**[2026-06-20 10:00]**
- Initial research document created
```
