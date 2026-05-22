<transcription_page_header>Responses API</transcription_page_header>

<!-- Section 1 -->
<!-- Column 1 -->
Responses API
Using tools

Agents SDK
Overview
Quickstart
Agent definitions
Models and providers
Running agents
Sandbox agents
Orchestration
Guardrails
Results and state
Integrations and observability
Evaluate agent workflows
Voice agents
Agent Builder >

Tools
Web search
MCP and Connectors
Skills
Shell
Computer use
File search and retrieval >
Tool search
More tools >

Run and scale
Conversation state
Background mode
Streaming
WebSocket mode
Webhooks
File inputs
Context management >

<!-- Column 2 -->
## Model pricing

<transcription_table>
**Model | Input | Cached input**

| Model | Input | Cached input |
|-------|-------:|:-------------|
| gpt-5.2 | $0.875 | $0.0875 |
| gpt-5.2-pro | $10.50 | - |
| gpt-5.1 | $0.625 | $0.0625 |
| gpt-5 | $0.625 | $0.0625 |
| gpt-5-mini | $0.125 | $0.0125 |
| gpt-5-nano | $0.025 | $0.0025 |
| gpt-5-pro | $7.50 | - |
| gpt-4.1 | $1.00 | - |
| gpt-4.1-mini | $0.20 | - |
| gpt-4.1-nano | $0.05 | - |
| gpt-4o | $1.25 | - |
| gpt-4o-mini | $0.075 | - |
| o4-mini | $0.55 | - |
| o3 | $1.00 | - |
| o3-mini | $0.55 | - |
| o3-pro | $10.00 | - |
| o1 | $7.50 | - |
| o1-mini | $0.55 | - |
| o1-pro | $75.00 | - |
| gpt-4o-2024-05-13 | $2.50 | - |
| gpt-4-turbo-2024-04-09 | $5.00 | - |
| gpt-4-0125-preview | $5.00 | - |
| gpt-4-1106-preview | $5.00 | - |
| gpt-4-1106-vision-preview | $5.00 | - |
| gpt-4-0613 | $15.00 | - |
| gpt-4-0314 | $15.00 | - |

<transcription_json>
{"table_type": "data_table", "title": "Model | Input | Cached input", "columns": ["Model","Input","Cached input"], "data": [{"Model":"gpt-5.2","Input":0.875,"Cached input":0.0875},{"Model":"gpt-5.2-pro","Input":10.50,"Cached input":null},{"Model":"gpt-5.1","Input":0.625,"Cached input":0.0625},{"Model":"gpt-5","Input":0.625,"Cached input":0.0625},{"Model":"gpt-5-mini","Input":0.125,"Cached input":0.0125},{"Model":"gpt-5-nano","Input":0.025,"Cached input":0.0025},{"Model":"gpt-5-pro","Input":7.50,"Cached input":null},{"Model":"gpt-4.1","Input":1.00,"Cached input":null},{"Model":"gpt-4.1-mini","Input":0.20,"Cached input":null},{"Model":"gpt-4.1-nano","Input":0.05,"Cached input":null},{"Model":"gpt-4o","Input":1.25,"Cached input":null},{"Model":"gpt-4o-mini","Input":0.075,"Cached input":null},{"Model":"o4-mini","Input":0.55,"Cached input":null},{"Model":"o3","Input":1.00,"Cached input":null},{"Model":"o3-mini","Input":0.55,"Cached input":null},{"Model":"o3-pro","Input":10.00,"Cached input":null},{"Model":"o1","Input":7.50,"Cached input":null},{"Model":"o1-mini","Input":0.55,"Cached input":null},{"Model":"o1-pro","Input":75.00,"Cached input":null},{"Model":"gpt-4o-2024-05-13","Input":2.50,"Cached input":null},{"Model":"gpt-4-turbo-2024-04-09","Input":5.00,"Cached input":null},{"Model":"gpt-4-0125-preview","Input":5.00,"Cached input":null},{"Model":"gpt-4-1106-preview","Input":5.00,"Cached input":null},{"Model":"gpt-4-1106-vision-preview","Input":5.00,"Cached input":null},{"Model":"gpt-4-0613","Input":15.00,"Cached input":null},{"Model":"gpt-4-0314","Input":15.00,"Cached input":null}], "unit": "USD"}
</transcription_json>

