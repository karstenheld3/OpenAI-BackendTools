<transcription_page_header>Models & pricing / Models | Model deprecations</transcription_page_header>

<!-- Section 1 -->
<!-- Column 1 -->
Models

Models overview  
Model IDs and versioning  
Choosing a model  
What's new in Claude Opus 4.7  
Upgrade between model versions  
Model deprecations  
Model cards  
System prompts  
Pricing

<!-- Column 2 -->

# Model deprecations

As safer and more capable models launch, Anthropic regularly retires older ones. Applications relying on Anthropic models may need occasional updates to keep working. Impacted customers will always be notified by email and in the documentation.

This page lists all API deprecations, along with recommended replacements.

## Overview

Anthropic uses the following terms to describe the model lifecycle:

- Active: The model is fully supported and recommended for use.  
- Legacy: The model will no longer receive updates and may be deprecated in the future.  
- Deprecated: The model is still functional but no longer recommended. Anthropic provides a recommended replacement and assigns a retirement date.  
- Retired: The model is no longer available for use. Requests to retired models will fail.

> Deprecated models are likely to be less reliable than active models. Move workloads to active models to maintain the highest level of support and reliability.

The dates on this page apply to Anthropic-operated platforms: the Claude API, Claude Platform on AWS, and Microsoft Foundry. Partner-operated platforms (Amazon Bedrock and Vertex AI) set their own retirement schedules, so a model's lifecycle status and dates can differ. See the Amazon Bedrock, Amazon Bedrock (legacy), and Vertex AI model tables.

## Migrating to replacements

Once a model is deprecated, migrate all usage to a suitable replacement before the retirement date. Requests to models past the retirement date will fail.

To help measure the performance of replacement models on your tasks, consider thorough testing of your applications with the new models well before the retirement date.

For specific instructions on migrating to the latest Claude models, see the Migration guide.

## Notifications

Anthropic notifies customers with active deployments for models with upcoming retirements, providing at least 60 days notice before model retirement for publicly released models.

## Auditing model usage

[unclear: full paragraph not entirely visible]

<!-- Section 2 -->
<!-- Column 3 -->

Overview

- Migrating to replacements
- Notifications
- Auditing model usage
- Best practices
- Deprecation downsides and mitigations
- Model status
- Deprecation history

Deprecation history

- 2026-04-14: Claude Sonnet 4 and Claude Opus 4 models  
- 2026-02-19: Claude Haiku 3 model  
- 2025-12-19: Claude Haiku 3.5 model  
- 2025-10-28: Claude Sonnet 3.7 model  
- 2025-08-13: Claude Sonnet 3.5 models  
- 2025-06-30: Claude Opus 3 model  
- 2025-01-21: Claude 2, Claude 2.1, and Claude Sonnet 3 models  
- 2024-09-04: Claude 1 and Instant models

<transcription_notes>
- Page type: Documentation web page (Claude API Docs).  
- Layout: 3-column layout: left navigation (light beige background), main content center (white/very light background), right sidebar table of contents.  
- Visual elements: Breadcrumb above title reads "Models & pricing / Models". Title "Model deprecations" is H1 centered-left. Warning box (pale yellow/beige with orange border and warning icon) contains the sentence about deprecated models being less reliable. Right sidebar shows an "Overview" navigation and "Deprecation history" list with date-prefixed entries (most recent at top). Left navigation highlights "Model deprecations". Top nav and site chrome are decorative and not transcribed.  
- Colors: left nav background: very light beige; main content background: very light cream; warning box background: pale yellow/beige with thin darker border; right sidebar text in muted grey.  
- Missing / unclear text: The full "Auditing model usage" section paragraph text is partially cut off in the provided image — marked with [unclear]. No charts or tables on the visible portion of the page.  
</transcription_notes>

<transcription_page_footer>Page [unclear] | Anthropic</transcription_page_footer>
<transcription_page_header>Auditing model usage</transcription_page_header>

# Auditing model usage

<!-- Section 1 -->
To help identify usage of deprecated models, customers can access an audit of their API usage. Follow these steps:

1. Go to the Usage page in Claude Console  
2. Click the "Export" button  
3. Review the downloaded CSV to see usage broken down by API key and model

This audit will help you locate any instances where your application is still using deprecated models, allowing you to prioritize updates to newer models before the retirement date.

