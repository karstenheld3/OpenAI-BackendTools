<transcription_page_header>Models & pricing | Models</transcription_page_header>

<!-- Section 1 -->
<!-- Column 1 -->
- Search...
- Models
- Models overview
- Model IDs and versioning
- Choosing a model
- What's new in Claude Opus 4.7
- Upgrade between model versions
- Model deprecations
- Model cards
- System prompts
- Pricing

<!-- Column 2 -->
# Pricing

Learn about Anthropic's pricing structure for models and features

This page provides detailed pricing information for Anthropic's models and features. All prices are in USD.

For the most current pricing information, visit claude.com/pricing.

## Model pricing

The following table shows pricing for all Claude models:

<transcription_table>
**Model pricing**

| Model | Base Input Tokens | 5m Cache Writes | 1h Cache Writes | Cache Hits & Refreshes | Output Tokens |
|-------|-------------------:|----------------:|----------------:|-----------------------:|--------------:|
| Claude Opus 4.7 | $5 / MTok | $6.25 / MTok | $10 / MTok | $0.50 / MTok | $25 / MTok |
| Claude Opus 4.6 | $5 / MTok | $6.25 / MTok | $10 / MTok | $0.50 / MTok | $25 / MTok |
| Claude Opus 4.5 | $5 / MTok | $6.25 / MTok | $10 / MTok | $0.50 / MTok | $25 / MTok |
| Claude Opus 4.1 | $15 / MTok | $18.75 / MTok | $30 / MTok | $1.50 / MTok | $75 / MTok |
| Claude Opus 4 (deprecated) | $15 / MTok | $18.75 / MTok | $30 / MTok | $1.50 / MTok | $75 / MTok |
| Claude Sonnet 4.6 | $3 / MTok | $3.75 / MTok | $6 / MTok | $0.30 / MTok | $15 / MTok |
| Claude Sonnet 4.5 | $3 / MTok | $3.75 / MTok | $6 / MTok | $0.30 / MTok | $15 / MTok |
| Claude Sonnet 4 (deprecated) | $3 / MTok | $3.75 / MTok | $6 / MTok | $0.30 / MTok | $15 / MTok |
| Claude Haiku 4.5 | $1 / MTok | $1.25 / MTok | $2 / MTok | $0.10 / MTok | $5 / MTok |
| Claude Haiku 3.5 (retired, except on Bedrock and Vertex AI) | $0.80 / MTok | $1 / MTok | $1.60 / MTok | $0.08 / MTok | $4 / MTok |

<transcription_json>
{"table_type":"data_table","title":"Model pricing","columns":["Model","Base Input Tokens","5m Cache Writes","1h Cache Writes","Cache Hits & Refreshes","Output Tokens"],"data":[{"Model":"Claude Opus 4.7","Base Input Tokens":5.0,"5m Cache Writes":6.25,"1h Cache Writes":10.0,"Cache Hits & Refreshes":0.5,"Output Tokens":25.0},{"Model":"Claude Opus 4.6","Base Input Tokens":5.0,"5m Cache Writes":6.25,"1h Cache Writes":10.0,"Cache Hits & Refreshes":0.5,"Output Tokens":25.0},{"Model":"Claude Opus 4.5","Base Input Tokens":5.0,"5m Cache Writes":6.25,"1h Cache Writes":10.0,"Cache Hits & Refreshes":0.5,"Output Tokens":25.0},{"Model":"Claude Opus 4.1","Base Input Tokens":15.0,"5m Cache Writes":18.75,"1h Cache Writes":30.0,"Cache Hits & Refreshes":1.5,"Output Tokens":75.0},{"Model":"Claude Opus 4 (deprecated)","Base Input Tokens":15.0,"5m Cache Writes":18.75,"1h Cache Writes":30.0,"Cache Hits & Refreshes":1.5,"Output Tokens":75.0},{"Model":"Claude Sonnet 4.6","Base Input Tokens":3.0,"5m Cache Writes":3.75,"1h Cache Writes":6.0,"Cache Hits & Refreshes":0.3,"Output Tokens":15.0},{"Model":"Claude Sonnet 4.5","Base Input Tokens":3.0,"5m Cache Writes":3.75,"1h Cache Writes":6.0,"Cache Hits & Refreshes":0.3,"Output Tokens":15.0},{"Model":"Claude Sonnet 4 (deprecated)","Base Input Tokens":3.0,"5m Cache Writes":3.75,"1h Cache Writes":6.0,"Cache Hits & Refreshes":0.3,"Output Tokens":15.0},{"Model":"Claude Haiku 4.5","Base Input Tokens":1.0,"5m Cache Writes":1.25,"1h Cache Writes":2.0,"Cache Hits & Refreshes":0.1,"Output Tokens":5.0},{"Model":"Claude Haiku 3.5 (retired, except on Bedrock and Vertex AI)","Base Input Tokens":0.8,"5m Cache Writes":1.0,"1h Cache Writes":1.6,"Cache Hits & Refreshes":0.08,"Output Tokens":4.0}],"unit":"USD per MTok"}
</transcription_json>

<transcription_notes>
- Location: center column of the page, under "Model pricing" heading.
- Table style: simple bordered table with light horizontal dividers; column headers bold.
- Units: "MTok" = Million tokens. Prices shown as "$X / MTok".
- Some models are marked "(deprecated)" or "(retired, except on Bedrock and Vertex AI)" in the Model column.
- The cache-related columns ("5m Cache Writes", "1h Cache Writes", "Cache Hits & Refreshes") are specific to prompt caching pricing.
</transcription_notes>
</transcription_table>

MTok = Million tokens. The "Base Input Tokens" column shows standard input pricing, the "5m Cache Writes", "1h Cache Writes", and "Cache Hits & Refreshes" columns are specific to prompt caching, and "Output Tokens" shows output pricing. See prompt caching pricing for an explanation of the cache columns and pricing multipliers.

Opus 4.7 uses a new tokenizer compared to previous models, contributing to its improved performance on a wide range of tasks. This new tokenizer may use up to 35% more tokens for the same fixed text.

<!-- Column 3 -->
- Model pricing
- Cloud platform pricing
- Claude Platform on AWS pricing
  - Inference geography
  - Private offers
