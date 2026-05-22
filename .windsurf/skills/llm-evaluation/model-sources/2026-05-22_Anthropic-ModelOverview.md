<transcription_page_header> Models overview | Models & pricing </transcription_page_header>

<!-- Decorative: [Claude logo (top-left), search box, top navigation bar, "Copy page" button, page scrollbars, "Ask Docs" floating button] -->

<!-- Section 1 -->
<!-- Column 1 -->
Models

- Models overview (selected)
- Model IDs and versioning
- Choosing a model
- What's new in Claude Opus 4.7
- Upgrade between model versions
- Model deprecations
- Model cards
- System prompts
- Pricing

<!-- Column 2 -->
Models & pricing  /  Models

# Models overview

Claude is a family of state-of-the-art large language models developed by Anthropic. This guide introduces the available models and compares their performance.

## Choosing a model

If you're unsure which model to use, consider starting with **Claude Opus 4.7** for the most complex tasks. It is our most capable generally available model, with a step‑change improvement in agentic coding over Claude Opus 4.6.

All current Claude models support text and image input, text output, multilingual capabilities, and vision. Models are available through the Claude API, Claude Platform on AWS, Amazon Bedrock, Vertex AI, and Microsoft Foundry.

Once you've picked a model, learn how to make your first API call.

## Latest models comparison

<transcription_table>
**Table 1: Latest models comparison**

| Feature | Claude Opus 4.7 | Claude Sonnet 4.6 | Claude Haiku 4.5 |
|---------|------------------|-------------------|------------------|
| Description | Our most capable generally available model for complex reasoning and agentic coding | The best combination of speed and intelligence | The fastest model with near‑frontier intelligence |
| Claude API ID | claude-opus-4-7 | claude-sonnet-4-6 | claude-haiku-4-5-20251001 |
| Claude API alias | claude-opus-4-7 | claude-sonnet-4-6 | claude-haiku-4-5 |
| AWS Bedrock ID | anthropic.claude-opus-4-7³ | anthropic.claude-sonnet-4-6 | anthropic.claude-haiku-4-5-20251001-v1:0 |
| Vertex AI ID | claude-opus-4-7 | claude-sonnet-4-6 | claude-haiku-4-5[unclear] |
| Pricing¹ | $5 / input MTok $25 / output MTok | $3 / input MTok $15 / output MTok | $1 / input MTok $5 / output MTok |
| Extended thinking | No | Yes | Yes |
| Adaptive thinking | Yes | Yes | No |

<transcription_json>
{"table_type":"data_table","title":"Latest models comparison","columns":["Feature","Claude Opus 4.7","Claude Sonnet 4.6","Claude Haiku 4.5"],"data":[{"Feature":"Description","Claude Opus 4.7":"Our most capable generally available model for complex reasoning and agentic coding","Claude Sonnet 4.6":"The best combination of speed and intelligence","Claude Haiku 4.5":"The fastest model with near-frontier intelligence"},{"Feature":"Claude API ID","Claude Opus 4.7":"claude-opus-4-7","Claude Sonnet 4.6":"claude-sonnet-4-6","Claude Haiku 4.5":"claude-haiku-4-5-20251001"},{"Feature":"Claude API alias","Claude Opus 4.7":"claude-opus-4-7","Claude Sonnet 4.6":"claude-sonnet-4-6","Claude Haiku 4.5":"claude-haiku-4-5"},{"Feature":"AWS Bedrock ID","Claude Opus 4.7":"anthropic.claude-opus-4-7³","Claude Sonnet 4.6":"anthropic.claude-sonnet-4-6","Claude Haiku 4.5":"anthropic.claude-haiku-4-5-20251001-v1:0"},{"Feature":"Vertex AI ID","Claude Opus 4.7":"claude-opus-4-7","Claude Sonnet 4.6":"claude-sonnet-4-6","Claude Haiku 4.5":"claude-haiku-4-5[unclear]"},{"Feature":"Pricing¹","Claude Opus 4.7":"$5 / input MTok $25 / output MTok","Claude Sonnet 4.6":"$3 / input MTok $15 / output MTok","Claude Haiku 4.5":"$1 / input MTok $5 / output MTok"},{"Feature":"Extended thinking","Claude Opus 4.7":"No","Claude Sonnet 4.6":"Yes","Claude Haiku 4.5":"Yes"},{"Feature":"Adaptive thinking","Claude Opus 4.7":"Yes","Claude Sonnet 4.6":"Yes","Claude Haiku 4.5":"No"}],"unit":null}
</transcription_json>

