# INFO: OpenAI API - Conversations

**Doc ID**: OAIAPI-IN28
**Goal**: Document Conversations API for Responses
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `_INFO_OAIAPI_RESPONSES.md [OAIAPI-IN11]` for context

## Summary

The Conversations API manages multi-turn conversation state for the Responses API. By providing `previous_response_id` when creating a new response, conversations are automatically linked and context is maintained. This enables stateful conversations without manually managing message history. Conversations can be listed and individual responses retrieved to reconstruct conversation history.

## Key Facts

- **State management**: Via `previous_response_id` [VERIFIED]
- **Context**: Automatically maintained across responses [VERIFIED]
- **Retrieval**: List all responses in a conversation [VERIFIED]

## Quick Reference

### Linking Responses

```python
from openai import OpenAI

client = OpenAI()

# First message
response1 = client.responses.create(
    model="gpt-4o",
    input="My name is Alice."
)

# Continue conversation
response2 = client.responses.create(
    model="gpt-4o",
    input="What is my name?",
    previous_response_id=response1.id
)
# Model knows the name from context
```

### List Conversation

```python
# Get all responses in conversation
responses = client.responses.list(
    conversation_id=response1.id
)
```

## Sources

- OAIAPI-IN01-SC-OAI-CONV - Official conversations documentation

## Document History

**[2026-01-30 10:35]**
- Initial documentation created
