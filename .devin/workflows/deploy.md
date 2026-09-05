---
description: Deploy project to configured hosting platform (Netlify, Vercel, Azure, SharePoint)
auto_execution_mode: 3
---

# Deploy Workflow

Deploy a project to its configured hosting platform. Creates deploy scripts if missing.

Scope: Production deployment only. Use platform UI for preview/staging deploys.

**Goal**: Project deployed to production with shareable URL, `_deploy.bat` + `_deploy.ps1` checked into project

**Why**: Reproducible deployments for all team members without manual CLI knowledge

## Required Skills

- @skills:hosting for platform detection, command-line interface (CLI) install, and deploy script templates

## Prerequisites

- Project has buildable source (package.json, config.toml, or similar)
- Network access to deployment platform
- For Netlify/Vercel: `npm` available
- For Azure: PowerShell 7 available
- For SharePoint: PowerShell 7 + Node.js 18.x available (SharePoint Framework requires 18.x)

## MUST-NOT-FORGET

- **DO NOT USE** Windsurf deploy tool (`deploy_web_app`) or `*.windsurf.build` domains. Always use platform CLI directly.
- Deploy scripts (`_deploy.bat` + `_deploy.ps1`) MUST exist in project after workflow completes
- Scripts must install all required tools if not present (self-contained)
- Never deploy without successful build first
- Update PROGRESS.md after successful deploy
- Use non-blocking execution for long-running deploys (Azure zip upload, SharePoint Framework build)

## GLOBAL-RULES

Apply to ALL deployment contexts.

1. Detect platform (see @skills:hosting SKILL.md "Detection Order")
2. Verify project builds cleanly before any deploy attempt
3. Ensure `_deploy.bat` + `_deploy.ps1` exist (create from templates if missing)
4. Deploy to production
5. Verify deployment succeeded (live URL returns HTTP 200 or platform confirms success)

# CONTEXT-SPECIFIC

## Context: Deploy Scripts Missing

Entry condition: No `_deploy.bat` in project root (or `scripts/` folder for projects with that convention).

1. Determine platform from detection order in @skills:hosting SKILL.md
2. Copy `_deploy_template.bat` from `[AGENT_FOLDER]/skills/hosting/{platform}/_deploy_template.bat` → project as `_deploy.bat`
3. Copy `_deploy_template.ps1` from `[AGENT_FOLDER]/skills/hosting/{platform}/_deploy_template.ps1` → project as `_deploy.ps1`
4. Adapt placeholders in `_deploy.ps1`:
   - `{{SITE_NAME}}` → from `netlify.toml`, `vercel.json`, or `!NOTES.md`
   - `{{STARTUP_COMMAND}}` → from project config
   - `{{SPFX_PROJECT_DIR}}` → from project structure
   - `{{TARGET_SITE_URL}}` → from `!NOTES.md`
   - `$BUILD_COMMAND` → from `package.json` scripts or project convention
   - `$PUBLISH_DIR` / `$SOURCE_DIR` → from build config
5. Place scripts in project root (or `scripts/` if project uses that convention)
6. Continue to platform-specific deploy context below

## Context: Netlify

Entry condition: `netlify.toml` exists or platform detected as Netlify.

**Account slug**: `karstenheld3` (use `--account-slug karstenheld3` on all `sites:create` commands to avoid interactive team prompt)

1. Verify `netlify.toml` exists with `[build]` section
2. Run build command from `package.json` or `netlify.toml`
3. If site not yet created:
   - `npx netlify sites:create --name {site-name} --account-slug karstenheld3`
   - This auto-links the project (creates `.netlify/` folder)
4. Deploy: `npx netlify deploy --prod --dir={publish_dir}`
5. Verify: confirm "Deploy is live" output and print production URL

## Context: Vercel

Entry condition: `vercel.json` exists or platform detected as Vercel.

1. Run build command if needed (Vercel builds remotely by default)
2. Deploy: `vercel --prod`
3. Verify: confirm deployment URL in output

## Context: Azure App Service

Entry condition: `.env` with `AZURE_APP_SERVICE_NAME` or platform detected as Azure.

1. Run `_deploy.ps1` (handles auth, zip, deploy)
2. Verify: print app service URL, optionally check HTTP 200

## Context: SharePoint App Catalog

Entry condition: `config/package-solution.json` exists or platform detected as SharePoint.

1. Run `_deploy.ps1` (handles build, upload, publish)
2. Verify: confirm "Deploy complete" output

## Context: Custom Script Exists

Entry condition: `_deploy.bat` already exists but platform not recognized above.

1. Run existing `_deploy.bat` via PowerShell
2. Report output to user

## Context: Zola Site

Entry condition: `config.toml` with Zola markers detected.

1. Determine hosting target (check for `netlify.toml` or `vercel.json`)
2. Build: `zola build`
3. Route to Netlify or Vercel context for actual deploy

## Context: No Context Match

Entry condition: No platform detected by any method above.

1. List detection attempts and results
2. Ask user which platform to deploy to
3. After user responds, create `_deploy.bat` + `_deploy.ps1` from selected platform template
4. Add "Deployment" section to `!NOTES.md` or `NOTES.md` for future detection

## Stuck Detection

If deployment fails:
1. Check CLI output for error message
2. Common fixes:
   - 401/403 → Re-authenticate (`netlify login`, `vercel login`, `az login`)
   - Build failure → Fix build locally first, then retry
   - Site not found → Check site name/ID in config matches platform
3. If 2 consecutive deploy attempts fail:
   - Document error in PROBLEMS.md
   - Ask user for guidance

## Execution Rules

**Build** (blocking, verify exit code):
```powershell
npm run build
if ($LASTEXITCODE -ne 0) { throw "Build failed" }
```

**Create Netlify site** (blocking, only if site not linked):
```powershell
npx netlify sites:create --name "$SITE_NAME" --account-slug karstenheld3
```

**Deploy Netlify** (blocking):
```powershell
npx netlify deploy --prod --dir="dist"
```

**Deploy Vercel** (blocking):
```powershell
npx vercel --prod --yes
```

**Deploy Azure/SharePoint** (non-blocking for long uploads):
```powershell
# Run as non-blocking with WaitMsBeforeAsync: 10000
pwsh -f "_deploy.ps1"
```

# VERIFICATION

1. Deployment succeeded (CLI exit code 0, "live" or "complete" in output)
2. `_deploy.bat` and `_deploy.ps1` exist in project (created or pre-existing)
3. Live URL accessible (if applicable)
4. Update PROGRESS.md with deploy URL and timestamp

## Output

`Deployed: {platform} | URL: {live_url} | Scripts: {created|existed}`
