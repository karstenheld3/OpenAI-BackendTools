<DevSystem MarkdownTablesAllowed=true />

# Anthropic Pricing Data - 2026-03-20

## Sources

- **Primary**: https://platform.claude.com/docs/en/about-claude/pricing
- **Screenshots**: Captured 2026-03-20 from Claude API Docs
  - `2026-03-20_Anthropic-ModelPricing-01.jpg` - Model pricing, prompt caching, batch processing, long context
  - `2026-03-20_Anthropic-ModelPricing-02.jpg` - Tool use pricing, code execution, text editor, web search/fetch
  - `2026-03-20_Anthropic-ModelPricing-03.jpg` - Computer use, agent pricing examples, cost optimization

## Model Pricing (per 1M tokens)

[Source: Screenshot 01 - "Model pricing" table]

| Model                       | Context | Input   | Cache Write | Cache Read | Output  |
|-----------------------------|---------|---------|-------------|------------|---------|
| Claude Opus 4.6             | 200K    | $15.00  | $18.75      | $1.50      | $75.00  |
| Claude Opus 4.5             | 200K    | $15.00  | $18.75      | $1.50      | $75.00  |
| Claude Opus 4.1             | 200K    | $15.00  | $18.75      | $1.50      | $75.00  |
| Claude Opus 4               | 200K    | $15.00  | $18.75      | $1.50      | $75.00  |
| Claude Sonnet 4.6           | 200K    | $3.00   | $3.75       | $0.30      | $15.00  |
| Claude Sonnet 4.5           | 200K    | $3.00   | $3.75       | $0.30      | $15.00  |
| Claude Sonnet 4             | 200K    | $3.00   | $3.75       | $0.30      | $15.00  |
| Claude Sonnet 3.7 (dep.)    | 200K    | $3.00   | $3.75       | $0.30      | $15.00  |
| Claude Haiku 4.5            | 200K    | $1.00   | $1.25       | $0.10      | $5.00   |
| Claude Haiku 3.5            | 200K    | $0.80   | $1.00       | $0.08      | $4.00   |
| Claude 3 Opus (dep.)        | 200K    | $15.00  | $18.75      | $1.50      | $75.00  |
| Claude 3 Haiku              | 200K    | $0.25   | $0.30       | $0.03      | $1.25   |

**Note**: MTok = Million tokens. All prices in USD.

## Prompt Caching

[Source: Screenshot 01 - "Prompt caching" section]

Prompt caching reduces costs and latency by reusing previously processed portions of your prompt across API calls. Instead of reprocessing the same large system prompt, document, or conversation history on every request, the API reads from cache at a fraction of the standard input price.

Two ways to enable prompt caching:
- **Automatic caching**: Add a single `cache_control` field at the top level of your request. The system automatically manages cache breakpoints via conversation sync. This is the recommended starting point for most use cases.
- **Explicit cache breakpoints**: Place `cache_control` directly on individual content blocks for fine-grained control over exactly what gets cached.

### Cache Pricing Multipliers

| Cache Operation     | Multiplier            | Duration                   |
|---------------------|----------------------|----------------------------|
| 5-min cache write   | 1.25x base input price | -                          |
| 1-hour cache write  | Use 1-hour option      | Cache valid for 5 minutes  |
| Min cache read      | 1x base input price    | Cache valid for 5 minutes  |
| Cache hit           | 0.1x base input price  | Scales as the preceding value |

Cache write tokens are charged when content to be cached. Cache read tokens are charged when a subsequent request retrieves the cached content. A cache hit is 10% of the standard input price, which means caching pays off after one cache read for the 5-minute duration (1.25x writes), or after two cache reads for the 1-hour duration (2x writes).

These multipliers stack with other pricing modifiers, including the Batch API discount, long context pricing, and data residency.

## Batch Processing (50% discount)

[Source: Screenshot 01 - "Batch processing" section]

The Batch API allows asynchronous processing of large volumes of requests with a 50% discount on both input and output tokens.

| Model             | Batch Input | Batch Output |
|-------------------|-------------|--------------|
| Claude Opus 4.6   | $7.50/MTok  | $37.50/MTok  |
| Claude Opus 4.5   | $7.50/MTok  | $37.50/MTok  |
| Claude Opus 4     | $7.50/MTok  | $37.50/MTok  |
| Claude Sonnet 4.5 | $1.50/MTok  | $7.50/MTok   |
| Claude Haiku 4.5  | $0.50/MTok  | $2.50/MTok   |
| Claude Haiku 3    | $0.125/MTok | $0.625/MTok  |

