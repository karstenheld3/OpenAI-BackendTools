# Domain Profile: Software

Research domain for software APIs, frameworks, libraries, SDKs, and developer tools.

## When to Use

- Research subject is a software API, framework, library, SDK, or developer tool
- Prompt mentions: API, SDK, library, framework, package, module, endpoint, rate limit, authentication
- Output will be consumed by developers or architects

## Source Tiers

- **Tier 1 (official/primary)**: Official documentation, API references, SDK source code, official PDFs/specs
- **Tier 2 (vendor/issuer)**: Official blog, GitHub repo, release notes, changelog, conference talks by maintainers
- **Tier 3 (community/analyst)**: Stack Overflow, expert blogs, GitHub issues/discussions, Reddit, Discord

## Document Handling

- Read API docs fully (not just selected endpoints)
- Code examples must be syntactically correct for the target language
- Version-match all sources to the documented version
- Download and transcribe official PDFs (whitepapers, specs) via source processing pipeline
- For large API references: transcribe fully, use `<transcription_json>` extraction for endpoint tables

## Template Additions

Add these sections to the standard topic template:

- **Quick Reference** - One-screen lookup of essential parameters (limits, endpoints, config)
- **Use Cases** - Common implementation scenarios with code snippets
- **SDK Examples** - Adapt to relevant languages (C#, Python, TypeScript, PowerShell, JavaScript, Go, etc.)
- **Error Responses** - Error codes with descriptions and resolution
- **Rate Limiting / Throttling** - Limits, headers, retry strategies
- **Authentication** - Auth methods, token lifecycle, scopes
- **Limitations and Known Issues** - From community sources, cross-referenced with official bug trackers
- **Gotchas and Quirks** - Undocumented behavior, edge cases from community sources

## Version Scope

Every topic document MUST state the version being documented in the header block:
- Versioned API: `v2.1.0`, `API v3`
- Unversioned: documentation date `YYYY-MM-DD`
- Filter community sources to match documented version - discard outdated version-specific issues

## Anti-Patterns

- Checkboxes in Summary file topic lists (use links instead)
- Short summaries (2-3 sentences) for complex topics - use 5-15 sentences
- Missing "Related APIs/Technologies" section
- Source IDs not matching between SOURCES and topic files
- Non-clickable references in Summary file (use markdown links)
- Ignoring community sources for known issues
- Treating community reports as verified without citation
- Non-sequential file numbering

## Quality Criteria

Additional checks for software domain quality pipeline:

- All code examples syntactically correct (or marked `[ASSUMED]` if untested)
- Version scope explicitly stated in every topic document
- Rate limiting section populated (or explicitly noted as "not applicable")
- Error codes documented with resolution guidance
- Community-sourced limitations cross-referenced with official bug trackers where available
- No Markdown tables (use lists per core conventions)
- Summary copy/paste ready for executive use
- Every topic file verified against source URLs