<transcription_notes>
- Type: Comparison table with 4 columns (Feature + 3 model columns).  
- Visual: centered column contains the table; left column is site navigation; right column is a small page local nav. Table cells have light background tokens for IDs (rounded rectangles). There are footnote markers: Pricing has a superscript "1"; AWS Bedrock ID for Opus has superscript "3". Some text in the Vertex AI ID for Claude Haiku is partially obscured/unclear in the image — marked as [unclear]. Fonts: serif headings, sans-serif body. Colors: page background off‑white, left nav column pale beige, table header text dark, table cell tokens very light beige with monospace-like appearance for IDs.
- Source: Claude API Docs page "Models overview".
</transcription_notes>
</transcription_table>

<!-- Column 3 -->
> Sidebar: Choosing a model
> - Latest models comparison
> - Prompt and output performance
> - Migrating to Claude Opus 4.7
> - Get started with Claude

<transcription_page_footer> Page 1 | Claude API Docs </transcription_page_footer>
<!-- Section 1 -->
<transcription_table>
**Model comparison (partial — right-side table, header row not visible)**

| Feature | [Column 1] | [Column 2] | [Column 3] |
|---------|------------|------------|------------|
| Priority Tier | Yes | Yes | Yes |
| Comparative latency | Moderate | Fast | Fastest |
| Context window | 1M tokens | 1M tokens | 200k tokens |
| Max output | 128k tokens | 64k tokens | 64k tokens |
| Reliable knowledge cutoff | Jan 2026^2 | Aug 2025^2 | Feb 2025 |
| Training data cutoff | Jan 2026 | Jan 2026 | Jul 2025 |

<transcription_json>
{"table_type":"data_table","title":"Model comparison (partial)","columns":["Feature","[Column 1]","[Column 2]","[Column 3]"],"data":[{"Feature":"Priority Tier","[Column 1]":"Yes","[Column 2]":"Yes","[Column 3]":"Yes"},{"Feature":"Comparative latency","[Column 1]":"Moderate","[Column 2]":"Fast","[Column 3]":"Fastest"},{"Feature":"Context window","[Column 1]":"1M tokens","[Column 2]":"1M tokens","[Column 3]":"200k tokens"},{"Feature":"Max output","[Column 1]":"128k tokens","[Column 2]":"64k tokens","[Column 3]":"64k tokens"},{"Feature":"Reliable knowledge cutoff","[Column 1]":"Jan 2026^2","[Column 2]":"Aug 2025^2","[Column 3]":"Feb 2025"},{"Feature":"Training data cutoff","[Column 1]":"Jan 2026","[Column 2]":"Jan 2026","[Column 3]":"Jul 2025"}],"unit":"tokens"}
</transcription_json>

<transcription_notes>
- Location: right-hand table fragment near top of page (only portion visible).
- Visuals: simple 4-column table with first column listing features; three model columns to the right (column headers not visible in the image — marked as [Column 1], [Column 2], [Column 3]).
- Notable typography: superscript "2" appears after "Jan 2026" and "Aug 2025" in the Reliable knowledge cutoff row (rendered here as ^2).
- Units: "tokens" shown for context window and max output entries.
</transcription_notes>
</transcription_table>

<!-- Section 2 -->
Jan 2026²
: 1 - See Pricing for complete pricing information including Batch API discounts and prompt caching rates.

Reliable knowledge cutoff:
: 2 - Reliable knowledge cutoff indicates the date through which a model's knowledge is most extensive and reliable. Training data cutoff is the broader date range of training data used. For more information, see Anthropic's Transparency Hub.

:
: 3 - Claude Opus 4.7 is available on Bedrock through Claude in Amazon Bedrock (the Messages-API Bedrock endpoint).

