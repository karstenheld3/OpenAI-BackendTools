---
name: hosting
description: Platform-specific deployment to Netlify, Vercel, Azure App Service, or SharePoint. Apply when deploying projects or creating deploy scripts.
compatibility: Windows, PowerShell 7+, Node.js 18+ (for Netlify/Vercel CLI). Auto-installs platform CLIs if missing.
---

# Hosting Skill

Platform-specific deployment knowledge, command-line interface (CLI) tooling, and deploy script templates.

**References** (loaded on demand per platform):
- `{platform}/SETUP.md` - Installation and authentication
- `{platform}/UNINSTALL.md` - Removal
- `{platform}/_deploy_template.bat` + `_deploy_template.ps1` - Deploy script templates

## MUST-NOT-FORGET

- Always create both `_deploy.bat` AND `_deploy.ps1` (bat is entry point, ps1 has logic)
- Scripts must be self-contained: install missing tools before attempting deploy
- Never hardcode absolute paths in generated scripts - use `$PSScriptRoot` and relative paths
- Template placeholders (`{{...}}`) must ALL be replaced before script is functional

## Intent Lookup

**User wants to...**
- **Deploy static site / Single-Page Application (SPA)** -> Netlify or Vercel (check for `netlify.toml` or `vercel.json`)
- **Deploy Python/Node backend** -> Azure App Service (`azure-app-service/`)
- **Deploy SharePoint Framework (SPFx) package** -> SharePoint App Catalog (`sharepoint-app-catalog/`)
- **Build Zola site** -> `zola/` for build, then Netlify/Vercel for hosting
- **Create deploy scripts for team** -> Detection Order + template copy
- **Set up CLI tools** -> `{platform}/SETUP.md`
- **Remove CLI tools** -> `{platform}/UNINSTALL.md`

## Platform Registry

- **netlify/** - Static sites, Single-Page Applications (SPAs), serverless functions (Netlify Content Delivery Network)
- **vercel/** - Static sites, Server-Side Rendering (SSR) with Next.js, edge functions (Vercel Edge Network)
- **azure-app-service/** - Python/Node backends, Docker containers (Azure Platform as a Service)
- **sharepoint-app-catalog/** - SharePoint Framework (SPFx) packages to SharePoint Online Site Collection App Catalog
- **zola/** - Static site generator (build tool only, deploys via netlify or vercel)

## Subfolder Contents

Each platform subfolder contains:
- `SETUP.md` - Install CLI tools, authenticate, link project
- `UNINSTALL.md` - Remove CLI tools, unlink project
- `_deploy_template.bat` - Template: Windows batch wrapper (checks PowerShell 7, calls `_deploy.ps1`)
- `_deploy_template.ps1` - Template: Install tools if missing, read config, build, deploy, verify

Exception: `zola/` has no deploy templates (build tool, not a host).

## Detection Order

When `/deploy` is invoked, determine platform by scanning (first match wins):

1. `!NOTES.md` or `NOTES.md` "Deployment" section (explicit, highest priority)
2. Existing `_deploy.bat` or `_deploy.ps1` in project root or `scripts/` folder
3. Config files in project root:
   - `netlify.toml` → Netlify
   - `vercel.json` → Vercel
   - `azure-pipelines.yml` or `.env` with `AZURE_APP_SERVICE_NAME` → Azure App Service
   - `config/package-solution.json` → SharePoint App Catalog
4. Framework inference:
   - `config.toml` with `[extra]` section → Zola (then check for `netlify.toml`)
   - `vite.config.ts` or `next.config.js` without host config → prompt to select host

## Deploy Script Conventions

### `_deploy.bat` Pattern

All `_deploy.bat` files follow this structure:
1. Check PowerShell 7 exists at `C:\Program Files\PowerShell\7\pwsh.exe`
2. `cd /d "%~dp0"` to script directory
3. `Unblock-File` the `.ps1` script
4. Run `_deploy.ps1` with PowerShell 7
5. `pause` at end

### `_deploy.ps1` Pattern

All `_deploy.ps1` files follow this structure:
1. **Check/install tools** - Platform CLI (netlify-cli, vercel, az CLI)
2. **Read config** - From `netlify.toml`, `vercel.json`, `.env`, or `package.json`
3. **Build** - Run project build command (`npm run build`, `zola build`, etc.)
4. **Deploy** - Platform-specific deploy command
5. **Verify** - Print live URL, optionally check HTTP 200

### Placement in Projects

Deploy scripts are placed in the **project root** (not `scripts/`) for discoverability:
- `_deploy.bat` - Windows batch entry point (checked into git)
- `_deploy.ps1` - PowerShell 7 implementation (checked into git)

Exception: Projects with existing `scripts/` folder convention keep scripts there.

## Gotchas

- **Netlify CLI auth expires** - Token stored at `~/.netlify/config.json`. If deploy fails with 401, re-run `netlify login`
- **Vercel auto-detects wrong framework** - Override with `vercel.json` `buildCommand` and `outputDirectory`
- **Azure zip deploy ignores nested folders** - `Compress-Archive` flattens by default. Script uses `-Path $items` pattern to preserve structure
- **SharePoint Node version** - SPFx 1.20 REQUIRES Node.js 18.x. Node 20+ breaks the build silently
- **Netlify `--site-name` only works for new sites** - For existing sites, use `netlify link` first or `--site-id`
- **PowerShell `Unblock-File`** - Required after git clone on Windows (NTFS alternate data stream blocks execution)

## When to Use

- `/deploy` workflow references this skill for platform-specific commands
- Agent creates `_deploy.bat` + `_deploy.ps1` from templates when missing
- Templates are adapted to project (build command, site name, publish dir)