<!-- Section 2 -->
## Best practices

1. Regularly check the documentation for updates on model deprecations.  
2. Test your applications with newer models well before the retirement date of your current model.  
3. Update your code to use the recommended replacement model as soon as possible.  
4. Contact the support team if you need assistance with migration or have any questions.

<!-- Section 3 -->
## Deprecation downsides and mitigations

Anthropic currently deprecates and retires models to ensure capacity for new model releases. This comes with downsides:

- Users who value specific models must migrate to new versions  
- Researchers lose access to models for ongoing and comparative studies  
- Model retirement introduces safety- and model welfare-related risks

At some point, Anthropic hopes to make past models publicly available again. In the meantime, Anthropic has committed to long-term preservation of model weights and other measures to help mitigate these impacts. For more details, see Commitments on Model Deprecation and Preservation.

<!-- Section 4 -->
## Model status

Current and recently retired models are listed in the following table with their status:

<transcription_table>
**Model status**

| API model name | Current state | Deprecated | Tentative retirement date |
|----------------|---------------|-----------:|---------------------------|
| claude-opus-4-7 | Active | N/A | Not sooner than April 16, 2027 |
| claude-opus-4-6 | Active | N/A | Not sooner than February 5, 2027 |
| claude-opus-4-5-20251101 | Active | N/A | Not sooner than November 24, 2026 |
| claude-opus-4-1-20250805 | Active | N/A | Not sooner than August 5, 2026 |
| claude-opus-4-20250514 | Deprecated | April 14, 2026 | June 15, 2026 |
| claude-sonnet-4-6 | Active | N/A | Not sooner than February 17, 2027 |
| claude-sonnet-4-5-20250929 | Active | N/A | Not sooner than September 29, 2026 |
| claude-sonnet-4-20250514 | Deprecated | April 14, 2026 | June 15, 2026 |

<transcription_json>
{"table_type":"data_table","title":"Model status","columns":["API model name","Current state","Deprecated","Tentative retirement date"],"data":[{"API model name":"claude-opus-4-7","Current state":"Active","Deprecated":"N/A","Tentative retirement date":"Not sooner than April 16, 2027"},{"API model name":"claude-opus-4-6","Current state":"Active","Deprecated":"N/A","Tentative retirement date":"Not sooner than February 5, 2027"},{"API model name":"claude-opus-4-5-20251101","Current state":"Active","Deprecated":"N/A","Tentative retirement date":"Not sooner than November 24, 2026"},{"API model name":"claude-opus-4-1-20250805","Current state":"Active","Deprecated":"N/A","Tentative retirement date":"Not sooner than August 5, 2026"},{"API model name":"claude-opus-4-20250514","Current state":"Deprecated","Deprecated":"April 14, 2026","Tentative retirement date":"June 15, 2026"},{"API model name":"claude-sonnet-4-6","Current state":"Active","Deprecated":"N/A","Tentative retirement date":"Not sooner than February 17, 2027"},{"API model name":"claude-sonnet-4-5-20250929","Current state":"Active","Deprecated":"N/A","Tentative retirement date":"Not sooner than September 29, 2026"},{"API model name":"claude-sonnet-4-20250514","Current state":"Deprecated","Deprecated":"April 14, 2026","Tentative retirement date":"June 15, 2026"}]}
</transcription_json>

<transcription_notes>
- Table appears as a multi-row list with left column showing model names in grey rounded "pill" labels.  
- Columns (left to right): API model name | Current state | Deprecated | Tentative retirement date.  
- Dates use literal phrasing "Not sooner than <date>" for active models; deprecated models show a deprecation date and a separate tentative retirement date.  
- Visual: alternating row backgrounds are subtle; pill-style model names are light grey with rounded corners.  
- The screenshot shows additional rows below this region that are cut off; table likely continues beyond the visible area. [unclear: exact number of total rows beyond view]
</transcription_notes>
</transcription_table>

<transcription_page_footer>Page [unclear] | Anthropic</transcription_page_footer>
<transcription_page_header> Deprecation history | Models </transcription_page_header>

# Deprecation history

All deprecations are listed below, with the most recent announcements at the top.

<!-- Section 1 -->
## 2026-04-14: Claude Sonnet 4 and Claude Opus 4 models