<!-- Section 3 -->
> **Sidebar: Claude Mythos Preview**
> Claude Mythos Preview is offered separately as a research preview model for defensive cybersecurity workflows as part of Project Glasswing. Access is invitation-only and there is no self‑serve sign‑up.

> **Sidebar: Model IDs and snapshots**
> Every Claude model ID is a pinned snapshot. Models with a date in the ID (for example, 20250929) are fixed to that specific release. Starting with the Claude 4.6 generation, model IDs use a dateless format that is also a pinned snapshot, not an evergreen pointer. For models before the 4.6 generation, entries in the Claude API alias column are convenience pointers that resolve to a dated model ID. For details on the naming convention and how versioning works, see Model IDs and versioning.

> **Sidebar: Endpoints (Sonnet & Bedrock)**
> Starting with Claude Sonnet 4.5 and all subsequent models (including Claude Sonnet 4.6), Bedrock offers two endpoint types: global endpoints (dynamic routing for maximum availability) and regional endpoints (guaranteed data routing through specific geographic regions). Vertex AI offers three endpoint types: global endpoints, multi-region endpoints (dynamic routing within a geographic area), and regional endpoints. For more information, see Cloud platform pricing.

> **Sidebar: Claude Platform on AWS**
> Claude Platform on AWS uses the same model IDs as the Claude API (for example, claude-opus-4-6), not Bedrock-style IDs. Model lifecycle on Claude Platform on AWS follows Anthropic's first-party Model deprecations, not Bedrock's. See Available models for the model list.

<!-- Section 4 -->
You can query model capabilities and token limits programmatically with the Models API. The response includes max_input_tokens, max_tokens, and a capabilities object for every available model.

<transcription_notes>
- Visual details: Multiple stacked informational callout boxes with a blue border and a circular "i" icon at the left of each; one beige/neutral info box with a light bulb icon precedes the bottom explanatory paragraph. Text in callouts contains bolded model names and inline code-like tokens (e.g., max_input_tokens, max_tokens). The callouts have left padding and rounded corners.
- Colors: callouts are light-blue background with blue border; the explanatory box near the bottom is light-beige with a darker beige border; icons are blue (for blue callouts) or beige (for beige box).
- Page context: only the right content column is visible; left page margin is blank. A floating "Ask Docs" chat bubble appears in the lower-right corner (decorative).
</transcription_notes>

<!-- Decorative: Ask Docs chat bubble -->
<transcription_page_header> Prompt and output performance | Claude </transcription_page_header>

# Prompt and output performance

<!-- Section 1 -->
Claude 4 models excel in:

- **Performance:** Top-tier results in reasoning, coding, multilingual tasks, long-context handling, honesty, and image processing. See the Claude 4 blog post for more information.
- **Engaging responses:** Claude models are ideal for applications that require rich, human-like interactions.
  - If you prefer more concise responses, you can adjust your prompts to guide the model toward the desired output length. Refer to the prompt engineering guides for details.
  - For prompting best practices, see Prompting best practices.
- **Output quality:** When migrating from previous model generations to Claude 4, you may notice larger improvements in overall performance.

<!-- Section 2 -->
## Migrating to Claude Opus 4.7

If you’re currently using Claude Opus 4.6 or older Claude models, consider migrating to Claude Opus 4.7 to take advantage of improved intelligence and a step-change jump in agentic coding. For detailed migration instructions, see Migrating to Claude Opus 4.7.

<!-- Section 3 -->
## Get started with Claude

If you’re ready to start exploring what Claude can do for you, dive in! Whether you’re a developer looking to integrate Claude into your applications or a user wanting to experience the power of AI firsthand, the following resources can help.

> ℹ️ Looking to chat with Claude? Visit claude.ai!

<!-- Section 4 -->
<!-- Column 1 -->
**Intro to Claude**

Explore Claude's capabilities and development flow.

<!-- Column 2 -->
**Quickstart**

Learn how to make your first API call in minutes.

<!-- Column 3 -->
**Claude Console**

Craft and test powerful prompts directly in your browser.

<!-- Decorative: [Ask Docs chat button (bottom-right), scrollbar, page chrome not transcribed] -->