- Feature-specific pricing
  - Prompt caching
  - Data residency pricing
  - Fast mode pricing
  - Batch processing
  - Long context pricing
  - Tool use pricing
  - Specific tool pricing
- Claude Managed Agents pricing
  - Tokens
  - Session runtime
  - Worked example
- Additional pricing considerations
  - Cost optimization strategies
  - Rate limits
  - Volume discounts
  - Enterprise pricing
  - Billing and payment
  - Frequently asked questions

<!-- Decorative: logo at top-left, search box icons, page chrome -->

<transcription_page_footer>Page 1 | Anthropic</transcription_page_footer>
<transcription_page_header>Cloud platform pricing</transcription_page_header>

# Cloud platform pricing

<!-- Section 1 -->
This section covers partner-operated cloud platforms, where the cloud provider invoices you. For Anthropic-operated cloud platforms billed through a marketplace, see Claude Platform on AWS pricing and Claude in Microsoft Foundry.

Claude models are available on Amazon Bedrock and Vertex AI. For official pricing, visit:
- Amazon Bedrock pricing
- Vertex AI pricing

<transcription_image>
**Figure 1: Regional and multi-region endpoint pricing for Claude 4.5 models and beyond**

```ascii
[INFO BOX - REGIONAL AND MULTI-REGION ENDPOINT PRICING]
Regional and multi-region endpoint pricing for Claude 4.5 models and beyond

Starting with Claude Sonnet 4.5, Haiku 4.5, and Opus 4.5:

• Bedrock offers two endpoint types:
  - global endpoints (dynamic routing for maximum availability)
  - regional endpoints (guaranteed data routing through specific geographic regions)

• Vertex AI offers three endpoint types:
  - global endpoints
  - multi-region endpoints (dynamic routing within a geographic area)
  - regional endpoints

Regional and multi-region endpoints include a 10% premium over global endpoints.
The Claude API (first-party) is global by default; for first-party data residency options and pricing, see Data residency pricing.

Scope: This pricing structure applies to Claude Sonnet 4.5, Haiku 4.5, Opus 4.5, and all future models.
Earlier models (Claude Sonnet 4 (deprecated), Opus 4 (deprecated), and prior releases) retain their existing pricing.

For implementation details and code examples:
• Amazon Bedrock global vs regional endpoints for Opus 4.7, Haiku 4.5, and later models, or the legacy integration for all other models on Bedrock
• Vertex AI global, multi-region, and regional endpoints
```

<transcription_json>
{"chart_type":"info_box","title":"Regional and multi-region endpoint pricing for Claude 4.5 models and beyond","intro":"Starting with Claude Sonnet 4.5, Haiku 4.5, and Opus 4.5","bullets":[{"platform":"Bedrock","details":["global endpoints (dynamic routing for maximum availability)","regional endpoints (guaranteed data routing through specific geographic regions)"]},{"platform":"Vertex AI","details":["global endpoints","multi-region endpoints (dynamic routing within a geographic area)","regional endpoints"]}],"pricing_note":"Regional and multi-region endpoints include a 10% premium over global endpoints.","api_note":"The Claude API (first-party) is global by default; for first-party data residency options and pricing, see Data residency pricing.","scope":"Applies to Claude Sonnet 4.5, Haiku 4.5, Opus 4.5, and all future models. Earlier models (Claude Sonnet 4 (deprecated), Opus 4 (deprecated), and prior releases) retain their existing pricing.","implementation_links":["Amazon Bedrock global vs regional endpoints for Opus 4.7, Haiku 4.5, and later models, or the legacy integration for all other models on Bedrock","Vertex AI global, multi-region, and regional endpoints"],"premium_percent":10,"units":"percent"}
</transcription_json>

<transcription_notes>
- Type: Informational callout box (boxed panel).
- Colors: light blue background, darker blue border; icon: circular info icon top-left.
- Layout: title, short intro line, bullet lists for Bedrock and Vertex AI, pricing note, API note, scope, and links.
- Visual placement: medium-width panel centered in page column, with internal padding and list bullets.
- Purpose: clarifies endpoint types and the 10% premium applied to regional and multi-region endpoints for Claude 4.5+ models.
</transcription_notes>
</transcription_image>

<!-- Section 2 -->
## Claude Platform on AWS pricing

Claude Platform on AWS bills through AWS Marketplace using Claude Consumption Units (CCUs). Anthropic rates your token usage in USD at standard per-model, per-feature rates, applies any negotiated discount, converts the result to CCUs at $0.01 per CCU, and reports the CCU quantity to AWS Marketplace hourly. Your AWS bill shows a single CCU line item.

See the billing details table below for the key billing concepts and values.

<transcription_table>
**Table 1: Claude Platform on AWS — billing details**

| Concept | Details |
|--------|---------|
| Billing unit | Claude Consumption Unit (CCU) |
| CCU price | $0.01 per CCU (fixed; discounts apply at token-to-CCU conversion, not to the CCU price) |
| Conversion | Token usage rated in USD at standard per-model, per-feature rates (same as Claude API pricing), then converted to CCUs at $0.01 per CCU |
| Billing frequency | Hourly metering to AWS Marketplace; monthly invoices |

<transcription_json>
{"table_type":"data_table","title":"Claude Platform on AWS — billing details","columns":["Concept","Details"],"data":[{"Concept":"Billing unit","Details":"Claude Consumption Unit (CCU)"},{"Concept":"CCU price","Details":"$0.01 per CCU (fixed; discounts apply at token-to-CCU conversion, not to the CCU price)"},{"Concept":"Conversion","Details":"Token usage rated in USD at standard per-model, per-feature rates (same as Claude API pricing), then converted to CCUs at $0.01 per CCU"},{"Concept":"Billing frequency","Details":"Hourly metering to AWS Marketplace; monthly invoices"}],"unit":"USD / CCU"}
</transcription_json>

<transcription_notes>
- Source: Claude Platform on AWS pricing section of the web page.
- Table visual: two-column bordered table; left column label text bolded visually; right column explanatory text.
- Important values: CCU price = $0.01 per CCU; conversion method described above; billing is hourly metered to AWS Marketplace with monthly invoices.
- Only visible rows (four rows) are transcribed; additional rows may exist off-screen.
</transcription_notes>
</transcription_table>

