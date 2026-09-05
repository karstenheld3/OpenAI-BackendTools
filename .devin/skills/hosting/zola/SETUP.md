# Zola Setup

Zola is a static site generator (build tool). It outputs to `public/` which is then deployed via a hosting platform (Netlify, Vercel, Cloudflare Pages).

## Prerequisites

- Windows 10/11

## Install

### Via Scoop (recommended)

```powershell
scoop install zola
```

### Via Chocolatey

```powershell
choco install zola
```

### Manual Download

Download from https://github.com/getzola/zola/releases and add to PATH.

Verify: `zola --version`

## Build Command

```powershell
# Standard build (output: public/)
zola build

# Preview build with custom base URL
zola build --base-url $DEPLOY_URL

# Dev server with live reload
zola serve
```

## Integration with Hosting Platforms

Zola is a build tool, not a host. Deploy via:

- **Netlify**: Set `ZOLA_VERSION` env var, `command = "zola build"`, `publish = "public"`
- **Vercel**: Select "Zola" framework preset, set `ZOLA_VERSION` env var
- **Cloudflare Pages**: Select "Zola" framework preset, set `ZOLA_VERSION` env var

See `netlify/` or `vercel/` subfolders for host-specific deploy scripts.

## Key Facts

- Output directory: `public/` (configurable via `output_dir` in `config.toml`)
- Single binary, no runtime dependencies
- Supports Sass/SCSS compilation built-in
- Image processing (resize, crop) built-in
- Search index generation built-in
