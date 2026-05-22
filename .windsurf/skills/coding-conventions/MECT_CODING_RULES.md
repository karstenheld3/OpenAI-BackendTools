# MECT Coding Rules

Applies MECT and APAPALAN to code quality. Target audience: coding agents writing or reviewing code.

**Abstraction levels:**
- **MECT** = General principles that guide judgment. Answers: "What makes good code?"
- **APAPALAN** = Concrete enforceable rules with measurable criteria. Answers: "How do I check compliance?"

This document merges both into actionable rules for identifiers, functions, types, comments, logs, errors, and APIs. Each rule states the principle (MECT) and the enforcement pattern (APAPALAN).

**Core concept - Signal vs Noise:**
Every design choice in code is either **Signal** (purposeful, carries information the reader needs) or **Noise** (arbitrary, carries no information but the reader interprets as if it does). MECT strengthens signals and eliminates noise. APAPALAN enforces specific patterns to achieve this.

## Rule Index

Precision (PR) - Every name and message unambiguous
- MC-PR-01: One name per concept across codebase
- MC-PR-02: Unambiguous compound names (word order determines meaning)
- MC-PR-03: No dangerous meta-words without qualifier
- MC-PR-04: Be specific in comments - concrete, verifiable statements
- MC-PR-05: Error messages state what failed, why, and recovery action
- MC-PR-06: Log messages: self-contained, full disclosure
- MC-PR-07: Include canonical identifiers in errors (file, line, entity ID)

Brevity (BR) - Minimal without losing meaning
- MC-BR-01: Simplest verb - no hidden verbs in names
- MC-BR-02: Comments: drop filler, be direct
- MC-BR-03: Function names describe output, not mechanism
- MC-BR-04: Boolean functions: is_/has_/can_ prefix, no "check_"
- MC-BR-05: Every code artifact must carry information

Consistency (CO) - Same pattern everywhere
- MC-CO-01: Corresponding pairs use same word stem
- MC-CO-02: Consistent key=value format in logs
- MC-CO-03: Convergent naming - same terms in URL, payload, docs, logs
- MC-CO-04: Consistent patterns across all similar constructs
- MC-CO-05: Keep established API names - don't rename working terms

Naming Design (ND) - Structure for scalable naming
- MC-ND-01: Naming structure method (explicit -> specifiers -> states -> mnemonics)
- MC-ND-02: Canonical form for IDs and data structures
- MC-ND-03: No recursive/implicit naming
- MC-ND-04: No product-as-term collision
- MC-ND-05: Type name = domain concept, not implementation detail
- MC-ND-06: Disambiguate by qualifying, not renaming
- MC-ND-07: Intuitive opposites for paired parameters
- MC-ND-08: No terminological synonymy - one name per concept across codebase
- MC-ND-09: No inverted semantics - name direction must match value direction

Documentation (DC) - Code-adjacent writing
- MC-DC-01: Four description types (what/why/how/where)
- MC-DC-02: Match description type to audience
- MC-DC-03: Plain language in user-facing messages

## Table of Contents

