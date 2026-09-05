# Vercel Uninstall

## Remove CLI

```powershell
npm uninstall -g vercel
```

## Remove Auth

```powershell
vercel logout
```

## Unlink Project

Delete `.vercel/` folder from project root.

## Delete Project (destructive)

```powershell
vercel project rm PROJECT_NAME
```
