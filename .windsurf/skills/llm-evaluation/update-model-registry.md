# Update Model Registry

**Goal**: Refresh `model-registry.json`, `model-pricing.json`, and `model-parameter-mapping.json` with current data from official provider websites. Verify new models work with `call-llm.py`.

**Design principle**: Document Object Model (DOM) extraction is the authoritative source of numeric data. Screenshots and markdown transcriptions are archival references for historical cost tracking. Every phase has a verification gate.

**Code block convention**: Blocks showing `browser_navigate(...)`, `browser_evaluate(...)`, `browser_run_code(...)` illustrate Playwright MCP tool invocations. The string inside `function:` / `code:` is the actual JavaScript argument.

**Replaces**: `UPDATE_MODEL_PRICING.md` and `UPDATE_MODEL_REGISTRY.md` (both deleted).

## Placeholders

- `[SKILL_FOLDER]`: Folder containing this workflow (e.g., `DevSystemV3.7/skills/llm-evaluation`)
- `[MODEL_SOURCES]`: `[SKILL_FOLDER]/model-sources`
- `[DATE]`: Today in `YYYY-MM-DD`
- `[VENV_PYTHON]`: `../.tools/llm-venv/Scripts/python.exe`
- `[TRANSCRIPTION_SCRIPT]`: `.windsurf/skills/llm-transcription/transcribe-image-to-markdown.py`
- `[AGENT_FOLDER]`: Active agent folder (e.g., `.windsurf`)
- `[KEYS_FILE]`: API keys file path

## Sources

**Anthropic:**
- A1 - Pricing: `https://docs.anthropic.com/en/docs/about-claude/pricing`
- A2 - Models (API IDs): `https://docs.anthropic.com/en/docs/about-claude/models`
- A3 - Models Overview: `https://platform.claude.com/docs/en/about-claude/models/overview`
- A4 - Deprecations: `https://platform.claude.com/docs/en/about-claude/model-deprecations`

**OpenAI:**
- O1 - Standard Pricing: `https://developers.openai.com/api/docs/pricing?latest-pricing=standard`
- O2 - Batch Pricing: `https://developers.openai.com/api/docs/pricing?latest-pricing=batch`
- O3 - Model Compare: `https://platform.openai.com/docs/models/compare`

## Pricing Dimensions

For every model, capture all available:

- **Input** per 1M tokens
- **Cached input** per 1M tokens (null if not offered)
- **Output** per 1M tokens
- **Long context input/cached/output** per 1M tokens (OpenAI only, null if model has no long-context tier)
- **Tier**: Standard and Batch (captured as separate datasets)
- **Context window** (K tokens)

`model-pricing.json` stores **Standard tier** prices for both providers. Models with a long-context pricing tier store those prices in a nested `long_context` object. Both tiers are still captured for the archive.

## Archive Convention

All artifacts go to `[MODEL_SOURCES]` with date prefix:

```
model-sources/
  [DATE]_Anthropic-Pricing-DOM.json       # DOM extraction (authoritative data)
  [DATE]_Anthropic-ModelIDs-DOM.json      # Resolved API IDs
  [DATE]_OpenAI-Standard-DOM.json
  [DATE]_OpenAI-Batch-DOM.json
  [DATE]_Anthropic-Pricing.md             # Stitched screenshot transcriptions
  [DATE]_Anthropic-ModelOverview.md
  [DATE]_Anthropic-Deprecations.md
  [DATE]_OpenAI-Standard.md
  [DATE]_OpenAI-Batch.md
  [DATE]_OpenAI-Compare.md
  [DATE]_screenshots/                     # Screenshot archive
    Anthropic-Pricing/01.jpg, 02.jpg, ...
    Anthropic-ModelOverview/...
    Anthropic-Deprecations/...
    OpenAI-Standard/...
    OpenAI-Batch/...
    OpenAI-Compare/...
```

## Phase 1: Pre-Flight Checks

1. Read `last_updated` from `model-pricing.json`, `_updated` from `model-registry.json` and `model-parameter-mapping.json`.
2. If any equals today's `[DATE]` → confirm with user whether to re-run.
3. Confirm `[MODEL_SOURCES]` exists. If missing, create it.
4. Create `[MODEL_SOURCES]/[DATE]_screenshots/` and subfolders for each source (A1, A3-A4, O1-O3). A2 is DOM-only — no screenshot subfolder. Pre-existing files in these paths **will be overwritten** on re-run — confirm before proceeding.