<transcription_page_footer>Page 1</transcription_page_footer>
<transcription_page_header> [unclear: page title] | [unclear: section] </transcription_page_header>

# [unclear: Document title]

<!-- Section 1 -->
<!-- Column 1 -->
<transcription_table>
**Table: Pricing / billing details (snippet visible on page)**

| Field | Details |
|-------|---------|
| Payment model | Arrears only (postpaid); no prepaid credits |
| Discounts | Applied as fewer CCUs metered |
| Tax | Pre-tax metering; AWS Marketplace handles tax |
| Cost visibility | Real-time breakdown in the Claude Console (access through the AWS Console); AWS Cost Explorer shows aggregated CCU |

<transcription_json>
{"table_type": "data_table", "title": "Pricing / billing details (snippet)", "columns": ["Field", "Details"], "data": [{"Field":"Payment model","Details":"Arrears only (postpaid); no prepaid credits"},{"Field":"Discounts","Details":"Applied as fewer CCUs metered"},{"Field":"Tax","Details":"Pre-tax metering; AWS Marketplace handles tax"},{"Field":"Cost visibility","Details":"Real-time breakdown in the Claude Console (access through the AWS Console); AWS Cost Explorer shows aggregated CCU"}]}
</transcription_json>

<transcription_notes>
- Location: small two-column table snippet near top-right of the visible page.
- Visual: left column is label (bold), right column is description text. Light horizontal separators between rows.
- Context: part of a larger pricing/billing table not fully visible on this page image.
</transcription_notes>
</transcription_table>

<!-- Section 2 -->
<transcription_image>
**Figure 1: Claude Consumption Units (info box)**

```ascii
[INFO BOX]
i Claude Consumption Units. If Customer accesses the Services through certain Marketplace Platforms (e.g., Claude
Platform on AWS), usage will be invoiced in Claude Consumption Units ("CCU") rather than per MTok. A CCU is a unit
of measure used solely for Marketplace Platform invoicing. One hundred (100) CCU represents $1.00 USD of fees
owed for the Services, calculated at the applicable prices on claude.com/pricing#api, after application of any
discounts.
```

<transcription_json>
{"chart_type": "info_box", "title": "Claude Consumption Units", "text": "If Customer accesses the Services through certain Marketplace Platforms (e.g., Claude Platform on AWS), usage will be invoiced in Claude Consumption Units (\"CCU\") rather than per MTok. A CCU is a unit of measure used solely for Marketplace Platform invoicing. One hundred (100) CCU represents $1.00 USD of fees owed for the Services, calculated at the applicable prices on claude.com/pricing#api, after application of any discounts."}
</transcription_json>

<transcription_notes>
- Visual: blue bordered rounded rectangle with an "i" info icon at top-left; blue text inside.
- Contains a short explanation of "Claude Consumption Units" and mapping: 100 CCU = $1.00 USD.
- Link to: claude.com/pricing#api (rendered as inline link in source).
</transcription_notes>
</transcription_image>

<!-- Section 3 -->
## Inference geography

For Claude Opus 4.6, Claude Sonnet 4.6, and later models, using `inference_geo: "us"` applies a 1.1x pricing multiplier. `inference_geo: "global"` (default) uses standard pricing. See Data residency for details.

<!-- Section 4 -->
## Private offers

When you sign up on the AWS Console **Claude Platform on AWS** service page, the AWS Console looks up any private offer associated with your account and prompts you to accept it in AWS Marketplace. Contact your Anthropic account representative for private offer terms.

<transcription_image>
**Figure 2: Private offers - Bedrock private offer note (info box)**

```ascii
[INFO BOX]
i If you have an existing Amazon Bedrock private offer, contact your Anthropic or AWS account representative before
getting started with Claude Platform on AWS to ensure your discounts are applied correctly. Discounts cannot be
applied retroactively to usage incurred before your private offer is accepted.
```

<transcription_json>
{"chart_type":"info_box","title":"Private offers - Amazon Bedrock note","text":"If you have an existing Amazon Bedrock private offer, contact your Anthropic or AWS account representative before getting started with Claude Platform on AWS to ensure your discounts are applied correctly. Discounts cannot be applied retroactively to usage incurred before your private offer is accepted."}
</transcription_json>

<transcription_notes>
- Visual: blue bordered rounded rectangle with an "i" info icon at top-left; blue text inside.
- Advises contacting Anthropic or AWS account representative to ensure discounts are applied and notes discounts are not retroactive.
</transcription_notes>
</transcription_image>

<!-- Section 5 -->
## Feature-specific pricing

### Prompt caching

Prompt caching reduces costs and latency by reusing previously processed portions of your prompt across API calls. Instead of reprocessing the same large system prompt, document, or conversation history on every request, the API reads from cache at a fraction of the standard input price.

There are two ways to enable prompt caching:
- Automatic caching: Add a single `cache_control` field at the top level of your request. The system automatically manages cache breakpoints as conversations grow. This is the recommended starting point for most use cases.
- Explicit cache breakpoints: Place `cache_control` directly on individual content blocks for fine-grained control over exactly what gets cached.

<!-- Section 6 -->
<!-- Column 1 -->
[unclear: any remaining text below Prompt caching is not fully visible in the image]

<transcription_page_footer> Page [unclear] | Anthropic </transcription_page_footer>
<!-- Section 1 -->
## Prompt caching

Prompt caching uses the following pricing multipliers relative to base input token rates:

<transcription_table>
**Table 1: Prompt caching pricing multipliers**

| Cache operation | Multiplier | Duration |
|-----------------|-----------:|---------|
| 5-minute cache write | 1.25x base input price | Cache valid for 5 minutes |
| 1-hour cache write | 2x base input price | Cache valid for 1 hour |
| Cache read (hit) | 0.1x base input price | Same duration as the preceding write |

<transcription_json>
{"table_type":"data_table","title":"Prompt caching pricing multipliers","columns":["Cache operation","Multiplier","Duration"],"data":[{"Cache operation":"5-minute cache write","Multiplier":1.25,"Multiplier_unit":"x base input price","Duration":"Cache valid for 5 minutes"},{"Cache operation":"1-hour cache write","Multiplier":2.0,"Multiplier_unit":"x base input price","Duration":"Cache valid for 1 hour"},{"Cache operation":"Cache read (hit)","Multiplier":0.1,"Multiplier_unit":"x base input price","Duration":"Same duration as the preceding write"}],"notes":"Multipliers relative to base input token rates"}
</transcription_json>

