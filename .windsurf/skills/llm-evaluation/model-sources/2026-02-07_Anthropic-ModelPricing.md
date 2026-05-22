<transcription_page_header> Claude API Docs | Pricing </transcription_page_header>

# Pricing

Models & pricing

Learn about Anthropic’s pricing structure for models and features

This page provides detailed pricing information for Anthropic’s models and features. All prices are in USD.

For the most current pricing information, please visit claude.com/pricing.

<!-- Section 1 -->
<!-- Column 1 -->
<!-- Left navigation column (not transcribed; decorative) -->

<!-- Column 2 -->
## Model pricing

The following table shows pricing for all Claude models across different usage tiers:

<transcription_table>
**Model pricing**

| Model | Base Input Tokens | 5m Cache Writes | 1h Cache Writes | Cache Hits & Refreshes | Output Tokens |
|-------|-------------------:|----------------:|----------------:|-----------------------:|--------------:|
| Claude Opus 4.6 | $5 / MTok | $6.25 / MTok | $10 / MTok | $0.50 / MTok | $25 / MTok |
| Claude Opus 4.5 | $5 / MTok | $6.25 / MTok | $10 / MTok | $0.50 / MTok | $25 / MTok |
| Claude Opus 4.1 | $15 / MTok | $18.75 / MTok | $30 / MTok | $1.50 / MTok | $75 / MTok |
| Claude Opus 4 | $15 / MTok | $18.75 / MTok | $30 / MTok | $1.50 / MTok | $75 / MTok |
| Claude Sonnet 4.5 | $3 / MTok | $3.75 / MTok | $6 / MTok | $0.30 / MTok | $15 / MTok |
| Claude Sonnet 4 | $3 / MTok | $3.75 / MTok | $6 / MTok | $0.30 / MTok | $15 / MTok |
| Claude Sonnet 3.7 (deprecated) | $3 / MTok | $3.75 / MTok | $6 / MTok | $0.30 / MTok | $15 / MTok |
| Claude Haiku 4.5 | $1 / MTok | $1.25 / MTok | $2 / MTok | $0.10 / MTok | $5 / MTok |
| Claude Haiku 3.5 | $0.80 / MTok | $1 / MTok | $1.6 / MTok | $0.08 / MTok | $4 / MTok |

<transcription_json>
{"table_type":"data_table","title":"Model pricing","columns":["Model","Base Input Tokens","5m Cache Writes","1h Cache Writes","Cache Hits & Refreshes","Output Tokens"],"data":[{"Model":"Claude Opus 4.6","Base Input Tokens":"$5 / MTok","5m Cache Writes":"$6.25 / MTok","1h Cache Writes":"$10 / MTok","Cache Hits & Refreshes":"$0.50 / MTok","Output Tokens":"$25 / MTok"},{"Model":"Claude Opus 4.5","Base Input Tokens":"$5 / MTok","5m Cache Writes":"$6.25 / MTok","1h Cache Writes":"$10 / MTok","Cache Hits & Refreshes":"$0.50 / MTok","Output Tokens":"$25 / MTok"},{"Model":"Claude Opus 4.1","Base Input Tokens":"$15 / MTok","5m Cache Writes":"$18.75 / MTok","1h Cache Writes":"$30 / MTok","Cache Hits & Refreshes":"$1.50 / MTok","Output Tokens":"$75 / MTok"},{"Model":"Claude Opus 4","Base Input Tokens":"$15 / MTok","5m Cache Writes":"$18.75 / MTok","1h Cache Writes":"$30 / MTok","Cache Hits & Refreshes":"$1.50 / MTok","Output Tokens":"$75 / MTok"},{"Model":"Claude Sonnet 4.5","Base Input Tokens":"$3 / MTok","5m Cache Writes":"$3.75 / MTok","1h Cache Writes":"$6 / MTok","Cache Hits & Refreshes":"$0.30 / MTok","Output Tokens":"$15 / MTok"},{"Model":"Claude Sonnet 4","Base Input Tokens":"$3 / MTok","5m Cache Writes":"$3.75 / MTok","1h Cache Writes":"$6 / MTok","Cache Hits & Refreshes":"$0.30 / MTok","Output Tokens":"$15 / MTok"},{"Model":"Claude Sonnet 3.7 (deprecated)","Base Input Tokens":"$3 / MTok","5m Cache Writes":"$3.75 / MTok","1h Cache Writes":"$6 / MTok","Cache Hits & Refreshes":"$0.30 / MTok","Output Tokens":"$15 / MTok"},{"Model":"Claude Haiku 4.5","Base Input Tokens":"$1 / MTok","5m Cache Writes":"$1.25 / MTok","1h Cache Writes":"$2 / MTok","Cache Hits & Refreshes":"$0.10 / MTok","Output Tokens":"$5 / MTok"},{"Model":"Claude Haiku 3.5","Base Input Tokens":"$0.80 / MTok","5m Cache Writes":"$1 / MTok","1h Cache Writes":"$1.6 / MTok","Cache Hits & Refreshes":"$0.08 / MTok","Output Tokens":"$4 / MTok"}],"unit":"USD per MTok"}
</transcription_json>