<transcription_notes>
- Visual layout: two-column page (left navigation column + main content column).
- Left column: navigation list (Agents SDK, Tools, Run and scale sections) in small left-aligned type.
- Right/main column: table titled by column headers "Model", "Input", "Cached input".
- Many rows have "-" shown in Cached input column indicating not available (represented as null in JSON).
- Minor visual elements: vertical scrollbar on the right edge of the main column; thin horizontal separators between table rows.
- Colors: left navigation text in muted gray, active/section headings slightly darker; table header bold/dark; table cell text dark gray. Scrollbar light gray.
- Page appears to be a documentation page (documentation-style font, ample whitespace).
</transcription_notes>
</transcription_table>

<!-- Decorative: vertical scrollbar, page chrome, logos --> 

<transcription_page_footer>Page 1</transcription_page_footer>
<transcription_page_header> Responses API | [unclear] </transcription_page_header>

# Responses API

<!-- Section 1 -->
<!-- Column 1 -->
Agents SDK

Overview  
Quickstart  
Agent definitions  
Models and providers  
Running agents  
Sandbox agents  
Orchestration  
Guardrails  
Results and state  
Integrations and observability  
Evaluate agent workflows  
Voice agents  
Agent Builder  >

Tools

Web search  
MCP and Connectors  
Skills  
Shell  
Computer use  
File search and retrieval  >  
Tool search  
More tools  >

Run and scale

Conversation state  
Background mode  
Streaming  
WebSocket mode  
Webhooks  
File inputs  
Context management  >

<!-- Column 2 -->
<!-- Section 2 -->

## Model pricing table

<transcription_table>
**Model | Input | Cached input**

| Model | Input | Cached input |
|-------|-------:|--------------:|
| gpt-5.2 | $0.875 | $0.0875 |
| gpt-5.2-pro | $10.50 | - |
| gpt-5.1 | $0.625 | $0.0625 |
| gpt-5 | $0.625 | $0.0625 |
| gpt-5-mini | $0.125 | $0.0125 |
| gpt-5-nano | $0.025 | $0.0025 |
| gpt-5-pro | $7.50 | - |
| gpt-4.1 | $1.00 | - |
| gpt-4.1-mini | $0.20 | - |
| gpt-4.1-nano | $0.05 | - |
| gpt-4o | $1.25 | - |
| gpt-4o-mini | $0.075 | - |
| o4-mini | $0.55 | - |
| o3 | $1.00 | - |
| o3-mini | $0.55 | - |
| o3-pro | $10.00 | - |
| o1 | $7.50 | - |
| o1-mini | $0.55 | - |
| o1-pro | $75.00 | - |
| gpt-4o-2024-05-13 | $2.50 | - |
| gpt-4-turbo-2024-04-09 | $5.00 | - |
| gpt-4-0125-preview | $5.00 | - |
| gpt-4-1106-preview | $5.00 | - |
| gpt-4-1106-vision-preview | $5.00 | - |
| gpt-4-0613 | $15.00 | - |
| gpt-4-0314 | $15.00 | - |

<transcription_json>
{"table_type":"data_table","title":"Model pricing table","columns":["Model","Input","Cached input"],"data":[{"Model":"gpt-5.2","Input":0.875,"Cached input":0.0875},{"Model":"gpt-5.2-pro","Input":10.50,"Cached input":null},{"Model":"gpt-5.1","Input":0.625,"Cached input":0.0625},{"Model":"gpt-5","Input":0.625,"Cached input":0.0625},{"Model":"gpt-5-mini","Input":0.125,"Cached input":0.0125},{"Model":"gpt-5-nano","Input":0.025,"Cached input":0.0025},{"Model":"gpt-5-pro","Input":7.50,"Cached input":null},{"Model":"gpt-4.1","Input":1.00,"Cached input":null},{"Model":"gpt-4.1-mini","Input":0.20,"Cached input":null},{"Model":"gpt-4.1-nano","Input":0.05,"Cached input":null},{"Model":"gpt-4o","Input":1.25,"Cached input":null},{"Model":"gpt-4o-mini","Input":0.075,"Cached input":null},{"Model":"o4-mini","Input":0.55,"Cached input":null},{"Model":"o3","Input":1.00,"Cached input":null},{"Model":"o3-mini","Input":0.55,"Cached input":null},{"Model":"o3-pro","Input":10.00,"Cached input":null},{"Model":"o1","Input":7.50,"Cached input":null},{"Model":"o1-mini","Input":0.55,"Cached input":null},{"Model":"o1-pro","Input":75.00,"Cached input":null},{"Model":"gpt-4o-2024-05-13","Input":2.50,"Cached input":null},{"Model":"gpt-4-turbo-2024-04-09","Input":5.00,"Cached input":null},{"Model":"gpt-4-0125-preview","Input":5.00,"Cached input":null},{"Model":"gpt-4-1106-preview","Input":5.00,"Cached input":null},{"Model":"gpt-4-1106-vision-preview","Input":5.00,"Cached input":null},{"Model":"gpt-4-0613","Input":15.00,"Cached input":null},{"Model":"gpt-4-0314","Input":15.00,"Cached input":null}],"unit":"USD"}
</transcription_json>

