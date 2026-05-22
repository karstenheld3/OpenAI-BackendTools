#!/usr/bin/env python3
"""
set_mp3_tags_from_youtube_metadata.py - Write ID3v2.3 tags to MP3 files from enriched YouTube metadata JSON.

Usage:
  python set_mp3_tags_from_youtube_metadata.py <json_path> <mp3_folder> [--dry-run]

Exit codes: 0 = all OK, 1 = partial failure, 2 = fatal error
"""

import os, sys, json, argparse
from pathlib import Path
from datetime import datetime

from mutagen.id3 import ID3, TIT2, TPE1, TENC, TDRC, COMM, WXXX, ID3NoHeaderError

# ----------------------------------------- START: Tag Writing -----------------------------------------------------------

# Write ID3v2.3 tags to mp3_path using fields from video dict. Preserves file mtime.
def write_tags(mp3_path: Path, video: dict) -> None:
  try:
    tags = ID3(str(mp3_path))
  except ID3NoHeaderError:
    tags = ID3()

  tags.delall("TIT2"); tags.delall("TPE1"); tags.delall("TENC")
  tags.delall("COMM"); tags.delall("WXXX")
  tags.delall("TXXX:comment")  # Remove ffmpeg leftover if re-tagging

  tags.add(TIT2(encoding=3, text=[video["mp3_title"]]))
  tags.add(TPE1(encoding=3, text=[video["mp3_artist"]]))
  tags.add(TENC(encoding=3, text=[video["mp3_encoded_by"]]))

  # Comment: description + newline + url (encoding=3 = UTF-8)
  comment_text = video.get("description", "")
  url = video.get("url", "")
  if url:
    comment_text = f"{comment_text}\n{url}" if comment_text else url
  tags.add(COMM(encoding=3, lang="deu", desc="", text=comment_text))

  if url:
    tags.add(WXXX(encoding=3, desc="", url=url))

  # Year: set TDRC then update_to_v23() to produce correct TYER frame on disk
  year = video.get("mp3_year", "")
  if year:
    tags.delall("TDRC"); tags.delall("TYER")
    tags.add(TDRC(encoding=3, text=[str(year)]))

  tags.update_to_v23()
  mtime = mp3_path.stat().st_mtime
  tags.save(str(mp3_path), v2_version=3)
  os.utime(mp3_path, (mp3_path.stat().st_atime, mtime))

# ----------------------------------------- END: Tag Writing -------------------------------------------------------------


# ----------------------------------------- START: Source File Lookup -----------------------------------------------------

# Three-try source lookup: orphaned temp -> [youtube_id].mp3 -> [mp3_filename]. Returns (path, status).
def find_source_file(mp3_folder: Path, youtube_id: str, mp3_filename: str) -> tuple:
  target_path = mp3_folder / mp3_filename
  temp_path = mp3_folder / f"{mp3_filename}_"
  id_path = mp3_folder / f"{youtube_id}.mp3"

  # First try: orphaned temp file from interrupted run
  if temp_path.exists() and not id_path.exists() and not target_path.exists():
    return temp_path, 'resumed'

  # Second try: [youtube_id].mp3
  if id_path.exists():
    return id_path, 'found'

  # Third try: already renamed to mp3_filename
  if target_path.exists():
    return target_path, 'found'

  return None, 'not_found'

# ----------------------------------------- END: Source File Lookup -------------------------------------------------------


# ----------------------------------------- START: Helpers ---------------------------------------------------------------

def format_size_mb(size_bytes: int) -> str:
  return f"{size_bytes / (1024 * 1024):.1f}"

