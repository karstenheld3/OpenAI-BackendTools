# Netlify Uninstall

## Remove CLI

```powershell
npm uninstall -g netlify-cli
```

## Remove Auth Token

```powershell
netlify logout
```

Or manually delete `~/.netlify/config.json`.

## Unlink Project

```powershell
netlify unlink
```

Removes `.netlify/state.json` from project.

## Delete Site (destructive)

```powershell
netlify sites:delete --site-id SITE_ID
```