**Gate 1**: Proceed only if all dates < `[DATE]` or user confirmed re-run.

## Common Procedures

### Cookie / Overlay Dismissal

Run once per page after `browser_navigate` + `browser_resize`:

```
browser_evaluate(function: "(() => {
  ['#cookie-banner','#cookieModal','.cookie-consent','[class*=\"cookie\"]',
   '[id*=\"cookie\"]','.gdpr-banner','#onetrust-consent-sdk']
    .forEach(sel => document.querySelectorAll(sel).forEach(el => el.remove()));
  document.querySelectorAll('.modal-backdrop,[class*=\"overlay\"]').forEach(el => el.remove());
  document.body.style.overflow = 'auto';
  document.querySelectorAll('header, nav, [class*=\"sticky\"], [class*=\"fixed\"]')
    .forEach(el => { el.style.position = 'relative'; });
})()")
```

### Expand Collapsed Sections

Click all "All models" / "View more" / "Show all" / "Expand" buttons:

```
browser_evaluate(function: "async () => {
  const delay = ms => new Promise(r => setTimeout(r, ms));
  for (const btn of document.querySelectorAll('button, [role=\"button\"]')) {
    const t = btn.textContent.toLowerCase().trim();
    if (/all models|view more|show all|expand/.test(t)) { btn.click(); await delay(400); }
  }
}")
```

### Table Extraction

Extract all visible tables from the page:

```
browser_evaluate(function: "() => {
  const tables = Array.from(document.querySelectorAll('table'));
  return tables.map((t, idx) => ({
    idx,
    caption: (t.caption?.textContent || t.closest('section,div')?.querySelector('h1,h2,h3,h4')?.textContent || '').trim().slice(0,120),
    headers: Array.from(t.querySelectorAll('thead th, tr:first-child th, tr:first-child td')).map(h => h.textContent.trim()),
    rows: Array.from(t.querySelectorAll('tbody tr')).map(r =>
      Array.from(r.querySelectorAll('td')).map(c => c.textContent.trim()))
  })).filter(t => t.rows.length);
}")
```

### Standard Page Setup

For every page in Phase 2 and Phase 3, execute these steps in order:

1. `browser_navigate(url: "<URL>")`
2. `browser_resize(width: 1920, height: 1080)`
3. `browser_wait_for(time: 2)`
4. Run Cookie / Overlay Dismissal.
5. Run Expand Collapsed Sections.

## Phase 2: DOM Extraction (Primary Data Source)

This phase produces the **authoritative** machine-readable data. It runs independently of screenshots. For each page, perform Standard Page Setup, then extract and save.

### 2.1 Anthropic Pricing (A1)

URL: `https://docs.anthropic.com/en/docs/about-claude/pricing`

After Standard Page Setup, run Table Extraction. Save to: `[MODEL_SOURCES]/[DATE]_Anthropic-Pricing-DOM.json`

Key columns: `Base Input Tokens`, `Cache Hits & Refreshes`, `Output Tokens`. Full column-to-schema mapping in Phase 6 Rule 5.

### 2.2 Anthropic Model ID Resolution (A2)

URL: `https://docs.anthropic.com/en/docs/about-claude/models`

The pricing page shows friendly names without API date suffixes. Resolve the exact API ID using the fallback chain:

1. After Standard Page Setup, extract full page text. Search for `claude-<family>-<version>-YYYYMMDD` patterns.
2. If not found, query the live API:
   ```
   curl https://api.anthropic.com/v1/models -H "x-api-key: $KEY" -H "anthropic-version: 2023-06-01"
   ```
3. If still missing, write the undated alias (e.g. `claude-opus-4-7`) and add a sibling key: `"_note_<alias>": "date suffix pending"`. Do **NOT** skip the entry.

Save to: `[MODEL_SOURCES]/[DATE]_Anthropic-ModelIDs-DOM.json`

### 2.3 OpenAI Standard Pricing (O1)

URL: `https://developers.openai.com/api/docs/pricing?latest-pricing=standard`

