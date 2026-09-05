# IndexNow Setup

## Prerequisites

- A live website accessible via HTTPS
- Ability to place a text file at domain root (e.g., Astro `/public/` folder)

## Authentication

IndexNow uses key file verification (no dashboard, no OAuth):

1. Generate key: 8-128 chars, alphanumeric + dash only
2. Create file `{key}.txt` containing just the key string
3. Place at domain root: `https://yourdomain.com/{key}.txt`
4. Include key in API requests

## Step-by-Step

### 1. Generate Key

PowerShell:
```powershell
$key = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object { [char]$_ })
Write-Host "IndexNow Key: $key"
Write-Host "File to create: $key.txt (content = $key)"
```

Or use: https://www.indexnow.org (generates key on page refresh)

### 2. Place Key File

For Astro on Netlify:
```
project-root/
  public/
    {key}.txt    <- contains just the key string
```

The file deploys to `https://yourdomain.com/{key}.txt` automatically.

### 3. Store Key

Add to project NOTES.md or environment:
```
INDEXNOW_KEY=your_generated_key
INDEXNOW_HOST=yourdomain.com
```

### 4. Verify

```powershell
$key = "your_generated_key"
$host = "yourdomain.com"
Invoke-WebRequest -Uri "https://$host/$key.txt" | Select-Object -ExpandProperty Content
```

Expected: Returns the key string. If 404, file not deployed yet.

## Submit URLs

### Single URL (GET)
```
GET https://api.indexnow.org/indexnow?url=https://yourdomain.com/blog/new-post&key=YOUR_KEY
```

### Batch (POST, up to 10,000)
```
POST https://api.indexnow.org/IndexNow
Content-Type: application/json

{
  "host": "yourdomain.com",
  "key": "YOUR_KEY",
  "keyLocation": "https://yourdomain.com/YOUR_KEY.txt",
  "urlList": [
    "https://yourdomain.com/blog/post-1",
    "https://yourdomain.com/blog/post-2"
  ]
}
```

### Response Codes
- 200 - OK, URLs submitted
- 202 - Key pending verification (retry in a few minutes)
- 422 - Invalid key or URL format
- 403 - Key file not accessible

## Key Facts

- Free, unlimited (10,000 URLs per request)
- Covers: Bing, Yandex, Seznam, Naver
- Does NOT cover Google (use Google Indexing API separately)
- One submission propagates to ALL participating engines
- Key file must be HTTPS-accessible
- Key file name = key value + ".txt"
- No account, no dashboard, no signup required