<transcription_notes>
- Table type: pricing table for Claude models.
- Columns left-to-right: Model, Base Input Tokens, 5m Cache Writes, 1h Cache Writes, Cache Hits & Refreshes, Output Tokens.
- Units: USD per MTok (price per million tokens). Where visible, values include cents/decimals exactly as shown.
- Visual context: central content column on a light beige background; left navigation column and right sidebar contain links (not transcribed). Table rows have subtle horizontal separators; typographic emphasis on model names.
</transcription_notes>
</transcription_table>

<!-- Section 2 -->
<!-- Right column (sidebar: model pricing links and additional topics; decorative) -->

<transcription_page_footer> Page 1 | Anthropic </transcription_page_footer>
<transcription_page_header> [unclear] | Pricing </transcription_page_header>

# [unclear]

<!-- Section 1 -->
<!-- Column 1 -->
[Navigation column — omitted (left-side site navigation visible in image)]

<!-- Column 2 -->
## Third-party platform pricing

Claude models are available on AWS Bedrock, Google Vertex AI, and Microsoft Foundry.  
For official pricing, visit:

- AWS Bedrock pricing
- Google Vertex AI pricing
- Microsoft Foundry pricing

<transcription_image>
**Figure 1: Prompt caching pricing notes (info box visible above the "Third-party platform pricing" heading)**

```ascii
[INFO BOX]
ℹ️ MTok = Million tokens. The "Base Input Tokens" column shows standard input pricing,
"Cache Writes" and "Cache Hits" are specific to prompt caching, and "Output Tokens"
shows output pricing. Prompt caching offers both 5-minute (default) and 1-hour cache
durations to optimize costs for different use cases.

The table above reflects the following pricing multipliers for prompt caching:

• 5-minute cache write tokens are 1.25 times the base input tokens price
• 1-hour cache write tokens are 2 times the base input tokens price
• Cache read tokens are 0.1 times the base input tokens price
```

<transcription_json>
{"box_type":"info_box","title":"MTok = Million tokens","content":"The \"Base Input Tokens\" column shows standard input pricing, \"Cache Writes\" and \"Cache Hits\" are specific to prompt caching, and \"Output Tokens\" shows output pricing. Prompt caching offers both 5-minute (default) and 1-hour cache durations to optimize costs for different use cases.","bullets":[{"text":"5-minute cache write tokens are 1.25 times the base input tokens price","multiplier":1.25},{"text":"1-hour cache write tokens are 2 times the base input tokens price","multiplier":2.0},{"text":"Cache read tokens are 0.1 times the base input tokens price","multiplier":0.1}],"notes":"This info box appears visually as a light-blue rounded rectangle with a darker-blue header border and an information icon on the top-left."}
</transcription_json>

<transcription_notes>
- Type: informational callout / info box
- Visual: light blue background, darker blue rounded border, small circled info icon at top-left
- Position on page: centered in the main content column above "Third-party platform pricing"
- The ASCII block preserves wording and bullet multipliers; graphical styling (shades, padding, icon) not captured exactly.
</transcription_notes>
</transcription_image>

<!-- Section 2 -->
<!-- Column 1 -->
[Main content continued]

<transcription_image>
**Figure 2: Regional endpoint pricing for Claude 4.5 models and beyond (blue info box below the third-party links)**

```ascii
[INFO BOX]
ℹ️ Regional endpoint pricing for Claude 4.5 models and beyond

Starting with Claude Sonnet 4.5 and Haiku 4.5, AWS Bedrock and Google Vertex AI offer
two endpoint types:

• Global endpoints: Dynamic routing across regions for maximum availability
• Regional endpoints: Data routing guaranteed within specific geographic regions

Regional endpoints include a 10% premium over global endpoints. The Claude API (1P)
is global by default and unaffected by this change. The Claude API is global-only
(equivalent to the global endpoint offering and pricing from other providers).

Scope: This pricing structure applies to Claude Sonnet 4.5, Haiku 4.5, and all future
models. Earlier models (Claude Sonnet 4, Opus 4, and prior releases) retain their
existing pricing.

For implementation details and code examples:
[links not fully visible in image]
```

<transcription_json>
{"box_type":"info_box","title":"Regional endpoint pricing for Claude 4.5 models and beyond","content":"Starting with Claude Sonnet 4.5 and Haiku 4.5, AWS Bedrock and Google Vertex AI offer two endpoint types: Global endpoints and Regional endpoints. Regional endpoints include a 10% premium over global endpoints. The Claude API (1P) is global by default and unaffected by this change. The Claude API is global-only (equivalent to the global endpoint offering and pricing from other providers).","bullets":[{"label":"Global endpoints","description":"Dynamic routing across regions for maximum availability"},{"label":"Regional endpoints","description":"Data routing guaranteed within specific geographic regions"},{"label":"Regional premium","description":"Regional endpoints include a 10% premium over global endpoints","value":"10%"}],"scope":"This pricing structure applies to Claude Sonnet 4.5, Haiku 4.5, and all future models. Earlier models (Claude Sonnet 4, Opus 4, and prior releases) retain their existing pricing.","notes":"The bottom of this info box contains links and further implementation details; some link text is partially out of frame and marked as [unclear] where not fully visible."}
</transcription_json>

<transcription_notes>
- Type: informational callout / info box
- Visual: large light-blue rounded rectangle with darker-blue border and circled info icon at top-left
- Location: main content column below the third-party platform links
- Exact links at the bottom are partially out of frame; visible heading and core bullets are fully legible
</transcription_notes>
</transcription_image>