After Standard Page Setup, run Table Extraction. The Standard pricing URL renders **both Standard and Batch** tables in the DOM. Identify tiers by price (Batch = roughly half Standard). Use Standard-tier tables only. Save to: `[MODEL_SOURCES]/[DATE]_OpenAI-Standard-DOM.json`

### 2.4 OpenAI Batch Pricing (O2)

URL: `https://developers.openai.com/api/docs/pricing?latest-pricing=batch`

After Standard Page Setup, run Table Extraction. Save to: `[MODEL_SOURCES]/[DATE]_OpenAI-Batch-DOM.json`

### Gate 2

Every model visible on the pricing pages has:
- Numeric input / output prices captured
- Cached price captured or explicitly `null`
- (Anthropic) resolved or flagged API ID

If any check fails, retry extraction or escalate to user before Phase 3.

## Phase 3: Screenshot Archive

Screenshots serve as a visual audit trail for historical cost tracking. They are **NOT** used to derive prices — Phase 2 DOM extraction already did that.

For each page: perform Standard Page Setup, then capture using the appropriate scroll method.

### Body-Scroll Capture (Anthropic pages)

Anthropic docs pages use the document body for scrolling:

```js
browser_run_code(code: "async (page) => {
  await page.evaluate(async () => {
    const delay = ms => new Promise(r => setTimeout(r, ms));
    let prev = -1;
    for (let i = 0; i < 80; i++) {
      window.scrollBy(0, 600); await delay(250);
      if (document.body.scrollHeight === prev) break;
      prev = document.body.scrollHeight;
    }
    window.scrollTo(0, 0);
  });
  const total = await page.evaluate(() => document.body.scrollHeight);
  const vh = await page.evaluate(() => window.innerHeight);
  const n = Math.ceil(total / vh);
  for (let i = 0; i < n; i++) {
    await page.evaluate(y => window.scrollTo(0, y), i * vh);
    await page.waitForTimeout(400);
    const s = String(i + 1).padStart(2, '0');
    await page.screenshot({ path: '[FOLDER]/' + s + '.jpg', scale: 'css', type: 'jpeg', quality: 90 });
  }
  return { n };
}")
```

### Inner-Scroll Capture (OpenAI Pricing pages)

OpenAI pricing pages use `.docs-scroll-container`. Falls back to body scroll if selector not found:

```js
browser_run_code(code: "async (page) => {
  await page.evaluate(async () => {
    const delay = ms => new Promise(r => setTimeout(r, ms));
    for (const btn of document.querySelectorAll('button')) {
      if (/all models|view more/i.test(btn.textContent)) { btn.click(); await delay(400); }
    }
  });
  await page.waitForTimeout(800);
  const info = await page.evaluate(async () => {
    const delay = ms => new Promise(r => setTimeout(r, ms));
    const c = document.querySelector('.docs-scroll-container') || document.scrollingElement || document.body;
    const useBody = c === document.body || c === document.scrollingElement;
    let prev = -1;
    for (let i = 0; i < 80; i++) {
      if (useBody) window.scrollBy(0, 600); else c.scrollBy(0, 600);
      await delay(250);
      const h = useBody ? document.body.scrollHeight : c.scrollHeight;
      if (h === prev) break;
      prev = h;
    }
    if (useBody) window.scrollTo(0, 0); else c.scrollTo(0, 0);
    return {
      total: useBody ? document.body.scrollHeight : c.scrollHeight,
      vh: useBody ? window.innerHeight : c.clientHeight,
      useBody
    };
  });
  const n = Math.ceil(info.total / info.vh);
  for (let i = 0; i < n; i++) {
    await page.evaluate(({idx, ub}) => {
      const c = ub ? null : document.querySelector('.docs-scroll-container');
      if (ub) window.scrollTo(0, idx * window.innerHeight);
      else c.scrollTo(0, idx * c.clientHeight);
    }, {idx: i, ub: info.useBody});
    await page.waitForTimeout(400);
    const s = String(i + 1).padStart(2, '0');
    await page.screenshot({ path: '[FOLDER]/' + s + '.jpg', scale: 'css', type: 'jpeg', quality: 90 });
  }
  return { n };
}")
```

### Page-to-Folder Mapping