<transcription_notes>
- Layout: single-column page, table centered in content column.
- Visual details: light horizontal rules separate table rows; typography: serif body font.
- Context: Explains prompt caching charge multipliers relative to base input token pricing.
</transcription_notes>
</transcription_table>

Cache write tokens are charged when content is first stored. Cache read tokens are charged when a subsequent request retrieves the cached content. A cache hit costs 10% of the standard input price, which means caching pays off after just one cache read for the 5-minute duration (1.25x write), or after two cache reads for the 1-hour duration (2x write).

These multipliers stack with other pricing modifiers, including the Batch API discount and data residency.

For implementation details, supported models, and code examples, see Prompt caching.

<!-- Section 2 -->
## Data residency pricing

For Claude Opus 4.6, Claude Sonnet 4.6, and later models, specifying US-only inference through the `inference_geo` parameter incurs a 1.1x multiplier on all token pricing categories, including input tokens, output tokens, cache writes, and cache reads. Global routing (the default) uses standard pricing.

This applies to the Claude API (first-party) and Claude Platform on AWS. Partner-operated platforms (Bedrock and Vertex AI) have independent regional pricing. See Bedrock and Vertex AI for details. Earlier models do not support the `inference_geo` parameter and always use standard pricing; requests that include the parameter on these models return a 400 error.

For more information, see Data residency.

<!-- Section 3 -->
## Fast mode pricing

Fast mode, in beta (research preview), provides significantly faster output for Claude Opus 4.6 and Claude Opus 4.7 at premium pricing (6x standard rates). Fast mode pricing applies across the full context window, including requests over 200k input tokens. Fast mode is not available on Claude Platform on AWS.

<transcription_table>
**Table 2: Fast mode pricing**

| Input | Output |
|-------:|-------:|
| $30 / MTok | $150 / MTok |

<transcription_json>
{"table_type":"data_table","title":"Fast mode pricing","columns":["Input","Output"],"data":[{"Input":"$30 / MTok","Input_value":30,"Input_unit":"$/MTok"},{"Output":"$150 / MTok","Output_value":150,"Output_unit":"$/MTok"}],"notes":"Prices listed are premium fast-mode rates per million tokens (MTok)."}
</transcription_json>

<transcription_notes>
- Layout: two-column price cells under a small heading. Currency shown as dollar sign ($).
- Visual: prices in bold in the original; Input column left, Output column right.
- Context: Fast mode premium pricing per MTok.
</transcription_notes>
</transcription_table>

Fast mode pricing stacks with other pricing modifiers:
- Prompt caching multipliers apply on top of fast mode pricing
- Data residency multipliers apply on top of fast mode pricing

Fast mode is not available with the Batch API.

For more information, see Fast mode.

<!-- Section 4 -->
## Batch processing

The Batch API allows asynchronous processing of large volumes of requests with a 50% discount on both input and output tokens.

<!-- Decorative: Ask Docs chat button in bottom-right of page -->
<transcription_page_header> [unclear] | [unclear] </transcription_page_header>

# [unclear]

<!-- Section 1 -->

<transcription_image>
**Figure 1: Batch pricing by model**

```ascii
[TABLE - Batch pricing]
Model                                              | Batch input    | Batch output
--------------------------------------------------------------------------------
Claude Opus 4.7                                    | $2.50 / MTok   | $12.50 / MTok
Claude Opus 4.6                                    | $2.50 / MTok   | $12.50 / MTok
Claude Opus 4.5                                    | $2.50 / MTok   | $12.50 / MTok
Claude Opus 4.1                                    | $7.50 / MTok   | $37.50 / MTok
Claude Opus 4 (deprecated)                         | $7.50 / MTok   | $37.50 / MTok
Claude Sonnet 4.6                                  | $1.50 / MTok   | $7.50 / MTok
Claude Sonnet 4.5                                  | $1.50 / MTok   | $7.50 / MTok
Claude Sonnet 4 (deprecated)                       | $1.50 / MTok   | $7.50 / MTok
Claude Haiku 4.5                                   | $0.50 / MTok   | $2.50 / MTok
Claude Haiku 3.5 (retired, except on Bedrock and
 Vertex AI)                                        | $0.40 / MTok   | $2 / MTok
```

<transcription_json>
{"chart_type":"pricing_table","title":"Batch pricing by model","columns":["Model","Batch input","Batch output"],"data":[{"Model":"Claude Opus 4.7","Batch input":2.50,"Batch output":12.50,"unit":"$ / MTok"},{"Model":"Claude Opus 4.6","Batch input":2.50,"Batch output":12.50,"unit":"$ / MTok"},{"Model":"Claude Opus 4.5","Batch input":2.50,"Batch output":12.50,"unit":"$ / MTok"},{"Model":"Claude Opus 4.1","Batch input":7.50,"Batch output":37.50,"unit":"$ / MTok"},{"Model":"Claude Opus 4 (deprecated)","Batch input":7.50,"Batch output":37.50,"unit":"$ / MTok"},{"Model":"Claude Sonnet 4.6","Batch input":1.50,"Batch output":7.50,"unit":"$ / MTok"},{"Model":"Claude Sonnet 4.5","Batch input":1.50,"Batch output":7.50,"unit":"$ / MTok"},{"Model":"Claude Sonnet 4 (deprecated)","Batch input":1.50,"Batch output":7.50,"unit":"$ / MTok"},{"Model":"Claude Haiku 4.5","Batch input":0.50,"Batch output":2.50,"unit":"$ / MTok"},{"Model":"Claude Haiku 3.5 (retired, except on Bedrock and Vertex AI)","Batch input":0.40,"Batch output":2.00,"unit":"$ / MTok"}]}
</transcription_json>

<transcription_notes>
- Type: Two-column data table (Model | Batch input | Batch output)
- Visual: light tan background, table text dark gray. Thin horizontal separators between rows.
- The last model row wraps text across two visual lines: "Claude Haiku 3.5 (retired, except on Bedrock and Vertex AI)".
- Link below table: "For more information about batch processing, see Batch processing." (hyperlink in original).
- Units: "$ / MTok" (dollar per thousand tokens) shown in table cells.
- Decorative element: bottom-right "Ask Docs" floating button (not transcribed as content).
</transcription_notes>
</transcription_image>

