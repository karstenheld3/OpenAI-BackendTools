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

**Standard location**: `[WORKSPACE_FOLDER]\..\.tools\.api-keys.txt` (in shared .tools folder)

**Format** (one key per line):
```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

**Usage**: Pass `--keys-file` to scripts:
```powershell
python transcribe-image-to-markdown.py --keys-file ..\.tools\.api-keys.txt --input-file image.png
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
- Ensure keys file exists at standard location (see Configure API Keys above)
- Pass correct path via `--keys-file` argument

**"Unsupported file format"**
- Check supported formats in SKILL.md
- For audio, ensure ffmpeg is installed for conversion

**"Rate limit exceeded"**
- Wait and retry
- Consider using batch mode with lower concurrency