- A1 Anthropic Pricing — Body-Scroll → `[MODEL_SOURCES]/[DATE]_screenshots/Anthropic-Pricing`
- A3 Anthropic Overview — Body-Scroll → `[MODEL_SOURCES]/[DATE]_screenshots/Anthropic-ModelOverview`
- A4 Anthropic Deprecations — Body-Scroll → `[MODEL_SOURCES]/[DATE]_screenshots/Anthropic-Deprecations`
- O1 OpenAI Standard — Inner-Scroll → `[MODEL_SOURCES]/[DATE]_screenshots/OpenAI-Standard`
- O2 OpenAI Batch — Inner-Scroll → `[MODEL_SOURCES]/[DATE]_screenshots/OpenAI-Batch`
- O3 OpenAI Compare — Inner-Scroll → `[MODEL_SOURCES]/[DATE]_screenshots/OpenAI-Compare`

A2 (Anthropic Models) is DOM-only — no screenshots needed (text page, no pricing tables).

Replace `[FOLDER]` in the capture templates with the full screenshot folder path.

O3 (OpenAI Compare) uses custom div-based model cards, **not HTML `<table>` elements**. Table Extraction returns empty. For context window data, use `innerText` search:

```js
browser_evaluate(function: "() => {
  const text = document.body.innerText;
  const matches = [];
  let idx = 0;
  while ((idx = text.indexOf('Window', idx)) !== -1) {
    matches.push(text.substring(Math.max(0, idx - 100), idx + 100));
    idx += 10;
  }
  return matches;
}")
```

For full-page screenshots: use Body-Scroll Capture (body scroll works on Compare page).

**Gate 3**: Each folder contains >= 1 .jpg. Spot-check one screenshot per folder to confirm the Output column is visible. If clipped → increase viewport width and re-run the affected folder only.

## Phase 4: Transcribe Screenshots

Produces human-readable markdown alongside raw screenshots for historical reference.

### 4.1 Transcribe Each Source

```powershell
$sources = @(
  "Anthropic-Pricing",
  "Anthropic-ModelOverview",
  "Anthropic-Deprecations",
  "OpenAI-Standard",
  "OpenAI-Batch",
  "OpenAI-Compare"
)
foreach ($src in $sources) {
  $folder = "[MODEL_SOURCES]/[DATE]_screenshots/$src"
  if (Test-Path $folder) {
    & [VENV_PYTHON] [TRANSCRIPTION_SCRIPT] `
      --input-folder $folder `
      --output-folder $folder `
      --model gpt-5-mini --initial-candidates 1 `
      --keys-file [KEYS_FILE] --force
  }
}
```

### 4.2 Stitch and Clean

Concatenate per-page .md files into single combined files at `[MODEL_SOURCES]`:

```powershell
$stitch = @{
  "Anthropic-Pricing"       = "[MODEL_SOURCES]/[DATE]_Anthropic-Pricing.md"
  "Anthropic-ModelOverview"  = "[MODEL_SOURCES]/[DATE]_Anthropic-ModelOverview.md"
  "Anthropic-Deprecations"   = "[MODEL_SOURCES]/[DATE]_Anthropic-Deprecations.md"
  "OpenAI-Standard"          = "[MODEL_SOURCES]/[DATE]_OpenAI-Standard.md"
  "OpenAI-Batch"             = "[MODEL_SOURCES]/[DATE]_OpenAI-Batch.md"
  "OpenAI-Compare"           = "[MODEL_SOURCES]/[DATE]_OpenAI-Compare.md"
}
foreach ($src in $stitch.Keys) {
  $folder = "[MODEL_SOURCES]/[DATE]_screenshots/$src"
  if (Test-Path "$folder/*.md") {
    Get-ChildItem "$folder/*.md" | Sort-Object Name |
      ForEach-Object { Get-Content $_.FullName -Raw } |
      Out-File $stitch[$src] -Encoding utf8
    Remove-Item "$folder/*.md" -Force -ErrorAction SilentlyContinue
    Remove-Item "$folder/_batch_summary.json" -Force -ErrorAction SilentlyContinue
  }
}
```

**Gate 4**: Combined markdowns exist in `[MODEL_SOURCES]` for each source that had screenshots. No action is blocked by transcription quality — Phase 5-7 use DOM data.

## Phase 5: Update `model-registry.json`