## Long Context Pricing

[Source: Screenshot 01 - "Long context pricing" section]

For Claude Opus 4.5 and Sonnet 4.5: 1M token context window at standard pricing. A 1M-token context window is available to partners with extended processing disclosure; standard rates apply for tokens up to 200K.

For Claude Sonnet 4.5: the 1M token context window beta is for organizations who opt-in using `anthropic-beta: max-tokens-3-5-sonnet-2024-07-15` header. Context >200K triggers automatic "long context" surcharge at **2x standard rates**.

| Model             | Context   | >200K Input  | >200K Output  |
|-------------------|-----------|--------------|---------------|
| Claude Opus 4.5   | up to 1M  | $30.00/MTok  | $150.00/MTok  |
| Claude Sonnet 4.5 | up to 1M  | $6.00/MTok   | $30.00/MTok   |

- Batch API 50% discount applies to long context pricing
- Prompt caching multipliers apply on top of long context pricing
- The 200K threshold is based solely on input tokens (including cache_read_input_tokens). Output token count does not affect pricing; output tokens are always at the right column rate regardless of context length

## Tool Use Pricing

[Source: Screenshot 02 - "Tool use pricing" section]

Tool use requests are priced based on:
1. Total number of input tokens sent to the model (including the `tools` parameter)
2. Number of output tokens generated
3. For server-side tools: additional usage-based pricing (e.g., web search charges per search performed)

| Model                    | Tool Choice | System Prompt Tokens |
|--------------------------|-------------|----------------------|
| Claude Opus 4.6          | auto, none  | 3K tokens            |
| Claude Opus 4.5          | auto, none  | 3K tokens            |
| Claude Opus 4.1          | auto, text  | 3K tokens            |
| Claude Opus 4            | auto, text  | 3K tokens            |
| Claude Sonnet 4.6        | auto, none  | 3K tokens            |
| Claude Sonnet 4.5        | auto, none  | 3K tokens            |
| Claude Sonnet 4          | auto, none  | 3K tokens            |
| Claude Sonnet 3.7 (dep.) | auto, none  | 3K tokens            |
| Claude Haiku 4.5         | auto, none  | 24K tokens           |
| Claude Haiku 3.5         | auto, none  | 3K tokens            |

## Bash Tool

[Source: Screenshot 02 - "Bash tool" section]

Adds 245 input tokens to API calls. Additional tokens consumed by:
- Command outputs (stdout/stderr)
- Error messages
- Large file contents

## Code Execution Tool

[Source: Screenshot 02 - "Code execution tool" section]

Code execution is **free** when used with web search or web fetch. When `web_search_20250305` or `web_fetch_preview` is included in API request, there are no additional charges for code execution tool calls beyond the standard input and output token pricing.

When used without these tools, code execution is billed by execution time, tracked separately from token usage:
- Execution time has a minimum of 5 minutes
- Each organization receives **1,500 free hours** of usage per month
- Additional usage beyond 1,500 hours is billed at **$0.05 per hour per container**
- If files are written in the request, even if not read, time is billed due to files being persisted onto the container

Code execution usage is tracked in the response:
```json
{
  "usage": {
    "input_tokens": 589,
    "output_tokens": 225,
    "cache_read_input_tokens": 1,
    "code_execution_requests": 1
  }
}
```

## Text Editor Tool

[Source: Screenshot 02 - "Text editor tool" section]

Same pricing structure as other tools used with Claude. Standard input and output token pricing based on the Claude model.

| Tool                 | Additional Input Tokens |
|----------------------|-------------------------|
| text_editor_20250429 | 722 tokens              |
| text_editor_20250124 | 700 tokens              |

## Web Search Tool

[Source: Screenshot 02 - "Web search tool" section]

Web search is available on the Claude API for **$10 per 1,000 searches**, plus standard token costs for search-generated content.

Usage response example:
```json
{
  "input_tokens": 609,
  "output_tokens": 1422,
  "cache_read_input_tokens": 7123,
  "web_search_requests": 1
}
```

