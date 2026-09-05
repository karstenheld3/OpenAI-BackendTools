# Vercel Setup

## Prerequisites

- Node.js 18+ installed
- npm available in PATH

## Install CLI

```powershell
npm install -g vercel
```

Verify: `vercel --version`

## Authenticate

```powershell
vercel login
```

Opens browser for OAuth or email-based login. Token stored locally.

## Link Project

```powershell
# In project root
vercel link
```

Creates `.vercel/project.json` with org and project IDs.

## Optional Config File

`vercel.json` in project root (not required for Vite/Next.js - auto-detected):
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

## Deploy Commands

```powershell
# Production deploy
vercel --prod

# Preview deploy
vercel

# Deploy pre-built output
vercel build
vercel deploy --prebuilt --prod
```

## Key Facts

- Free tier: 100GB bandwidth/month, unlimited deploys
- Auto-detects Vite, Next.js, SvelteKit, Remix, Astro
- Each deploy gets unique URL: `https://{project}-{hash}-{org}.vercel.app`
- Production URL: `https://{project}.vercel.app`
- No `vercel.json` needed for standard frameworks (zero-config)