On April 14, 2026, Anthropic notified developers using Claude Sonnet 4 and Claude Opus 4 models of their upcoming retirement on the Claude API.

<transcription_table>
**Table: Claude Sonnet 4 & Claude Opus 4 deprecation**

| Retirement date | Deprecated model | Recommended replacement |
|-----------------|------------------|-------------------------|
| June 15, 2026 | claude-sonnet-4-20250514 | claude-sonnet-4-6 |
| June 15, 2026 | claude-opus-4-20250514 | claude-opus-4-7 |

<transcription_json>
{"table_type":"data_table","title":"Claude Sonnet 4 & Claude Opus 4 deprecation","columns":["Retirement date","Deprecated model","Recommended replacement"],"data":[{"Retirement date":"June 15, 2026","Deprecated model":"claude-sonnet-4-20250514","Recommended replacement":"claude-sonnet-4-6"},{"Retirement date":"June 15, 2026","Deprecated model":"claude-opus-4-20250514","Recommended replacement":"claude-opus-4-7"}],"unit":null}
</transcription_json>

<transcription_notes>
- Table has three columns: "Retirement date", "Deprecated model", "Recommended replacement".
- Deprecated model and replacement values are displayed in rounded, pale-beige code/pill UI elements on the page.
- Table rows are separated by subtle horizontal rules; typography is serif for headings and sans-serif for table content.
</transcription_notes>
</transcription_table>

<!-- Section 2 -->
## 2026-02-19: Claude Haiku 3 model

<transcription_image>
**Figure: Info box — Claude Haiku 3 retirement**

```ascii
[INFO BOX - rounded blue]
(i) This model was retired April 20, 2026.
```

<transcription_json>
{"figure_type":"info_box","text":"This model was retired April 20, 2026.","icon":"information","color":"blue","style":"rounded","associated_with":"Claude Haiku 3 deprecation announcement (2026-02-19)"}
</transcription_json>

<transcription_notes>
- A full-width rounded rectangular blue box with a left information icon (circled "i").
- Box background: light blue; border darker blue; text centered vertically in the box.
- Purpose: callout indicating the model's actual retirement date.
</transcription_notes>
</transcription_image>

On February 19, 2026, Anthropic notified developers using Claude Haiku 3 model of its upcoming retirement on the Claude API.

<transcription_table>
**Table: Claude Haiku 3 deprecation**

| Retirement date | Deprecated model | Recommended replacement |
|-----------------|------------------|-------------------------|
| April 20, 2026 | claude-3-haiku-20240307 | claude-haiku-4-5-20251001 |

<transcription_json>
{"table_type":"data_table","title":"Claude Haiku 3 deprecation","columns":["Retirement date","Deprecated model","Recommended replacement"],"data":[{"Retirement date":"April 20, 2026","Deprecated model":"claude-3-haiku-20240307","Recommended replacement":"claude-haiku-4-5-20251001"}],"unit":null}
</transcription_json>

<transcription_notes>
- Single-row table. Model identifiers are shown in rounded beige code/pill UI elements.
- The retirement date in the blue info box (above) matches the "Retirement date" table cell.
</transcription_notes>
</transcription_table>

<!-- Section 3 -->
## 2025-12-19: Claude Haiku 3.5 model

<transcription_image>
**Figure: Info box — Claude Haiku 3.5 retirement**

```ascii
[INFO BOX - rounded blue]
(i) This model was retired February 19, 2026.
```

<transcription_json>
{"figure_type":"info_box","text":"This model was retired February 19, 2026.","icon":"information","color":"blue","style":"rounded","associated_with":"Claude Haiku 3.5 deprecation announcement (2025-12-19)"}
</transcription_json>

<transcription_notes>
- Same visual style as other info boxes: light-blue rounded rectangle with an information icon at the left.
- Text inside the box: "This model was retired February 19, 2026."
</transcription_notes>
</transcription_image>

On December 19, 2025, Anthropic notified developers using Claude Haiku 3.5 model of its upcoming retirement on the Claude API.

<transcription_table>
**Table: Claude Haiku 3.5 deprecation**

| Retirement date | Deprecated model | Recommended replacement |
|-----------------|------------------|-------------------------|
| February 19, 2026 | claude-3-5-haiku-20241022 | claude-haiku-4-5-20251001 |