- Web search results (titles and content) are counted as input tokens
- In search iterations, each retrieving a single URL results in standard rates applying only on the search request cost
- Web search using `web_search_auto` returns as many uses as necessary
- If no error occurs during web search, the web search will not be billed

## Web Fetch Tool

[Source: Screenshot 02 - "Web fetch tool" section]

Web fetch has **no additional charges** beyond standard token costs.

Usage response example:
```json
{
  "input_tokens": 25036,
  "output_tokens": 331,
  "cache_read_input_tokens": 2,
  "server_tool_use": {
    "web_fetch_requests": 1
  }
}
```

The web fetch is a **multi-modal tool**. You only pay standard token costs for the fetched content that becomes part of your conversation content.

Use `max_content_tokens` parameter to set appropriate size limits.

Example token usage for typical content:
- Average web page: ~10,000 tokens
- Large documentation page: 70K-100K tokens
- Research paper PDF (30-40 KB): ~125,000 tokens

## Computer Use Tool

[Source: Screenshot 02-03 - "Computer use tool" section]

Computer use follows the standard tool use pricing.

**System prompt overhead:** The computer use beta adds **466-499 tokens** to the system prompt.

| Model                    | Input Tokens per Tool Definition |
|--------------------------|----------------------------------|
| Claude 4.x models        | 735 tokens                       |
| Claude Sonnet 3.7 (dep.) | 735 tokens                       |

**Additional token consumption:**
- Screenshots/images have Vision pricing
- Tool execution results returned to Claude

## Agent Pricing Examples

[Source: Screenshot 03 - "Agent use case pricing examples" section]

### Customer Support Agent Example

Example calculation for processing 10,000 support tickets:
- Average ~3,700 tokens per conversation
- Using Claude Opus 4.5 at $30K/54K input: $10M/Mo total
- Total cost: ~$7,000 over 10,000 tickets

### General Agent Workflow Pricing

For more complex agent architectures with multiple steps:

1. **Initial request processing**
   - Typical inputs: 500-1,000 tokens
   - Processing cost: ~$0.02 per request

2. **Memory and context retrieval**
   - Retrieved context: 3,000-5,000 tokens
   - Cost per retrieval: ~$0.05 per operation

3. **Action planning and execution**
   - Planning tokens: 1,000-2,000
   - Execution feedback: 500-1,000
   - Combined cost: ~$0.04 per action

## Cost Optimization Strategies

[Source: Screenshot 03 - "Cost optimization strategies" section]

1. **Use appropriate models**: Choose Haiku for simple tasks, Sonnet for complex reasoning
2. **Implement prompt caching**: Reduce costs for repeated context
3. **Batch operations**: Use the Batch API for non-time-sensitive tasks
4. **Monitor usage patterns**: Track token consumption to identify optimization opportunities

## Additional Pricing Considerations

[Source: Screenshot 03 - "Additional pricing considerations" section]

### Rate Limits

| Tier       | Description                              |
|------------|------------------------------------------|
| Tier 1     | Entry level usage with basic limits      |
| Tier 2     | Increased limits for growing applications |
| Tier 3     | Higher limits for established applications |
| Tier 4     | Maximum limits available                 |
| Enterprise | Custom limits available                  |

### Volume Discounts

Volume discounts may be available for high-volume users. These are negotiated on a case-by-case basis:
- Standard: use the pricing shown above
- Enterprise: customers can contact sales for custom pricing
- Academic and research discounts may be available

## Billing and Payment

[Source: Screenshot 03 - "Billing and payment" section]

- Billing is calculated monthly based on actual usage
- Payments are processed in USD
- Credit card and invoicing options available
- Usage tracking available in the Claude Console

## Frequently Asked Questions

[Source: Screenshot 03 - "Frequently asked questions" section]

**How is token usage calculated?**
Tokens are pieces of text that models process. As a rough estimate, 1 token is approximately 4 characters or 0.75 words in English. The exact count varies by language and content type.

**Are there free tiers or trials?**
New users receive a small amount of free credits to test the API. Contact sales for information about extended trials for enterprise evaluation.

**How do discounts stack?**
Batch API and prompt caching discounts can be combined. For example, using both features together provides significant cost savings compared to standard API calls. See prompt caching pricing for how the multipliers interact.

**What payment methods are accepted?**
Major credit cards are accepted for standard accounts. Enterprise customers can arrange invoicing and other payment options.