<transcription_notes>
- Type: Two-column documentation page (left navigation, right content table).
- Visual: Left column shows site navigation headings "Agents SDK", "Tools", "Run and scale" with nested items; right column contains a three-column pricing table with thin grey divider lines and a vertical scrollbar visible on the far right.
- Colors: Navigation text in dark grey on very light background; table header bold/darker; table rows separated by light grey horizontal lines. Scrollbar is light grey.
- The table header reads: "Model    Input    Cached input".
- Dash ("-") in "Cached input" column indicates no cached-input price (represented as null in JSON).
- Page cropping: bottom of left navigation may continue beyond visible area; some navigation items shown with trailing chevrons (">") indicating subpages.
</transcription_notes>
</transcription_table>

<transcription_page_footer> Page [unclear] | [unclear: Company?] </transcription_page_footer>
<transcription_page_header>Models | Pricing</transcription_page_header>

<!-- Section 1 -->
<!-- Column 1 -->
**Navigation**

Responses API  
Using tools

Agents SDK

Overview  
Quickstart  
Agent definitions  
Models and providers  
Running agents  
Sandbox agents  
Orchestration  
Guardrails  
Results and state  
Integrations and observability  
Evaluate agent workflows  
Voice agents  
Agent Builder  >

Tools

Web search  
MCP and Connectors  
Skills  
Shell  
Computer use  
File search and retrieval  >  
Tool search  
More tools  >

Run and scale

Conversation state  
Background mode  
Streaming  
WebSocket mode  
Webhooks  
File inputs  
Context management  >

<!-- Column 2 -->
**Model pricing (table visible in center column)**

<transcription_table>
**Table 1: Model | Input | Cached input**

| Model                                 | Input    | Cached input |
|---------------------------------------|----------:|--------------|
| gpt-5.2                               | $0.875   | $0.0875      |
| gpt-5.2-pro                           | $10.50   | -            |
| gpt-5.1                               | $0.625   | $0.0625      |
| gpt-5                                 | $0.625   | $0.0625      |
| gpt-5-mini                            | $0.125   | $0.0125      |
| gpt-5-nano                            | $0.025   | $0.0025      |
| gpt-5-pro                             | $7.50    | -            |
| gpt-4.1                               | $1.00    | -            |
| gpt-4.1-mini                          | $0.20    | -            |
| gpt-4.1-nano                          | $0.05    | -            |
| gpt-4o                                | $1.25    | -            |
| gpt-4o-mini                           | $0.075   | -            |
| o4-mini                               | $0.55    | -            |
| o3                                    | $1.00    | -            |
| o3-mini                               | $0.55    | -            |
| o3-pro                                | $10.00   | -            |
| o1                                    | $7.50    | -            |
| o1-mini                               | $0.55    | -            |
| o1-pro                                | $75.00   | -            |
| gpt-4o-2024-05-13                     | $2.50    | -            |
| gpt-4-turbo-2024-04-09                | $5.00    | -            |
| gpt-4-0125-preview                    | $5.00    | -            |
| gpt-4-1106-preview                    | $5.00    | -            |
| gpt-4-1106-vision-preview             | $5.00    | -            |
| gpt-4-0613                            | $15.00   | -            |
| gpt-4-0314                            | $15.00   | -            |

