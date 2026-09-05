# Prompts File Guide

Read BEFORE writing `_PROMPTS_[Topic].md` files. Follow `PROMPTS_RULES.md` for verification.

## 1. Classify the Task

Determine what the prompts file accomplishes. This determines decomposition and structure:

1. **Single task** - One prompt, one concern (file edit, question, simple generation)
2. **Multi-step pipeline** - Sequential prompts where each builds on prior output (research → implement → test)
3. **Setup + work** - First prompt establishes environment/context, subsequent prompts do the work
4. **Exploration** - Open-ended research or investigation, each prompt refining direction based on prior findings

Single tasks need one prompt. Pipelines and setup+work patterns need multiple. Exploration may need either, depending on how predictable the path is.

## 2. Decide Decomposition

Split into multiple prompts when:
- The task has more than one reasoning mode (research vs implementation vs validation)
- Intermediate output should be reviewed before continuing
- One step produces a large artifact the next step consumes

Keep as one prompt when:
- Single reasoning mode (one edit, one search, one generation)
- No intermediate checkpoint needed
- Splitting adds coordination overhead without quality benefit

Common mistake: splitting every task into 5 prompts. Static decomposition with no conditional logic can cost more than a monolithic prompt if early steps fail and force reruns of all downstream steps.

## 3. Structure Each Prompt

Every prompt contains up to four parts, in this order:

1. **Objective** - What the finished state looks like (1-3 sentences). State the outcome, not implementation steps. "Fix the auth bug so expired tokens return 401" not "Open file X, add try-catch on line Y"
2. **Context** - Facts the agent needs but cannot infer: tech stack, relevant files (1-3), business rules, conventions. Selective, not exhaustive. Treat context window as a budget
3. **Constraints** - What NOT to do: no new dependencies, do not modify schema, stay within these files. Constraints prevent more failures than detailed instructions
4. **Verification** - Machine-checkable success criteria: "run tests", "endpoint returns 200", "file exists with these sections". Without this, the agent decides when it is done

Not every prompt needs all four. A simple "list all Python files" needs only the objective. An implementation prompt needs all four. Rule of thumb: the higher the stakes, the more parts you include.

When a prompt must produce output in a specific format, add an optional 5th element: **Example** (between Constraints and Verification). See section 9 for when examples are worth the tokens.

## 4. Plan State Flow

In a `_PROMPTS_[Topic].md` file, all prompts run as turns of ONE session. Later prompts see all earlier conversation.

Plan what each prompt produces that the next one needs:
- Name artifacts explicitly: "Using the analysis from the previous step..."
- Do not assume the model will infer which prior output matters
- Do not restate facts already established - they are in conversation history
- Never contradict constraints from earlier prompts

Use commentary sections (before the first prompt or between `---` and next fence) to document expected state for human readers. Commentary density depends on file type:

- **Final output files**: heading + max 1 sentence per prompt. The sentence captures expected state for the human reviewer. More than one sentence is noise — the prompt itself carries the detail.
- **Template files**: no limit. Templates need authoring instructions, placeholder explanations, and conditional guidance that get removed when filling the template.

## 5. Manage Prompt Density

Practitioner heuristic: limit each prompt to 5-8 high-priority rules or instructions. Beyond that, the model tends to skip items in the middle of long lists (lost-in-the-middle effect). The exact threshold varies by model and task.

If a prompt needs more than 8 instructions:
- Split into two prompts (first sets up, second executes)
- Move standing rules into the agent's rules file instead of repeating per-prompt
- Promote the most critical constraints to the top and bottom of the prompt (models attend to edges)

## 6. Handle Failure Paths

For prompts that perform actions (file changes, API calls, installations):
- State what to do if the action fails: retry, skip, or abort
- Define retry limits if applicable: "If tests fail after 2 attempts, document failures and continue"
- Specify stop conditions: "If no matching files found, report and stop - do not create placeholder files"

Prompts without failure handling produce agents that either loop indefinitely or silently suppress errors and continue on broken state.

## 7. Select Fence Length

Examine each prompt for inner fenced code blocks:

- No inner fences → 3 backticks
- Contains ``` blocks → 4+ backtick outer fence
- Contains ```` blocks (markdown examples with ``` inside) → 5+ backtick outer fence
- Maximum: 9 backticks

When in doubt, use one more backtick than the deepest inner fence. The parser closes at the first line with >= N backticks.

## 8. Prioritize Precision Over Token Savings

Prompts are instructions, not documentation. The APAPALAN priority order applies: **Precision first (Priority 1), Brevity second (Priority 2)**. A vague 20-token prompt that produces wrong output costs more than a precise 200-token prompt that succeeds on first execution.

### 8.1 Why Token Savings Backfire in Prompts

The cost equation for prompts differs from documentation:

- **Failed prompt** = full re-execution (thousands of tokens wasted), debugging time, potentially corrupted state
- **Precise prompt** = extra 50-100 tokens upfront, correct output on first run
- **Ratio**: One failed re-execution costs 10-50x more tokens than the precision tokens would have

