<!-- PROMPTS TEMPLATE
Filename: _PROMPTS_[Topic].md
Location: session folder (default), workspace root, or user-specified path
Topic: CamelCase description (e.g., SetupProject, MigrateAuth, AnalyzePerformance)

Read PROMPTS_GUIDES.md BEFORE writing. Verify against all PRMT-* rules in PROMPTS_RULES.md.
Remove ALL XML comments after creating the document. First non-empty line must be an opening fence.
Heading recommendation (PRMT-FT-07): use `## Prompt N - [title]` before each prompt for readability.
If headings are used, ALL prompts MUST have headings (consistency enforced). -->

<!-- Simple prompt: 3-backtick fence when no inner code blocks.
Heading before the fence is optional but recommended (PRMT-FT-07). -->
## Prompt 1 - [short title]

```
[Objective: what the finished state looks like (1-3 sentences)]

Constraints:
- [What NOT to do]
- [Boundaries to respect]

Verify: [Machine-checkable done criteria]
```

---

<!-- Commentary: purpose of next prompt and expected state from previous step.
For human readers only - never sent to model. Remove if no commentary needed. -->

<!-- Prompt with inner code blocks: 4-backtick fence. Outer must exceed deepest inner fence. -->
## Prompt 2 - [short title]

````
[Objective referencing output from previous prompt explicitly]

Example output format:
```[language]
[Representative example showing expected structure]
```

Constraints:
- [What NOT to do]

Verify: [Observable success criteria]
````

<!-- EXAMPLE: Reference only. Do not copy into new documents. Shows a completed 2-prompt file with headings (PRMT-FT-07). -->

## Full Example

`````markdown
## Prompt 1 - Security analysis

```
Analyze the authentication module in src/auth/ for security vulnerabilities.
Focus on: token validation, session management, and password hashing.

Constraints:
- Do not modify any code in this step
- Limit analysis to src/auth/ directory only

Verify: Output a numbered list of findings with severity (HIGH/MEDIUM/LOW) and file location.
```

---

## Step 2 - Fix highest-severity finding

````
Using the analysis from the previous step, fix the highest-severity vulnerability identified.

Example fix pattern:
```typescript
try {
  const token = jwt.verify(input, secret, { algorithms: ['HS256'] })
} catch (err) {
  return res.status(401).json({ error: 'Invalid token' })
}
```

Constraints:
- Fix only the single highest-severity issue
- Do not change the public API of any exported function
- Do not add new dependencies

Verify: Run `pnpm test:auth`. All tests pass. The specific vulnerability from step 1 is no longer present.
````
`````
