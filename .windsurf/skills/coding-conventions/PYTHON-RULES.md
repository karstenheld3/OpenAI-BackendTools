# Python Coding Rules

## Table of Contents

1. [Rule Index](#rule-index)
2. [Definitions](#definitions)
3. [Formatting Rules (FT)](#formatting-rules-ft)
4. [Import Rules (IM)](#import-rules-im)
5. [Code Generation Rules (CG)](#code-generation-rules-cg)
6. [Naming Rules (NM)](#naming-rules-nm)
7. [Comment Rules (CM)](#comment-rules-cm)

## Rule Index

**Formatting (FT)**
- **PYTHON-FT-01**: Indentation with TAB (2 spaces)
- **PYTHON-FT-02**: Single line for statements ≤ MAX_LINE_CHARS
- **PYTHON-FT-03**: Function signature on single line
- **PYTHON-FT-04**: One empty line between functions/classes
- **PYTHON-FT-05**: Function grouping with topic markers

**Imports (IM)**
- **PYTHON-IM-01**: All imports at top of file
- **PYTHON-IM-02**: Core imports on single line
- **PYTHON-IM-03**: No local imports inside functions
- **PYTHON-IM-04**: Group imports by origin
- **PYTHON-IM-05**: Prefer single-line multi-name imports

**Code Generation (CG)**
- **PYTHON-CG-01**: Do not rename existing symbols
- **PYTHON-CG-02**: Re-use existing patterns
- **PYTHON-CG-03**: Check for existing helpers before creating new
- **PYTHON-CG-04**: Principle of Least Surprise
- **PYTHON-CG-05**: Prefer explicit for loops over functional helpers
- **PYTHON-CG-06**: Prefer standard library
- **PYTHON-CG-07**: No emojis in code/logging
- **PYTHON-CG-08**: Use timezone-aware datetime
- **PYTHON-CG-09**: Handle singular/plural correctly

**Naming (NM)**
- **PYTHON-NM-01**: Use clear, fully written names
- **PYTHON-NM-02**: Follow existing naming patterns
- **PYTHON-NM-03**: Avoid ambiguous abbreviations
- **PYTHON-NM-04**: Corresponding pairs (pack/unpack, do/undo)
- **PYTHON-NM-05**: Avoid misleading concepts (visible/hidden vs visible/invisible)
- **PYTHON-NM-06**: Specific over generic (leftTo, rightTo vs nextTo)
- **PYTHON-NM-07**: Origin/destination not source/target
- **PYTHON-NM-08**: Don't rename established APIs (association field)

**Comments (CM)**
- **PYTHON-CM-01**: Comment intent, not obvious code
- **PYTHON-CM-02**: No docstrings for small functions
- **PYTHON-CM-03**: Docstrings for complex functions with examples
- **PYTHON-CM-04**: Use ASCII quotes in documentation
- **PYTHON-CM-05**: Use tree characters for hierarchies

## Definitions

```
MAX_LINE_CHARS = 220
TAB = "  " (2 spaces)
UNKNOWN = '[UNKNOWN]'
```

## Formatting Rules (FT)

### PYTHON-FT-01: Indentation
Indent code with TAB (2 spaces).

### PYTHON-FT-02: Single Line Statements
If a statement is ≤ MAX_LINE_CHARS characters (including spaces), keep it on a single line.
Ignore MAX_LINE_CHARS restrictions in Markdown; especially for tables and UI prototypes.

*BAD*:
```python
content_page = client.vector_stores.files.content(
  vector_store_id=vector_store_id,
  file_id=file_id
)
```
*GOOD*:
```python
content_page = client.vector_stores.files.content(vector_store_id=vector_store_id, file_id=file_id)
```

*BAD*:
```python
if not vector_store_id:
  raise ValueError(f"Expected a non-empty value for 'vector_store_id' but received {vector_store_id!r}")
```
*GOOD*:
```python
if not vector_store_id: raise ValueError(f"Expected a non-empty value for 'vector_store_id' but received {vector_store_id!r}")
```

### PYTHON-FT-03: Function Signatures
Put the full signature on a single line; function body starts on the next line.

### PYTHON-FT-04: Empty Lines
One empty line as delimiter between imports, functions and class definitions.

### PYTHON-FT-05: Function Grouping
Group functions under common topic with start/end markers (127 chars long). Single line space after each function.

*BAD*:
```python
def function01():
  ...


def function02():
  ...
def function03():
  ...
```
*GOOD*:
```python
# ----------------------------------------- START: Topic A --------------------------------------------------------------------

def function01():
  ...

def function02():
  ...

# ----------------------------------------- END: Topic A ----------------------------------------------------------------------


# ----------------------------------------- START: Topic B --------------------------------------------------------------------

def function03():
  ...

def function04():
  ...

# ----------------------------------------- END: Topic B ----------------------------------------------------------------------
```

*BAD*:
```python
# ============================================
# MONITOR ENDPOINT
# ============================================
[ ... CODE ... ]
```
*GOOD*:
```python
# ----------------------------------------- START: /monitor endpoint ----------------------------------------------------------

[ ... CODE ... ]

# ----------------------------------------- END: /monitor endpoint -------------------------------------------------------------
```

## Import Rules (IM)

### PYTHON-IM-01: Import Location
All imports at the top of the file.

### PYTHON-IM-02: Core Imports
All core imports on a single line (even if longer than MAX_LINE_CHARS).

*BAD*:
```python
import asyncio
import datetime
import json
import random
```
*GOOD*:
```python
import asyncio, datetime, json, random
```

### PYTHON-IM-03: No Local Imports
No local imports inside functions.

*BAD*:
```python
def function_abc():
  from utils import convert_to_nested_html_table
  # ...
```
*GOOD*:
```python
from utils import convert_to_flat_html_table, convert_to_nested_html_table

def function_abc():
  # ...
```

### PYTHON-IM-04: Import Grouping
Group imports: standard library first, then third-party libraries, then internal modules.

### PYTHON-IM-05: Multi-Name Imports
Prefer importing all needed names from a module in a single line.

## Code Generation Rules (CG)

### PYTHON-CG-01: No Symbol Renaming
Do not rename existing symbols unless explicitly asked.

### PYTHON-CG-02: Re-use Patterns
Analyze the existing codebase before creating new code. Re-use existing implementation patterns, naming patterns, code formatting, design philosophy, logging style and functions.

### PYTHON-CG-03: Check Existing Helpers
Before implementing new helper functions, make sure no alternatives exist in the codebase.

### PYTHON-CG-04: Principle of Least Surprise
Prefer simple, idiomatic Python over clever or magical code. Optimize for readability and maintainability, not micro-optimizations. Concise is good, but not at the expense of clarity.

### PYTHON-CG-05: Explicit Loops
Avoid `lambda`, `map`, `filter`, `reduce` and similar helpers for control flow; use explicit `for` loops.
**Exception**: string / list joins.

### PYTHON-CG-06: Standard Library First
Prefer standard library over third-party packages; add dependencies only if a helper function would be unreasonably complex.

### PYTHON-CG-07: No Emojis
No emojis in the code or logging.
**Exception**: UI may occasionally use ✅=yes/pass, ❌=no/fail, ⚠️=warning/partial, ★=filled star, ☆=outlined star, ⯪=half star

### PYTHON-CG-08: Timezone-Aware Datetime
Use `datetime.datetime.now(datetime.timezone.utc)` instead of deprecated `datetime.datetime.utcnow()`.

### PYTHON-CG-09: Singular/Plural
Handle singular and plural correctly: `0 files found.`, `1 file`, `2 files`. Avoid `1 file(s)`.

*BAD*:
```python
print(f"{count} file(s) found.")
```
*GOOD*:
```python
print(f"{count} file(s)".replace("(s)", "s" if count != 1 else "") + " found.")
```

## Naming Rules (NM)

### PYTHON-NM-01: Clear Names
Use clear, fully written names.

### PYTHON-NM-02: Follow Patterns
Follow existing naming patterns in the codebase.

### PYTHON-NM-03: No Abbreviations
Avoid ambiguous abbreviations.

*BAD* -> *GOOD*:
```
body_attrs -> body_attributes
content -> html_content
dynamic_count -> use_dynamic_count_for_updating
```

### PYTHON-NM-04: Corresponding Pairs
Use same word stem for opposites.

**Verbs:**
`send/receive`, `pack/unpack`, `accept/reject`, `enable/disable`, `visible/hidden`, `show/hide`, `do/undo`, `open/close`, `check/uncheck`, `validate/invalidate`, `include/exclude`, `existant/nonExistant`, `empty/filled`, `expand/shrink`

**Entities:**
`Input/Output`, `Addition/Removal`, `Activation/Deactivation`, `Source/Target`, `Current/Target`, `Origin/Destination`, `Departure/Arrival`, `Prefix/Suffix`

### PYTHON-NM-05: Avoid Misleading Concepts
`visible/invisible` implies object still occupies space. Use `visible/hidden` if hidden means "not there at all".

### PYTHON-NM-06: Specific Over Generic
Avoid `nextTo` (what context?). Use specific names:
- `leftTo`, `rightTo` (direction)
- `northTo`, `southTo` (axis)
- `nearTo` (distance)
- `closeTo` (relationship)

### PYTHON-NM-07: Origin/Destination Not Source/Target
"Several planes with the target Bagdad" = bad news. "Several planes with the destination Bagdad" = travel plans.

### PYTHON-NM-08: Don't Rename Established APIs
Even if the name became a misnomer, don't rename it. People predict behavior by the evoked association field, not the literal name. If `login()` worked for years, don't rename to `authenticate()` when credentials are no longer required. "Login" already means "authenticate" in users' minds. Like "horsepower" doesn't mean horses - it's the association field, not the name.

## Comment Rules (CM)

### PYTHON-CM-01: Comment Intent
Avoid comments that restate obvious code; comment intent, edge cases, and non-obvious behavior.

### PYTHON-CM-02: No Docstrings for Small Functions
No docstrings for small, single-purpose functions with self-explanatory names and arguments. Use a single comment above such functions if intent or types need clarification.

*BAD*:
```python
def generate_error_response(error_message: str, format: str, status_code: int = 400):
  """
  Generate error response in requested format.
  Args: ...
  Returns: ...
  """
  if format == 'json':
    return JSONResponse({"error": error_message}, status_code=status_code)
  else:
    return HTMLResponse(generate_error_div(error_message), status_code=status_code)
```
*GOOD*:
```python
# Generate HTTP error response in requested format ('json' | 'html')
def generate_error_response(error_message: str, format: str, status_code: int = 400):
  if format == 'json': return JSONResponse({"error": error_message}, status_code=status_code)
  else: return HTMLResponse(generate_error_div(error_message), status_code=status_code)
```

*BAD*:
```python
def set_config(app_config):
  """Set the configuration for Crawler management."""
  global config
  config = app_config
```
*GOOD*:
```python
# Set the configuration for Crawler management. app_config: Config dataclass with openai_client, persistent_storage_path, etc.
def set_config(app_config):
  global config
  config = app_config
```

### PYTHON-CM-03: Docstrings for Complex Functions
Use docstrings for FastAPI endpoints and complex functions (more than 5 arguments, multiple responsibilities, or complex/structured return types), and include example outputs.

*GOOD*:
```python
def generate_simple_page(title: str, html_content: str, body_attributes: str = "") -> str:
  """
  Generate simple HTML page with title and html content.
  
  Example output:
    <!DOCTYPE html><html><head>[GENERATE_HTML_HEAD_OUTPUT]</head>
    <body [BODY_ATTRIBUTES_IF_ANY]>
      [HTML_CONTENT]
    </body>
    </html>
  """
  head = generate_html_head(title)
  body_tag = f"<body {body_attributes}>" if body_attributes else "<body>"
  return f"""{head}
{body_tag}
  {html_content}
</body>
</html>"""
```

### PYTHON-CM-04: ASCII Quotes
For documentation or UI output, avoid "typographic quotes" and use typewriter / ASCII "double quotes" or 'single quotes'.

### PYTHON-CM-05: Hierarchy Characters
When creating hierarchies and maps, use "└──" for indenting.