For more information about batch processing, see Batch processing.

## Long context pricing

Claude Mythos Preview, Opus 4.7, Opus 4.6, and Sonnet 4.6 include the full 1M token context window at standard pricing. (A 900k-token request is billed at the same per-token rate as a 9k-token request.) Prompt caching and batch processing discounts apply at standard rates across the full context window.

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

When you use `tools`, the API also automatically includes a special system prompt for the model which enables tool use. The number of tool use tokens required for each model are listed below (excluding the additional tokens listed above). Note that the table assumes at least 1 tool is provided. If no `tools` are provided, then a tool choice of none uses 0 additional system prompt tokens.

<!-- Decorative: Ask Docs floating button -->

<transcription_page_footer> Page [unclear] | [unclear] </transcription_page_footer>
<transcription_page_header> [unclear: Page title] | [unclear: Section] </transcription_page_header>

# [unclear: Model tool token counts]

<!-- Section 1 -->
<!-- Column 1 -->

<transcription_table>
**Table: Model tool token counts**

| Model | Tool availability | System prompt token count |
|-------|-------------------|---------------------------|
| Claude Opus 4.7 | auto , none | 346 tokens |
| Claude Opus 4.7 | any , tool | 313 tokens |
| Claude Opus 4.6 | auto , none | 346 tokens |
| Claude Opus 4.6 | any , tool | 313 tokens |
| Claude Opus 4.5 | auto , none | 346 tokens |
| Claude Opus 4.5 | any , tool | 313 tokens |
| Claude Opus 4.1 | auto , none | 346 tokens |
| Claude Opus 4.1 | any , tool | 313 tokens |
| Claude Opus 4 (deprecated) | auto , none | 346 tokens |
| Claude Opus 4 (deprecated) | any , tool | 313 tokens |
| Claude Sonnet 4.6 | auto , none | 346 tokens |
| Claude Sonnet 4.6 | any , tool | 313 tokens |
| Claude Sonnet 4.5 | auto , none | 346 tokens |
| Claude Sonnet 4.5 | any , tool | 313 tokens |
| Claude Sonnet 4 (deprecated) | auto , none | 346 tokens |
| Claude Sonnet 4 (deprecated) | any , tool | 313 tokens |
| Claude Haiku 4.5 | auto , none | 346 tokens |
| Claude Haiku 4.5 | any , tool | 313 tokens |
| Claude Haiku 3.5 (retired, except on Bedrock and Vertex AI) | auto , none | 264 tokens |
| Claude Haiku 3.5 (retired, except on Bedrock and Vertex AI) | any , tool | 340 tokens |

<transcription_json>
{"table_type":"data_table","title":"Model tool token counts","columns":["Model","Tool availability","System prompt token count"],"data":[{"Model":"Claude Opus 4.7","Tool availability":"auto , none","System prompt token count":346},{"Model":"Claude Opus 4.7","Tool availability":"any , tool","System prompt token count":313},{"Model":"Claude Opus 4.6","Tool availability":"auto , none","System prompt token count":346},{"Model":"Claude Opus 4.6","Tool availability":"any , tool","System prompt token count":313},{"Model":"Claude Opus 4.5","Tool availability":"auto , none","System prompt token count":346},{"Model":"Claude Opus 4.5","Tool availability":"any , tool","System prompt token count":313},{"Model":"Claude Opus 4.1","Tool availability":"auto , none","System prompt token count":346},{"Model":"Claude Opus 4.1","Tool availability":"any , tool","System prompt token count":313},{"Model":"Claude Opus 4 (deprecated)","Tool availability":"auto , none","System prompt token count":346},{"Model":"Claude Opus 4 (deprecated)","Tool availability":"any , tool","System prompt token count":313},{"Model":"Claude Sonnet 4.6","Tool availability":"auto , none","System prompt token count":346},{"Model":"Claude Sonnet 4.6","Tool availability":"any , tool","System prompt token count":313},{"Model":"Claude Sonnet 4.5","Tool availability":"auto , none","System prompt token count":346},{"Model":"Claude Sonnet 4.5","Tool availability":"any , tool","System prompt token count":313},{"Model":"Claude Sonnet 4 (deprecated)","Tool availability":"auto , none","System prompt token count":346},{"Model":"Claude Sonnet 4 (deprecated)","Tool availability":"any , tool","System prompt token count":313},{"Model":"Claude Haiku 4.5","Tool availability":"auto , none","System prompt token count":346},{"Model":"Claude Haiku 4.5","Tool availability":"any , tool","System prompt token count":313},{"Model":"Claude Haiku 3.5 (retired, except on Bedrock and Vertex AI)","Tool availability":"auto , none","System prompt token count":264},{"Model":"Claude Haiku 3.5 (retired, except on Bedrock and Vertex AI)","Tool availability":"any , tool","System prompt token count":340}],"unit":"tokens"}
</transcription_json>

<transcription_notes>
- Layout: single centered content column with a narrow left margin; table rows show each model with two tool-availability variants (pills) and the corresponding token counts.
- Visuals: pale beige background, faint horizontal separators between rows. Tool availability appears as small rounded "pill" UI elements reading "auto , none" and "any , tool".
- The 346 / 313 token pattern repeats for most modern Opus/Sonnet/Haiku 4.x models; Claude Haiku 3.5 shows 264 and 340 tokens (label includes "retired, except on Bedrock and Vertex AI").
- Colors: muted greys and beige; pills have light grey background. Thin horizontal rule between rows.
- Captured values reflect the visible numeric token counts in the image.
</transcription_notes>
</transcription_table>

These token counts are added to your normal input and output tokens to calculate the total cost of a request. For current per-model prices, refer to the model pricing section. For more information about tool use implementation and best practices, see Tool use.

<!-- Section 2 -->
## Specific tool pricing

### Bash tool

The bash tool adds 245 input tokens to your API calls.

Additional tokens are consumed by:
- Command outputs (stdout/stderr)
- [unclear: other bullet items not fully visible in image]

<transcription_page_footer> Page [unclear] | [unclear: Company/site] </transcription_page_footer>
<transcription_page_header> [unclear: Page title] | Tools </transcription_page_header>