Input: All DOM artifacts from Phase 2 + transcribed deprecation and overview data.

### 5.0 Derive Change Set

Before modifying JSON files, compare DOM extraction output against current files to determine what changed.

1. Read current `model-registry.json` and `model-pricing.json`.
2. Parse each `[DATE]_*-DOM.json` from Phase 2. Extract all model IDs.
3. Build three lists:
   - `newRegistryIds` — IDs in DOM but absent from `models[]`
   - `newPricingIds` — IDs in DOM but absent from pricing file
   - `changedPricingIds` — IDs where DOM price differs from current pricing
4. If all three lists are empty: skip to Phase 10 (report "no changes detected").

Phases 6 and 8 reference these lists. `$newIds` in Gate 6 = `newPricingIds` union `changedPricingIds`. `$newEnabledModels` in Phase 8 = models from `newRegistryIds` where `enabled: true` in registry after Phase 5.1 updates.

### 5.1 Update `models[]`

1. **Add** new models not yet present with `"enabled": false, "status": "untested"`.
2. **Update** `context_window` for existing models if now known (from pricing page context_window_k * 1000, or from overview/compare pages).
3. **Update** `status` to `"deprecated"` and set `"enabled": false` for models on the deprecation page.
4. **Never remove** existing models — they may be referenced by evaluation results.
5. Insert new models at the top of their provider group, newest first.

### 5.2 Update `model_id_startswith[]`

1. **Update** `max_input` for existing prefix entries based on context window data.
2. Check if any new model fails to match an existing prefix.
   - If it matches an existing family (e.g., `gpt-5.5` matches `gpt-5` prefix): verify the method/effort config is compatible. If not, a new more-specific prefix entry is needed.
   - **Report** unmatched models — do NOT auto-add prefix entries (they require manual API behavior configuration for method, effort levels, max_output, thinking_max).

### 5.3 Update Metadata

- Bump `_updated` to `[DATE]`.
- Bump `_version` patch number.

### Gate 5 (Persistence + Consistency)

```powershell
$r = Get-Content "[SKILL_FOLDER]/model-registry.json" -Raw | ConvertFrom-Json
if ($r._updated -ne "[DATE]") { throw "registry _updated not bumped" }

# Every model matches at least one prefix
foreach ($m in $r.models) {
  $matched = $r.model_id_startswith | Where-Object { $m.model_id.StartsWith($_.prefix) }
  if (-not $matched) { Write-Warning "No prefix match: $($m.model_id)" }
}

# No duplicate model_ids
$ids = $r.models.model_id
if (($ids | Sort-Object -Unique).Count -ne $ids.Count) { throw "Duplicate model_ids" }
```

## Phase 6: Update `model-pricing.json`

Input: `[MODEL_SOURCES]/[DATE]_Anthropic-Pricing-DOM.json`, `[DATE]_OpenAI-Standard-DOM.json`, `[DATE]_Anthropic-ModelIDs-DOM.json`

### Rules

1. **Add** new models not currently in the file.
2. **Update** prices for existing models if changed.
3. **Never remove** legacy entries — even deprecated models stay for historical cost calc.
4. **Tier selection:** Standard tier for both providers.
5. **Column mapping:**
   - Anthropic: `Base Input Tokens` → `input_per_1m`, `Cache Hits & Refreshes` → `cached_per_1m`, `Output Tokens` → `output_per_1m`. Ignore `5m Cache Writes` and `1h Cache Writes`.
   - OpenAI short context: `Input` → `input_per_1m`, `Cached input` → `cached_per_1m`, `Output` → `output_per_1m`.
   - OpenAI long context: `Input (Long)` → `long_context.input_per_1m`, `Cached input (Long)` → `long_context.cached_per_1m`, `Output (Long)` → `long_context.output_per_1m`. Only present when the DOM row has non-empty long-context columns.
6. **Short/Long context split** (OpenAI only): store **Short context** numbers under the flat keys. If a model has long-context columns in the DOM, add a `long_context` nested object: `{input_per_1m, cached_per_1m|omit if null, output_per_1m, threshold_k: null}`. Set `threshold_k` to `null` until OpenAI documents the exact token threshold.
7. Every entry: `{input_per_1m, cached_per_1m|omit if null, output_per_1m, long_context|omit if no long tier, context_window_k, currency: "USD"}`.
8. Bump `last_updated` to `[DATE]`.
9. Update `sources` array if URLs changed.

