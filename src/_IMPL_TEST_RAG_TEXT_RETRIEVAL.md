# IMPL: RAG Text Retrieval

**Doc ID**: RAGTR-IP01
**Feature**: RAG_TEXT_RETRIEVAL
**Goal**: Implement chunk retrieval and text reconstruction from OpenAI vector stores
**Timeline**: Created 2026-02-02, Updated 0 times

**Target files**:
- `src/test_rag_text_retrieval.py` (NEW ~300 lines)

**Depends on:**
- `_SPEC_TEST_RAG_TEXT_RETRIEVAL.md` [RAGTR-SP01] for requirements and algorithm design
- `src/openai_backendtools.py` for `get_vector_store_file_content()`, `get_all_vector_store_file_contents()`

## MUST-NOT-FORGET

- Overlap is TOKEN-based, detection is CHARACTER-based (approximation)
- Search region must be 8000+ chars to handle max overlap (2048 tokens)
- Whitespace-normalized fallback required for PDF extraction quirks
- Chunk ordering assumed to match document order (verify empirically)

## Table of Contents

1. [File Structure](#1-file-structure)
2. [Edge Cases](#2-edge-cases)
3. [Implementation Steps](#3-implementation-steps)
4. [Test Cases](#4-test-cases)
5. [Verification Checklist](#5-verification-checklist)
6. [Document History](#6-document-history)

## 1. File Structure

```
src/
└── test_rag_text_retrieval.py  # Main script (~300 lines) [NEW]
    ├── Data Classes (3)
    │   ├── RAGTextRetrievalParams
    │   ├── ChunkOverlapInfo
    │   └── ReconstructionResult
    ├── Overlap Detection (2)
    │   ├── normalize_whitespace()
    │   └── detect_chunk_overlap()
    ├── Chunk Stitching (2)
    │   ├── stitch_chunks()
    │   └── get_filename_from_file()
    └── Main Functions (1)
        └── retrieve_and_reconstruct_files()
```

## 2. Edge Cases

### Input Boundaries

- **RAGTR-IP01-EC-01**: Empty vector store (0 files) -> Return empty list, log "No files to process"
- **RAGTR-IP01-EC-02**: File with 0 chunks -> Skip file, continue processing others
- **RAGTR-IP01-EC-03**: File with 1 chunk -> Output as-is, no overlap detection needed
- **RAGTR-IP01-EC-04**: All files have 1 chunk -> Skip overlap detection entirely, output_chars=0

### Overlap Detection

- **RAGTR-IP01-EC-05**: No exact overlap match found -> Try whitespace-normalized fallback
- **RAGTR-IP01-EC-06**: Normalized match fails too -> Use overlap_chars=0, concatenate with newline
- **RAGTR-IP01-EC-07**: Chunk shorter than detected overlap -> Use fallback (newline separator)
- **RAGTR-IP01-EC-08**: Empty chunk text -> Skip chunk, continue stitching

### File Handling

- **RAGTR-IP01-EC-09**: Output folder doesn't exist -> Create it with `os.makedirs()`
- **RAGTR-IP01-EC-10**: Output file already exists -> Overwrite without prompt (per RAGTR-IG-04)
- **RAGTR-IP01-EC-11**: Filename attribute missing -> Fallback to file ID
- **RAGTR-IP01-EC-12**: File ID also missing -> Use `[UNKNOWN]` placeholder

### Filtering

- **RAGTR-IP01-EC-13**: `only_these_filenames` filter matches no files -> Return empty list, log warning

## 3. Implementation Steps

### RAGTR-IP01-IS-01: Create Data Classes

**Location**: `test_rag_text_retrieval.py` > top of file after imports

**Action**: Add three dataclasses for configuration and results

**Code**:
```python
@dataclass
class RAGTextRetrievalParams:
  vector_store_id: str
  only_these_filenames: list = field(default_factory=list)
  output_folder: str = "./output"
  output_suffix: str = ".reconstructed.md"
  log_headers: bool = True

@dataclass
class ChunkOverlapInfo:
  overlap_chars: int
  confidence: str  # "exact", "normalized", "none"
  detection_method: str = "suffix_prefix_match"

@dataclass
class ReconstructionResult:
  filename: str
  original_file_id: str
  chunk_count: int
  reconstructed_bytes: int
  output_path: str
```

### RAGTR-IP01-IS-02: Implement Whitespace Normalization

**Location**: `test_rag_text_retrieval.py` > Overlap Detection section

**Action**: Add helper function for whitespace-normalized comparison

**Code**:
```python
# Normalize whitespace for comparison: collapse spaces, normalize line endings
def normalize_whitespace(text):
  if not text: return ""
  text = text.replace('\r\n', '\n').replace('\r', '\n')
  text = re.sub(r'[ \t]+', ' ', text)
  text = re.sub(r'\n+', '\n', text)
  return text.strip()
```

### RAGTR-IP01-IS-03: Implement Overlap Detection

**Location**: `test_rag_text_retrieval.py` > after `normalize_whitespace()`

**Action**: Add main overlap detection function with exact match + normalized fallback

**Code**:
```python
# Detect overlap between consecutive chunks using suffix-prefix matching
# Returns ChunkOverlapInfo with overlap_chars, confidence, detection_method
def detect_chunk_overlap(chunk_a_text, chunk_b_text, max_search_chars=8000):
  # Step 1: Try exact suffix-prefix match
  # Step 2: Try whitespace-normalized fallback
  # Step 3: Return none if both fail
  ...
```

**Note**: Use `rfind()` to locate candidate overlap region, then verify full match.

### RAGTR-IP01-IS-04: Implement Chunk Stitching

**Location**: `test_rag_text_retrieval.py` > Chunk Stitching section

**Action**: Add function to concatenate chunks with overlap removal

**Code**:
```python
# Concatenate chunks by removing detected overlap from each subsequent chunk
def stitch_chunks(chunks, overlap_chars):
  if not chunks: return ""
  result = chunks[0].text
  for i in range(1, len(chunks)):
    chunk_text = chunks[i].text
    if overlap_chars > 0 and len(chunk_text) > overlap_chars:
      result += chunk_text[overlap_chars:]
    else:
      result += "\n" + chunk_text  # Fallback
  return result
```

### RAGTR-IP01-IS-05: Implement Filename Extraction

**Location**: `test_rag_text_retrieval.py` > after `stitch_chunks()`

**Action**: Add helper to extract filename from file object

**Code**:
```python
# Extract filename from file object attributes, fallback to file ID
def get_filename_from_file(file_obj):
  # Try direct filename attribute
  # Try attributes dict
  # Fallback to file ID or UNKNOWN
  ...
```

### RAGTR-IP01-IS-06: Implement Main Orchestration Function

**Location**: `test_rag_text_retrieval.py` > Main Functions section

**Action**: Add main function that ties everything together

**Code**:
```python
def retrieve_and_reconstruct_files(client, params: RAGTextRetrievalParams):
  # Step 1: Get all files and chunks
  # Step 2: Filter by only_these_filenames
  # Step 3: Detect overlap from first multi-chunk file
  # Step 4: Create output folder
  # Step 5: Process each file (stitch + write)
  # Return list of ReconstructionResult
  ...
```

### RAGTR-IP01-IS-07: Implement Main Block

**Location**: `test_rag_text_retrieval.py` > bottom of file

**Action**: Add main block with client setup and example params

**Code**:
```python
if __name__ == '__main__':
  # Client setup (same pattern as test_rag_operations.py)
  # RAGTextRetrievalParams configuration
  # Call retrieve_and_reconstruct_files()
  # Print summary
  ...
```

## 4. Test Cases

### Category 1: Overlap Detection (4 tests)

- **RAGTR-IP01-TC-01**: Exact overlap found -> ok=true, confidence="exact", overlap_chars > 0
- **RAGTR-IP01-TC-02**: Normalized overlap found -> ok=true, confidence="normalized"
- **RAGTR-IP01-TC-03**: No overlap found -> ok=true, confidence="none", overlap_chars=0
- **RAGTR-IP01-TC-04**: Empty input chunks -> ok=true, overlap_chars=0

### Category 2: Chunk Stitching (3 tests)

- **RAGTR-IP01-TC-05**: Multiple chunks with overlap -> ok=true, no duplicated text
- **RAGTR-IP01-TC-06**: Single chunk -> ok=true, output equals input
- **RAGTR-IP01-TC-07**: Chunk shorter than overlap -> ok=true, uses newline fallback

### Category 3: End-to-End (3 tests)

- **RAGTR-IP01-TC-08**: Vector store with multiple files -> ok=true, all files reconstructed
- **RAGTR-IP01-TC-09**: Filename filter matches subset -> ok=true, only filtered files output
- **RAGTR-IP01-TC-10**: Empty vector store -> ok=true, empty results, no error

## 5. Verification Checklist

### Prerequisites

- [x] **RAGTR-IP01-VC-01**: SPEC [RAGTR-SP01] read and understood
- [x] **RAGTR-IP01-VC-02**: Existing `openai_backendtools.py` functions verified

### Implementation

- [x] **RAGTR-IP01-VC-03**: IS-01 completed (data classes)
- [x] **RAGTR-IP01-VC-04**: IS-02 completed (whitespace normalization)
- [x] **RAGTR-IP01-VC-05**: IS-03 completed (overlap detection)
- [x] **RAGTR-IP01-VC-06**: IS-04 completed (chunk stitching)
- [x] **RAGTR-IP01-VC-07**: IS-05 completed (filename extraction)
- [x] **RAGTR-IP01-VC-08**: IS-06 completed (main orchestration)
- [x] **RAGTR-IP01-VC-09**: IS-07 completed (main block)

### Validation

- [ ] **RAGTR-IP01-VC-10**: Syntax check passes (`python -m py_compile`)
- [ ] **RAGTR-IP01-VC-11**: Manual test with real vector store
- [ ] **RAGTR-IP01-VC-12**: Reconstructed text matches original (spot check)

### Code Quality

- [x] **RAGTR-IP01-VC-13**: Follows PYTHON-RULES.md (2-space indent, single-line statements)
- [x] **RAGTR-IP01-VC-14**: Logging follows PYTHON-LG-* rules
- [x] **RAGTR-IP01-VC-15**: Edge cases from EC-* handled

## 6. Document History

**[2026-02-02 10:54]**
- Added EC-10 for RAGTR-IG-04 (overwrite existing files)
- Renumbered EC-11, EC-12, EC-13

**[2026-02-02 10:52]**
- Initial implementation plan created
- Implementation already complete (marked VC items as done)