# [unclear: Document title]

<!-- Section 1 -->
## Code execution tool

Code execution is free when used with web search or web fetch. When `web_search_20260209` or `web_fetch_20260209` is included in your API request, there are no additional charges for code execution tool calls beyond the standard input and output token costs.

When used without these tools, code execution is billed by execution time, tracked separately from token usage:
- Execution time has a minimum of 5 minutes
- Each organization receives **1,550 free hours** of usage per month
- Additional usage beyond 1,550 hours is billed at **$0.05 per hour, per container**
- If files are included in the request, execution time is billed even if the tool is not invoked, due to files being preloaded onto the container

Code execution usage is tracked in the response:

```json
{
  "usage": {
    "input_tokens": 105,
    "output_tokens": 239,
    "server_tool_use": {
      "code_execution_requests": 1
    }
  }
}
```

<!-- Section 2 -->
## Text editor tool

The text editor tool uses the same pricing structure as other tools used with Claude. It follows the standard input and output token pricing based on the Claude model you're using.

In addition to the base tokens, the following additional input tokens are needed for the text editor tool:

<transcription_table>
**Table 1: Text editor additional input tokens**

| Tool | Additional input tokens |
|------|-------------------------|
| `text_editor_20250429` (Claude 4.x) | 700 tokens |

<transcription_json>
{"table_type":"data_table","title":"Text editor additional input tokens","columns":["Tool","Additional input tokens"],"data":[{"Tool":"text_editor_20250429 (Claude 4.x)","Additional input tokens":"700 tokens"}],"unit":"tokens"}
</transcription_json>

<transcription_notes>
- Table shows the tool identifier `text_editor_20250429` associated with Claude 4.x and an additional input token requirement of 700 tokens.
- Visual layout: two-column table, single data row. No colors required for data extraction.
</transcription_notes>
</transcription_table>

See tool use pricing for complete pricing details.

<!-- Section 3 -->
## Web search tool

Web search usage is charged in addition to token usage:

<!-- Decorative: "Ask Docs" help button visible in lower-right; not transcribed --> 

<transcription_page_footer> Page [unclear] | [unclear: Company] </transcription_page_footer>
<transcription_page_header> [unclear: Title?] | [unclear] </transcription_page_header>

<!-- Section 1 -->
## Web search

Web search is available on the Claude API for $10 per 1,000 searches, plus standard token costs for search-generated content. Web search results retrieved throughout a conversation are counted as input tokens, in search iterations executed during a single turn and in subsequent conversation turns.

Each web search counts as one use, regardless of the number of results returned. If an error occurs during web search, the web search will not be billed.

<!-- Section 2 -->
## Web fetch tool

Web fetch usage has no additional charges beyond standard token costs:

```json
{
  "usage": {
    "input_tokens": 25039,
    "output_tokens": 931,
    "cache_read_input_tokens": 0,
    "cache_creation_input_tokens": 0,
    "server_tool_use": {
      "web_fetch_requests": 1
    }
  }
}
```

The web fetch tool is available on the Claude API at no additional cost. You only pay standard token costs for the fetched content that becomes part of your conversation context.

To protect against inadvertently fetching large content that would consume excessive tokens, use the max_content_tokens parameter to set appropriate limits based on your use case and budget considerations.

Example token usage for typical content:
- Average web page (10 kB): ~2,500 tokens
- Large documentation page (100 kB): ~25,000 tokens
- Research paper PDF (500 kB): ~125,000 tokens

<!-- Section 3 -->
## Computer use tool

Computer use follows the standard tool use pricing. When using the computer use tool:

<!-- Decorative: [Ask Docs widget in bottom-right corner] -->

<transcription_notes>
- Page layout: single-column content area centered with wide side margins.
- Code blocks: displayed inside rounded light-grey boxes with monospaced font; syntax highlighting present (numbers/keys in teal/green, braces in dark text).
- Visual context: the screenshot shows the lower-middle portion of a documentation page; the top of the page and some preceding code are partially visible but cropped.
- Decorative elements: an "Ask Docs" floating widget is visible in the bottom-right corner (decorative UI).
</transcription_notes>

<transcription_page_footer> Page [unclear] | [unclear] </transcription_page_footer>
<transcription_page_header> Claude Managed Agents pricing | Pricing </transcription_page_header>

<!-- Section 1 -->
System prompt overhead: The computer use beta adds 466-499 tokens to the system prompt

Computer use tool token usage:

<transcription_table>
**Table 1: Computer use tool token usage**

| Model | Input tokens per tool definition |
|-------|----------------------------------|
| Claude 4.x models | 735 tokens |

<transcription_json>
{"table_type":"data_table","title":"Computer use tool token usage","columns":["Model","Input tokens per tool definition"],"data":[{"Model":"Claude 4.x models","Input tokens per tool definition":"735 tokens"}],"unit":null}
</transcription_json>

<transcription_notes>
- Context: This table describes token consumption charged when using the "computer use" tool.
- Visual: single-row table with thin grey divider lines.
</transcription_notes>
</transcription_table>

Additional token consumption:
- Screenshot images (see Vision pricing)
- Tool execution results returned to Claude

> If you're also using bash or text editor tools alongside computer use, those tools have their own token costs as documented in their respective pages.

<!-- Section 2 -->
# Claude Managed Agents pricing

Claude Managed Agents is billed on two dimensions: tokens and session runtime.

<!-- Section 3 -->
## Tokens

All tokens consumed by a Claude Managed Agents session are billed at the rates shown in Model pricing. Prompt caching multipliers apply identically. Web search triggered inside a session incurs the standard $10 per 1,000 searches. On Claude Platform on AWS, session token and runtime charges convert to Claude Consumption Units at the standard rate.

The following Messages API modifiers do not apply to Claude Managed Agents sessions:

<transcription_table>
**Table 2: Messages API modifiers that do not apply**

| Modifier | Why it doesn't apply |
|----------|----------------------|
| Batch API discount | Sessions are stateful and interactive. There is no batch mode. |
| Fast mode premium | Inference speed is managed by the runtime. |
| Data residency multiplier | inference_geo is a Messages API request field. |
| Cloud platform pricing | Not available on partner-operated cloud platforms. |