<!-- Decorative: Ask Docs floating button (bottom-right) -->

<transcription_page_footer> Page [unclear] | [unclear] </transcription_page_footer>
<transcription_page_header> Feature-specific pricing | Pricing </transcription_page_header>

<!-- Section 1 -->
<!-- Column 1 -->
Agent Skills

Overview  
Quickstart  
Best practices  
Skills for enterprise  
Using Skills with the API

Agent SDK

Overview  
Quickstart  
TypeScript SDK  
TypeScript V2 (preview)  
Python SDK  
Migration Guide  
Guides

MCP in the API

MCP connector  
Remote MCP servers

Claude on 3rd-party platforms

Amazon Bedrock  
Microsoft Foundry  
Vertex AI

Prompt engineering

Overview  
Prompt generator  
Use prompt templates  
Prompt improver  
Be clear and direct

<!-- Column 2 -->
# Feature-specific pricing

## Data residency pricing

For Claude Opus 4.6 and newer models, specifying US-only inference via the `inference_geo` parameter incurs a 1.1x multiplier on all token pricing categories, including input tokens, output tokens, cache writes, and cache reads. Global routing (the default) uses standard pricing.

This applies to the Claude API (1P) only. Third-party platforms have their own regional pricing — see AWS Bedrock, Google Vertex AI, and Microsoft Foundry for details. Earlier models retain their existing pricing regardless of `inference_geo` settings.

For more information, see our data residency documentation.

## Batch processing

The Batch API allows asynchronous processing of large volumes of requests with a 50% discount on both input and output tokens.

<transcription_table>
**Table: Batch processing**

| Model | Batch input | Batch output |
|-------|-------------:|-------------:|
| Claude Opus 4.6 | $2.50 / MTok | $12.50 / MTok |
| Claude Opus 4.5 | $2.50 / MTok | $12.50 / MTok |
| Claude Opus 4.1 | $7.50 / MTok | $37.50 / MTok |
| Claude Opus 4 | $7.50 / MTok | $37.50 / MTok |
| Claude Sonnet 4.5 | $1.50 / MTok | $7.50 / MTok |
| Claude Sonnet 4 | $1.50 / MTok | $7.50 / MTok |
| Claude Sonnet 3.7 (deprecated) | $1.50 / MTok | $7.50 / MTok |
| Claude Haiku 4.5 | $0.50 / MTok | $2.50 / MTok |
| Claude Haiku 3.5 | $0.40 / MTok | $2 / MTok |
| Claude Opus 3 (deprecated) | $7.50 / MTok | $37.50 / MTok |
| Claude Haiku 3 | $0.125 / MTok | $0.625 / MTok |

<transcription_json>
{"table_type": "data_table", "title": "Batch processing", "columns": ["Model", "Batch input", "Batch output"], "data": [{"Model":"Claude Opus 4.6","Batch input":2.50,"Batch output":12.50,"unit":"$/MTok"},{"Model":"Claude Opus 4.5","Batch input":2.50,"Batch output":12.50,"unit":"$/MTok"},{"Model":"Claude Opus 4.1","Batch input":7.50,"Batch output":37.50,"unit":"$/MTok"},{"Model":"Claude Opus 4","Batch input":7.50,"Batch output":37.50,"unit":"$/MTok"},{"Model":"Claude Sonnet 4.5","Batch input":1.50,"Batch output":7.50,"unit":"$/MTok"},{"Model":"Claude Sonnet 4","Batch input":1.50,"Batch output":7.50,"unit":"$/MTok"},{"Model":"Claude Sonnet 3.7 (deprecated)","Batch input":1.50,"Batch output":7.50,"unit":"$/MTok","deprecated":true},{"Model":"Claude Haiku 4.5","Batch input":0.50,"Batch output":2.50,"unit":"$/MTok"},{"Model":"Claude Haiku 3.5","Batch input":0.40,"Batch output":2.00,"unit":"$/MTok"},{"Model":"Claude Opus 3 (deprecated)","Batch input":7.50,"Batch output":37.50,"unit":"$/MTok","deprecated":true},{"Model":"Claude Haiku 3","Batch input":0.125,"Batch output":0.625,"unit":"$/MTok"}], "unit":"$/MTok"}
</transcription_json>

<transcription_notes>
- Table Title: "Batch processing"
- Visual: three-column table; left column model names (text, left-aligned), right two columns numeric pricing (right-aligned).
- Deprecated models are visually marked with "(deprecated)" in the model name.
- Units shown in-table as "$X / MTok".
- Styling: light horizontal separators between rows, ample whitespace; numbers aligned to the right.
</transcription_notes>
</transcription_table>
<transcription_page_header>Long context pricing | Pricing</transcription_page_header>

<!-- Decorative: [left navigation menu with links such as "Test & evaluate", "Strengthen guardrails", "Administration and monitoring", etc.] -->

# Long context pricing

When using Claude Opus 4.6, Sonnet 4.5, or Sonnet 4 with the 1M token context window enabled, requests that exceed 200K input tokens are automatically charged at premium long context rates:

<transcription_image>
**Figure 1: Beta availability info box**