<transcription_json>
{"table_type":"data_table","title":"Model | Input | Cached input","columns":["Model","Input","Cached input"],"data":[{"Model":"gpt-5.2","Input":0.875,"Cached input":0.0875},{"Model":"gpt-5.2-pro","Input":10.50,"Cached input":null},{"Model":"gpt-5.1","Input":0.625,"Cached input":0.0625},{"Model":"gpt-5","Input":0.625,"Cached input":0.0625},{"Model":"gpt-5-mini","Input":0.125,"Cached input":0.0125},{"Model":"gpt-5-nano","Input":0.025,"Cached input":0.0025},{"Model":"gpt-5-pro","Input":7.50,"Cached input":null},{"Model":"gpt-4.1","Input":1.00,"Cached input":null},{"Model":"gpt-4.1-mini","Input":0.20,"Cached input":null},{"Model":"gpt-4.1-nano","Input":0.05,"Cached input":null},{"Model":"gpt-4o","Input":1.25,"Cached input":null},{"Model":"gpt-4o-mini","Input":0.075,"Cached input":null},{"Model":"o4-mini","Input":0.55,"Cached input":null},{"Model":"o3","Input":1.00,"Cached input":null},{"Model":"o3-mini","Input":0.55,"Cached input":null},{"Model":"o3-pro","Input":10.00,"Cached input":null},{"Model":"o1","Input":7.50,"Cached input":null},{"Model":"o1-mini","Input":0.55,"Cached input":null},{"Model":"o1-pro","Input":75.00,"Cached input":null},{"Model":"gpt-4o-2024-05-13","Input":2.50,"Cached input":null},{"Model":"gpt-4-turbo-2024-04-09","Input":5.00,"Cached input":null},{"Model":"gpt-4-0125-preview","Input":5.00,"Cached input":null},{"Model":"gpt-4-1106-preview","Input":5.00,"Cached input":null},{"Model":"gpt-4-1106-vision-preview","Input":5.00,"Cached input":null},{"Model":"gpt-4-0613","Input":15.00,"Cached input":null},{"Model":"gpt-4-0314","Input":15.00,"Cached input":null}],"unit":"USD"}
</transcription_json>

<transcription_notes>
- Visual layout: three-column page: narrow left nav, wide center with table, narrow right whitespace and scrollbar visible.
- Table header: "Model" | "Input" | "Cached input" aligned at top of center column.
- Most "Cached input" cells are a dash ("-") except for models where a cached rate is shown (gpt-5.2: $0.0875; gpt-5.1 and gpt-5: $0.0625; gpt-5-mini: $0.0125; gpt-5-nano: $0.0025).
- Fonts: small, UI-style; muted grey dividers between rows.
- Right edge: vertical scrollbar visible (indicates more content may be scrollable).
- Left navigation: hierarchical with sections ("Agents SDK", "Tools", "Run and scale"); some items show a ">" chevron indicating nested pages (rendered here as ">").
- No decorative logos transcribed.
</transcription_notes>
</transcription_table>

<transcription_page_footer>Page 1 | OpenAI</transcription_page_footer>
<transcription_page_header>Responses API | Using tools</transcription_page_header>

# Responses API

<!-- Section 1 -->
<!-- Column 1 -->
Responses API
Using tools

Agents SDK

Overview
Quickstart
Agent definitions
Models and providers
Running agents
Sandbox agents
Orchestration
Guardrails
Results and state
Integrations and observability
Evaluate agent workflows
Voice agents
Agent Builder ›

Tools

Web search
MCP and Connectors
Skills
Shell
Computer use
File search and retrieval ›
Tool search
More tools ›

Run and scale

Conversation state
Background mode
Streaming
WebSocket mode
Webhooks
File inputs
Context management ›

<!-- Column 2 -->

<transcription_table>
**Table: Model | Input | Cached input**

| Model | Input | Cached input |
|-------|-------:|--------------:|
| gpt-5.2 | $0.875 | $0.0875 |
| gpt-5.2-pro | $10.50 | - |
| gpt-5.1 | $0.625 | $0.0625 |
| gpt-5 | $0.625 | $0.0625 |
| gpt-5-mini | $0.125 | $0.0125 |
| gpt-5-nano | $0.025 | $0.0025 |
| gpt-5-pro | $7.50 | - |
| gpt-4.1 | $1.00 | - |
| gpt-4.1-mini | $0.20 | - |
| gpt-4.1-nano | $0.05 | - |
| gpt-4o | $1.25 | - |
| gpt-4o-mini | $0.075 | - |
| o4-mini | $0.55 | - |
| o3 | $1.00 | - |
| o3-mini | $0.55 | - |
| o3-pro | $10.00 | - |
| o1 | $7.50 | - |
| o1-mini | $0.55 | - |
| o1-pro | $75.00 | - |
| gpt-4o-2024-05-13 | $2.50 | - |
| gpt-4-turbo-2024-04-09 | $5.00 | - |
| gpt-4-0125-preview | $5.00 | - |
| gpt-4-1106-preview | $5.00 | - |
| gpt-4-1106-vision-preview | $5.00 | - |
| gpt-4-0613 | $15.00 | - |
| gpt-4-0314 | $15.00 | - |

