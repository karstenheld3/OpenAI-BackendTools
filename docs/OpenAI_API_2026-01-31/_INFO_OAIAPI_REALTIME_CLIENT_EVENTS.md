# INFO: OpenAI API - Realtime Client Events

**Doc ID**: OAIAPI-IN43
**Goal**: Document client-to-server events for Realtime API
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `_INFO_OAIAPI_REALTIME.md [OAIAPI-IN26]` for context

## Summary

Client events are WebSocket messages sent from the client to the Realtime API server. They control session configuration, audio input, conversation items, and response generation.

## Key Facts

- **Protocol**: JSON over WebSocket [VERIFIED]
- **Direction**: Client → Server [VERIFIED]

## Event Reference

### Session Events

- `session.update` - Update session configuration (voice, instructions, tools)

### Audio Input Events

- `input_audio_buffer.append` - Append audio data (base64 PCM16)
- `input_audio_buffer.commit` - Commit audio buffer as user input
- `input_audio_buffer.clear` - Clear audio buffer

### Conversation Events

- `conversation.item.create` - Add item to conversation
- `conversation.item.truncate` - Truncate item
- `conversation.item.delete` - Delete item

### Response Events

- `response.create` - Request model response
- `response.cancel` - Cancel in-progress response

## Event Examples

### Session Update

```json
{
  "type": "session.update",
  "session": {
    "voice": "alloy",
    "instructions": "You are helpful.",
    "turn_detection": {
      "type": "server_vad",
      "threshold": 0.5
    }
  }
}
```

### Append Audio

```json
{
  "type": "input_audio_buffer.append",
  "audio": "base64-encoded-pcm16-audio..."
}
```

### Create Response

```json
{
  "type": "response.create",
  "response": {
    "modalities": ["text", "audio"]
  }
}
```

## Sources

- OAIAPI-IN01-SC-OAI-RTCLIENT - Official realtime client events documentation

## Document History

**[2026-01-30 11:15]**
- Initial documentation created