```ascii
[INFO BOX - BETA AVAILABILITY]
i  The 1M token context window is currently in beta for organizations in usage tier 4 and
   organizations with custom rate limits. The 1M token context window is only available for
   Claude Opus 4.6, Sonnet 4.5, and Sonnet 4.
```

<transcription_json>
{"figure_type":"info_box","title":"Beta availability","text":"The 1M token context window is currently in beta for organizations in usage tier 4 and organizations with custom rate limits. The 1M token context window is only available for Claude Opus 4.6, Sonnet 4.5, and Sonnet 4.","icon":"info"}
</transcription_json>

<transcription_notes>
- Visual: blue rounded rectangle with an "i" info icon on the left.
- Color: light blue background, darker blue border.
- Purpose: highlights beta availability and eligibility for the 1M token context window.
</transcription_notes>
</transcription_image>

<!-- Section 1 -->
<!-- Column 1 -->
**Model pricing table**

<transcription_table>
**Table 1: Long context pricing by model**

| Model | ≤ 200K input tokens | > 200K input tokens |
|-------|---------------------|----------------------|
| Claude Opus 4.6 | Input: $5 / MTok<br>Output: $25 / MTok | Input: $10 / MTok<br>Output: $37.50 / MTok |
| Claude Sonnet 4.5 / 4 | Input: $3 / MTok<br>Output: $15 / MTok | Input: $6 / MTok<br>Output: $22.50 / MTok |

<transcription_json>
{"table_type":"data_table","title":"Long context pricing by model","columns":["Model","≤ 200K input tokens"," > 200K input tokens"],"data":[{"Model":"Claude Opus 4.6","≤ 200K input tokens":"Input: $5 / MTok; Output: $25 / MTok"," > 200K input tokens":"Input: $10 / MTok; Output: $37.50 / MTok"},{"Model":"Claude Sonnet 4.5 / 4","≤ 200K input tokens":"Input: $3 / MTok; Output: $15 / MTok"," > 200K input tokens":"Input: $6 / MTok; Output: $22.50 / MTok"}],"unit":"price per million tokens (MTok)"}
</transcription_json>

<transcription_notes>
- Table shows separate input and output rates per model and per input-token threshold.
- Unit: dollars per MTok (million tokens).
- Visual: table with subtle row separators and plain text pricing; no additional icons.
</transcription_notes>
</transcription_table>

Long context pricing stacks with other pricing modifiers:

- The Batch API 50% discount applies to long context pricing
- Prompt caching multipliers apply on top of long context pricing
- The data residency 1.1x multiplier applies on top of long context pricing

<transcription_image>
**Figure 2: Pricing clarification info box**

```ascii
[INFO BOX - PRICING CLARIFICATION]
i  Even with the beta flag enabled, requests with fewer than 200K input tokens are charged
   at standard rates. If your request exceeds 200K input tokens, all tokens incur premium
   pricing.

   The 200K threshold is based solely on input tokens (including cache reads/writes).
   Output token count does not affect pricing tier selection, though output tokens are charged
   at the higher rate when the input threshold is exceeded.
```

<transcription_json>
{"figure_type":"info_box","title":"Pricing clarification","text":"Even with the beta flag enabled, requests with fewer than 200K input tokens are charged at standard rates. If your request exceeds 200K input tokens, all tokens incur premium pricing.\n\nThe 200K threshold is based solely on input tokens (including cache reads/writes). Output token count does not affect pricing tier selection, though output tokens are charged at the higher rate when the input threshold is exceeded.","icon":"info"}
</transcription_json>

<transcription_notes>
- Visual: second blue rounded rectangle with an "i" icon; same styling as the first info box.
- Purpose: clarifies threshold behavior and how output tokens are charged.
</transcription_notes>
</transcription_image>

To check if your API request was charged at the 1M context window rates, examine the usage object in the API response:

```json
{
  "usage": {
    "input_tokens": [unclear: 250000?],
    "output_tokens": [unclear],
    "total_tokens": [unclear]
  }
}
```

<!-- Section End -->

<transcription_page_footer>Page [unclear] | Documentation</transcription_page_footer>
<transcription_page_header> Calculate input tokens | Tool use pricing </transcription_page_header>

<!-- Section 1 -->
Calculate the total input tokens by summing:

- `input_tokens`
- `cache_creation_input_tokens` (if using prompt caching)
- `cache_read_input_tokens` (if using prompt caching)

If the total exceeds 200,000 tokens, the entire request was billed at 1M context rates.

For more information about the `usage` object, see the API response documentation.

## Tool use pricing

Tool use requests are priced based on:

1. The total number of input tokens sent to the model (including in the `tools` parameter)
2. The number of output tokens generated
3. For server-side tools, additional usage-based pricing (e.g., web search charges per search performed)

Client-side tools are priced the same as any other Claude API request, while server-side tools may incur additional charges based on their specific usage.

The additional tokens from tool use come from:

- The `tools` parameter in API requests (tool names, descriptions, and schemas)
- `tool_use` content blocks in API requests and responses
- `tool_result` content blocks in API requests

When you use `tools`, we also automatically include a special system prompt for the model which enables tool use. The number of tool use tokens required for each model are listed below (excluding the additional tokens listed above). Note that the table assumes at least 1 tool is provided. If no `tools` are provided, then a tool choice of `none` uses 0 additional system prompt tokens.