<transcription_json>
{"table_type":"pricing_table","title":"Model pricing (Input & Cached input)","columns":["Model","Input","Cached input"],"unit":"USD","data":[{"Model":"gpt-5.2","Input":0.875,"Cached_input":0.0875},{"Model":"gpt-5.2-pro","Input":10.50,"Cached_input":null},{"Model":"gpt-5.1","Input":0.625,"Cached_input":0.0625},{"Model":"gpt-5","Input":0.625,"Cached_input":0.0625},{"Model":"gpt-5-mini","Input":0.125,"Cached_input":0.0125},{"Model":"gpt-5-nano","Input":0.025,"Cached_input":0.0025},{"Model":"gpt-5-pro","Input":7.50,"Cached_input":null},{"Model":"gpt-4.1","Input":1.00,"Cached_input":null},{"Model":"gpt-4.1-mini","Input":0.20,"Cached_input":null},{"Model":"gpt-4.1-nano","Input":0.05,"Cached_input":null},{"Model":"gpt-4o","Input":1.25,"Cached_input":null},{"Model":"gpt-4o-mini","Input":0.075,"Cached_input":null},{"Model":"o4-mini","Input":0.55,"Cached_input":null},{"Model":"o3","Input":1.00,"Cached_input":null},{"Model":"o3-mini","Input":0.55,"Cached_input":null},{"Model":"o3-pro","Input":10.00,"Cached_input":null},{"Model":"o1","Input":7.50,"Cached_input":null},{"Model":"o1-mini","Input":0.55,"Cached_input":null},{"Model":"o1-pro","Input":75.00,"Cached_input":null},{"Model":"gpt-4o-2024-05-13","Input":2.50,"Cached_input":null},{"Model":"gpt-4-turbo-2024-04-09","Input":5.00,"Cached_input":null},{"Model":"gpt-4-0125-preview","Input":5.00,"Cached_input":null},{"Model":"gpt-4-1106-preview","Input":5.00,"Cached_input":null},{"Model":"gpt-4-1106-vision-preview","Input":5.00,"Cached_input":null},{"Model":"gpt-4-0613","Input":15.00,"Cached_input":null},{"Model":"gpt-4-0314","Input":15.00,"Cached_input":null}]}
</transcription_json>

<transcription_notes>
- Layout: two-column page; left column is navigation (Agents SDK, Tools, Run and scale sections). Right column is a pricing table titled implicitly by column headers "Model | Input | Cached input".
- Visuals: light grey table gridlines, black text. Right-side vertical scrollbar visible (decorative).
- Many "Cached input" cells display "-" (represented as null in JSON).
- Left navigation contains chevrons for expandable items (Agent Builder ›, File search and retrieval ›, More tools ›, Context management ›).
- Source: UI screenshot of documentation/settings page. No logos transcribed.
</transcription_notes>
</transcription_table>

<!-- Decorative: [right scrollbar] -->

<transcription_page_footer>Page [unclear] | [unclear]</transcription_page_footer>
<transcription_page_header> Responses API | Models Pricing </transcription_page_header>

# Responses API

<!-- Section 1 -->
<!-- Column 1 -->
- Responses API
- Using tools

Agents SDK
: **Overview**
: **Quickstart**
: **Agent definitions**
: **Models and providers**
: **Running agents**
: **Sandbox agents**
: **Orchestration**
: **Guardrails**
: **Results and state**
: **Integrations and observability**
: **Evaluate agent workflows**
: **Voice agents**
: **Agent Builder** >

Tools
: **Web search**
: **MCP and Connectors**
: **Skills**
: **Shell**
: **Computer use**
: **File search and retrieval** >
: **Tool search**
: **More tools** >

Run and scale
: **Conversation state**
: **Background mode**
: **Streaming**
: **WebSocket mode**
: **Webhooks**
: **File inputs**
: **Context management** >

<!-- Column 2 -->
## Model pricing

<transcription_table>
**Table 1: Model Pricing**