<transcription_notes>
- Page layout: single central content column with very wide left and right gutters; serif headings, sans-serif body text.
- Background: very light cream/ivory.
- Headings: large, bold serif (dark).
- Bulleted list: standard black bullets; two nested bullet levels under "Engaging responses".
- Blue info box: light blue rounded rectangle with an information icon at left and the text "Looking to chat with Claude? Visit claude.ai!" in medium-weight text. Has subtle border and shadow.
- Three resource cards: horizontally aligned, each with a light rounded border and an icon above the title (icons not transcribed). Titles: "Intro to Claude", "Quickstart", "Claude Console". Each card contains a one-line description as transcribed.
- Visible UI elements not transcribed as content: expandable control "Legacy models" (collapsed), a small top info bar about max output values (partially visible), right-side scrollbar, and bottom-right "Ask Docs" floating button.
- No charts or numeric data present on this page segment.
</transcription_notes>

<transcription_page_footer> Page 1 </transcription_page_footer>
<transcription_page_header>Claude API Docs | Resources</transcription_page_header>

# Claude API Docs

<!-- Section 1 -->
## Resources

<transcription_image>
**Figure 1: Resources & Quick Links**

```ascii
[INFO BOX]
( i ) Looking to chat with Claude? Visit claude.ai!

[CARDS ROW]
[ CARD 1 ]            [ CARD 2 ]               [ CARD 3 ]
[ ✓ ] Intro to Claude  [ ⚡ ] Quickstart         [ </> ] Claude Console
      Explore Claude's    Learn how to make         Craft and test powerful
      capabilities and     your first API call in    prompts directly in your
      development flow.    minutes.                 browser.
```

<transcription_json>
{"chart_type":"cards","title":"Resources & Quick Links","info_box":"Looking to chat with Claude? Visit claude.ai!","data":[{"icon":"check","title":"Intro to Claude","description":"Explore Claude's capabilities and development flow."},{"icon":"bolt","title":"Quickstart","description":"Learn how to make your first API call in minutes."},{"icon":"code","title":"Claude Console","description":"Craft and test powerful prompts directly in your browser."}]}
</transcription_json>

<transcription_notes>
- Layout: top blue info box with info icon and link text; below a horizontal row of three rounded cards with light borders and subtle shadow.
- Card 1 icon: checkmark. Card 2 icon: lightning/bolt. Card 3 icon: code-brackets.
- Colors: info box background = light blue; cards = off-white with faint grey border; icons darker accent colors (not enough detail to exact color hex).
- Visual alignment: three equal-width cards horizontally centered in page column.
- Decorative: small ticks and icons on cards; not transcribed as separate links.
</transcription_notes>
</transcription_image>

<!-- Section 2 -->
If you have any questions or need assistance, don't hesitate to reach out to the support team or consult the Discord community.

---

Was this page helpful?

👍  👎

<!-- Decorative: [horizontal rule, small icons] -->

<!-- Section 3 -->
## Footer

<!-- Column 1 -->
Claude API Docs

Social icons:
: X
: [unclear]
: LinkedIn
: YouTube
: Instagram

<!-- Column 2 -->
**Solutions**

: AI agents
: Code modernization
: Coding
: Customer support
: Education
: Financial services
: Government
: Life sciences

<!-- Column 3 -->
**Company**

: Anthropic
: Careers
: Economic Futures
: Research
: News
: Responsible Scaling Policy
: Security and compliance
: Transparency

<!-- Column 4 -->
**Learn**

: Blog
: Courses
: Use cases
: Connectors
: Customer stories
: Engineering at Anthropic
: Events
: Powered by Claude
: Service partners
: Startups program

<!-- Column 5 -->
**Help and security**

: Availability
: Status
: Support
: Discord

**Terms and policies**

: Privacy policy
: Responsible disclosure policy
: Terms of service: Commercial
: Terms of service: Consumer
: Usage policy

<!-- Column 6 -->
**Partners**

: Amazon Bedrock
: Google Cloud's Vertex AI

<transcription_page_footer>Claude API Docs | Footer</transcription_page_footer>
