---
name: youtube-downloader
description: Download YouTube content as MP3 or video, extract metadata, apply ID3v2.3 tags. Use when downloading YouTube videos/playlists/channels or tagging MP3 files with YouTube metadata.
compatibility: Windows, PowerShell 5.1+, auto-downloads yt-dlp and ffmpeg. Python with mutagen required for ID3v2.3 tag writing.
---

# YouTube Downloader Skill

Download YouTube content as MP3 audio or video using yt-dlp with PowerShell scripts.

## MUST-NOT-FORGET

1. Tag writer uses Python/mutagen directly (no ffmpeg tagging). PowerShell wrapper delegates to `set_mp3_tags_from_youtube_metadata.py`
2. mutagen `save(v2_version=3)` silently converts TYER back to TDRC unless `update_to_v23()` is called first
3. Agent must enrich JSON `mp3_*` fields (title, artist, year, encoded_by, filename) before running tag writer
4. JSON files may have Byte Order Mark (BOM) from PowerShell; Python reads with `utf-8-sig` encoding

## Intent Lookup

- **Download MP3** → MP3 Download section (full workflow: metadata + download + enrich + tag)
- **Download MP3 without tags** → MP3 Download section, "Download Only" subsection
- **Download video** → Video Download section
- **Tag MP3 files** → MP3 Download section, tag writer subsections
- **Extract metadata only** → MP3 Download section, Download-Youtube-Metadata.ps1 subsection

## Prerequisites

- PowerShell 5.1+ (tested on 5.1.26100 and 7.5.4)
- Internet connection (auto-downloads yt-dlp and ffmpeg)
- Python with mutagen package (required for ID3v2.3 tag writing via `set_mp3_tags_from_youtube_metadata.py`)
- Windows Terminal (optional, for parallel tab support)

## Scripts

- **Download-Youtube-To-Mp3.ps1** - Extract audio as MP3
- **Download-Youtube-To-Video.ps1** - Download video files
- **Download-Youtube-Metadata.ps1** - Extract metadata from videos/playlists/channels to JSON
- **set_mp3_tags_from_youtube_metadata.py** - Write ID3v2.3 tags to MP3 files via mutagen (default)
- **Set-Mp3-Tags-From-Youtube-Metadata.ps1** - PowerShell wrapper, fallback if calling Python directly is not possible

## MP3 Download

Default workflow: download MP3s with YouTube metadata as ID3v2.3 tags.

### Workflow

```
Step 1: Download-Youtube-Metadata.ps1  -> JSON with video metadata
Step 2: Download-Youtube-To-Mp3.ps1    -> MP3 files (named as [youtube_id].mp3)
Step 3: Agent enriches JSON with mp3_* fields (title, artist, year, encoded_by, filename)
Step 4: set_mp3_tags_from_youtube_metadata.py  -> Tagged and renamed MP3 files
```

### Enrichment Rules (Step 3)

- **mp3_title**: Work title only (e.g., "In den Mauern von Eryx"), never "Author: Title". The author belongs in `mp3_artist`, not duplicated in the title.
- **mp3_artist**: Author or performer name
- **mp3_year**: Year from `published_date` (4-digit)
- **mp3_encoded_by**: Channel or producer + "/ yt-dlp"
- **mp3_filename**: Target filename following session naming convention

### Download Only (Without Tags)

```powershell
# Single URL
.\Download-Youtube-To-Mp3.ps1 -Urls "https://www.youtube.com/watch?v=VIDEO_ID"

# High quality
.\Download-Youtube-To-Mp3.ps1 -Urls "https://youtu.be/abc" -Quality 320k

# Playlist
.\Download-Youtube-To-Mp3.ps1 -Urls "https://youtube.com/watch?v=abc&list=RDxxx" -Playlist
```

### Download-Youtube-To-Mp3.ps1 Parameters

- **-Urls** (required) - YouTube URLs
- **-OutputFolder** - Default: `[WORKSPACE]/../.tools/_downloaded_audio`
- **-Quality** - `128k`, `192k`, `256k`, `320k` (default: `192k`)
- **-Playlist** - Download entire playlist (switch)
- **-UseCookies** - Use Chrome cookies (default: `$true`)
- **-ChromeProfile** - Chrome profile name (auto-detected)
- **-ToolsFolder** - Binaries location (default: `[WORKSPACE]/../.tools/youtube-downloader`)

### Download-Youtube-Metadata.ps1

Extracts metadata from YouTube videos, playlists, or channels via `yt-dlp --dump-json`.

```powershell
# Single video
.\Download-Youtube-Metadata.ps1 -Urls "https://www.youtube.com/watch?v=VIDEO_ID" -Topic "MyTopic" -OutputFolder "D:\downloads"

# Channel (all videos)
.\Download-Youtube-Metadata.ps1 -Urls "https://www.youtube.com/@channelname" -Topic "ChannelDump" -OutputFolder "D:\downloads" -Force
```

**Parameters:**
- **-Urls** (required) - YouTube URLs (video, playlist, or channel)
- **-Topic** (required) - Topic name for JSON filename
- **-OutputFolder** (required) - Output directory for JSON file
- **-ToolsFolder** - yt-dlp location (default: `[WORKSPACE]/../.tools/youtube-downloader`)
- **-Force** - Overwrite existing JSON (switch)