| Model | Input | Cached input |
|-------|-------:|-------------:|
| gpt-5.2 | $0.875 | $0.0875 |
| gpt-5.2-pro | $10.50 | - |
| gpt-5.1 | $0.625 | $0.0625 |
| gpt-5 | $0.625 | $0.0625 |
| gpt-5-mini | $0.125 | $0.0125 |
| gpt-5-nano | $0.025 | $0.0025 |
| gpt-5-pro | $7.50 | - |
| gpt-4.1 | $1.00 | - |
| gpt-4.1-mini | $0.20 | - |
| gpt-4.1-nano | $0.05 | - |
| gpt-4o | $1.25 | - |
| gpt-4o-mini | $0.075 | - |
| o4-mini | $0.55 | - |
| o3 | $1.00 | - |
| o3-mini | $0.55 | - |
| o3-pro | $10.00 | - |
| o1 | $7.50 | - |
| o1-mini | $0.55 | - |
| o1-pro | $75.00 | - |
| gpt-4o-2024-05-13 | $2.50 | - |
| gpt-4-turbo-2024-04-09 | $5.00 | - |
| gpt-4-0125-preview | $5.00 | - |
| gpt-4-1106-preview | $5.00 | - |
| gpt-4-1106-vision-preview | $5.00 | - |
| gpt-4-0613 | $15.00 | - |
| gpt-4-0314 | $15.00 | - |

<transcription_json>
{"table_type":"data_table","title":"Model Pricing","columns":["Model","Input","Cached input"],"data":[{"Model":"gpt-5.2","Input":0.875,"Cached input":0.0875},{"Model":"gpt-5.2-pro","Input":10.50,"Cached input":null},{"Model":"gpt-5.1","Input":0.625,"Cached input":0.0625},{"Model":"gpt-5","Input":0.625,"Cached input":0.0625},{"Model":"gpt-5-mini","Input":0.125,"Cached input":0.0125},{"Model":"gpt-5-nano","Input":0.025,"Cached input":0.0025},{"Model":"gpt-5-pro","Input":7.50,"Cached input":null},{"Model":"gpt-4.1","Input":1.00,"Cached input":null},{"Model":"gpt-4.1-mini","Input":0.20,"Cached input":null},{"Model":"gpt-4.1-nano","Input":0.05,"Cached input":null},{"Model":"gpt-4o","Input":1.25,"Cached input":null},{"Model":"gpt-4o-mini","Input":0.075,"Cached input":null},{"Model":"o4-mini","Input":0.55,"Cached input":null},{"Model":"o3","Input":1.00,"Cached input":null},{"Model":"o3-mini","Input":0.55,"Cached input":null},{"Model":"o3-pro","Input":10.00,"Cached input":null},{"Model":"o1","Input":7.50,"Cached input":null},{"Model":"o1-mini","Input":0.55,"Cached input":null},{"Model":"o1-pro","Input":75.00,"Cached input":null},{"Model":"gpt-4o-2024-05-13","Input":2.50,"Cached input":null},{"Model":"gpt-4-turbo-2024-04-09","Input":5.00,"Cached input":null},{"Model":"gpt-4-0125-preview","Input":5.00,"Cached input":null},{"Model":"gpt-4-1106-preview","Input":5.00,"Cached input":null},{"Model":"gpt-4-1106-vision-preview","Input":5.00,"Cached input":null},{"Model":"gpt-4-0613","Input":15.00,"Cached input":null},{"Model":"gpt-4-0314","Input":15.00,"Cached input":null}],"unit":"USD","currency_format":"dollar"}
</transcription_json>

<transcription_notes>
- Page layout: two-column. Left column is navigation; right column is the pricing table.
- Visual details: thin gray vertical scrollbar at right of content area; table centered in wide white content area with light gray horizontal row separators.
- Many "Cached input" values are "-" in the visual table; represented as null in JSON.
- Notable: "gpt-5-pro" appears twice with different Input prices ($7.50 and $10.50 for gpt-5.2-pro and gpt-5-pro) — preserved ordering as seen.
- Fonts: sans-serif UI, small left navigation, larger spacing on table rows.
- No decorative logos transcribed. Scrollbar and page chrome omitted.
</transcription_notes>
</transcription_table>

<transcription_page_footer> Page 1 | [unclear] </transcription_page_footer>
<transcription_page_header>Responses API | Using tools</transcription_page_header>

# Responses API

<!-- Section 1 -->
<!-- Column 1 -->
- Left navigation (sidebar) present with multiple sections (Agents SDK, Tools, Run and scale, etc.). Sidebar text not fully transcribed here (minimal transcription).

<!-- Column 2 -->
## Model pricing

<transcription_table>
**Model Pricing Table**

