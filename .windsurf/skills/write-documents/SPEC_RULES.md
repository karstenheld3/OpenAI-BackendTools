# SPEC Document Rules

Rules for writing specification documents with GOOD/BAD examples.

## Rule Index

**Requirements (RQ)**
- **SPEC-RQ-01**: Use numbered IDs for functional requirements (XXXX-FR-01)
- **SPEC-RQ-02**: Use numbered IDs for design decisions (XXXX-DD-01)
- **SPEC-RQ-03**: Use numbered IDs for implementation guarantees (XXXX-IG-01)

**Diagrams (DG)**
- **SPEC-DG-01**: Use ASCII box diagrams with component boundaries
- **SPEC-DG-02**: Show ALL buttons and actions in UI diagrams
- **SPEC-DG-03**: Use layer diagrams for multi-tier systems

**Content (CT)**
- **SPEC-CT-01**: Summarize styling - avoid CSS detail
- **SPEC-CT-02**: Code outline only - avoid implementation detail
- **SPEC-CT-03**: Single line statements when possible
- **SPEC-CT-04**: Document event flows with box-drawing characters
- **SPEC-CT-05**: Provide data structure examples (JSON, CSV)
- **SPEC-CT-06**: Compact object definitions - use lists, no empty lines between properties
- **SPEC-CT-07**: Compact gate checklists - use simple lists, not ASCII box diagrams

**Format (FT)**
- **SPEC-FT-01**: Use timestamped changelog, reverse chronological
- **SPEC-FT-02**: No Markdown tables in changelogs
- **SPEC-FT-03**: Proper header block and section order

## Table of Contents

