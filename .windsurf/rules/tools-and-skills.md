---
trigger: always_on
---

# Tools and Skills

Tool-specific knowledge and disambiguation.

## Browser Automation (Playwright vs Playwriter)

**These are different tools with confusingly similar names:**

- **Playwright MCP** (default) - Microsoft's MCP server. Spawns fresh browser instance. `npx @playwright/mcp@latest`
- **Playwriter** (exception) - Chrome extension + CLI. Uses your **real browser** with existing logins/cookies. Install from `playwriter.dev`

**When to use:**
- **Playwright MCP**: Default choice. Clean sessions, standard automation, no existing auth needed
- **Playwriter**: When explicitly asked for by user using `Playwriter` term

## Workflow-First Rule

Before executing any multi-step operation (file processing, deployment, transcription, email):

1. Search `[WORKFLOWS]` for applicable workflow: file type, action verb, or domain
2. Search `[SKILLS]` for applicable skill
3. **If workflow/skill exists**: MUST follow it step-by-step. No improvisation, no shortcuts.
4. **If not found**: Proceed with best judgment

Before installing Python or PowerShell modules: Check existing skills and workflows for established dependencies, venvs, and tool preferences first.

Violation = automatic CRITICAL in FAILS.md. No exceptions.

## Skill Registry

Skills are in `[AGENT_FOLDER]/skills/`. Each has a `SKILL.md` with usage instructions.

- **@coding-conventions** - Writing, editing, reviewing, or debugging code (Python, PowerShell)
- **@deep-research** - Deep research on technologies, APIs, frameworks (MEPI/MCPI patterns)
- **@edird-phase-planning** - Planning for long-running tasks in sessions
- **@git** - Git repositories, commit history, recovering files from previous commits
- **@git-conventions** - Commit messages, .gitignore configuration
- **@github** - GitHub repositories, issues, PRs, authentication
- **@google-account** - Google services (Gmail, Calendar, Drive, Tasks) via gogcli CLI
- **@llm-computer-use** - Desktop automation via LLM vision (click, type, navigate)
- **@llm-evaluation** - LLM performance testing, model comparison, LLM-as-judge scoring
- **@llm-transcription** - Image/audio to markdown transcription (ensemble + judge + refinement)
- **@ms-playwright-mcp** - Browser automation, web scraping, UI testing (default browser tool)
- **@pdf-tools** - PDF conversion, compression, analysis (convert-pdf-to-jpg, ghostscript, qpdf)
- **@playwriter-mcp** - Real browser automation with existing logins (ONLY when user says "Playwriter")
- **@session-management** - Session init, save, resume, finalize, archive
- **@travel-info** - Travel lookups: flights, trains, transit, country-specific info
- **@windows-desktop-control** - Windows screenshots, window management, keyboard/mouse
- **@windsurf-auto-model-switcher** - Switch Cascade AI model tier programmatically
- **@write-documents** - Create/edit INFO, SPEC, IMPL, TEST, FIX documents, STRUT plans, CONVERSATION files
- **@youtube-downloader** - Download YouTube content as MP3 or video via yt-dlp

## Tool Locations

Executable tools outside the workspace:

- **Python venv**: `[WORKSPACE_FOLDER]/../.tools/llm-venv/Scripts/python.exe`
- **API keys**: `[WORKSPACE_FOLDER]/../.tools/.api-keys.txt` (default; override in session or workspace NOTES.md)
- **Poppler** (PDF): `[WORKSPACE_FOLDER]/../.tools/poppler/Library/bin/`
- **Ghostscript**: `[WORKSPACE_FOLDER]/../.tools/gs/bin/`
- **QPDF**: `[WORKSPACE_FOLDER]/../.tools/qpdf/bin/`
- **7-Zip**: `[WORKSPACE_FOLDER]/../.tools/7z/`
- **gogcli config**: `[WORKSPACE_FOLDER]/../.tools/gogcli-client-secret.json`