| Model | Input | Cached input |
|-------|-------:|:------------:|
| gpt-5.2 | $0.875 | $0.0875 |
| gpt-5.2-pro | $10.50 | - |
| gpt-5.1 | $0.625 | $0.0625 |
| gpt-5 | $0.625 | $0.0625 |
| gpt-5-mini | $0.125 | $0.0125 |
| gpt-5-nano | $0.025 | $0.0025 |
| gpt-5-pro | $7.50 | - |
| gpt-4.1 | $1.00 | - |
| gpt-4.1-mini | $0.20 | - |
| gpt-4.1-nano | $0.05 | - |
| gpt-4o | $1.25 | - |
| gpt-4o-mini | $0.075 | - |
| o4-mini | $0.55 | - |
| o3 | $1.00 | - |
| o3-mini | $0.55 | - |
| o3-pro | $10.00 | - |
| o1 | $7.50 | - |
| o1-mini | $0.55 | - |
| o1-pro | $75.00 | - |
| gpt-4o-2024-05-13 | $2.50 | - |
| gpt-4-turbo-2024-04-09 | $5.00 | - |
| gpt-4-0125-preview | $5.00 | - |
| gpt-4-1106-preview | $5.00 | - |
| gpt-4-1106-vision-preview | $5.00 | - |
| gpt-4-0613 | $15.00 | - |
| gpt-4-0314 | $15.00 | - |

<transcription_json>
{"table_type":"data_table","title":"Model Pricing Table","columns":["Model","Input","Cached input"],"data":[{"Model":"gpt-5.2","Input":0.875,"Cached input":0.0875},{"Model":"gpt-5.2-pro","Input":10.5,"Cached input":null},{"Model":"gpt-5.1","Input":0.625,"Cached input":0.0625},{"Model":"gpt-5","Input":0.625,"Cached input":0.0625},{"Model":"gpt-5-mini","Input":0.125,"Cached input":0.0125},{"Model":"gpt-5-nano","Input":0.025,"Cached input":0.0025},{"Model":"gpt-5-pro","Input":7.5,"Cached input":null},{"Model":"gpt-4.1","Input":1.0,"Cached input":null},{"Model":"gpt-4.1-mini","Input":0.2,"Cached input":null},{"Model":"gpt-4.1-nano","Input":0.05,"Cached input":null},{"Model":"gpt-4o","Input":1.25,"Cached input":null},{"Model":"gpt-4o-mini","Input":0.075,"Cached input":null},{"Model":"o4-mini","Input":0.55,"Cached input":null},{"Model":"o3","Input":1.0,"Cached input":null},{"Model":"o3-mini","Input":0.55,"Cached input":null},{"Model":"o3-pro","Input":10.0,"Cached input":null},{"Model":"o1","Input":7.5,"Cached input":null},{"Model":"o1-mini","Input":0.55,"Cached input":null},{"Model":"o1-pro","Input":75.0,"Cached input":null},{"Model":"gpt-4o-2024-05-13","Input":2.5,"Cached input":null},{"Model":"gpt-4-turbo-2024-04-09","Input":5.0,"Cached input":null},{"Model":"gpt-4-0125-preview","Input":5.0,"Cached input":null},{"Model":"gpt-4-1106-preview","Input":5.0,"Cached input":null},{"Model":"gpt-4-1106-vision-preview","Input":5.0,"Cached input":null},{"Model":"gpt-4-0613","Input":15.0,"Cached input":null},{"Model":"gpt-4-0314","Input":15.0,"Cached input":null}],"unit":"USD"}
</transcription_json>

<transcription_notes>
- Layout: two-column page with left navigation (sidebar) and main content area (table) on the right.
- Visual: light background, gray divider lines between table rows, vertical scrollbar visible on right.
- Table header columns: "Model", "Input", "Cached input".
- Dashes ("-") in "Cached input" were recorded as null in JSON.
- No additional chart/graphics on this page besides the pricing table and sidebar.
</transcription_notes>
</transcription_table>

<!-- Decorative: [vertical scrollbar] -->

<transcription_page_footer>Page 1 | OpenAI</transcription_page_footer>
<transcription_page_header> Responses API | [unclear] </transcription_page_header>

<!-- Section 1 -->
<!-- Column 1 -->
**Agents SDK**

Overview  
Quickstart  
Agent definitions  
Models and providers  
Running agents  
Sandbox agents  
Orchestration  
Guardrails  
Results and state  
Integrations and observability  
Evaluate agent workflows  
Voice agents  
Agent Builder >

**Tools**

Web search  
MCP and Connectors  
Skills  
Shell  
Computer use  
File search and retrieval >  
Tool search  
More tools >

**Run and scale**

Conversation state  
Background mode  
Streaming  
WebSocket mode  
Webhooks  
File inputs  
Context management >