- [Requirements Format](#requirements-format)
- [UI Diagrams](#ui-diagrams)
- [Layer Architecture Diagrams](#layer-architecture-diagrams)
- [Summarize Styling](#summarize-styling)
- [Code Outline Only](#code-outline-only)
- [Single Line Statements](#single-line-statements)
- [Compact Object Definitions](#compact-object-definitions)
- [Compact Gate Checklists](#compact-gate-checklists)
- [Event Flow Documentation](#event-flow-documentation)
- [Data Structure Examples](#data-structure-examples)
- [Document History Format](#document-history-format)
- [Section Order and Header](#section-order-and-header)

## Requirements Format

**BAD:**
```
- Toast notifications should support info, success, error types
- Auto-dismiss should be configurable
```

**GOOD:**
```
**UI-FR-01: Toast Notifications**
- Support info, success, error, warning message types
- Auto-dismiss configurable per toast (default 5000ms)

**DD-UI-03:** Declarative button configuration. Buttons use `data-*` attributes for endpoint URL, method, format - no custom JS per action.
```

**BAD** (invented ID type):
```
**CORNER-01:** Empty input list returns empty result
**EDGE-02:** Network timeout after 30 seconds
```

**GOOD** (standard EC type):
```
**CRWL-EC-01:** Empty input list -> Return empty result, log warning
**CRWL-EC-02:** Network timeout -> Retry 3 times, then fail with error
```

## UI Diagrams

Use ASCII box diagrams with component boundaries. Show ALL buttons and actions.

**BAD:**
```
+-------------------------------------------------------------+
|  Jobs Table (Reactive Rendering)                            |
|  +----+---------+----------+---------+------------------+   |
|  | ID | Router  | Endpoint | State   | Actions          |   |
|  +----+---------+----------+---------+------------------+   |
|  | 42 | crawler | update   | running | [Monitor] [Pause]|   |
|  | 41 | crawler | update   | done    | [Monitor]        |   |
|  +----+---------+----------+---------+------------------+   |
|                                                             |
|  +----------------------------------------------------------+
|  | [Resize Handle - Draggable]                              |
|  | Console Output                                   [Clear] |
|  | ---------------------------------------------------------|
|  | [ 1 / 20 ] Processing 'document_001.pdf'...              |
|  |   OK.                                                    |
|  +----------------------------------------------------------+
|                                                             |
|  +----------------------------------------------------------+
|  | Job Started | ID: 42 | Total: 20 items               [x] | <- Toast
|  +----------------------------------------------------------+
+-------------------------------------------------------------+
```

**GOOD:**
```
Main HTML:
+-------------------------------------------------------------------------------+
|  Streaming Jobs (2)                                                           |
|                                                                               |
|  [Start Job]  [Refresh]                                 [Toasts appear here]  |
|                                                                               |
|  +----+---------+----------+---------+-------------------------------------+  |
|  | ID | Router  | Endpoint | State   | Actions                             |  |
|  +----+---------+----------+---------+-------------------------------------+  |
|  | 42 | crawler | update   | running | [Monitor] [Pause / Resume] [Cancel] |  |
|  | 41 | crawler | update   | done    | [Monitor]                           |  |
|  +----+---------+----------+---------+-------------------------------------+  |
|                                                                               |
|  +-------------------------------------------------------------------------+  |
|  | [Resize Handle - Draggable]                                             |  |
|  | Console Output                                                  [Clear] |  |
|  | ------------------------------------------------------------------------|  |
|  | [ 1 / 20 ] Processing 'document_001.pdf'...                             |  |
|  |   OK.                                                                   |  |
|  | [ 2 / 20 ] Processing 'document_002.pdf'...                             |  |
|  |   OK.                                                                   |  |
|  +-------------------------------------------------------------------------+  |
|                                                                               |
+-------------------------------------------------------------------------------+

Toast:
+-----------------------------------------------+
| Job Started | ID: 42 | Total: 20 items   [x]  |
+-----------------------------------------------+
```

## Layer Architecture Diagrams

For multi-layer systems, use ASCII box diagrams showing call hierarchy:

**GOOD:**
```
┌───────────────────────────────────────────────────────────────────────────┐
│  High-Level (Router)                                                      │
│  ├─> function_a()         # Called by router endpoints                    │
├───────────────────────────────────────────────────────────────────────────┤
│  Mid-Level (Components)                                                   │
│  ├─> function_b()         # Generates HTML fragments                      │
│  ├─> function_c()         # Generates JavaScript                          │
├───────────────────────────────────────────────────────────────────────────┤
│  Low-Level (Helpers)                                                      │
│  └─> json_result()        # Response formatting                           │
└───────────────────────────────────────────────────────────────────────────┘
```

## Summarize Styling

Avoid too much CSS detail in specs.

**BAD:**
```css
.toast {
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-left: 4px solid #0078d4;
  padding: 0.75rem 1rem;
  border-radius: 4px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  animation: slideIn 0.3s ease-out;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  color: #212529;
}

.toast.toast-info { border-left-color: #0078d4; }
```

**GOOD:**
```css
.toast { /* Individual toast notification with light theme */ }
.toast.toast-info { /* Blue left border */ }
.toast.toast-success { /* Green left border */ }
```

## Code Outline Only

Avoid implementation detail. Focus on architecture completeness. Document intention.

**BAD:**
```javascript
// Render functions
function renderJobRow(job) {
  const actions = renderJobActions(job);
  // Format timestamps consistently (handle both ISO format with T and space format)
  const formatTimestamp = (ts) => {
    if (!ts) return '';
    return ts.substring(0, 19).replace('T', ' ');
  };
  const started = formatTimestamp(job.started);
  const finished = job.finished ? formatTimestamp(job.finished) : '-';
  return `
    <tr id="job-${job.id}">
      <td>${job.id}</td>
      <td>${job.router}</td>
      <td>${job.endpoint}</td>
      <td>${job.state}</td>
      <td>${started}</td>
      <td>${finished}</td>
      <td>${actions}</td>
    </tr>
  `;
}
```

**GOOD:**
```javascript
// Generate <tr> HTML for single job
function renderJobRow(job) { ... }
```

## Single Line Statements

Fit single statements/decisions/objects on a single line.

**BAD:**
```html
**Pause Button** (requests job pause):
<button class="btn-small" onclick="controlJob(42, 'pause')">
  Pause
</button>
```

**GOOD:**
```html
**Pause Button** (requests job pause):
<button class="btn-small" onclick="controlJob(42, 'pause')"> Pause </button>
```

## Compact Object Definitions

Use lists for object/phase definitions. No empty lines between properties.

**BAD:**
```
### [EXPLORE]

**Purpose**: Understand the situation before acting

**BUILD focus**: What feature? What constraints? What patterns?

**SOLVE focus**: What's the real problem? What do I need to learn?

**Entry**: Start of workflow

**Exit**: Gate EXPLORE→DESIGN passes

**Key verbs**: [RESEARCH], [ANALYZE], [ASSESS], [SCOPE], [GATHER], [CONSULT], [DECIDE]
```

**GOOD:**
```
### [EXPLORE]

- **Purpose**: Understand the situation before acting
- **BUILD**: What feature? What constraints? What patterns?
- **SOLVE**: What's the real problem? What do I need to learn?
- **Entry**: Start of workflow
- **Exit**: Gate EXPLORE→DESIGN passes
- **Verbs**: [RESEARCH], [ANALYZE], [ASSESS], [SCOPE], [GATHER], [CONSULT], [DECIDE]
```

## Compact Gate Checklists

Use simple lists for gate/transition checklists. ASCII box diagrams waste characters.

**BAD:** (ASCII box wastes ~600 chars)
```
┌─ Gate: X → Y ────────────────────────┐
│  [ ] Item 1                          │
│  [ ] Item 2                          │
│  If unchecked → remain in [X]        │
└──────────────────────────────────────┘
```

**GOOD:** (simple list)
```
### Gate: X → Y
- [ ] Item 1
- [ ] Item 2

**Pass**: proceed to [Y] | **Fail**: remain in [X]
```

## Event Flow Documentation

Document call chains with box-drawing characters (├─> └─> │).

**GOOD:**
```
User clicks [Pause] or [Resume]
├─> controlJob(jobId, 'pause' | 'resume')
│   └─> fetch(`/testrouter3/control?id=${id}&action=${action}`)
│       └─> On success (data.success):
│           └─> Optimistically updateJob(jobId, { state: 'paused' | 'running' })
│               └─> renderAllJobs()
│                   └─> renderJobActions() # Button changes to Resume/Pause
```

## Data Structure Examples

Provide examples for JSON, CSV, and other data formats.

**GOOD:**
```
<start_json>
{"id": 42, "router": "testrouter3", "endpoint": "streaming01", "state": "running", "total": 3, "started": "2025-11-27T11:30:00"}
</start_json>
<log>
[ 1 / 3 ] Processing 'doc_001.pdf'...
  OK.
[ 2 / 3 ] Processing 'doc_002.pdf'...
  OK.
[ 3 / 3 ] Processing 'doc_003.pdf'...
  OK.
</log>
<end_json>
{"id": 42, "state": "completed", "result": "ok", "finished": "2025-11-27T11:30:15"}
</end_json>
```

## Document History Format

Use timestamped changelog, reverse chronological. Avoid tables.

**BAD:**
```
| Date | Change |
|------|--------|
| 2024-12-17 | Initial specification created |
| 2024-12-17 | Added Key Mechanisms section |
```

**GOOD:**
```
## Document History

**[2024-12-17 14:30]**
- Added: "Scenario" section with Problem/Solution/What we don't want
- Added: Document History section

**[2024-12-17 11:45]**
- Added: "Key Mechanisms" section with declarative button pattern
- Changed: Placeholder standardized to `{itemId}` (camelCase)
- Fixed: Modal OK button signature to match `callEndpoint(btn, itemId, bodyData)`

**[2024-12-17 10:00]**
- Initial specification created
```

## Section Order and Header

**BAD:**
```

**Target files**:

## Scenario
...
---



## Architecture
...
---
```

**GOOD:**
```
# V0 Crawler Toolkit - Standalone SharePoint Crawler

**Goal**: Document the architecture and workflow of the standalone SharePoint-GPT-Crawler-Toolkit.

**Does not depend on:**
- Any V2 specifications (this is the predecessor toolkit)
...

## Overview
...

## Table of Contents
...
```
