# Netlify Setup

## Prerequisites

- Node.js 18+ installed
- npm available in PATH

## Install CLI

```powershell
npm install -g netlify-cli
```

Verify: `netlify --version`

## Authenticate

```powershell
netlify login
```

Opens browser for OAuth. After auth, token stored locally at `~/.netlify/config.json`.

## Link Project

```powershell
# In project root (where netlify.toml lives)
netlify link
```

Or create new site:
```powershell
netlify sites:create --name my-site-name
```

## Required Config File

`netlify.toml` in project root:
```toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

## Deploy Commands

```powershell
# Production deploy (pre-built)
netlify deploy --prod --dir=dist

# Draft deploy (preview URL)
netlify deploy --dir=dist

# Deploy with site name (no link needed)
netlify deploy --prod --dir=dist --site-name=my-site
```

## Key Facts

- Free tier: 100GB bandwidth/month, 300 build minutes/month
- Deploy is atomic (all-or-nothing)
- Each deploy gets unique URL: `https://{deploy-id}--{site}.netlify.app`
- Production URL: `https://{site}.netlify.app`
- SPA redirect rule required for client-side routing