<!-- Column 2 -->
<!-- Section 2 -->

<transcription_table>
**Table: Model pricing — Input and Cached input**

| Model | Input | Cached input |
|-------|-------:|-------------:|
| gpt-5.2 | $0.875 | $0.0875 |
| gpt-5.2-pro | $10.50 | - |
| gpt-5.1 | $0.625 | $0.0625 |
| gpt-5 | $0.625 | $0.0625 |
| gpt-5-mini | $0.125 | $0.0125 |
| gpt-5-nano | $0.025 | $0.0025 |
| gpt-5-pro | $7.50 | - |
| gpt-4.1 | $1.00 | - |
| gpt-4.1-mini | $0.20 | - |
| gpt-4.1-nano | $0.05 | - |
| gpt-4o | $1.25 | - |
| gpt-4o-mini | $0.075 | - |
| o4-mini | $0.55 | - |
| o3 | $1.00 | - |
| o3-mini | $0.55 | - |
| o3-pro | $10.00 | - |
| o1 | $7.50 | - |
| o1-mini | $0.55 | - |
| o1-pro | $75.00 | - |
| gpt-4o-2024-05-13 | $2.50 | - |
| gpt-4-turbo-2024-04-09 | $5.00 | - |
| gpt-4-0125-preview | $5.00 | - |
| gpt-4-1106-preview | $5.00 | - |
| gpt-4-1106-vision-preview | $5.00 | - |
| gpt-4-0613 | $15.00 | - |
| gpt-4-0314 | $15.00 | - |

<transcription_json>
{"table_type":"data_table","title":"Model pricing — Input and Cached input","columns":["Model","Input","Cached input"],"data":[{"Model":"gpt-5.2","Input":0.875,"Cached input":0.0875},{"Model":"gpt-5.2-pro","Input":10.50,"Cached input":null},{"Model":"gpt-5.1","Input":0.625,"Cached input":0.0625},{"Model":"gpt-5","Input":0.625,"Cached input":0.0625},{"Model":"gpt-5-mini","Input":0.125,"Cached input":0.0125},{"Model":"gpt-5-nano","Input":0.025,"Cached input":0.0025},{"Model":"gpt-5-pro","Input":7.50,"Cached input":null},{"Model":"gpt-4.1","Input":1.00,"Cached input":null},{"Model":"gpt-4.1-mini","Input":0.20,"Cached input":null},{"Model":"gpt-4.1-nano","Input":0.05,"Cached input":null},{"Model":"gpt-4o","Input":1.25,"Cached input":null},{"Model":"gpt-4o-mini","Input":0.075,"Cached input":null},{"Model":"o4-mini","Input":0.55,"Cached input":null},{"Model":"o3","Input":1.00,"Cached input":null},{"Model":"o3-mini","Input":0.55,"Cached input":null},{"Model":"o3-pro","Input":10.00,"Cached input":null},{"Model":"o1","Input":7.50,"Cached input":null},{"Model":"o1-mini","Input":0.55,"Cached input":null},{"Model":"o1-pro","Input":75.00,"Cached input":null},{"Model":"gpt-4o-2024-05-13","Input":2.50,"Cached input":null},{"Model":"gpt-4-turbo-2024-04-09","Input":5.00,"Cached input":null},{"Model":"gpt-4-0125-preview","Input":5.00,"Cached input":null},{"Model":"gpt-4-1106-preview","Input":5.00,"Cached input":null},{"Model":"gpt-4-1106-vision-preview","Input":5.00,"Cached input":null},{"Model":"gpt-4-0613","Input":15.00,"Cached input":null},{"Model":"gpt-4-0314","Input":15.00,"Cached input":null}],"unit":"[unclear]"}
</transcription_json>

<transcription_notes>
- Type: Two-column page: left column = navigation (Agents SDK, Tools, Run and scale). Right column = pricing table.
- Visual details: Right-side table is center-aligned on page with a vertical scrollbar visible at right edge of table area. Text is black on white background. Left navigation uses smaller font; some nav items have trailing chevrons ">" indicating nested pages.
- Cached input column shows "-" for many models (represented as null in JSON).
- No additional numeric context (e.g., per-token or per-1K-tokens unit) is readable in the visible portion of the page — unit marked as [unclear].
- Decorative: scrollbar on right, page margins, and small UI chrome are decorative and not transcribed.
</transcription_notes>
</transcription_table>

<transcription_page_footer> Page [unclear] | [unclear] </transcription_page_footer>
