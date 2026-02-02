# INFO: OpenAI API - Realtime Server Events

**Doc ID**: OAIAPI-IN44
**Goal**: Document server-to-client events for Realtime API
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `_INFO_OAIAPI_REALTIME.md [OAIAPI-IN26]` for context

## Summary

Server events are WebSocket messages sent from the Realtime API server to the client. They communicate session state, conversation updates, audio output, and errors.

## Key Facts

- **Protocol**: JSON over WebSocket [VERIFIED]
- **Direction**: Server → Client [VERIFIED]

## Event Reference

### Session Events

- `session.created` - Session established
- `session.updated` - Session config changed
- `error` - Error occurred

### Conversation Events

- `conversation.created` - Conversation started
- `conversation.item.created` - Item added
- `conversation.item.truncated` - Item truncated
- `conversation.item.deleted` - Item deleted
- `input_audio_buffer.committed` - Audio committed
- `input_audio_buffer.cleared` - Buffer cleared
- `input_audio_buffer.speech_started` - VAD detected speech
- `input_audio_buffer.speech_stopped` - VAD detected silence

### Response Events

- `response.created` - Response started
- `response.done` - Response complete
- `response.output_item.added` - Output item started
- `response.output_item.done` - Output item complete
- `response.content_part.added` - Content part started
- `response.content_part.done` - Content part complete
- `response.text.delta` - Text chunk
- `response.text.done` - Text complete
- `response.audio.delta` - Audio chunk (base64)
- `response.audio.done` - Audio complete
- `response.audio_transcript.delta` - Transcript chunk
- `response.audio_transcript.done` - Transcript complete
- `response.function_call_arguments.delta` - Function args chunk
- `response.function_call_arguments.done` - Function call complete

### Rate Limiting

- `rate_limits.updated` - Rate limit info

## Event Examples

### Session Created

```json
{
  "type": "session.created",
  "session": {
    "id": "sess_abc123",
    "voice": "alloy",
    "model": "gpt-4o-realtime-preview"
  }
}
```

### Audio Delta

```json
{
  "type": "response.audio.delta",
  "response_id": "resp_123",
  "item_id": "item_456",
  "delta": "base64-audio-chunk..."
}
```

### Error

```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "Invalid audio format"
  }
}
```

## Sources

- OAIAPI-IN01-SC-OAI-RTSERVER - Official realtime server events documentation

## Document History

**[2026-01-30 11:15]**
- Initial documentation created