<!-- Section 2 -->
**Model**  | **Tool choice** | **Tool use system prompt token count**
:---------:|:---------------:|:------------------------------------
[unclear]  | [unclear]       | [unclear]

<transcription_table>
**Table: Tool use system prompt token counts (page partially visible)**

| Model | Tool choice | Tool use system prompt token count |
|-------|-------------|------------------------------------|
| [unclear: partial row visible on page] | [unclear] | [unclear] |

<transcription_json>
{"table_type":"data_table","title":"Tool use system prompt token counts (partial)","columns":["Model","Tool choice","Tool use system prompt token count"],"data":[{"Model":"[unclear: partial row visible]","Tool choice":"[unclear]","Tool use system prompt token count":"[unclear]"}],"notes":"Table is partially visible on the scanned page; full rows/values are cut off."}
</transcription_json>

<transcription_notes>
- Visual: A table header with three columns is visible: "Model", "Tool choice", "Tool use system prompt token count".
- Only the top of the table is visible; subsequent rows are cut off by the image bottom edge.
- Colors/formatting: standard documentation table style (header bold). Right-side floating UI ("Ask Docs") is decorative and omitted.
- Source context: Documentation page about token billing and tool use pricing.
</transcription_notes>
</transcription_table>

<transcription_page_footer> Page [unclear] | [unclear: Company/Docs] </transcription_page_footer>
<!-- Decorative: right-side scrollbar, "Ask Docs" floating button -->

<!-- Section 1 -->

<transcription_table>
**Table: Model token counts**

| Model | Mode | Tokens |
|-------|------|--------|
| Claude Opus 4.6 | auto , none | 346 tokens |
| Claude Opus 4.6 | any , tool | 313 tokens |
| Claude Opus 4.5 | auto , none | 346 tokens |
| Claude Opus 4.5 | any , tool | 313 tokens |
| Claude Opus 4.1 | auto , none | 346 tokens |
| Claude Opus 4.1 | any , tool | 313 tokens |
| Claude Opus 4 | auto , none | 346 tokens |
| Claude Opus 4 | any , tool | 313 tokens |
| Claude Sonnet 4.5 | auto , none | 346 tokens |
| Claude Sonnet 4.5 | any , tool | 313 tokens |
| Claude Sonnet 4 | auto , none | 346 tokens |
| Claude Sonnet 4 | any , tool | 313 tokens |
| Claude Sonnet 3.7 (deprecated) | auto , none | 346 tokens |
| Claude Sonnet 3.7 (deprecated) | any , tool | 313 tokens |
| Claude Haiku 4.5 | auto , none | 346 tokens |
| Claude Haiku 4.5 | any , tool | 313 tokens |
| Claude Haiku 3.5 | auto , none | 264 tokens |
| Claude Haiku 3.5 | any , tool | 340 tokens |
| Claude Opus 3 (deprecated) | auto , none | 530 tokens |
| Claude Opus 3 (deprecated) | any , tool | 281 tokens |
| Claude Sonnet 3 | auto , none | 159 tokens |
| Claude Sonnet 3 | any , tool | 235 tokens |
| Claude Haiku 3 | auto , none | 264 tokens |
| Claude Haiku 3 | any , tool | 340 tokens |

<transcription_json>
{"table_type":"data_table","title":"Model token counts","columns":["Model","Mode","Tokens"],"data":[{"Model":"Claude Opus 4.6","Mode":"auto , none","Tokens":346},{"Model":"Claude Opus 4.6","Mode":"any , tool","Tokens":313},{"Model":"Claude Opus 4.5","Mode":"auto , none","Tokens":346},{"Model":"Claude Opus 4.5","Mode":"any , tool","Tokens":313},{"Model":"Claude Opus 4.1","Mode":"auto , none","Tokens":346},{"Model":"Claude Opus 4.1","Mode":"any , tool","Tokens":313},{"Model":"Claude Opus 4","Mode":"auto , none","Tokens":346},{"Model":"Claude Opus 4","Mode":"any , tool","Tokens":313},{"Model":"Claude Sonnet 4.5","Mode":"auto , none","Tokens":346},{"Model":"Claude Sonnet 4.5","Mode":"any , tool","Tokens":313},{"Model":"Claude Sonnet 4","Mode":"auto , none","Tokens":346},{"Model":"Claude Sonnet 4","Mode":"any , tool","Tokens":313},{"Model":"Claude Sonnet 3.7 (deprecated)","Mode":"auto , none","Tokens":346},{"Model":"Claude Sonnet 3.7 (deprecated)","Mode":"any , tool","Tokens":313},{"Model":"Claude Haiku 4.5","Mode":"auto , none","Tokens":346},{"Model":"Claude Haiku 4.5","Mode":"any , tool","Tokens":313},{"Model":"Claude Haiku 3.5","Mode":"auto , none","Tokens":264},{"Model":"Claude Haiku 3.5","Mode":"any , tool","Tokens":340},{"Model":"Claude Opus 3 (deprecated)","Mode":"auto , none","Tokens":530},{"Model":"Claude Opus 3 (deprecated)","Mode":"any , tool","Tokens":281},{"Model":"Claude Sonnet 3","Mode":"auto , none","Tokens":159},{"Model":"Claude Sonnet 3","Mode":"any , tool","Tokens":235},{"Model":"Claude Haiku 3","Mode":"auto , none","Tokens":264},{"Model":"Claude Haiku 3","Mode":"any , tool","Tokens":340}],"unit":"tokens"}
</transcription_json>