<transcription_json>
{"table_type":"data_table","title":"Claude Haiku 3.5 deprecation","columns":["Retirement date","Deprecated model","Recommended replacement"],"data":[{"Retirement date":"February 19, 2026","Deprecated model":"claude-3-5-haiku-20241022","Recommended replacement":"claude-haiku-4-5-20251001"}],"unit":null}
</transcription_json>

<transcription_notes>
- Single-row table; deprecated and replacement model identifiers presented in inline pill/code style.
- The blue info box above indicates the model was retired on February 19, 2026.
</transcription_notes>
</transcription_table>

<transcription_page_footer> Page 1 | Anthropic </transcription_page_footer>
<transcription_page_header> [unclear: page title] | Anthropic </transcription_page_header>

# [unclear: Model retirement notices]

<!-- Section 1 -->
## 2025-10-28: Claude Sonnet 3.7 model

This model was retired February 19, 2026.

On October 28, 2025, Anthropic notified developers using Claude Sonnet 3.7 model of its upcoming retirement on the Claude API.

<transcription_table>
**Table: Retirement details — Claude Sonnet 3.7**

| Retirement date | Deprecated model | Recommended replacement |
|-----------------|------------------|-------------------------|
| February 19, 2026 | claude-3-7-sonnet-20250219 | claude-sonnet-4-6 |

<transcription_json>
{"table_type":"data_table","title":"Retirement details — Claude Sonnet 3.7","columns":["Retirement date","Deprecated model","Recommended replacement"],"data":[{"Retirement date":"February 19, 2026","Deprecated model":"claude-3-7-sonnet-20250219","Recommended replacement":"claude-sonnet-4-6"}]}
</transcription_json>

<transcription_notes>
- Visual: single-row table with three columns. Deprecated model and Recommended replacement shown in light-gray rounded pill/label UI elements.
- The info box above the paragraph is a blue rounded rectangle with an information icon (i) at the left; background color light blue, border slightly darker blue.
- Page background: off-white; content column centered with wide left whitespace.
</transcription_notes>
</transcription_table>

<!-- Section 2 -->
## 2025-08-13: Claude Sonnet 3.5 models

These models were retired October 28, 2025.

On August 13, 2025, Anthropic notified developers using Claude Sonnet 3.5 models of their upcoming retirement.

<transcription_table>
**Table: Retirement details — Claude Sonnet 3.5**

| Retirement date | Deprecated model | Recommended replacement |
|-----------------|------------------|-------------------------|
| October 28, 2025 | claude-3-5-sonnet-20240620 | claude-sonnet-4-6 |
| October 28, 2025 | claude-3-5-sonnet-20241022 | claude-sonnet-4-6 |

<transcription_json>
{"table_type":"data_table","title":"Retirement details — Claude Sonnet 3.5","columns":["Retirement date","Deprecated model","Recommended replacement"],"data":[{"Retirement date":"October 28, 2025","Deprecated model":"claude-3-5-sonnet-20240620","Recommended replacement":"claude-sonnet-4-6"},{"Retirement date":"October 28, 2025","Deprecated model":"claude-3-5-sonnet-20241022","Recommended replacement":"claude-sonnet-4-6"}]}
</transcription_json>

<transcription_notes>
- Visual: two-row table; deprecated model strings are shown as light-gray rounded pill/labels.
- Info box above paragraph: blue rounded rectangle with information icon; text reads "These models were retired October 28, 2025."
</transcription_notes>
</transcription_table>

<!-- Section 3 -->
## 2025-06-30: Claude Opus 3 model

This model was retired January 5, 2026.

On June 30, 2025, Anthropic notified developers using Claude Opus 3 model of its upcoming retirement on the Claude API.

<transcription_table>
**Table: Retirement details — Claude Opus 3**

| Retirement date | Deprecated model | Recommended replacement |
|-----------------|------------------|-------------------------|
| January 5, 2026 | claude-3-opus-20240229 | claude-opus-4-7 |

<transcription_json>
{"table_type":"data_table","title":"Retirement details — Claude Opus 3","columns":["Retirement date","Deprecated model","Recommended replacement"],"data":[{"Retirement date":"January 5, 2026","Deprecated model":"claude-3-opus-20240229","Recommended replacement":"claude-opus-4-7"}]}
</transcription_json>

