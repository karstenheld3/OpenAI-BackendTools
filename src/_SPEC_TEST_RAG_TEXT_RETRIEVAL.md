# SPEC: RAG Text Retrieval

**Doc ID**: RAGTR-SP01
**Goal**: Retrieve embedded file chunks from vector stores and reconstruct original text content
**Timeline**: Created 2026-02-02, Updated 1 time
**Target file**: `src/test_rag_text_retrieval.py`

**Depends on:**
- `src/openai_backendtools.py` for `get_vector_store_file_content()`, `get_all_vector_store_file_contents()`

## MUST-NOT-FORGET

- Chunks have TOKEN-based overlap, not character-based
- First file pair determines overlap pattern for entire vector store (same chunking strategy)
- Overlap detection uses longest-suffix-prefix matching algorithm
- Output files preserve original filename with `.reconstructed.md` suffix

## Table of Contents

1. [Scenario](#1-scenario)
2. [Context](#2-context)
3. [Domain Objects](#3-domain-objects)
4. [Functional Requirements](#4-functional-requirements)
5. [Design Decisions](#5-design-decisions)
6. [Implementation Guarantees](#6-implementation-guarantees)
7. [Key Mechanisms](#7-key-mechanisms)
8. [Action Flow](#8-action-flow)
9. [Data Structures](#9-data-structures)
10. [Implementation Details](#10-implementation-details)
11. [Document History](#11-document-history)

## 1. Scenario

**Problem:** Files embedded in OpenAI vector stores are chunked and cannot be directly downloaded. Users need to recover original text content for backup, migration, or verification purposes.

**Solution:**
- Retrieve all chunks for each file via `vector_stores.files.content()` API
- Detect overlap between consecutive chunks using suffix-prefix matching
- Stitch chunks together by removing duplicate overlap regions
- Output reconstructed markdown files

**What we don't want:**
- Naive concatenation that duplicates overlap regions
- Character-based overlap assumptions (OpenAI uses tokens)
- Per-chunk overlap calculation (wasteful - use first pair to calibrate)

## 2. Context

OpenAI vector stores chunk files using configurable `max_chunk_size_tokens` and `chunk_overlap_tokens`. The overlap ensures semantic continuity but means consecutive chunks share content. This spec defines how to reverse the chunking process.

Existing infrastructure in `openai_backendtools.py`:
- `get_vector_store_file_content(client, vs_id, file_id)` - Returns list of chunk objects
- `get_all_vector_store_file_contents(client, vs_id)` - Returns `[{"file": file_obj, "chunks": [...]}, ...]`

## 3. Domain Objects

### RAGTextRetrievalParams

Configuration dataclass for the retrieval script.

**Properties:**
- `vector_store_id` - str, required. Target vector store ID
- `only_these_filenames` - list[str], optional. Filter to specific filenames (empty = all files)
- `output_folder` - str, default "./output". Destination for reconstructed files
- `output_suffix` - str, default ".reconstructed.md". Appended to original filename
- `log_headers` - bool, default True. Enable function header/footer logging

### ChunkOverlapInfo

Result of overlap detection between two consecutive chunks.

**Properties:**
- `overlap_chars` - int. Detected character overlap length
- `confidence` - str. "exact" (suffix matches prefix exactly), "normalized" (whitespace-normalized match), or "none"
- `detection_method` - str. Algorithm used: "suffix_prefix_match"

## 4. Functional Requirements

**RAGTR-FR-01: Chunk Retrieval**
- Retrieve all chunks for specified files from vector store
- Support filtering by filename list (empty list = all files)
- Handle pagination via existing `get_vector_store_file_content()` function

**RAGTR-FR-02: Overlap Detection**
- Analyze first two chunks of first multi-chunk file to detect overlap pattern
- If no multi-chunk file exists, skip overlap detection (overlap_chars=0)
- Use longest-suffix-prefix matching algorithm
- Cache detected overlap for remaining chunks (same chunking strategy applies)

**RAGTR-FR-03: Chunk Stitching**
- Concatenate chunks by removing detected overlap from each subsequent chunk
- Handle edge cases: single chunk files, empty chunks, no overlap found

**RAGTR-FR-04: File Output**
- Write reconstructed content to `{output_folder}/{original_filename}{output_suffix}`
- Create output folder if not exists
- Log progress: files processed, chunks stitched, bytes written

**RAGTR-FR-05: Filename Filtering**
- If `only_these_filenames` is non-empty, process only matching files
- Match against file attributes: `filename` or fallback to file ID

## 5. Design Decisions

**RAGTR-DD-01:** Detect overlap once using first file's first two chunks. Rationale: All files in a vector store use the same chunking strategy, so overlap pattern is consistent. [ASSUMED]

**RAGTR-DD-02:** Use suffix-prefix matching for overlap detection. Rationale: Token boundaries don't align with character boundaries, but the actual text content overlaps exactly.

**RAGTR-DD-03:** Output as `.reconstructed.md` regardless of original format. Rationale: Chunking process extracts text only; original formatting (PDF, DOCX) is lost.

**RAGTR-DD-04:** Fail gracefully on overlap detection failure. Rationale: If no overlap found, concatenate with newline separator and log warning.

## 6. Implementation Guarantees

**RAGTR-IG-01:** Script handles vector stores with 0, 1, or many files without error.

**RAGTR-IG-02:** Script handles files with 0, 1, or many chunks without error.

**RAGTR-IG-03:** Output folder is created if it does not exist.

**RAGTR-IG-04:** Existing output files are overwritten without prompt.

**RAGTR-IG-05:** If all files have only 1 chunk, overlap detection is skipped and chunks are output as-is.

## 7. Key Mechanisms

### Overlap Detection Algorithm

**Problem:** Find the overlap length between consecutive chunks where chunk N's end matches chunk N+1's beginning.

**Algorithm: Longest Suffix-Prefix Match**

```
function detect_overlap(chunk_a_text, chunk_b_text):
    # Start with maximum possible overlap (smaller of the two chunks)
    max_check = min(len(chunk_a_text), len(chunk_b_text))
    
    # Try decreasing overlap sizes until match found
    for overlap_len in range(max_check, 0, -1):
        suffix_a = chunk_a_text[-overlap_len:]
        prefix_b = chunk_b_text[:overlap_len]
        if suffix_a == prefix_b:
            return ChunkOverlapInfo(overlap_chars=overlap_len, confidence="exact")
    
    # No exact match found
    return ChunkOverlapInfo(overlap_chars=0, confidence="none")
```

**Optimization:** Instead of checking every length, use binary search or step by word boundaries:

```
function detect_overlap_optimized(chunk_a_text, chunk_b_text):
    # Step 1: Find candidate overlap regions by searching for chunk_b's first N chars in chunk_a's tail
    search_prefix = chunk_b_text[:100]  # First 100 chars of chunk B
    search_region = chunk_a_text[-2000:]  # Last 2000 chars of chunk A (generous buffer)
    
    idx = search_region.rfind(search_prefix)
    if idx == -1:
        return ChunkOverlapInfo(overlap_chars=0, confidence="none")
    
    # Step 2: Refine by extending match forward
    candidate_overlap = len(search_region) - idx
    suffix_a = chunk_a_text[-candidate_overlap:]
    prefix_b = chunk_b_text[:candidate_overlap]
    
    if suffix_a == prefix_b:
        return ChunkOverlapInfo(overlap_chars=candidate_overlap, confidence="exact")
    
    # Step 3: Binary search refinement if partial match
    # ... (fallback to linear search in overlap region)
```

### Stitching Algorithm

```
function stitch_chunks(chunks, overlap_chars):
    if len(chunks) == 0: return ""
    if len(chunks) == 1: return chunks[0].text
    
    result = chunks[0].text
    for i in range(1, len(chunks)):
        chunk_text = chunks[i].text
        if overlap_chars > 0 and len(chunk_text) > overlap_chars:
            result += chunk_text[overlap_chars:]
        else:
            result += "\n" + chunk_text  # Fallback: newline separator
    return result
```

## 8. Action Flow

```
User runs test_rag_text_retrieval.py
├─> Load RAGTextRetrievalParams from script config
├─> Create OpenAI client (openai or azure_openai)
├─> retrieve_and_reconstruct_files(client, params)
│   ├─> Get all files from vector store
│   │   └─> get_all_vector_store_file_contents(client, vs_id)
│   ├─> Filter files by only_these_filenames (if specified)
│   ├─> Find first file with 2+ chunks for overlap detection
│   │   ├─> If found: detect_chunk_overlap(chunk_0, chunk_1)
│   │   └─> If not found: use overlap_chars=0 (no overlap removal)
│   │       └─> Return ChunkOverlapInfo
│   ├─> For each file:
│   │   ├─> stitch_chunks(file.chunks, overlap_info.overlap_chars)
│   │   ├─> Write to output_folder/filename.reconstructed.md
│   │   └─> Log: "Reconstructed {filename}: {chunk_count} chunks -> {bytes} bytes"
│   └─> Return summary: files_processed, total_chunks, total_bytes
└─> Print completion summary
```

## 9. Data Structures

### RAGTextRetrievalParams

```python
@dataclass
class RAGTextRetrievalParams:
    vector_store_id: str
    only_these_filenames: list = field(default_factory=list)
    output_folder: str = "./output"
    output_suffix: str = ".reconstructed.md"
    log_headers: bool = True
```

### ChunkOverlapInfo

```python
@dataclass
class ChunkOverlapInfo:
    overlap_chars: int
    confidence: str  # "exact", "normalized", "none"
    detection_method: str = "suffix_prefix_match"
```

### Function Return: ReconstructionResult

```python
@dataclass
class ReconstructionResult:
    filename: str
    original_file_id: str
    chunk_count: int
    reconstructed_bytes: int
    output_path: str
```

## 10. Implementation Details

### File: `test_rag_text_retrieval.py`

**Imports:**
```python
from dataclasses import dataclass, field
from dotenv import load_dotenv
from openai_backendtools import *
import os
```

**Functions:**

- `detect_chunk_overlap(chunk_a_text: str, chunk_b_text: str) -> ChunkOverlapInfo`
  - Implements suffix-prefix matching algorithm
  - Returns overlap info with confidence level

- `stitch_chunks(chunks: list, overlap_chars: int) -> str`
  - Concatenates chunks removing overlap
  - Returns reconstructed text

- `get_filename_from_file(file_obj) -> str`
  - Extracts filename from file object attributes
  - Fallback to file ID if no filename attribute

- `retrieve_and_reconstruct_files(client, params: RAGTextRetrievalParams) -> list[ReconstructionResult]`
  - Main orchestration function
  - Returns list of reconstruction results

**Main block:**
```python
if __name__ == '__main__':
    # Client setup (same pattern as test_rag_operations.py)
    # RAGTextRetrievalParams configuration
    # Call retrieve_and_reconstruct_files()
    # Print summary
```

### Console Output Format

```
[2026-02-02 10:30:00] START: Retrieve and reconstruct files from vector store...
  Vector store: vs_abc123
  Detecting overlap from first file...
    Overlap detected: 1847 chars (confidence: exact)
  Processing 3 files...
    [ 1 / 3 ] document1.pdf: 12 chunks -> 45,230 bytes -> ./output/document1.pdf.reconstructed.md
    [ 2 / 3 ] notes.md: 3 chunks -> 8,102 bytes -> ./output/notes.md.reconstructed.md
    [ 3 / 3 ] report.docx: 8 chunks -> 31,455 bytes -> ./output/report.docx.reconstructed.md
[2026-02-02 10:30:05] END: Retrieve and reconstruct files from vector store (5 secs).
  Summary: 3 files, 23 chunks, 84,787 bytes reconstructed
```

## 11. Document History

**[2026-02-02 10:54]**
- Synced ChunkOverlapInfo.confidence values: "approximate" -> "normalized" (matches implementation)

**[2026-02-02 10:30]**
- Initial specification created