<transcription_json>
{"table_type":"data_table","title":"Messages API modifiers that do not apply","columns":["Modifier","Why it doesn't apply"],"data":[{"Modifier":"Batch API discount","Why it doesn't apply":"Sessions are stateful and interactive. There is no batch mode."},{"Modifier":"Fast mode premium","Why it doesn't apply":"Inference speed is managed by the runtime."},{"Modifier":"Data residency multiplier","Why it doesn't apply":"inference_geo is a Messages API request field."},{"Modifier":"Cloud platform pricing","Why it doesn't apply":"Not available on partner-operated cloud platforms."}]}
</transcription_json>

<transcription_notes>
- Source: Pricing documentation section for Claude Managed Agents.
- Table styling: two-column layout, left column bolded headings in original.
</transcription_notes>
</transcription_table>

<!-- Section 4 -->
## Session runtime

<transcription_table>
**Table 3: Session runtime**

| SKU | Rate | Metering |
|-----|------|----------|
| Session runtime | $0.08 per session-hour | running status duration |

<transcription_json>
{"table_type":"data_table","title":"Session runtime","columns":["SKU","Rate","Metering"],"data":[{"SKU":"Session runtime","Rate":"$0.08 per session-hour","Metering":"running status duration"}],"unit":"USD"}
</transcription_json>

<transcription_notes>
- Rate unit: dollars per session-hour.
- "Metering" indicates runtime is billed while session status is "running".
- Visual: three-column table with subtle dividers.
</transcription_notes>
</transcription_table>

Runtime is measured to the millisecond and accrues only while the session's status is running. Time spent idle (waiting for your next message or a tool confirmation), rescheduling, or terminated does not count toward runtime.

<transcription_page_footer> Page 1 | </transcription_page_footer>
# Worked example

A one-hour coding session using Claude Opus 4.7 that consumes 50,000 input tokens and 15,000 output tokens:

<!-- Section 1 -->
<transcription_table>
**Table 1: One-hour coding session (Claude Opus 4.7)**

| Line item        | Calculation                         | Cost     |
|------------------|-------------------------------------|---------:|
| Input tokens     | 50,000 × $5 / 1,000,000            | $0.25    |
| Output tokens    | 15,000 × $25 / 1,000,000           | $0.375   |
| Session runtime  | 1.0 hour × $0.08                   | $0.08    |
| **Total**        |                                     | **$0.705** |

<transcription_json>
{"table_type":"data_table","title":"One-hour coding session (Claude Opus 4.7)","columns":["Line item","Calculation","Cost"],"data":[{"Line item":"Input tokens","Calculation":"50,000 × $5 / 1,000,000","Cost":"$0.25"},{"Line item":"Output tokens","Calculation":"15,000 × $25 / 1,000,000","Cost":"$0.375"},{"Line item":"Session runtime","Calculation":"1.0 hour × $0.08","Cost":"$0.08"},{"Line item":"Total","Calculation":"","Cost":"$0.705"}],"unit":"USD"}
</transcription_json>

<transcription_notes>
- Table shows a worked pricing example for Claude Opus 4.7.
- Styling notes: thin horizontal separators between rows, right-aligned numeric "Cost" column.
- Units: USD. Calculations show per-million-token pricing applied to token counts.
</transcription_notes>
</transcription_table>

If prompt caching is active and 40,000 of the input tokens are cache reads:

<transcription_table>
**Table 2: One-hour session with prompt caching (40,000 cache reads)**

| Line item             | Calculation                                | Cost     |
|-----------------------|--------------------------------------------|---------:|
| Uncached input tokens | 10,000 × $5 / 1,000,000                    | $0.05    |
| Cache read tokens     | 40,000 × $5 × 0.1 / 1,000,000              | $0.02    |
| Output tokens         | 15,000 × $25 / 1,000,000                   | $0.375   |
| Session runtime       | 1.0 hour × $0.08                           | $0.08    |
| **Total**             |                                            | **$0.525** |

<transcription_json>
{"table_type":"data_table","title":"One-hour session with prompt caching (40,000 cache reads)","columns":["Line item","Calculation","Cost"],"data":[{"Line item":"Uncached input tokens","Calculation":"10,000 × $5 / 1,000,000","Cost":"$0.05"},{"Line item":"Cache read tokens","Calculation":"40,000 × $5 × 0.1 / 1,000,000","Cost":"$0.02"},{"Line item":"Output tokens","Calculation":"15,000 × $25 / 1,000,000","Cost":"$0.375"},{"Line item":"Session runtime","Calculation":"1.0 hour × $0.08","Cost":"$0.08"},{"Line item":"Total","Calculation":"","Cost":"$0.525"}],"unit":"USD"}
</transcription_json>

<transcription_notes>
- Cache read tokens are charged at 10% of input token price in this example (0.1 multiplier).
- Units: USD. Numeric precision matches displayed cents/milli-dollar values.
</transcription_notes>
</transcription_table>

<transcription_image>
**Figure 1: Example calculation for processing 10,000 support tickets**

```ascii
[INFO BOX - BLUE BORDER]
Example calculation for processing 10,000 support tickets:
  • Average ~3,700 tokens per conversation
  • Using Claude Haiku 4.5 at $1/MTok input, $5/MTok output
  • Total cost: ~$37.00 per 10,000 tickets
```

<transcription_json>
{"chart_type":"info_box","title":"Example calculation for processing 10,000 support tickets","bullets":["Average ~3,700 tokens per conversation","Using Claude Haiku 4.5 at $1/MTok input, $5/MTok output","Total cost: ~$37.00 per 10,000 tickets"],"context":"Estimate example shown in a highlighted blue information box on the page"}
</transcription_json>

<transcription_notes>
- Visual: rounded rectangle info box with light blue background and darker blue border; small circular info icon at top-left.
- Text inside is a bulleted list of three lines. First bullet uses approximation symbol "~3,700".
- Monetary units: $ and per 10,000 tickets summary provided.
</transcription_notes>
</transcription_image>

For a detailed walkthrough of this calculation, see the customer support agent guide.

<!-- Section 2 -->
## Additional pricing considerations

Cost optimization strategies

1. Use appropriate models: Choose Haiku for simple tasks, Sonnet for most production workloads, and Opus for the most complex reasoning.
<transcription_page_header> [unclear: page title] | Pricing & usage </transcription_page_header>