<transcription_notes>
- The deprecated model token appears to be "claude-3-opus-20240229" (reads as a date-style suffix).
- Info box above paragraph: blue rounded rectangle with icon; text "This model was retired January 5, 2026."
</transcription_notes>
</transcription_table>

<!-- Section 4 -->
## 2025-01-21: Claude 2, Claude 2.1, and Claude Sonnet 3 models

These models were retired July 21, 2025.

(On the visible portion of the page the heading and the blue info box "These models were retired July 21, 2025." are visible; further details/tables are below the visible fold and not fully captured in this image.)

<transcription_notes>
- Page layout: single content column with section headings in bold serif-like font; blue info boxes used to highlight retirement dates and status.
- Decorative elements visible: large left margin of off-white/cream color; small circular "Ask Docs" floating button at lower right (decorative UI element).
- No charts or graphical data visualizations present on the visible area—only informational tables and blue info boxes.
</transcription_notes>

<transcription_page_footer> Page [unclear] | Anthropic </transcription_page_footer>
<transcription_page_header> Claude API Docs | Model retirements </transcription_page_header>

<!-- Section 1 -->
<!-- Column 1 -->
On January 21, 2025, Anthropic notified developers using Claude 2, Claude 2.1, and Claude Sonnet 3 models of their upcoming retirements.

<transcription_table>
**Retirements notified January 21, 2025**

| Retirement date | Deprecated model | Recommended replacement |
|-----------------|------------------|-------------------------|
| July 21, 2025 | claude-2.0 | claude-opus-4-7 |
| July 21, 2025 | claude-2.1 | claude-opus-4-7 |
| July 21, 2025 | claude-3-sonnet-20240229 | claude-sonnet-4-6 |

<transcription_json>
{"table_type":"data_table","title":"Retirements notified January 21, 2025","columns":["Retirement date","Deprecated model","Recommended replacement"],"data":[{"Retirement date":"July 21, 2025","Deprecated model":"claude-2.0","Recommended replacement":"claude-opus-4-7"},{"Retirement date":"July 21, 2025","Deprecated model":"claude-2.1","Recommended replacement":"claude-opus-4-7"},{"Retirement date":"July 21, 2025","Deprecated model":"claude-3-sonnet-20240229","Recommended replacement":"claude-sonnet-4-6"}]}
</transcription_json>

<transcription_notes>
- Visual: three-row table with three columns (Retirement date, Deprecated model, Recommended replacement).
- Model names shown in rounded grey inline-code style chips in original.
- Table background: white; divider lines faint grey.
</transcription_notes>
</transcription_table>

# 2024-09-04: Claude 1 and Instant models

> ℹ️ These models were retired November 6, 2024.

On September 4, 2024, Anthropic notified developers using Claude 1 and Instant models of their upcoming retirements.

<transcription_table>
**Retirements notified September 4, 2024**

| Retirement date | Deprecated model | Recommended replacement |
|-----------------|------------------|-------------------------|
| November 6, 2024 | claude-1.0 | claude-haiku-4-5-20251001 |
| November 6, 2024 | claude-1.1 | claude-haiku-4-5-20251001 |
| November 6, 2024 | claude-1.2 | claude-haiku-4-5-20251001 |
| November 6, 2024 | claude-1.3 | claude-haiku-4-5-20251001 |
| November 6, 2024 | claude-instant-1.0 | claude-haiku-4-5-20251001 |
| November 6, 2024 | claude-instant-1.1 | claude-haiku-4-5-20251001 |
| November 6, 2024 | claude-instant-1.2 | claude-haiku-4-5-20251001 |

<transcription_json>
{"table_type":"data_table","title":"Retirements notified September 4, 2024","columns":["Retirement date","Deprecated model","Recommended replacement"],"data":[{"Retirement date":"November 6, 2024","Deprecated model":"claude-1.0","Recommended replacement":"claude-haiku-4-5-20251001"},{"Retirement date":"November 6, 2024","Deprecated model":"claude-1.1","Recommended replacement":"claude-haiku-4-5-20251001"},{"Retirement date":"November 6, 2024","Deprecated model":"claude-1.2","Recommended replacement":"claude-haiku-4-5-20251001"},{"Retirement date":"November 6, 2024","Deprecated model":"claude-1.3","Recommended replacement":"claude-haiku-4-5-20251001"},{"Retirement date":"November 6, 2024","Deprecated model":"claude-instant-1.0","Recommended replacement":"claude-haiku-4-5-20251001"},{"Retirement date":"November 6, 2024","Deprecated model":"claude-instant-1.1","Recommended replacement":"claude-haiku-4-5-20251001"},{"Retirement date":"November 6, 2024","Deprecated model":"claude-instant-1.2","Recommended replacement":"claude-haiku-4-5-20251001"}]}
</transcription_json>

