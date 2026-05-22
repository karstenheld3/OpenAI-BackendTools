# LLM Computer Use Skill

Desktop automation via LLM vision. The AI sees your screen, decides what to click/type, and executes actions.

## When to Use

Apply when automating desktop interactions that require visual understanding:
- Opening and controlling applications
- Clicking buttons, menus, or UI elements
- Typing text into fields
- Navigating file systems
- Browser automation
- System tasks

## Requirements

- Python 3.10+
- Anthropic API key (ANTHROPIC_API_KEY environment variable)
- Windows

## CLI Usage

```bash
# Navigate to skill folder first
cd .windsurf/skills/llm-computer-use

# Dry-run (safe, no actions executed)
python -m llm_computer_use "Click the Start button"

# Execute mode
python -m llm_computer_use -x "Open Notepad and type Hello World"

# With API key file
python -m llm_computer_use -x -k ../.tools/.api-keys.txt "Open Calculator"
```

## Options

- `-x, --execute` - Execute actions (default: dry-run)
- `-n, --max-iterations` - Max iterations (default: 10, ~$0.01-0.02 each)
- `-m, --model` - Model: claude-sonnet-4-5 (default), claude-haiku-4-5, claude-opus-4
- `-k, --keys-file` - API keys file path
- `-s, --save-log` - Save session log as JSON
- `-q, --quiet` - Minimal output

## Programmatic Usage

```python
import sys
sys.path.insert(0, ".windsurf/skills/llm-computer-use")

from llm_computer_use import AgentSession

session = AgentSession(
    task_prompt="Open Notepad",
    max_iterations=5,
    dry_run=False,
    model="claude-sonnet-4-5"
)

summary = session.run()
print(f"Cost: ${summary['estimated_cost_usd']:.4f}")
```

## Cost Estimate

| Model | Cost per Iteration | 10 Iterations |
|-------|-------------------|---------------|
| claude-opus-4 | ~$0.05-0.10 | ~$0.50-1.00 |
| claude-sonnet-4-5 | ~$0.01-0.02 | ~$0.10-0.20 |
| claude-haiku-4-5 | ~$0.003-0.005 | ~$0.03-0.05 |

## Safety

- Dry-run by default (no actions executed)
- High-risk action confirmation (Alt+F4, delete, shutdown)
- Iteration limits prevent runaway costs
- pyautogui fail-safe (move mouse to corner to abort)

## Version

0.5.0