The SKILL_GUIDES.md "Token Optimization" section (section 4) applies to skill files that sit in the context window permanently. Prompts are different: they execute once, and the cost of failure is re-running the entire prompt sequence.

### 8.2 Where to Invest Tokens (Precision Wins)

Spend tokens on content that prevents misunderstanding or wrong action:

- **Specific objectives** - "Fix the auth bug so expired tokens return 401" vs "Fix the auth bug" (AP-PR-07)
- **Constraints** - "Do not modify the database schema" prevents a class of failures no amount of brevity recovers from
- **Verification criteria** - "Run `pnpm test`. All tests pass" is 8 tokens that prevent unbounded debugging
- **Disambiguation** - "The `user` table (PostgreSQL, not the application User model)" prevents the model from editing the wrong thing
- **Examples** - A 3-line input/output example communicates format more precisely than a 10-line description (AP-BR-05)

MECT's "deliberate redundancy" applies here: restating a referent ("the authentication retry" instead of "it") costs 2 tokens but prevents the model from binding "it" to the wrong antecedent. This is signal redundancy - it strengthens the model's understanding, not noise.

### 8.3 Where to Save Tokens (Brevity Applies)

After precision is secured, cut aggressively:

- **Filler phrases** - "I would like you to please" → just state the objective
- **Restating known context** - If prompt 1 established the tech stack, prompt 3 does not need to repeat it (conversation history persists)
- **Generic instructions** - "Write clean, well-documented code" adds zero signal. The model already does this by default
- **Implementation micromanagement** - "Open file X, go to line Y, add Z" wastes tokens on steps the model can determine itself (PRMT-CT-04)
- **Politeness tokens** - "Could you kindly", "Thank you in advance" - the model does not respond to social cues

### 8.4 The MECT Test for Token Value

For every phrase in a prompt, apply MECT's signal vs noise distinction:

- **Signal** = Removing this phrase forces the model to guess. Keep it.
- **Noise** = Removing this phrase changes nothing about the model's understanding. Cut it.

When uncertain: keep the phrase. Precision (Priority 1) wins over brevity (Priority 2). A prompt that is 20% longer but unambiguous beats a terse prompt that the model misinterprets.

## 9. When to Include Examples

Examples are the highest-precision, lowest-ambiguity way to communicate format and behavior. AP-BR-05 (show format over describing format) applies directly: a 3-line example replaces a 10-line description and communicates more precisely.

### 9.1 When Examples Are Worth the Tokens

- **Output format matters** - If the prompt must produce a specific structure (JSON, markdown table, config file), show one complete example of the expected output
- **Pattern must be replicated** - If the agent must follow an existing codebase pattern, include a representative sample
- **Edge cases need handling** - Show the edge case input and expected output, not a description of the edge case
- **Ambiguity exists** - When the same instruction could produce two valid but different outputs, an example resolves which one you want

### 9.2 When Examples Waste Tokens

- **Behavior is obvious** - "Create a Python file with a main function" needs no example
- **The codebase IS the example** - If the agent can read existing files, reference them instead: "Follow the pattern in `src/api/users.py`"
- **Multiple valid outputs** - If any reasonable format is acceptable, an example over-constrains

### 9.3 Example Placement in Prompts

Place examples after the objective and constraints, before verification. The structure becomes:

1. Objective (what)
2. Context (relevant files, facts)
3. Constraints (what NOT to do)
4. Example (what the output looks like)
5. Verification (how to check)

Keep examples minimal: one representative instance, not three variations of the same pattern. The model generalizes from one example better than it follows a verbose description.

### 9.4 Examples and Fence Depth

Examples containing code blocks require deeper outer fences. A prompt showing a markdown example with ``` inside needs a 4+ backtick outer fence. Plan fence depth AFTER writing examples (section 7).

## 10. Review Checklist

Before considering the prompts file complete:

- [ ] First non-empty line is an opening fence (no frontmatter, no header)
- [ ] Each prompt has a clear objective (verifiable from artifact per PRMT-ST-01)
- [ ] Implementation prompts have constraints and verification criteria
- [ ] No prompt mixes more than one reasoning mode (research + implement = split)
- [ ] Sequential prompts do not contradict earlier constraints
- [ ] Later prompts explicitly reference prior output when dependent
- [ ] Commentary sections explain purpose for human readers, not duplicate prompts
- [ ] Fence lengths exceed all inner fence lengths within each prompt
- [ ] `---` separator between every pair of consecutive prompts
- [ ] No prompt content outside fences (would be silently dropped)
- [ ] Precision tokens preserved: constraints, verification, disambiguation not cut for brevity (PRMT-CT-05)
- [ ] Signal redundancy preserved: explicit referents, not pronouns for ambiguous antecedents (PRMT-CT-06)
- [ ] Format-critical prompts use examples instead of prose descriptions (PRMT-CT-07)