<transcription_notes>
- Layout: single vertical list of model rows (left) with two small pill-style mode labels per model (center) and token counts aligned at right.
- Pill labels: rounded, light beige/gray background with darker text. Two labels per model read exactly "auto , none" (top) and "any , tool" (below) for most models; some models have differing token numbers per label.
- Token counts are plain text to the right of labels, e.g., "346 tokens", "313 tokens", etc. Values are integers representing token counts.
- Visible decorative UI elements omitted: right-side scrollbar, bottom-right "Ask Docs" floating button.
- Source/context: likely a model reference/token-costs section of documentation. Units: tokens.
</transcription_notes>
</transcription_table>

These token counts are added to your normal input and output tokens to calculate the total cost of a request.

For current per-model prices, refer to our model pricing section above.

For more information about tool use implementation and best practices, see our tool use [unclear]
<transcription_page_header> Specific tool pricing </transcription_page_header>

<!-- Section 1 -->
## Specific tool pricing

### Bash tool

The bash tool adds 245 input tokens to your API calls.

Additional tokens are consumed by:

- Command outputs (stdout/stderr)
- Error messages
- Large file contents

See tool use pricing for complete pricing details.

### Code execution tool

Code execution tool usage is tracked separately from token usage. Execution time has a minimum of 5 minutes. If files are included in the request, execution time is billed even if the tool is not used due to files being preloaded onto the container.

Each organization receives 1,550 free hours of usage with the code execution tool per month. Additional usage beyond the first 1,550 hours is billed at $0.05 per hour, per container.

### Text editor tool

The text editor tool uses the same pricing structure as other tools used with Claude. It follows the standard input and output token pricing based on the Claude model you're using.

In addition to the base tokens, the following additional input tokens are needed for the text editor tool:

<transcription_table>
**Table 1: Text editor tool — additional input tokens**

| Tool | Additional input tokens |
|------|-------------------------|
| text_editor_20250429 (Claude 4.x) | 700 tokens |
| text_editor_20250124 (Claude Sonnet 3.7 (deprecated)) | 700 tokens |

<transcription_json>
{"table_type":"data_table","title":"Text editor tool - additional input tokens","columns":["Tool","Additional input tokens"],"data":[{"Tool":"text_editor_20250429 (Claude 4.x)","Additional input tokens":"700 tokens"},{"Tool":"text_editor_20250124 (Claude Sonnet 3.7 (deprecated))","Additional input tokens":"700 tokens"}],"unit":"tokens"}
</transcription_json>

<transcription_notes>
- Visual: Tool names appear in light-gray rounded rectangular code-like boxes on the left column; the "Additional input tokens" column is right-aligned numeric text.
- Table has light horizontal separators and a minimal, neutral color scheme.
- Source context: Pricing documentation page section titled "Specific tool pricing".
</transcription_notes>
</transcription_table>

See tool use pricing for complete pricing details.

<transcription_page_footer> Page [unclear] </transcription_page_footer>
<transcription_page_header> Web search tool | Documentation </transcription_page_header>

# Web search tool

Web search usage is charged in addition to token usage:

<!-- Section 1 -->
<transcription_image>
**Figure 1: Web search usage example (JSON usage object)**

```ascii
"usage": {
  "input_tokens": 105,
  "output_tokens": 6039,
  "cache_read_input_tokens": 7123,
  "cache_creation_input_tokens": 7345,
  "server_tool_use": {
    "web_search_requests": 1
  }
}
```

<transcription_json>
{"chart_type":"code_snippet","title":"Web search usage example","data":{"usage":{"input_tokens":105,"output_tokens":6039,"cache_read_input_tokens":7123,"cache_creation_input_tokens":7345,"server_tool_use":{"web_search_requests":1}}},"format":"JSON"}
</transcription_json>

<transcription_notes>
- Visual: Rounded rectangular light-grey code box with monospace text.
- Colors: keys in teal/green, numbers in black/dark, braces/brackets in grey.
- Context: This JSON snippet represents a usage object returned by a web search request example.
- Location on page: Directly under the "Web search usage is charged in addition to token usage:" sentence.
</transcription_notes>
</transcription_image>

Web search is available on the Claude API for $10 per 1,000 searches, plus standard token costs for search-generated content. Web search results retrieved throughout a conversation are counted as input tokens, in search iterations executed during a single turn and in subsequent conversation turns.

Each web search counts as one use, regardless of the number of results returned. If an error occurs during web search, the web search will not be billed.

<!-- Section 2 -->
## Web fetch tool

Web fetch usage has no additional charges beyond standard token costs:

<transcription_image>
**Figure 2: Web fetch usage example (JSON usage object)**

```ascii
"usage": {
  "input_tokens": 25039,
  "output_tokens": 931,
  "cache_read_input_tokens": 0,
  "cache_creation_input_tokens": 0,
  "server_tool_use": {
    "web_fetch_requests": 1
  }
}
```

<transcription_json>
{"chart_type":"code_snippet","title":"Web fetch usage example","data":{"usage":{"input_tokens":25039,"output_tokens":931,"cache_read_input_tokens":0,"cache_creation_input_tokens":0,"server_tool_use":{"web_fetch_requests":1}}},"format":"JSON"}
</transcription_json>

