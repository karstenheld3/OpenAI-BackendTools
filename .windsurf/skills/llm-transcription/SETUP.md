# LLM Transcription Skill Setup

## Prerequisites

- Python 3.10+
- OpenAI API key (for GPT vision models and Whisper)
- Anthropic API key (optional, for Claude models)

## Installation

### 1. Install Python Dependencies

```bash
pip install openai anthropic httpx
```

### 2. Configure API Keys

Create `~/.llm-keys` file:
```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

Or set environment variables:
```bash
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...
```

### 3. Verify Installation

```bash
# Test image transcription
python transcribe-image-to-markdown.py --help

# Test audio transcription  
python transcribe-audio-to-markdown.py --help
```

## Audio Transcription Requirements

For audio transcription, `ffmpeg` is recommended for format conversion:

**Windows:**
```powershell
winget install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt install ffmpeg
```

## Troubleshooting

**"API key not found"**
- Ensure `~/.llm-keys` exists with correct format
- Or set `OPENAI_API_KEY` environment variable

**"Unsupported file format"**
- Check supported formats in SKILL.md
- For audio, ensure ffmpeg is installed for conversion

**"Rate limit exceeded"**
- Wait and retry
- Consider using batch mode with lower concurrency
