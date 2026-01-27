# LLM Transcription Skill

Universal transcription tools using LLMs with optimized prompts for each purpose.

## When to Use This Skill

**Apply when:**
- Converting images (screenshots, documents, diagrams) to markdown
- Transcribing audio files to markdown text
- Batch processing multiple files for transcription
- Preserving document structure in markdown format

**Do NOT apply when:**
- Evaluating LLM performance (use @llm-evaluation)
- Simple text extraction without formatting needs
- Real-time transcription (these are batch tools)

## Quick Start

1. Run `SETUP.md` once to install dependencies
2. Choose your script:
   - **Image Pipeline** (recommended): `transcribe-image-to-markdown-advanced.py` - Ensemble + judge + refinement
   - **Image Simple**: `transcribe-image-to-markdown.py` - Single-shot transcription
   - **Audio to Markdown**: `transcribe-audio-to-markdown.py`

## Available Scripts

**Image Transcription:**
- `transcribe-image-to-markdown-advanced.py` - Ensemble transcription with judge and refinement (recommended)
- `transcribe-image-to-markdown.py` - Simple single-shot transcription

**Audio Transcription:**
- `transcribe-audio-to-markdown.py` - Convert audio to markdown transcript

## Usage Examples

**Image Pipeline (recommended):**
```bash
python transcribe-image-to-markdown-advanced.py --input doc.png --output doc.md --verbose
python transcribe-image-to-markdown-advanced.py --input-dir ./images --output-dir ./out --ensemble-size 3 --min-score 3.5
```

**Image Simple:**
```bash
python transcribe-image-to-markdown.py --input screenshot.png --output result.md
python transcribe-image-to-markdown.py --input document.jpg --model gpt-4o --output doc.md
```

**Audio Transcription:**
```bash
python transcribe-audio-to-markdown.py --input recording.mp3 --output transcript.md
python transcribe-audio-to-markdown.py --input meeting.wav --model whisper-1 --output meeting.md
```

## Supported Formats

**Images:** `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`
**Audio:** `.mp3`, `.wav`, `.m4a`, `.ogg`, `.flac`

## Key Features

- **Optimized prompts** for each transcription type
- **Structure preservation** - headings, lists, tables maintained
- **Batch processing** support for multiple files
- **Cost tracking** with token usage reports
- **Multiple model support** - OpenAI and Anthropic

## Configuration

API keys required in `~/.llm-keys` or environment variables:
- `OPENAI_API_KEY` - For GPT models and Whisper
- `ANTHROPIC_API_KEY` - For Claude models