<transcription_notes>
- Visual: seven-row table with three columns. Each "Recommended replacement" cell contains the same model string "claude-haiku-4-5-20251001" shown in rounded grey inline-code chips.
- Above the table is a blue information box with an information icon and the text "These models were retired November 6, 2024."
- Page styling: serif headings, muted body text, light-grey horizontal dividers.
</transcription_notes>
</transcription_table>

Was this page helpful?
: [thumbs up icon]  [thumbs down icon]

<!-- Decorative: footer logo ("Claude API Docs") and social icons -->
<transcription_page_footer> Page [unclear] | Claude API Docs </transcription_page_footer>
# Claude API Docs

On September 4, 2024, Anthropic notified developers using Claude 1 and Instant models of their upcoming retirements.

<!-- Section 1 -->
<!-- Column 1 -->

<transcription_table>
**Table 1: Model retirement schedule**

| Retirement date | Deprecated model | Recommended replacement |
|-----------------|------------------|-------------------------|
| November 6, 2024 | claude-1.0 | claude-haiku-4-5-20251001 |
| November 6, 2024 | claude-1.1 | claude-haiku-4-5-20251001 |
| November 6, 2024 | claude-1.2 | claude-haiku-4-5-20251001 |
| November 6, 2024 | claude-1.3 | claude-haiku-4-5-20251001 |
| November 6, 2024 | claude-instant-1.0 | claude-haiku-4-5-20251001 |
| November 6, 2024 | claude-instant-1.1 | claude-haiku-4-5-20251001 |
| November 6, 2024 | claude-instant-1.2 | claude-haiku-4-5-20251001 |

<transcription_json>
{"table_type":"data_table","title":"Model retirement schedule","columns":["Retirement date","Deprecated model","Recommended replacement"],"data":[{"Retirement date":"November 6, 2024","Deprecated model":"claude-1.0","Recommended replacement":"claude-haiku-4-5-20251001"},{"Retirement date":"November 6, 2024","Deprecated model":"claude-1.1","Recommended replacement":"claude-haiku-4-5-20251001"},{"Retirement date":"November 6, 2024","Deprecated model":"claude-1.2","Recommended replacement":"claude-haiku-4-5-20251001"},{"Retirement date":"November 6, 2024","Deprecated model":"claude-1.3","Recommended replacement":"claude-haiku-4-5-20251001"},{"Retirement date":"November 6, 2024","Deprecated model":"claude-instant-1.0","Recommended replacement":"claude-haiku-4-5-20251001"},{"Retirement date":"November 6, 2024","Deprecated model":"claude-instant-1.1","Recommended replacement":"claude-haiku-4-5-20251001"},{"Retirement date":"November 6, 2024","Deprecated model":"claude-instant-1.2","Recommended replacement":"claude-haiku-4-5-20251001"}],"unit":null}
</transcription_json>

<transcription_notes>
- Table appears centered on page with three columns: "Retirement date", "Deprecated model", "Recommended replacement".
- Deprecated model and Recommended replacement values are shown in pill-shaped code-styled labels.
- All rows share the same retirement date: "November 6, 2024".
- All recommended replacements are "claude-haiku-4-5-20251001".
- Visual style: light background, subtle horizontal separators between rows, code pills have a very light beige background.
</transcription_notes>
</transcription_table>

Was this page helpful?

👍 👎

<!-- Decorative: footer logo, social icons, separators -->

<!-- Section 2 -->
<!-- Column 1 -->
<!-- Column 2 -->
<!-- Column 3 -->
<!-- Column 4 -->
(Multi-column footer with navigation links and partner lists — omitted transcription per "multi-column text-only layouts" guideline.)

<transcription_page_footer>Claude API Docs | Page 1</transcription_page_footer>
