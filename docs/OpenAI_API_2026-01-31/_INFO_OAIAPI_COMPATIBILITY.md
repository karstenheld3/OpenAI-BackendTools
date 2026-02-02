# INFO: OpenAI API - Backward Compatibility

**Doc ID**: OAIAPI-IN05
**Goal**: Document versioning policy and backward compatibility guarantees
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `__OAIAPI_SOURCES.md [OAIAPI-IN01]` for source references

## Summary

OpenAI is committed to providing stability for API users by avoiding breaking changes in major API versions whenever reasonably possible. This stability applies to the REST API (currently v1), official SDKs (which follow semantic versioning), and model families (like gpt-4o or o4-mini). However, model prompting behavior between snapshots is subject to change since model outputs are inherently variable. Users should use pinned model versions and implement evals to ensure consistent behavior. Certain changes are considered backward-compatible and may be introduced without version bumps, including adding new endpoints, optional parameters, response properties, and event types. The changelog documents both compatible changes and rare breaking changes.

## Key Facts

- **REST API version**: v1 (stable) [VERIFIED]
- **SDK versioning**: Semantic versioning [VERIFIED]
- **Model families**: Stable (e.g., gpt-4o, o4-mini) [VERIFIED]
- **Model snapshots**: Behavior may change between versions [VERIFIED]
- **Changelog**: https://platform.openai.com/docs/changelog [VERIFIED]

## Use Cases

- **Version pinning**: Use specific model snapshots (e.g., `gpt-4o-2024-08-06`) for consistent behavior
- **Migration planning**: Check changelog before updating SDK versions
- **Testing**: Implement evals to detect behavior changes between model versions

## Quick Reference

### Stable Components

- REST API version (v1)
- First-party SDK major versions
- Model family aliases (gpt-4o, o4-mini)

### Variable Components

- Model prompting behavior between snapshots
- Model output formatting and style
- Specific response content

### Backward-Compatible Changes (No Version Bump)

- Adding new resources (URLs) to the REST API and SDKs
- Adding new optional API parameters
- Adding new properties to JSON response objects or event data
- Changing the order of properties in a JSON response object
- Changing the length or format of opaque strings (resource IDs, UUIDs)
- Adding new event types (streaming, Realtime API)

## Model Version Strategy

### Aliases vs Pinned Versions

- **Alias** (e.g., `gpt-4o`): Points to latest snapshot, auto-updates
- **Pinned** (e.g., `gpt-4o-2024-08-06`): Fixed behavior, no updates

### Best Practices

- Use aliases for development and experimentation
- Use pinned versions for production systems requiring consistency
- Implement evals to validate behavior when updating versions
- Monitor changelog for deprecation notices

## Gotchas and Quirks

- Same prompt may produce different outputs between model snapshots
- JSON property order in responses may change (don't rely on order)
- New properties may appear in responses (handle gracefully)
- Resource ID formats may change (treat as opaque strings)

## Related Endpoints

- `_INFO_OAIAPI_MODELS.md` - List and describe available models

## Sources

- OAIAPI-IN01-SC-OAI-COMPAT - Official backward compatibility documentation
- OAIAPI-IN01-SC-OAI-CHANGELOG - API changelog

## Document History

**[2026-01-30 09:25]**
- Initial documentation created from API reference
