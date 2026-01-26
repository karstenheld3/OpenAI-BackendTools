# Devil's Advocate Review: SETUP.md

**Reviewed**: 2026-01-22 21:33
**Document**: `.windsurf/skills/llm-evaluation/SETUP.md`
**Reviewer**: Devil's Advocate

## MUST-NOT-FORGET

- User wants venv in `.tools/` folder, not skill folder
- Scripts need to load .env file - but scripts don't exist yet
- Reference patterns from pdf-tools and ms-playwright-mcp SETUP.md

## MUST-RESEARCH

1. **Python venv on Windows** - Common activation failures and solutions
2. **API key security** - Best practices for .env files with LLM keys
3. **pip install failures** - SSL, network, and permission issues
4. **Python version compatibility** - openai/anthropic minimum versions
5. **Cross-platform paths** - Windows vs Unix path handling

## Industry Research Findings

### Python venv on Windows (Stack Overflow, Python bugs)

- **ExecutionPolicy** is the #1 failure mode - SETUP.md addresses this
- **Path differences**: `Scripts/` on Windows vs `bin/` on Unix - correctly handled
- **Missing:** `python -m venv` can fail if `venv` module not installed (rare but possible)

### API Key Security (OpenAI Help Center, Anthropic Support)

- **CRITICAL**: Both OpenAI and Anthropic explicitly warn against hardcoding keys
- **Best practice**: Use `python-dotenv` to load .env files
- **Missing from SETUP.md**: Scripts need `python-dotenv` package to load .env
- **Risk**: .env in working directory may not be found if scripts run from different CWD

### pip Install Failures

- **SSL errors**: Corporate proxies, outdated certificates
- **SETUP.md addresses**: `--trusted-host` workaround documented
- **Missing**: Offline install option for air-gapped environments

## Critical Issues

### LLMEV-RV-001: Missing python-dotenv Dependency

**Severity**: CRITICAL
**Location**: Section 4 (Install Dependencies)

**Problem**: SETUP.md installs `openai` and `anthropic` but NOT `python-dotenv`. The scripts will need to load `.env` files, but without `python-dotenv`, the standard pattern `load_dotenv()` won't work.

**Evidence**: SPEC requires `.env` support, but scripts need a library to read it.

**Risk**: Scripts will fail to find API keys unless user manually sets environment variables.

**Suggested fix**: Add `python-dotenv` to requirements:
```powershell
pip install openai>=1.0.0 anthropic>=0.18.0 python-dotenv
```

### LLMEV-RV-002: .env Location Ambiguity

**Severity**: HIGH
**Location**: Section 5 (Configure API Keys)

**Problem**: Document says "Create `.env` file in your working directory (where you run scripts)". But scripts may be invoked from different directories.

**Risk**: User creates .env in project root, runs script from subfolder, .env not found.

**Suggested fix**: Either:
- A) Scripts should search for .env in multiple locations (CWD, script dir, user home)
- B) Add `--keys-file` parameter that defaults to searching order
- C) Document that CWD must contain .env, or use `--keys-file` explicitly

### LLMEV-RV-003: venv Module May Not Exist

**Severity**: LOW
**Location**: Section 3 (Create Virtual Environment)

**Problem**: `python -m venv` assumes the venv module is installed. On some minimal Python installs (e.g., Ubuntu `python3-minimal`), venv is a separate package.

**Risk**: Command fails with "No module named venv" on minimal installations.

**Suggested fix**: Add check:
```powershell
python -m venv --help
# If fails: "Install python3-venv package or use full Python installer"
```

## High Priority

### LLMEV-RV-004: No Version Pinning in pip install

**Severity**: HIGH
**Location**: Section 4 (Install Dependencies)

**Problem**: Using `>=1.0.0` allows any version. OpenAI SDK has had breaking changes between major versions.

**Risk**: Future OpenAI/Anthropic SDK versions may break scripts.

**Suggested fix**: Pin to specific versions or version ranges:
```
openai>=1.0.0,<2.0.0
anthropic>=0.18.0,<1.0.0
```

### LLMEV-RV-005: Test API Connection Doesn't Load .env

**Severity**: HIGH
**Location**: Section 6 (Test API Connection)

**Problem**: Test script uses `os.environ.get('OPENAI_API_KEY', 'sk-test')` but doesn't call `load_dotenv()`. Will always use fallback 'sk-test' unless user manually exports env var.

**Evidence**: The test will "pass" even with wrong setup because it creates client with dummy key.

**Suggested fix**: Test should verify actual connection:
```python
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()  # Will fail if no key
response = client.models.list()  # Actually calls API
```

## Medium Priority

### LLMEV-RV-006: No Proxy Configuration

**Severity**: MEDIUM
**Location**: Troubleshooting section

**Problem**: Corporate environments often require HTTP proxy for external API calls. No guidance provided.

**Risk**: API calls fail with connection errors in corporate networks.

**Suggested fix**: Add proxy configuration section:
```powershell
$env:HTTP_PROXY = "http://proxy.corp:8080"
$env:HTTPS_PROXY = "http://proxy.corp:8080"
```

### LLMEV-RV-007: Hardcoded Example Path

**Severity**: LOW
**Location**: Section 1, line 8

**Problem**: Example path `$workspaceFolder = "E:\Dev\IPPS"` is specific to author's machine.

**Suggested fix**: Use generic example or placeholder:
```powershell
$workspaceFolder = (Get-Location).Path  # or: $workspaceFolder = "C:\Projects\MyProject"
```

## Questions That Need Answers

1. **Should scripts auto-find .env?** Or require explicit `--keys-file` if not in CWD?
2. **What about python-dotenv?** Is it an intentional omission (scripts will implement own parser)?
3. **Offline install?** Should we support `pip install --no-index --find-links=./packages/`?
4. **API key rotation?** What happens when keys expire mid-batch?

## Document History

**[2026-01-22 21:33]**
- Initial Devil's Advocate review
- 3 critical/high issues found
- 4 medium/low issues found
- 4 questions raised

