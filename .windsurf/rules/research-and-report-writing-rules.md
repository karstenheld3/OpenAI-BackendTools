# Research Rules

Source: https://github.com/karstenheld3/IPPS/blob/master/Docs/Concepts/_INFO_MEPI_MCPI_PRINCIPLE.md

## When to Use MEPI (Default)

**MEPI** = Most Executable Point of Information. Present 2-3 curated options.

Use when:
- Decision is reversible or low-stakes
- Time is constrained
- Decision-maker is not domain expert
- Implicit intentions can be inferred
- Action matters more than perfection

## When to Use MCPI (Exception)

**MCPI** = Most Complete Point of Information. Present exhaustive options.

Use when:
- Decision is irreversible and high-stakes (surgery, legal, compliance)
- Decision-maker is domain expert who will recognize patterns
- Regulatory/audit requirements demand documented consideration
- Research is for archival reference, not immediate action
- [ACTOR] explicitly requests exhaustive options

### The Car Example

Buying a used car, $5,000 budget, needs 1 year maintenance-free.

**MCPI approach**: Present 20 cars matching price filter. Decision-maker must evaluate all, apply own model, manage FOMO.

**MEPI approach**: Identify implicit intentions (no maintenance hassle, no luxury premium). Present 3 archetypes:
- **Option A**: $4,800 Honda Civic, 80K miles - safe middle ground
- **Option B**: $900 Toyota Corolla, 150K miles - extreme value
- **Option C**: $5,800 Honda Accord, 60K miles, warranty - extreme reliability

Result: Decision takes minutes, not hours.

## Pre-Research Checklist

Before searching:

1. **Implicit goals** - What does [ACTOR] actually want beyond stated request?
   - "Find a database" → Minimal ops burden, team familiarity, cost control

2. **Decision type** - Type 1 (irreversible: architecture, vendor lock-in) or Type 2 (reversible: library choice)?
   - Type 2 → MEPI. Type 1 → Consider MCPI but still filter.

3. **Constraints** - 3-5 hard requirements
   - "Must handle 10K users", "Must have active maintenance", "No paid license"

4. **Exclusions** - What's out of scope?
   - "No enterprise-only", "No Docker required", "No alpha products"

5. **Assumptions** - Flag with `[ASSUMED]`, verify critical ones first
   - "We need real-time sync" → Maybe eventual consistency is fine?

## Research Types

**Decision Research** (choose between options)
→ MEPI: Recommendation + 2-3 options + "Not Considered" with reasons

**Exploratory Research** ("How does X work?", "What is Y?")
→ Define scope boundary, target audience, depth limit
→ Output: Summary (2-3 sentences) + Key Concepts + Details + Sources

**Problem-Solving Research** ("Why is X broken?", "How to fix Y?")
→ Clarify symptom, gather context, form 2-3 hypotheses
→ Search: exact error → official docs → forums → broaden
→ Output: Problem + Root Cause + Solution + Verification

## Anti-Patterns

- **20 options without curation** - forces maximizer mode
- **Skipping implicit goal extraction** - may miss the point
- **Assuming MCPI is "more thorough"** - often leads to worse decisions
- **Not documenting exclusions** - [ACTOR] wonders why X wasn't considered
- **10 possible causes without narrowing** - MCPI for problems

## Quick Reference

- **How many options?** - MEPI: 2-3 / MCPI: All viable
- **Who filters?** - MEPI: Researcher / MCPI: Decision-maker
- **Default?** - MEPI: Yes / MCPI: Requires justification