- [Precision Rules (PR)](#precision-rules-pr)
- [Brevity Rules (BR)](#brevity-rules-br)
- [Consistency Rules (CO)](#consistency-rules-co)
- [Naming Design Rules (ND)](#naming-design-rules-nd)
- [Documentation Rules (DC)](#documentation-rules-dc)

## Precision Rules (PR)

### MC-PR-01: One Name Per Concept Across Codebase

One concept = one name everywhere: variables, functions, classes, database columns, API fields, log messages, documentation. No synonyms, no polysemy.

**Why:** Synonyms cause search failures ("I searched for 'workshop' but the code uses 'garage'"). Polysemy causes silent misunderstandings - developers THINK they agree when they don't.

**BAD:**
```python
# Three names for same concept
def get_workshop(id): ...
def fetch_garage(id): ...
def load_service_center(id): ...

# Polysemy: "meter" means three things
class Meter:          # connection point? device? contract?
    meter_id: str     # which meter?
```

**GOOD:**
```python
# One name everywhere
def get_workshop(id): ...

# Qualified names eliminate polysemy
class MeterPoint:      # connection point
class MeterDevice:     # physical device
class MeterContract:   # customer relationship
```

**Cross-boundary rule:** If the database column is `workshop_id`, the API field is `workshop_id`, the variable is `workshop_id`, and the log says `workshop_id='abc'`. Never translate between layers.

### MC-PR-02: Unambiguous Compound Names

Word order determines meaning. If a compound name has multiple readings, restructure it.

**BAD:**
```python
empty_collection_key    # Is the collection empty, or is the key empty?
invalid_user_input      # Is the user invalid, or is the input invalid?
active_session_count    # Active sessions counted, or count is active?
```

**GOOD:**
```python
key_of_empty_collection   # The collection is empty
input_from_invalid_user   # The user is invalid
count_of_active_sessions  # Counting the active sessions
```

**Test:** Read the name aloud. If a colleague could reasonably interpret it two ways, restructure it.

### MC-PR-03: No Dangerous Meta-Words Without Qualifier

These words seem specific but hide ambiguity: Module, Service, Manager, Handler, Helper, Utility, Provider, Processor, Controller, Check, Asset, Payload.

**BAD:**
```python
class ProductModule:    # Does Product contain Module or Module contain Product?
class UserService:      # Named after consumer, provider, or product?
def check(order):       # Returns bool ("check if")? Or always runs ("perform check")?
class DataProcessor:    # Processes what data? How?
```

**GOOD:**
```python
class ProductCatalog:       # Clear what it is
class UserAuthProvider:     # Clear role (provides auth for users)
def validate_order(order):  # Clear: returns bool
def run_data_cleanup():     # Clear: performs action, names output
class CsvRowParser:         # Clear: parses CSV rows
```

**Rule:** If you use a meta-word, qualify it until the name answers "what does it contain/do/provide?"

### MC-PR-04: Be Specific in Comments

No generic or abstract comments. Every comment must add concrete, verifiable information that the code doesn't already express.

**BAD:**
```python
# Handle errors appropriately
# Process the data
# Set up configuration
# This is important
```

**GOOD:**
```python
# Retry 3 times with exponential backoff (1s, 2s, 4s), then raise TimeoutError
# Parse CSV rows into OrderLine objects, skip rows with missing SKU
# Load config from ENV, fall back to config.yaml, fail if neither exists
# Rate limit: 100 req/min per IP. Exceeding returns 429.
```

**Test:** Delete the comment. If nothing is lost, the comment was useless. If the reader would now miss critical information, keep it.

### MC-PR-05: Error Messages State What Failed, Why, and Recovery

Every error message answers three questions: What happened? Why? What should the user/developer do?

**BAD:**
```python
raise Exception("Error")
raise ValueError("Invalid input")
raise ConnectionError("Failed to connect")
logger.error("Something went wrong")
```

**GOOD:**
```python
raise ValueError(
    f"Order quantity must be 1-999, got {quantity}. "
    f"Check input validation in checkout_form.py."
)
raise ConnectionError(
    f"Failed to connect to database at {host}:{port} after 3 retries. "
    f"Verify DB_HOST and DB_PORT environment variables."
)
logger.error(
    f"Payment processing failed for order_id='{order_id}': "
    f"gateway returned status=503. Retry in 30 seconds or check gateway status page."
)
```

### MC-PR-07: Include Canonical Identifiers in Errors

Error messages must include traceable identifiers so the error can be located without debugging: entity ID, file path, line number, request ID.

**BAD:**
```python
raise ValueError("Invalid order")
logger.error("Processing failed")
raise FileNotFoundError("Config file missing")
```

**GOOD:**
```python
raise ValueError(
    f"Invalid order id='{order_id}' in file='orders.csv' line={line_num}: "
    f"missing required field 'sku'"
)
logger.error(
    f"Processing failed for batch_id='{batch_id}' at step=3: "
    f"timeout after 30s. See request_id='{req_id}' in logs."
)
raise FileNotFoundError(
    f"Config file not found: path='{config_path}'. "
    f"Expected at $APP_HOME/config.yaml or set CONFIG_PATH env var."
)
```

**Rule:** Every error must contain at least one canonical identifier that enables `grep` to find the related context.

### MC-PR-06: Log Messages Are Self-Contained

Each log line must be understandable without reading other log lines. Include context: what operation, what data, how much, with what parameters.

**BAD:**
```python
logger.info("Starting...")
logger.info("Processing...")
logger.info("Done.")
logger.info("1 failed")
```

**GOOD:**
```python
logger.info("Starting order export for date='2026-03-17', format='csv'...")
logger.info("Processing 342 orders from region='eu-west'...")
logger.info("Order export complete: exported=341, failed=1, duration=12.3s")
logger.error("Order id='ORD-4521' failed: missing shipping_address field")
```

**Full disclosure principle:** State what you're doing, with how many items, using what parameters. The reader should never need to search for context.

## Brevity Rules (BR)

### MC-BR-01: Simplest Verb in Names

Replace verbose verb phrases with single verbs. Hidden verbs bury the action inside nouns.

**BAD:**
```python
def perform_validation(data): ...
def execute_data_cleanup(): ...
def carry_out_migration(): ...
def make_determination_of(status): ...
def do_calculation_of_total(items): ...
```

**GOOD:**
```python
def validate(data): ...
def cleanup_data(): ...
def migrate(): ...
def determine(status): ...
def calculate_total(items): ...
```

### MC-BR-02: Comments Drop Filler

Remove articles, hedging, and verbose constructions from comments. Precision first, then cut.

**BAD:**
```python
# This function is responsible for the retrieval of the user object
# from the database based on the provided identifier.
# It should be noted that this may return None.
```

**GOOD:**
```python
# Retrieve user by ID from database. Returns None if not found.
```

### MC-BR-03: Function Names Describe Output, Not Mechanism

Name functions by what they produce, not how they work internally.

**BAD:**
```python
def iterate_and_filter_orders(orders): ...      # Describes mechanism
def loop_through_database_records(): ...         # Describes mechanism
def apply_regex_to_extract_emails(text): ...     # Describes mechanism
```

**GOOD:**
```python
def active_orders(orders): ...          # Describes output
def all_records(): ...                  # Describes output
def extract_emails(text): ...           # Describes output
```

**Exception:** When the mechanism IS the distinguishing factor (e.g., `sort_by_merge` vs `sort_by_quick`).

### MC-BR-04: Boolean Functions Use Predicate Prefix

Boolean-returning functions start with `is_`, `has_`, `can_`, `should_`, `needs_`. Never use ambiguous `check_`.

**BAD:**
```python
def check(order):           # Returns bool? Performs validation? Both?
def check_permission():     # Returns bool or raises?
def validate_active():      # Returns bool or raises?
```

**GOOD:**
```python
def is_valid(order):            # Returns bool
def has_permission(user, action): # Returns bool
def is_active(subscription):    # Returns bool

def validate(order):            # Raises on invalid (action, not predicate)
```

**Rule:** `is_/has_/can_` = returns bool, never raises. Action verbs (`validate`, `ensure`, `require`) = may raise.

### MC-BR-05: Every Code Artifact Must Carry Information

Applies the Signal vs Noise principle to code. Every artifact (comment, type hint, decorator, docstring, log prefix, wrapper) must add meaning the reader cannot get from the code structure alone. If the code already communicates something, restating it is noise. See MW-LT-04 for the writing equivalent.

**Test:** Remove the artifact. If the reader loses no information, delete it.

**BAD:**
```python
i += 1  # increment i
x: int = 42  # type is obvious from literal
def get_name(self) -> str:
    """Get the name."""  # restates signature
    return self.name
logger.info(f"get_orders: Getting orders...")  # function name in log = noise
```

**GOOD:**
```python
i += 1  # compensate for 0-based index from API
def get_name(self) -> str:
    return self.name
logger.info(f"Getting orders for customer_id='{cid}'")
```

**Applies to:**
- Comments restating what code already says
- Type hints obvious from the literal or return expression
- Docstrings that restate the function signature without adding context
- Log messages repeating the function name (stack trace already provides it)
- Decorators/wrappers that add no behavior
- Variable name prefixes that restate the type (`str_name`, `list_items`)

## Consistency Rules (CO)

### MC-CO-01: Corresponding Pairs Use Same Word Stem

Opposite operations must form predictable pairs. Users predict the counterpart from the first name.

**BAD:**
```python
def encode_url(url): ...
def plain_text(encoded): ...     # User searches for decode_url(), fails

def serialize(data): ...
def load(raw): ...               # User expects deserialize()

def open_connection(): ...
def destroy_connection(): ...    # User expects close_connection()
```

**GOOD:**
```python
def encode_url(url): ...
def decode_url(encoded): ...

def serialize(data): ...
def deserialize(raw): ...

def open_connection(): ...
def close_connection(): ...
```

**Standard pairs:** open/close, read/write, get/set, add/remove, create/delete, start/stop, begin/end, push/pop, encode/decode, serialize/deserialize, connect/disconnect, acquire/release, lock/unlock, show/hide, enable/disable, attach/detach, subscribe/unsubscribe, marshal/unmarshal

### MC-CO-02: Consistent Key=Value Format in Logs

Pick one log format and use it everywhere. Mix of formats forces readers to parse multiple grammars.

**BAD:**
```python
logger.info(f"Processing {filename}")
logger.info(f"User: {user_id}, Action: {action}")
logger.info(f"file={filename} user_id={user_id}")
logger.info(f"Completed with status '{status}'")
```

**GOOD:**
```python
logger.info(f"Processing file='{filename}'...")
logger.info(f"Action: user='{user_id}' action='{action}'")
logger.info(f"Processing complete: file='{filename}' status='{status}' duration={elapsed}s")
```

**Convention:** `key='value'` for strings, `key=value` for numbers/booleans. Consistent everywhere.

### MC-CO-03: Convergent Naming

Same concept uses same term in URL path, request payload, response body, database column, variable name, log message, and documentation.

**BAD:**
```
URL:      /api/users/{userId}/orders
Payload:  { "customer_id": "..." }
Database: client_id
Variable: person_id
Logs:     "Processing account='...'"
Docs:     "The buyer places an order"
```
(Six names for same concept: userId, customer_id, client_id, person_id, account, buyer)

**GOOD:**
```
URL:      /api/users/{user_id}/orders
Payload:  { "user_id": "..." }
Database: user_id
Variable: user_id
Logs:     "Processing user_id='...'"
Docs:     "The user places an order"
```

### MC-CO-04: Consistent Patterns Across Similar Constructs

Same type of thing = same code pattern. Don't invent new patterns for similar operations.

**BAD:**
```python
# Three different patterns for same operation type
def get_user(id):
    return db.query(User).filter_by(id=id).first()

def fetch_order(order_id):
    result = db.session.execute(select(Order).where(Order.id == order_id))
    return result.scalar_one_or_none()

def load_product(pid):
    return Product.objects.get(pk=pid)
```

**GOOD:**
```python
# One pattern for all entity retrieval
def get_user(id):
    return db.query(User).filter_by(id=id).first()

def get_order(id):
    return db.query(Order).filter_by(id=id).first()

def get_product(id):
    return db.query(Product).filter_by(id=id).first()
```

### MC-CO-05: Keep Established API Names

Don't rename working terms even if they became misnomers. Users predict behavior by the evoked association field, not the literal name.

**BAD:**
```python
# Renaming because system no longer requires credentials
login() -> authenticate()
# Renaming because it now writes to cloud, not disk
save() -> persist()
```

**GOOD:**
```python
# "Login" already means "authenticate" in users' minds
login()     # Keep
# "Save" already means "persist my work" regardless of storage
save()      # Keep
# New flow with genuinely different behavior gets a new name
sso_connect()   # New function for SSO flow
```

Like "horsepower" - the association field matters, not the literal name.

## Naming Design Rules (ND)

### MC-ND-01: Naming Structure Method

Build names by progressive qualification: most explicit name first, then specifiers, then states.

**Steps:**
1. Start with most explicit name: `project_start_date`
2. Add specifiers BEFORE: `planned_project_start_date`, `actual_project_start_date`
3. Add states AFTER: `planned_project_start_date_accepted`
4. Define short forms: external `ACTUAL_PROJECT_START_DATE` (`APSD`), internal `start_date` (`sd`)

**BAD:**
```python
date1 = ...
sd = ...
the_date = ...
project_date = ...    # Which project date? Start? End? Due?
```

**GOOD:**
```python
project_start_date = ...
planned_project_start_date = ...
actual_project_start_date = ...
```

### MC-ND-02: Canonical Form for IDs and Data Structures

Convert variable representations to predictable, matchable forms. Canonical forms enable automated compare, sort, match, join.

**BAD:**
```python
# Same concept, three representations - unmatchable
order_a = "Call on Dow Jones EStoxx 50, strike 4400, expires Feb 2008"
order_b = "ESTOXX 50 Call at 4400 (Feb 2008)"
order_c = {"type": "call", "index": "djestoxx50", "strike": 4400}
```

**GOOD:**
```python
# Canonical form - all representations converge to one ID
canonical_id = "CALL-DJESTOXX50@4400EX2008-02"

def to_canonical(order_text: str) -> str:
    """Parse any order text variant to canonical ID format."""
    ...
```

**Rule:** If data comes from multiple sources in different formats, define a canonical form and convert at the boundary.

### MC-ND-03: No Recursive/Implicit Naming

A name must not contain itself at a different level. A container name must describe what it contains.

**BAD:**
```python
class Name:
    name: str       # Recursive: Name.name
    surname: str

class InfoMeasurementModule:
    license_plate: str    # Nothing to do with measurements
```

**GOOD:**
```python
class PersonName:
    given_name: str
    surname: str

class VehicleRegistry:
    license_plate: str
```

### MC-ND-04: No Product-as-Term Collision

Avoid naming products with words that are common terms in the product's own domain.

**BAD:**
```python
# Microsoft Teams: "3 Teams in Teams", "my teams in Teams"
team = teams_client.get_team(team_id)  # Which "team"?

# Product named "Service" in a microservices architecture
service = Service.get_service(service_id)  # The product or the microservice?
```

**GOOD:**
```python
# Qualify to disambiguate
ms_team = teams_client.get_team(team_id)

# Or choose product names that don't collide
workspace = collaboration_client.get_workspace(workspace_id)
```

### MC-ND-05: Type Name = Domain Concept, Not Implementation

Name classes and types after what they represent in the domain, not how they're implemented.

**BAD:**
```python
class UserHashMap: ...          # Implementation detail
class OrderLinkedList: ...      # Implementation detail
class StringWrapper: ...        # Says nothing about domain
class DataObject: ...           # Says nothing about anything
```

**GOOD:**
```python
class UserDirectory: ...        # Domain concept
class OrderQueue: ...           # Domain concept (queue is acceptable - it describes behavior)
class EmailAddress: ...         # Domain concept
class ShippingLabel: ...        # Domain concept
```

### MC-ND-06: Disambiguate by Qualifying, Not Renaming

When two concepts collide in name, qualify both sides. Don't rename one to an unrelated term.

**BAD:**
```python
class Order:       # purchase order
class Sequence:    # was "sort order" - renamed to avoid collision

def process():     # process data
def handle():      # was "process request" - renamed to avoid collision
```

**GOOD:**
```python
class PurchaseOrder:
class SortOrder:

def process_data():
def process_request():
```

**Why:** Renaming to an unrelated term breaks the association field. "Sequence" doesn't evoke "ordering" the way "SortOrder" does. Qualifying preserves the original concept while adding precision.

### MC-ND-07: Intuitive Opposites for Paired Parameters

Parameters, return values, and configuration keys that form pairs must use predictable opposites.

**BAD:**
```python
def compare(reference_object, difference_object): ...
# Users expect: current/target, before/after, source/destination

config = {
    "start_time": "09:00",
    "finish_time": "17:00",    # Users expect "end_time"
}
```

**GOOD:**
```python
def compare(source, target): ...

config = {
    "start_time": "09:00",
    "end_time": "17:00",
}
```

**Standard opposites:** start/end, min/max, first/last, source/target, input/output, request/response, before/after, current/previous, local/remote, internal/external, public/private

### MC-ND-08: No Terminological Synonymy

One concept = one name across the entire codebase. Multiple names for the same thing create phantom entities in the developer's mental model.

**BAD:**
```python
# Three names for the same object across layers
def get_workshop(id): ...      # in service layer
def fetch_garage(id): ...      # in repository layer
def load_service_center(id): ...  # in API layer

# SDK uses different names than API
api_response = {"app_id": "123"}
sdk_object.client_id = "123"     # same GUID, different name
sdk_object.application_id = "123"  # third name for same thing
```

**GOOD:**
```python
# Same name everywhere
def get_workshop(id): ...   # service
def get_workshop(id): ...   # repository (or uses service)
workshop_id = "123"         # variable
api_response = {"workshop_id": "123"}

# SDK matches API naming
api_response = {"application_id": "123"}
sdk_object.application_id = "123"  # matches API
```

**Test:** Grep your codebase for all names referring to one concept. If you find synonyms across layers (API, SDK, database, logs), unify them to one canonical name.

### MC-ND-09: No Inverted Semantics

Parameter and field names must suggest the correct direction of the value. If the name implies one direction but the value means the opposite, rename.

**BAD:**
```python
# Name says "compression" (how much to remove)
# Value 40 means "40% output size" = 60% removed
config = {
    "target_compression_percent": 40  # Inverted: reader expects 40% removed
}

# Name says "timeout" (how long to wait)
# Value means "speed" (higher = faster response expected)
config = {
    "request_timeout": 5  # Is this 5 seconds to wait, or level 5 urgency?
}
```

**GOOD:**
```python
# Name matches value direction
config = {
    "target_reduction_percent": 60  # "Reduce by 60%" - unambiguous
}

config = {
    "request_timeout_seconds": 5  # Unit in name, direction clear
}
```

**Test:** Read the name and value aloud as a sentence: "Target compression is 40 percent." Does this sentence match the actual behavior? If not, rename until the sentence matches reality.

## Documentation Rules (DC)

### MC-DC-01: Four Description Types

Any code entity (function, class, module, system) can be documented from four perspectives:

- **Intentional** - WHY: What problem does this solve?
- **Functional** - WHAT: What does it accept, return, and guarantee?
- **Technical** - HOW: What algorithms, data structures, trade-offs?
- **Contextual** - WHERE: What depends on this? What does this depend on?

**Example - rate limiter module:**

```python
"""
Rate limiter for API endpoints.

WHY: Prevents API abuse by limiting request frequency per client.

WHAT: Counts requests per client IP within sliding window.
Returns 429 when limit exceeded. Default: 100 req/min.

HOW: Redis sorted set per IP. Score = timestamp.
ZRANGEBYSCORE counts window. ZADD + EXPIRE on each request.

WHERE: Between API gateway and application handlers.
Depends on Redis. Bypassed for /health endpoints.
Configured in rate_limits.yaml.
"""
```

Not every entity needs all four. Use judgement. But when documenting complex code, covering all four prevents "but why?" and "but where?" questions.

### MC-DC-02: Match Description Type to Audience

- **README** - intentional + functional (users need why + what)
- **Docstrings** - functional + technical (developers need what + how)
- **Architecture docs** - intentional + contextual (architects need why + where)
- **Onboarding** - all four, in order: why -> what -> how -> where

**BAD** (technical description in README):
```markdown
# Rate Limiter
Uses Redis sorted sets with ZRANGEBYSCORE to count requests
within a sliding window. O(log N) per request.
```

**GOOD** (intentional + functional in README):
```markdown
# Rate Limiter
Prevents API abuse by blocking clients that exceed 100 requests/minute.
Blocked clients receive HTTP 429 until their window resets.
```

### MC-DC-03: Plain Language in User-Facing Messages

User-facing text (error messages, UI labels, help text, CLI output) uses daily words. No internal jargon, no abbreviations, no code references.

**BAD:**
```python
print("ERR: ECONNREFUSED on tcp://db:5432 - check pg_hba.conf")
print("NullReferenceException in OrderProcessor.ProcessBatch()")
print("Invalid JWT: exp claim < now()")
```

**GOOD:**
```python
print("Cannot connect to database. Check that the database server is running.")
print("Order processing failed. Please try again or contact support.")
print("Your session has expired. Please sign in again.")
```

**Developer-facing messages** (logs, debug output) can use technical terms - they serve a different audience (see MC-DC-02).