<transcription_notes>
- Visual: Rounded rectangular light-grey code box with monospace text (same styling as Figure 1).
- Colors: keys in teal/green, numbers in black/dark.
- Context: Example JSON showing usage values for a single web fetch request.
- Notable values: input_tokens = 25039, output_tokens = 931.
</transcription_notes>
</transcription_image>

The web fetch tool is available on the Claude API at no additional cost. You only pay standard token costs for the fetched content that becomes part of your conversation context.

To protect against inadvertently fetching large content that would consume excessive tokens, use the `max_content_tokens` parameter to set appropriate limits based on your use case and budget considerations.

<!-- Decorative: [Ask Docs floating button] -->

<transcription_page_footer> Page 1 | Claude API Docs </transcription_page_footer>
<transcription_page_header> [unclear: document title?] | Pricing </transcription_page_header>

# [unclear: document title?]

<!-- Section 1 -->
## Example token usage for typical content:
- Average web page (10KB): ~2,500 tokens
- Large documentation page (100KB): ~25,000 tokens
- Research paper PDF (500KB): ~125,000 tokens

<!-- Section 2 -->
## Computer use tool

Computer use follows the standard tool use pricing. When using the computer use tool:

**System prompt overhead:** The computer use beta adds 466-499 tokens to the system prompt

### Computer use tool token usage:

<transcription_table>
**Computer use tool token usage**

| Model | Input tokens per tool definition |
|-------|----------------------------------|
| Claude 4.x models | 735 tokens |
| Claude Sonnet 3.7 (deprecated) | 735 tokens |

<transcription_json>
{"table_type":"data_table","title":"Computer use tool token usage","columns":["Model","Input tokens per tool definition"],"data":[{"Model":"Claude 4.x models","Input tokens per tool definition":735},{"Model":"Claude Sonnet 3.7 (deprecated)","Input tokens per tool definition":735}],"unit":"tokens"}
</transcription_json>

<transcription_notes>
- Table: two rows showing input token cost per tool definition for two models.
- Visual: simple two-column table with faint horizontal separators.
</transcription_notes>
</transcription_table>

**Additional token consumption:**
- Screenshot images (see Vision pricing)
- Tool execution results returned to Claude

<transcription_notes>
- Info box (blue, rounded) present on page with an information icon.
- Info box text (verbatim): "If you're also using bash or text editor tools alongside computer use, those tools have their own token costs as documented in their respective pages."
- Visual: blue background, rounded border, left icon (i), small centered padding.
</transcription_notes>

<!-- Section 3 -->
## Agent use case pricing examples

Understanding pricing for agent applications is crucial when building with Claude. These real-world examples can help you estimate costs for different agent patterns.

### Customer support agent example

When building a customer support agent, here's how costs might break down:

> Example calculation for processing 10,000 support tickets:
> - Average ~3,700 tokens per conversation
> - Using Claude Opus 4.6 at $5/MTok input, $25/MTok output

<transcription_notes>
- The example calculation appears inside a blue, rounded example box with an information icon.
- Second bullet references model "Claude Opus 4.6" and pricing "$5/MTok input, $25/MTok output".
- Some of the example box content continues beyond the visible area of the screenshot; only the visible lines are transcribed above.
</transcription_notes>

<!-- Decorative: Ask Docs chat bubble in bottom-right -->
<!-- Decorative: left page margin (blank) -->

<transcription_page_footer> Page [unclear] | [unclear: Company/Docs] </transcription_page_footer>
<!-- Section 1 -->

For a detailed walkthrough of this calculation, see our customer support agent guide.

# General agent workflow pricing

For more complex agent architectures with multiple steps:

1. **Initial request processing**
   - Typical input: 500-1,000 tokens
   - Processing cost: ~$0.003 per request

2. **Memory and context retrieval**
   - Retrieved context: 2,000-5,000 tokens
   - Cost per retrieval: ~$0.015 per operation

3. **Action planning and execution**
   - Planning tokens: 1,000-2,000
   - Execution feedback: 500-1,000
   - Combined cost: ~$0.045 per action

For a comprehensive guide on agent pricing patterns, see our agent use cases guide.

<!-- Section 2 -->

## Cost optimization strategies

When building agents with Claude.

1. **Use appropriate models:** Choose Haiku for simple tasks, Sonnet for complex reasoning  
2. **Implement prompt caching:** Reduce costs for repeated context  
3. **Batch operations:** Use the Batch API for non-time-sensitive tasks  
4. **Monitor usage patterns:** Track token consumption to identify optimization opportunities

> **Sidebar: High-volume agent applications**
> For high-volume agent applications, consider contacting our enterprise sales team for custom pricing arrangements.

<!-- Decorative: Ask Docs floating button -->
<transcription_page_header>Additional pricing considerations</transcription_page_header>

# Additional pricing considerations

<!-- Section 1 -->
## Rate limits

Rate limits vary by usage tier and affect how many requests you can make:

- **Tier 1:** Entry-level usage with basic limits
- **Tier 2:** Increased limits for growing applications
- **Tier 3:** Higher limits for established applications
- **Tier 4:** Maximum standard limits
- **Enterprise:** Custom limits available