def format_duration(seconds: float) -> str:
  if seconds < 60: return f"{seconds:.1f} secs"
  minutes = int(seconds // 60)
  secs = int(seconds % 60)
  if minutes < 60: return f"{minutes} mins {secs} secs"
  hours = int(minutes // 60)
  mins = minutes % 60
  return f"{hours} hours {mins} mins"

# ----------------------------------------- END: Helpers -----------------------------------------------------------------


# ----------------------------------------- START: Main ------------------------------------------------------------------

def parse_args():
  parser = argparse.ArgumentParser(description='Write ID3v2.3 tags to MP3 files from enriched YouTube metadata JSON.')
  parser.add_argument('json_path', type=Path, help='Path to enriched .tmp_[TOPIC]_youtube-metadata.json file')
  parser.add_argument('mp3_folder', type=Path, help='Folder containing MP3 files')
  parser.add_argument('--dry-run', action='store_true', help='Show planned operations without modifying files')
  return parser.parse_args()

def main():
  args = parse_args()
  json_path = args.json_path
  mp3_folder = args.mp3_folder
  dry_run = args.dry_run

  # Validate inputs
  if not json_path.exists():
    print(f"ERROR: JSON file not found: '{json_path}'.", file=sys.stderr)
    sys.exit(2)
  if not mp3_folder.exists():
    print(f"ERROR: MP3 folder not found: '{mp3_folder}'.", file=sys.stderr)
    sys.exit(2)

  # Parse JSON (utf-8-sig for Byte Order Mark tolerance)
  try:
    with open(json_path, 'r', encoding='utf-8-sig') as f:
      json_data = json.load(f)
  except Exception as e:
    print(f"ERROR: Failed to parse JSON '{json_path}' -> {e}", file=sys.stderr)
    sys.exit(2)

  videos = json_data.get("videos", [])
  if not videos:
    print("ERROR: No video entries in JSON file.", file=sys.stderr)
    sys.exit(2)

  total = len(videos)
  entry_word = "entry" if total == 1 else "entries"
  tagged = 0
  skipped = 0
  failed = 0
  resumed = 0
  start_time = datetime.now()
  pad = len(str(total))

  # Header
  print()
  print("====================================== START: MP3 TAG WRITER =======================================")
  print(start_time.strftime("%Y-%m-%d %H:%M:%S"))
  print()
  print(f"JSON: '{json_path.name}' ({total} {entry_word})")
  print(f"MP3 Folder: '{mp3_folder}'")
  print("Tool: mutagen (ID3v2.3)")
  if dry_run:
    print("Mode: DRY RUN (no files modified)")
  print()

  for index, video in enumerate(videos, 1):
    mp3_filename = video.get("mp3_filename", "")
    if not mp3_filename:
      skipped += 1
      continue

    youtube_id = video.get("youtube_id", "")
    print(f"[ {index:>{pad}} / {total} ] {mp3_filename}")

    # Three-try source lookup
    source_path, status = find_source_file(mp3_folder, youtube_id, mp3_filename)

    if status == 'resumed':
      if dry_run:
        print(f"  [DRY RUN] Would resume: rename '{source_path.name}' -> '{mp3_filename}'.")
        resumed += 1
        continue
      try:
        source_path.rename(mp3_folder / mp3_filename)
        print("  OK. Resumed from interrupted run.")
        resumed += 1
        tagged += 1
        continue
      except Exception as e:
        failed += 1
        print(f"  ERROR: Failed to resume rename -> {e}")
        continue

    if source_path is None:
      skipped += 1
      print(f"  SKIP: Source file not found (tried '{youtube_id}.mp3' and '{mp3_filename}').")
      continue

    source_size_mb = format_size_mb(source_path.stat().st_size)

    if dry_run:
      print(f"  [DRY RUN] Source: '{source_path.name}' ({source_size_mb} MB)")
      print(f"  Title: {video.get('mp3_title', '')}")
      print(f"  Artist: {video.get('mp3_artist', '')} | Year: {video.get('mp3_year', '')}")
      comment_len = len(video.get('description', ''))
      print(f"  Comment: ({comment_len} chars) | URL: {video.get('url', '')}")
      continue

    # Write tags at source path (before rename)
    try:
      write_tags(source_path, video)
    except Exception as e:
      failed += 1
      print(f"  ERROR: Tag writing failed -> {e}")
      continue

    # Rename to mp3_filename (if source != target, after successful tag write)
    target_path = mp3_folder / mp3_filename
    source_label = source_path.name
    needs_rename = source_path != target_path

    if needs_rename:
      try:
        source_path.rename(target_path)
      except Exception as e:
        failed += 1
        print(f"  ERROR: Failed to rename -> {e}")
        continue

    # Log success
    if needs_rename:
      print(f"  Source: '{source_label}' ({source_size_mb} MB) -> Tagged: '{mp3_filename}'. OK.")
    else:
      print(f"  Source: '{source_label}' ({source_size_mb} MB) -> Tagged. OK.")
    tagged += 1

  # Summary
  print()
  print(f"Tagged: {tagged}.")
  if resumed > 0: print(f"Resumed: {resumed}.")
  if skipped > 0: print(f"Skipped: {skipped}.")
  if failed > 0:
    print(f"Failed: {failed}.")
    print(f"PARTIAL FAIL: {tagged} tagged, {failed} failed.")
  else:
    print("OK.")

  # Footer
  elapsed = (datetime.now() - start_time).total_seconds()
  print()
  print("======================================== END: MP3 TAG WRITER =======================================")
  print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ({format_duration(elapsed)})")

  if failed > 0: sys.exit(1)
  sys.exit(0)

# ----------------------------------------- END: Main --------------------------------------------------------------------

if __name__ == '__main__':
  main()
