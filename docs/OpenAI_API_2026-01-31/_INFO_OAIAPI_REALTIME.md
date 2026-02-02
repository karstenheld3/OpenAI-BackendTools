# INFO: OpenAI API - Realtime

**Doc ID**: OAIAPI-IN26
**Goal**: Document Realtime API for voice interactions
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `__OAIAPI_SOURCES.md [OAIAPI-IN01]` for source references

## Summary

The Realtime API enables low-latency, multimodal voice conversations using WebSocket connections. It supports real-time audio input/output, automatic voice activity detection, and function calling during voice conversations. Clients connect via WebSocket, send audio frames and events, and receive streaming audio responses. The API manages session state, conversation items, and turn detection. Client secrets are obtained via REST before establishing WebSocket connections.

## Key Facts

- **Protocol**: WebSocket [VERIFIED]
- **Audio format**: PCM16, 24kHz [VERIFIED]
- **Voice activity detection**: Built-in [VERIFIED]
- **Models**: gpt-4o-realtime-preview [VERIFIED]

## Use Cases

- **Voice assistants**: Real-time conversational AI
- **Phone systems**: AI-powered phone agents
- **Accessibility**: Voice interfaces for applications
- **Gaming**: Real-time NPC dialogue

## Quick Reference

### Endpoints

- `POST /v1/realtime/sessions` - Create session (get client secret)
- WebSocket: `wss://api.openai.com/v1/realtime`

### Client Events (send)

- `session.update` - Configure session
- `input_audio_buffer.append` - Send audio
- `input_audio_buffer.commit` - Finalize audio input
- `conversation.item.create` - Add item
- `response.create` - Trigger response

### Server Events (receive)

- `session.created` - Session started
- `conversation.item.created` - Item added
- `response.audio.delta` - Audio chunk
- `response.done` - Response complete
- `error` - Error occurred

## Connection Flow

1. Create session via REST to get client secret
2. Connect WebSocket with client secret
3. Configure session with `session.update`
4. Send audio with `input_audio_buffer.append`
5. Receive responses via server events

## Request Examples

### Get Client Secret (Python)

```python
from openai import OpenAI

client = OpenAI()

session = client.realtime.sessions.create(
    model="gpt-4o-realtime-preview",
    voice="alloy"
)

client_secret = session.client_secret.value
print(f"Connect with: {client_secret}")
```

### WebSocket Connection (JavaScript)

```javascript
const ws = new WebSocket(
  "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview",
  {
    headers: {
      "Authorization": `Bearer ${clientSecret}`,
      "OpenAI-Beta": "realtime=v1"
    }
  }
);

ws.onopen = () => {
  // Configure session
  ws.send(JSON.stringify({
    type: "session.update",
    session: {
      voice: "alloy",
      instructions: "You are a helpful assistant.",
      turn_detection: { type: "server_vad" }
    }
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  if (data.type === "response.audio.delta") {
    // Play audio delta
    playAudio(data.delta);
  }
};
```

### Send Audio

```javascript
// Append audio chunk (base64 PCM16)
ws.send(JSON.stringify({
  type: "input_audio_buffer.append",
  audio: base64AudioChunk
}));

// Commit when done speaking
ws.send(JSON.stringify({
  type: "input_audio_buffer.commit"
}));

// Or let VAD detect automatically
```

## Session Configuration

```json
{
  "type": "session.update",
  "session": {
    "modalities": ["text", "audio"],
    "voice": "alloy",
    "instructions": "You are a helpful voice assistant.",
    "input_audio_format": "pcm16",
    "output_audio_format": "pcm16",
    "turn_detection": {
      "type": "server_vad",
      "threshold": 0.5,
      "prefix_padding_ms": 300,
      "silence_duration_ms": 500
    },
    "tools": [...]
  }
}
```

## Error Codes

- WebSocket close codes indicate errors
- `error` events contain details

## Gotchas and Quirks

- Audio must be PCM16 at 24kHz
- Client secrets expire after use
- VAD threshold affects turn detection sensitivity
- Function calls pause audio output

## Related Endpoints

- `_INFO_OAIAPI_REALTIME_SESSIONS.md` - Session creation
- `_INFO_OAIAPI_REALTIME_CLIENT_EVENTS.md` - Client event reference
- `_INFO_OAIAPI_REALTIME_SERVER_EVENTS.md` - Server event reference

## Sources

- OAIAPI-IN01-SC-OAI-REALTIME - Official realtime documentation

## Document History

**[2026-01-30 10:30]**
- Initial documentation created