For detailed rate limit information, see our rate limits documentation.

For higher rate limits or custom pricing arrangements, contact our sales team.

<!-- Section 2 -->
## Volume discounts

Volume discounts may be available for high-volume users. These are negotiated on a case-by-case basis.

- Standard tiers use the pricing shown above
- Enterprise customers can contact sales for custom pricing
- Academic and research discounts may be available

<!-- Section 3 -->
## Enterprise pricing

For enterprise customers with specific needs:

- Custom rate limits
- Volume discounts
- Dedicated support
- Custom terms

Contact our sales team at sales@anthropic.com or through the Claude Console to discuss enterprise pricing options.

<!-- Section 4 -->
## Billing and payment

- Billing is calculated monthly based on actual usage
- Payments are processed in USD
[unclear: remaining billing/payment items not fully visible]

<transcription_page_footer>Page [unclear] | [unclear]</transcription_page_footer>
<transcription_page_header>Frequently asked questions | Claude API Docs</transcription_page_header>

<!-- Section 1 -->
<!-- Column 1 -->
- Credit card and invoicing options available
- Usage tracking available in the Claude Console

# Frequently asked questions

### How is token usage calculated?

Tokens are pieces of text that models process. As a rough estimate, 1 token is approximately 4 characters or 0.75 words in English. The exact count varies by language and content type.

### Are there free tiers or trials?

New users receive a small amount of free credits to test the API. Contact sales for information about extended trials for enterprise evaluation.

### How do discounts stack?

Batch API and prompt caching discounts can be combined. For example, using both features together provides significant cost savings compared to standard API calls.

### What payment methods are accepted?

We accept major credit cards for standard accounts. Enterprise customers can arrange invoicing and other payment methods.

For additional questions about pricing, contact support@anthropic.com.

---

Was this page helpful?

: 👍
: 👎

<!-- Decorative: social icons (X, LinkedIn, Instagram), "Ask Docs" chat bubble (UI element) -->

<!-- Section 2 -->
<!-- Column 1 -->
**Claude API Docs** (logo)

<!-- Column 2 -->
**Solutions**
: **AI agents**
: **Code modernization**
: **Coding**
: **Customer support**
: **Education**

<!-- Column 3 -->
**Company**
: **Anthropic**
: **Careers**
: **Economic Futures**
: **Research**
: **News**

<!-- Column 4 -->
**Learn**
: **Blog**
: **Catalog**
: **Courses**
: **Use cases**
: **Connectors**

<!-- Column 5 -->
**Help and security**
: **Availability**
: **Status**
: **Support**
: **[unclear: Dis...]**

<transcription_notes>
- Page layout: centered single-column content area with wide side margins, footer in multiple columns.
- Colors: warm off-white/beige background; text is dark gray/black; footer links are muted gray.
- Visual elements: small star-like orange logo left of "Claude API Docs" in footer; social icons (X, LinkedIn, Instagram) appear near the logo.
- "Was this page helpful?" located just above footer with thumbs up / thumbs down icons.
- The "Ask Docs" chat bubble at bottom right is an interactive UI element; marked as decorative.
- The last item in the "Help and security" column is partially obscured and reads like "Dis..." — marked as [unclear].
</transcription_notes>

<transcription_page_footer>Page 1 | Claude API Docs</transcription_page_footer>
# Claude API Docs

<!-- Section 1 -->
## How do discounts stack?

Batch API and prompt caching discounts can be combined. For example, using both features together provides significant cost savings compared to standard API calls.

## What payment methods are accepted?

We accept major credit cards for standard accounts. Enterprise customers can arrange invoicing and other payment methods.

For additional questions about pricing, contact support@anthropic.com.

### Was this page helpful?

: 👍  
: 👎

<hr>

<!-- Section 2 -->
<!-- Column 1 -->
**Claude API Docs**

: (logo)
: X   ☐   ☐  <!-- small social icons: X, LinkedIn?, Instagram? (visual icons shown) -->

<!-- Column 2 -->
**Solutions**

Label items:
: **AI agents**
: **Code modernization**
: **Coding**
: **Customer support**
: **Education**
: **Financial services**
: **Government**
: **Life sciences**

Partners:
: **Amazon Bedrock**
: **Google Cloud's**
: **Vertex AI**

<!-- Column 3 -->
**Company**

Label items:
: **Anthropic**
: **Careers**
: **Economic Futures**
: **Research**
: **News**
: **Responsible Scaling**
: **Policy**
: **Security and compliance**
: **Transparency**

<!-- Column 4 -->
**Learn**

Label items:
: **Blog**
: **Catalog**
: **Courses**
: **Use cases**
: **Connectors**
: **Customer stories**
: **Engineering at Anthropic**
: **Events**
: **Powered by Claude**
: **Service partners**
: **Startups program**

<!-- Column 5 -->
**Help and security**

Label items:
: **Availability**
: **Status**
: **Support**
: **Discord**

**Terms and policies**

Label items:
: **Privacy policy**
: **Responsible disclosure policy**
: **Terms of service: Commercial**
: **Terms of service: Consumer**
: **Usage policy**

<!-- Decorative: Ask Docs floating button, Console UI (left) -->
<!-- Decorative: logo and separator graphics -->

<transcription_page_footer> Page 1 | Claude API Docs </transcription_page_footer>
