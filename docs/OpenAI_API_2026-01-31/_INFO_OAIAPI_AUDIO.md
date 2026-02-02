# INFO: OpenAI API - Audio

**Doc ID**: OAIAPI-IN16
**Goal**: Document Audio API endpoints (transcription, translation, TTS)
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `__OAIAPI_SOURCES.md [OAIAPI-IN01]` for source references

## Summary

The Audio API provides three capabilities: speech-to-text transcription, translation to English, and text-to-speech generation. Transcription uses Whisper models to convert audio to text in the original language. Translation converts non-English audio to English text. Text-to-speech generates natural-sounding audio from text using voices like alloy, echo, fable, onyx, nova, and shimmer. Supported input formats include mp3, mp4, mpeg, mpga, m4a, wav, and webm with a 25MB file size limit.

## Key Facts

- **Transcription model**: `whisper-1` [VERIFIED]
- **TTS models**: `tts-1`, `tts-1-hd` [VERIFIED]
- **Max file size**: 25 MB [VERIFIED]
- **Supported formats**: mp3, mp4, mpeg, mpga, m4a, wav, webm [VERIFIED]

## Use Cases

- **Voice assistants**: Transcribe user speech for processing
- **Accessibility**: Generate audio from text content
- **Translation**: Convert foreign audio to English text
- **Podcasts**: Generate voiceovers from scripts

## Quick Reference

### Endpoints

- `POST /v1/audio/transcriptions` - Speech to text
- `POST /v1/audio/translations` - Audio to English text
- `POST /v1/audio/speech` - Text to speech

### TTS Voices

- `alloy` - Neutral, balanced
- `echo` - Warm, conversational
- `fable` - British accent
- `onyx` - Deep, authoritative
- `nova` - Friendly, upbeat
- `shimmer` - Soft, gentle

## Endpoints

### Transcriptions

**Request**

```
POST /v1/audio/transcriptions
Content-Type: multipart/form-data
```

**Parameters**

- `file` (file, required) - Audio file
- `model` (string, required) - `whisper-1`
- `language` (string, optional) - ISO-639-1 code
- `prompt` (string, optional) - Context hint
- `response_format` (string, optional) - json, text, srt, verbose_json, vtt
- `temperature` (number, optional) - 0-1

### Translations

**Request**

```
POST /v1/audio/translations
Content-Type: multipart/form-data
```

**Parameters**

Same as transcriptions. Always outputs English.

### Speech (TTS)

**Request**

```
POST /v1/audio/speech
Content-Type: application/json
```

**Parameters**

- `model` (string, required) - `tts-1` or `tts-1-hd`
- `input` (string, required) - Text to convert (max 4096 chars)
- `voice` (string, required) - alloy, echo, fable, onyx, nova, shimmer
- `response_format` (string, optional) - mp3, opus, aac, flac, wav, pcm
- `speed` (number, optional) - 0.25 to 4.0

## Request Examples

### Transcription (cURL)

```bash
curl https://api.openai.com/v1/audio/transcriptions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F file="@audio.mp3" \
  -F model="whisper-1"
```

### Python Transcription

```python
from openai import OpenAI

client = OpenAI()

with open("audio.mp3", "rb") as audio_file:
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )

print(transcript.text)
```

### Python Translation

```python
from openai import OpenAI

client = OpenAI()

with open("german_audio.mp3", "rb") as audio_file:
    translation = client.audio.translations.create(
        model="whisper-1",
        file=audio_file
    )

print(translation.text)  # English text
```

### Python TTS

```python
from openai import OpenAI
from pathlib import Path

client = OpenAI()

speech_file = Path("speech.mp3")

response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="Hello, welcome to our podcast!"
)

response.stream_to_file(speech_file)
```

### Streaming TTS

```python
from openai import OpenAI

client = OpenAI()

with client.audio.speech.with_streaming_response.create(
    model="tts-1",
    voice="alloy",
    input="Hello, this is streaming audio."
) as response:
    response.stream_to_file("output.mp3")
```

## Response Examples

### Transcription Response

```json
{
  "text": "Hello, this is a test of the transcription API."
}
```

### Verbose Transcription

```json
{
  "task": "transcribe",
  "language": "english",
  "duration": 5.5,
  "text": "Hello, this is a test.",
  "segments": [
    {
      "id": 0,
      "start": 0.0,
      "end": 2.5,
      "text": "Hello, this is a test.",
      "tokens": [50364, 2425, 11, ...]
    }
  ]
}
```

## Error Codes

- `400 Bad Request` - Invalid file format or parameters
- `401 Unauthorized` - Invalid API key
- `413 Payload Too Large` - File exceeds 25MB
- `429 Too Many Requests` - Rate limit exceeded

## Gotchas and Quirks

- `tts-1` is faster but lower quality than `tts-1-hd`
- Transcription `prompt` helps with domain-specific terms
- Translation only outputs English regardless of input
- TTS `speed` affects playback rate, not voice

## Related Endpoints

- `_INFO_OAIAPI_CHAT.md` - Audio in chat (gpt-4o-audio)

## Sources

- OAIAPI-IN01-SC-OAI-AUDIO - Official audio documentation

## Document History

**[2026-01-30 10:00]**
- Initial documentation created