### Gate 6 (Persistence Check, MANDATORY)

```powershell
$p = Get-Content "[SKILL_FOLDER]/model-pricing.json" -Raw | ConvertFrom-Json
if ($p.last_updated -ne "[DATE]") { throw "last_updated not bumped" }

# Every new model_id from Phase 2 DOM is present
foreach ($id in $newIds) {
  if (-not $p.pricing.anthropic.$id -and -not $p.pricing.openai.$id) { throw "Missing $id" }
}
```

If any check fails: re-apply edit, re-run gate. Do not proceed.

## Phase 7: Update `model-parameter-mapping.json`

This file is usually stable — effort levels and their numeric mappings rarely change. This phase verifies compatibility with new models and flags gaps.

### 7.1 Check Compatibility

For each new model added in Phase 5:
1. Identify its `method` from `model_id_startswith[]` (temperature, reasoning_effort, thinking, effort).
2. Verify the method exists in `effort_mapping` (it maps to `temperature_factor`, `openai_reasoning_effort`, `anthropic_thinking_factor`, etc.).
3. If a new method type appears that isn't covered → **flag for manual update** and escalate to user.

### 7.2 Update Metadata

- If any changes were needed: bump `_updated` to `[DATE]` and `_version` patch.
- If no changes: leave as-is (do NOT bump date for a no-op).

### Gate 7

```powershell
$m = Get-Content "[SKILL_FOLDER]/model-parameter-mapping.json" -Raw | ConvertFrom-Json
$r = Get-Content "[SKILL_FOLDER]/model-registry.json" -Raw | ConvertFrom-Json

# Every method in registry has corresponding effort_mapping key
$methods = $r.model_id_startswith | ForEach-Object { $_.method } | Sort-Object -Unique
foreach ($method in $methods) {
  $key = switch ($method) {
    "temperature"       { "temperature_factor" }
    "reasoning_effort"  { "openai_reasoning_effort" }
    "thinking"          { "anthropic_thinking_factor" }
    default             { $method }
  }
  if (-not $m.effort_mapping.$key) { throw "Missing effort_mapping for method '$method' (key '$key')" }
}
```

## Phase 8: Test New Models

Run `test-call-llm.py` for each newly added model that has `enabled: true` in the registry.

```powershell
# Test specific new models
foreach ($modelId in $newEnabledModels) {
  & [VENV_PYTHON] "[SKILL_FOLDER]/test-call-llm.py" `
    --keys-file [KEYS_FILE] `
    --model $modelId
}
```

If `test-call-llm.py` has no test entries for a new model, the `--model` filter returns zero tests. In that case:
1. Add a minimal test entry to the appropriate `OPENAI_TESTS` or `ANTHROPIC_TESTS` list in `test-call-llm.py`.
2. Re-run.

**Gate 8**: All test runs exit with code 0. If a model fails:
- API error (401, 403): likely no access — set `status: "no_access"`, `enabled: false` in registry.
- API error (400): likely wrong parameters — check `model_id_startswith[]` config.
- Timeout: retry once, then flag in report.

## Phase 9: Sync to Dependent Locations

After all gates pass, copy the canonical files.

### 9.1 Sync to Dependent Skills

`model-pricing.json` and `model-registry.json` are consumed by other skills:

```powershell
$src = "[SKILL_FOLDER]"
$jsonFiles = @("model-pricing.json", "model-registry.json", "model-parameter-mapping.json")
$targets = @(
  "[AGENT_FOLDER]/skills/llm-transcription"
)
foreach ($dst in $targets) {
  foreach ($f in $jsonFiles) {
    if (Test-Path "$dst/$f") {
      Copy-Item "$src/$f" "$dst/$f" -Force
    }
  }
}
```

Only copy files that already exist at the target (not every skill uses all 3 JSONs).

### 9.2 Sync model-sources to .windsurf

The DevSystemV3.7 skill folder is the source of truth. Sync model-sources to the active agent folder:

```powershell
Copy-Item -Path "[SKILL_FOLDER]/model-sources/*" `
  -Destination "[AGENT_FOLDER]/skills/llm-evaluation/model-sources/" `
  -Recurse -Force
```