**Output:** `.tmp_[TOPIC]_youtube-metadata.json` with `videos` array containing `youtube_id`, `title`, `url`, `description`, `published_date`, `download_filename`, and empty `mp3_*` fields (`mp3_title`, `mp3_artist`, `mp3_year`, `mp3_encoded_by`, `mp3_filename`).

### set_mp3_tags_from_youtube_metadata.py (Default Tag Writer)

Writes ID3v2.3 tags to MP3 files via mutagen. Renames files from `[youtube_id].mp3` to `[mp3_filename]`. Preserves file timestamps.

```powershell
# Apply tags
python set_mp3_tags_from_youtube_metadata.py "D:\downloads\.tmp_MyTopic_youtube-metadata.json" "D:\downloads"

# Preview without changes
python set_mp3_tags_from_youtube_metadata.py "D:\downloads\.tmp_MyTopic_youtube-metadata.json" "D:\downloads" --dry-run
```

**Arguments:**
- **json_path** (required) - Path to enriched JSON file
- **mp3_folder** (required) - Folder containing MP3 files
- **--dry-run** - Preview operations without modifying files

**Exit codes:** 0 = all OK, 1 = partial failure, 2 = fatal error

**Tags written:** title (`TIT2`), artist (`TPE1`), year (`TYER`), encoded_by (`TENC`), comment (`COMM` from `description` + `url`), URL (`WXXX` from `url`). All frames written directly by mutagen as correct ID3v2.3 types.

### Set-Mp3-Tags-From-Youtube-Metadata.ps1 (Fallback Tag Writer)

PowerShell wrapper that calls the Python script. Use when calling Python directly is not possible.

```powershell
.\Set-Mp3-Tags-From-Youtube-Metadata.ps1 -JsonPath "D:\downloads\.tmp_MyTopic_youtube-metadata.json" -Mp3Folder "D:\downloads"
.\Set-Mp3-Tags-From-Youtube-Metadata.ps1 -JsonPath "D:\downloads\.tmp_MyTopic_youtube-metadata.json" -Mp3Folder "D:\downloads" -DryRun
```

## Video Download

```powershell
# Best quality
.\Download-Youtube-To-Video.ps1 -Urls "https://www.youtube.com/watch?v=VIDEO_ID"

# Specific format and quality
.\Download-Youtube-To-Video.ps1 -Urls "https://youtu.be/abc" -Format mp4 -Quality 1080p

# Playlist
.\Download-Youtube-To-Video.ps1 -Urls "https://youtube.com/watch?v=abc&list=RDxxx" -Playlist
```

### Video Parameters

- **-Urls** (required) - YouTube URLs
- **-OutputFolder** - Default: `[WORKSPACE]/../.tools/_downloaded_video`
- **-Format** - `best`, `mp4`, `webm`, `mkv` (default: `best`)
- **-Quality** - `best`, `1080p`, `720p`, `480p`, `360p` (default: `best`)
- **-Playlist** - Download entire playlist (switch)
- **-UseCookies** - Use Chrome cookies (default: `$true`)
- **-ChromeProfile** - Chrome profile name (auto-detected)
- **-ToolsFolder** - Binaries location (default: `[WORKSPACE]/../.tools/youtube-downloader`)

## Shared Features

Download scripts (`Download-Youtube-To-Mp3.ps1`, `Download-Youtube-To-Video.ps1`) share:
- Auto-download yt-dlp and ffmpeg if missing
- yt-dlp version checking and auto-update
- Chrome cookie auto-detection for age-restricted content
- DPAPI error fallback (retries without cookies)
- Pipeline input support
- Playlist support

## Parallel Downloads (Cascade)

When user provides multiple URLs, Cascade spawns multiple terminals:
- 2 URLs → 2 terminals
- 10 URLs → 10 terminals
- 50 URLs → 10 terminals (max), 5 URLs each

Cascade splits URLs and runs non-blocking commands with `-UseCookies $false`.

## Output Locations

- **Audio**: `[WORKSPACE]/../.tools/_downloaded_audio/`
- **Video**: `[WORKSPACE]/../.tools/_downloaded_video/`
- **Binaries**: `[WORKSPACE]/../.tools/youtube-downloader/`

## Gotchas

- **mutagen TYER corruption**: `save(v2_version=3)` silently converts TYER back to TDRC. Must call `update_to_v23()` before `save()` to produce correct TYER frame on disk.
- **mutagen mtime modification**: `save()` updates file mtime. Script saves mtime before write and restores with `os.utime()` after.
- **Chrome cookies + DPAPI**: Cookie extraction fails while Chrome is running. Scripts auto-retry without cookies on DPAPI error.
- **yt-dlp JS runtime**: Without a JavaScript runtime (deno/node), many videos return "This video is not available". Workaround: `--extractor-args "youtube:player_client=android"` (limits format selection to 360p).
- **JSON BOM from PowerShell**: Metadata JSON files may contain Byte Order Mark. Python script reads with `utf-8-sig` encoding for tolerance.

## References

- `Download-Youtube-To-Mp3.ps1` - MP3 audio download script
- `Download-Youtube-To-Video.ps1` - Video download script
- `Download-Youtube-Metadata.ps1` - Metadata extraction to JSON
- `set_mp3_tags_from_youtube_metadata.py` - ID3v2.3 tag writer using mutagen (default)
- `Set-Mp3-Tags-From-Youtube-Metadata.ps1` - PowerShell wrapper (fallback)
