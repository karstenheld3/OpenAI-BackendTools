# JSON Coding Conventions

Rules for writing JSON configuration and data files.

## Principle

**ASANAPAP**: As Short As Necessary, As Precise As Possible.

JSON files should be minimal but unambiguous. Avoid abbreviations in field names.

## Field Naming

- **Spell out field names** - No abbreviations
  - BAD: `temp_factor`, `max_tok`, `cfg`
  - GOOD: `temperature_factor`, `max_tokens`, `config`
- **Use snake_case** for field names
  - BAD: `temperatureFactor`, `MaxTokens`
  - GOOD: `temperature_factor`, `max_tokens`
- **Prefix provider-specific fields** with provider name
  - BAD: `effort`, `thinking_factor`
  - GOOD: `openai_reasoning_effort`, `anthropic_thinking_factor`

## Formatting

- **2-space indentation** - Use 2 spaces, not 4 or tabs
- **2D tables: one line = one row** - For mapping tables, align columns and keep each row on single line
  ```json
  "effort_mapping": {
    "none":    { "temperature_factor": 0.0,  "openai_effort": "none",    "output_factor": 0.25 },
    "minimal": { "temperature_factor": 0.1,  "openai_effort": "minimal", "output_factor": 0.5 },
    "low":     { "temperature_factor": 0.2,  "openai_effort": "low",     "output_factor": 0.5 }
  }
  ```
- **Align columns** for readability when rows have same structure

## Structure

- **Separate concerns** into distinct files when appropriate
  - Model properties → `model-registry.json`
  - Parameter mappings → `model-parameter-mapping.json`
- **Use comments via `_comment` field** for inline documentation
  - `"_comment": "Factor of model's max_output"`
- **Include metadata fields** at top
  - `_version`, `_updated`, `_comment`

## Values

- **Use `null`** for "not set" / "disabled by default"
  - BAD: `"seed": 0` or omitting the field
  - GOOD: `"seed": null`
- **Use factors (0.0-1.0)** for values that depend on model limits
  - Allows same config to work across models with different capacities