### Gate 9 (Sync Check)

```powershell
foreach ($dst in $targets) {
  foreach ($f in $jsonFiles) {
    if (Test-Path "$dst/$f") {
      $a = (Get-FileHash "$src/$f").Hash
      $b = (Get-FileHash "$dst/$f").Hash
      if ($a -ne $b) { throw "Sync mismatch: $dst/$f" }
    }
  }
}
```

## Phase 10: Report

Print a concise summary:

- **Added models**: `<provider>/<id>` with prices and context_window
- **Price changes**: `<id>: $old → $new`
- **Unchanged**: count only
- **Registry additions**: `<provider>/<id>` with `context_window`, `status`
- **Prefix gaps**: models that don't match any `model_id_startswith` prefix (requires manual config)
- **Parameter mapping**: changes made or "no changes needed"
- **Test results**: pass/fail per tested model
- **Long context**: models where `long_context` was added or updated (list model + threshold status)
- **Pending resolution**: undated Anthropic aliases, unresolved `threshold_k` values
- **Sources archived**: list of generated files in `[MODEL_SOURCES]`

## Failure Modes and Recovery

- **DOM extraction returns empty tables**: page DOM changed. Inspect via `browser_snapshot`, update selectors. Screenshots still valid as reference.
- **Output column clipped in screenshots**: Phase 2 (DOM) already captured the data. Fix viewport to 1920+ and re-run Phase 3 only if the archive matters.
- **Anthropic API ID unresolvable**: write the alias, add `_note_<alias>` key, flag in report. Do not block the run.
- **Gate 5, 6, 7, or 9 fails**: the edit did not persist or the sync did not complete. Most common cause: file was edited in memory but never written. Re-read from disk, re-apply, re-verify.
- **test-call-llm.py has no entries for new model**: add minimal test entry, re-run. Do not skip verification.
- **New dependent skill added**: append its folder to Phase 9 `$targets` and add to "Dependent skills" list.
- **Duplicate model in pricing vs registry**: reconcile toward the pricing file (prices are authoritative for existence); registry must follow.

## Document History

**[2026-05-22 09:25]**
- Added: Long context pricing support in Phase 6 Rules 5-7 (nested `long_context` object with `threshold_k`)
- Changed: Pricing Dimensions section to include long context tier
- Changed: Phase 10 report — long context now tracked, `threshold_k` listed as pending

**[2026-05-22 09:10]**
- Fixed: Inner-Scroll Capture `page.evaluate` multi-argument error (wrap args in object)
- Fixed: O1 Standard page note about dual Standard+Batch tables in DOM
- Fixed: O3 Compare page note about no HTML tables (use innerText search)

**[2026-05-22 08:58]**
- Changed: OpenAI pricing convention from Batch to Standard (user directive)

**[2026-05-22 08:28]**
- Fixed: Added `[AGENT_FOLDER]` to Placeholders (used in Phase 9 but undefined)

**[2026-05-22 08:27]**
- Fixed: Phase 1 step 4 — "A1-A4" corrected to "A1, A3-A4" (A2 has no screenshots)
- Fixed: Gate 6 — removed duplicate `$newIds` definition (already in Phase 5.0)
- Changed: Phase 2.1 column mapping → brief pointer to Phase 6 Rule 5 (AP-BR-03: single source of truth)

**[2026-05-22 08:26]**
- Added: Phase 5.0 "Derive Change Set" — defines how to determine new/changed models from DOM vs existing JSON
- Added: Gate 7 PowerShell verification script (consistency with other gates)
- Fixed: Phase 1 step 3 — "create if missing" for `[MODEL_SOURCES]` (SOCAS-06: underspecified)
- Fixed: Gate 5 — removed unused `$p` (model-pricing.json) read

**[2026-05-22 08:25]**
- Initial version — merged from `UPDATE_MODEL_PRICING.md` and `UPDATE_MODEL_REGISTRY.md`
- Added: Phase 7 (model-parameter-mapping.json compatibility check)
- Added: Phase 8 (test new models with test-call-llm.py)
- Changed: All artifacts stored in `[MODEL_SOURCES]` (replaces separate pricing-sources and registry-sources)
