---
auto_execution_mode: 1
description: Prime context with workspace files
---

# Prime Context Workflow

## Step 1: Read Agent Rules

Read all .md files in the agent rules folder:
```
find_by_name Pattern="*.md" SearchDirectory="[AGENT_FOLDER]/rules" Type="file"
```
These define core conventions and system behavior.

## Step 2: Find and Read Priority Documentation (! prefix)

Search for .md files starting with "!" - these contain critical specifications:
```
find_by_name Pattern="!*.md" SearchDirectory="[WORKSPACE_FOLDER]" Type="file"
```
Read each file found and **summarize key points internally** to better remember content.

## Step 3: Find and Read Standard Documentation

Search for .md files NOT starting with "_" or "!":
```
find_by_name Pattern="*.md" SearchDirectory="[WORKSPACE_FOLDER]" Type="file" Excludes=["_*", "!*"]
```

## Exclusions

- Skip .md files starting with "_"
- Skip ALL folders starting with "_" (task folders, archive, temp, tools, etc.)

## Step 4: Detect Workspace Scenario

Identify active scenario from three dimensions:
1. **Project Structure**: SINGLE-PROJECT or MONOREPO?
2. **Version Strategy**: SINGLE-VERSION or MULTI-VERSION?
3. **Work Mode**: SESSION-BASED or PROJECT-WIDE?

## Final Output

Answer in single row: "Read [a] .md files ([b] priority), [c] code files ( [d] .py, [e] ...). Mode: [scenario]"

Example: "Read 5 .md files (2 priority), 12 code files (10 .py, 2 .html). Mode: SINGLE-PROJECT + SINGLE-VERSION + SESSION-BASED"