# [unclear: page title]

<!-- Section 1 -->
<!-- Column 1 -->
> **Sidebar: For high-volume agent applications**
> For high-volume agent applications, contact the enterprise sales team for custom pricing arrangements.

<!-- Decorative: Ask Docs floating widget in lower-right -->

<!-- Section 2 -->
## Rate limits

Rate limits vary by usage tier and affect how many requests you can make:

- **Tier 1:** Entry-level usage with basic limits  
- **Tier 2:** Increased limits for growing applications  
- **Tier 3:** Higher limits for established applications  
- **Tier 4:** Maximum standard limits  
- **Enterprise:** Custom limits available

For detailed rate limit information, see Rate limits.

For higher rate limits or custom pricing arrangements, contact the sales team.

<!-- Section 3 -->
## Volume discounts

Volume discounts may be available for high-volume users. These are negotiated on a case-by-case basis.

- Standard tiers use the pricing shown in Model pricing  
- Enterprise customers can contact sales for custom pricing  
- Academic and research discounts may be available

<!-- Section 4 -->
## Enterprise pricing

For enterprise customers with specific needs:

- Custom rate limits  
- Volume discounts  
- Dedicated support  
- Custom terms

Contact the sales team at sales@anthropic.com or through the Claude Console to discuss enterprise pricing options.

<!-- Section 5 -->
## Billing and payment

- Billing is based on actual monthly usage  
- All payments are in USD  
- Credit card and invoicing options available  
- Usage tracking available in the Claude Console

<transcription_page_footer> Page 1 | Anthropic </transcription_page_footer>
<transcription_page_header>Frequently asked questions | </transcription_page_header>

# Frequently asked questions

<!-- Section 1 -->
## How is token usage calculated?
Tokens are pieces of text that models process. As a rough estimate, 1 token is approximately 4 characters or 0.75 words in English. The exact count varies by language and content type.

## Are there free tiers or trials?
New users receive a small amount of free credits to test the API. Contact sales for information about extended trials for enterprise evaluation.

## How do discounts stack?
Batch API and prompt caching discounts can be combined. For example, using both features together provides significant cost savings compared to standard API calls. See prompt caching pricing for how the multipliers interact.

## What payment methods are accepted?
Major credit cards are accepted for standard accounts. Enterprise customers can arrange invoicing and other payment methods.

For additional questions about pricing, contact support@anthropic.com.

Was this page helpful?

: 👍 (icon)
: 👎 (icon)

<!-- Decorative: logo, social icons, divider line -->

<!-- Section 2 -->
<!-- Column 1 -->
**Claude API Docs**

: (logo - decorative)
: (social icons: X, GitHub, LinkedIn, YouTube, Instagram) <!-- Decorative -->

<!-- Column 2 -->
**Solutions**

- AI agents
- Code modernization
- Coding
- Customer support
- Education
- Financial services
- Government
- Life sciences

<!-- Column 3 -->
**Company**

- Anthropic
- Careers
- Economic Futures
- Research
- News
- Responsible Scaling Policy
- Security and compliance
- Transparency

<!-- Column 4 -->
**Learn**

- Blog
- Courses
- Use cases
- Connectors
- Customer stories
- Engineering at Anthropic
- Events
- Powered by Claude
- Service partners
- Startups program

<!-- Column 5 -->
**Help and security**

- Availability
- Status
- Support
- Discord

**Terms and policies**

- Privacy policy
- Responsible disclosure policy
- Terms of service: Commercial
- Terms of service: Consumer
- Usage policy

<!-- Column 6 -->
**Partners**

- Amazon Bedrock
- Google Cloud's Vertex AI

<transcription_notes>
- Layout: central FAQ column near top of image; large multi-column footer occupying bottom half.
- Colors: background off-white/cream; text dark gray/black. Footer links appear in muted gray.
- Visual elements: horizontal divider above footer; page has generous side margins. Logo ("Claude API Docs") at left of footer with small social icons below it.
- Decorative items (not transcribed as content): site logo, social icon graphics, small thumbs icons, divider lines.
- If any footer entries are partially obscured or truncated in the image, they are transcribed to the best visible accuracy; use [unclear] if further verification needed.
</transcription_notes>

<transcription_page_footer>Claude API Docs | Anthropic</transcription_page_footer>
# Frequently asked questions

<!-- Section 1 -->
## How is token usage calculated?
Tokens are pieces of text that models process. As a rough estimate, 1 token is approximately 4 characters or 0.75 words in English. The exact count varies by language and content type.

## Are there free tiers or trials?
New users receive a small amount of free credits to test the API. Contact sales for information about extended trials for enterprise evaluation.

## How do discounts stack?
Batch API and prompt caching discounts can be combined. For example, using both features together provides significant cost savings compared to standard API calls. See prompt caching pricing for how the multipliers interact.

## What payment methods are accepted?
Major credit cards are accepted for standard accounts. Enterprise customers can arrange invoicing and other payment methods.

For additional questions about pricing, contact support@anthropic.com.

---

Was this page helpful?

👍  👎

<!-- Decorative: [Claude logo, social icons, footer separators] -->

<!-- Section 2 -->
<!-- Column 1 -->
**Claude API Docs**

<!-- Column 2 -->
**Solutions**

- AI agents
- Code modernization
- Coding
- Customer support
- Education
- Financial services
- Government
- Life sciences

<!-- Column 3 -->
**Company**

- Anthropic
- Careers
- Economic Futures
- Research
- News
- Responsible Scaling Policy
- Security and compliance
- Transparency

<!-- Column 4 -->
**Learn**

- Blog
- Courses
- Use cases
- Connectors
- Customer stories
- Engineering at Anthropic
- Events
- Powered by Claude
- Service partners
- Startups program

<!-- Column 5 -->
**Help and security**

- Availability
- Status
- Support
- Discord

**Terms and policies**

- Privacy policy
- Responsible disclosure policy
- Terms of service: Commercial
- Terms of service: Consumer
- Usage policy

<!-- Column 6 -->
**Partners**

- Amazon Bedrock
- Google Cloud's Vertex AI

<transcription_page_footer> Page [unclear] | Claude API Docs </transcription_page_footer>
