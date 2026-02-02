from dataclasses import dataclass, field
from dotenv import load_dotenv
from openai_backendtools import *
import os
import re

load_dotenv()

UNKNOWN = '[UNKNOWN]'

# ----------------------------------------------------- START: Data Classes --------------------------------------------------------

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

# ----------------------------------------------------- END: Data Classes ----------------------------------------------------------


# ----------------------------------------------------- START: Overlap Detection ---------------------------------------------------

# NOTE: Chunk ordering assumption [RAGTR-RV-001]
# This script assumes OpenAI returns chunks in document order. If chunks appear out of order,
# the reconstructed text will be scrambled. Verify with your data if results seem wrong.

# NOTE: Per-file chunking [RAGTR-RV-002]
# If files were added to the vector store with different chunking strategies, the overlap
# detected from the first file may be incorrect for others. Watch for "normalized" confidence.

def normalize_whitespace(text):
  """Normalize whitespace for comparison: collapse multiple spaces, normalize line endings."""
  if not text: return ""
  # Normalize line endings to single newline
  text = text.replace('\r\n', '\n').replace('\r', '\n')
  # Collapse multiple spaces/tabs to single space
  text = re.sub(r'[ \t]+', ' ', text)
  # Collapse multiple newlines to single newline
  text = re.sub(r'\n+', '\n', text)
  return text.strip()

def detect_chunk_overlap(chunk_a_text, chunk_b_text, max_search_chars=8000):
  """
  Detect overlap between two consecutive chunks using suffix-prefix matching.
  Returns ChunkOverlapInfo with overlap_chars, confidence, and detection_method.
  
  Algorithm:
  1. Search for chunk_b's first N chars in chunk_a's tail region
  2. If found, verify the full overlap matches
  3. If exact match fails, try whitespace-normalized matching
  """
  if not chunk_a_text or not chunk_b_text:
    return ChunkOverlapInfo(overlap_chars=0, confidence="none")
  
  # Step 1: Find candidate overlap by searching for chunk_b's prefix in chunk_a's suffix
  search_prefix_len = min(100, len(chunk_b_text))
  search_prefix = chunk_b_text[:search_prefix_len]
  search_region = chunk_a_text[-max_search_chars:] if len(chunk_a_text) > max_search_chars else chunk_a_text
  
  # Try exact match first
  idx = search_region.rfind(search_prefix)
  if idx != -1:
    # Calculate candidate overlap length
    candidate_overlap = len(search_region) - idx
    suffix_a = chunk_a_text[-candidate_overlap:]
    prefix_b = chunk_b_text[:candidate_overlap]
    
    if suffix_a == prefix_b:
      return ChunkOverlapInfo(overlap_chars=candidate_overlap, confidence="exact")
  
  # Step 2: Try whitespace-normalized matching as fallback
  norm_a = normalize_whitespace(chunk_a_text)
  norm_b = normalize_whitespace(chunk_b_text)
  norm_search_prefix = normalize_whitespace(search_prefix)
  norm_search_region = norm_a[-max_search_chars:] if len(norm_a) > max_search_chars else norm_a
  
  idx = norm_search_region.rfind(norm_search_prefix)
  if idx != -1:
    # Found normalized match - now we need to find the corresponding original overlap
    # This is approximate since normalization changes lengths
    candidate_norm_overlap = len(norm_search_region) - idx
    norm_suffix_a = norm_a[-candidate_norm_overlap:]
    norm_prefix_b = norm_b[:candidate_norm_overlap]
    
    if norm_suffix_a == norm_prefix_b:
      # Estimate original character overlap based on ratio
      ratio = len(chunk_b_text) / len(norm_b) if len(norm_b) > 0 else 1.0
      estimated_overlap = int(candidate_norm_overlap * ratio)
      return ChunkOverlapInfo(overlap_chars=estimated_overlap, confidence="normalized")
  
  # No overlap found
  return ChunkOverlapInfo(overlap_chars=0, confidence="none")

# ----------------------------------------------------- END: Overlap Detection -----------------------------------------------------


# ----------------------------------------------------- START: Chunk Stitching -----------------------------------------------------

def stitch_chunks(chunks, overlap_chars):
  """Concatenate chunks by removing detected overlap from each subsequent chunk."""
  if not chunks: return ""
  
  # Get text from first chunk
  first_chunk = chunks[0]
  result = first_chunk.text if hasattr(first_chunk, 'text') else (first_chunk.get('text', '') if isinstance(first_chunk, dict) else str(first_chunk))
  
  if len(chunks) == 1: return result
  
  for i in range(1, len(chunks)):
    chunk = chunks[i]
    chunk_text = chunk.text if hasattr(chunk, 'text') else (chunk.get('text', '') if isinstance(chunk, dict) else str(chunk))
    
    if not chunk_text: continue
    
    if overlap_chars > 0 and len(chunk_text) > overlap_chars:
      result += chunk_text[overlap_chars:]
    else:
      # Fallback: no overlap removal, add with newline separator
      result += "\n" + chunk_text
  
  return result

def get_filename_from_file(file_obj):
  """Extract filename from file object attributes, fallback to file ID."""
  if not file_obj: return UNKNOWN
  
  # Try direct filename attribute
  filename = getattr(file_obj, 'filename', None)
  if filename: return filename
  
  # Try attributes dict
  attributes = getattr(file_obj, 'attributes', None)
  if attributes and isinstance(attributes, dict):
    filename = attributes.get('filename')
    if filename: return filename
  
  # Fallback to file ID
  file_id = getattr(file_obj, 'id', None)
  return file_id if file_id else UNKNOWN

# ----------------------------------------------------- END: Chunk Stitching -------------------------------------------------------


# ----------------------------------------------------- START: Main Functions ------------------------------------------------------

def retrieve_and_reconstruct_files(client, params: RAGTextRetrievalParams):
  """
  Main orchestration function: retrieve chunks from vector store and reconstruct files.
  Returns list of ReconstructionResult.
  """
  function_name = 'Retrieve and reconstruct files from vector store'
  start_time = log_function_header(function_name) if params.log_headers else None
  
  print(f"  Vector store: '{params.vector_store_id}'")
  
  # Step 1: Get all files from vector store with filenames from global Files API
  print(f"  Retrieving file list from vector store...")
  vs = get_vector_store_by_id(client, params.vector_store_id)
  all_files = get_vector_store_files_with_filenames(client, vs)
  print(f"    {len(all_files)} file{'s' if len(all_files) != 1 else ''} found in vector store.")
  
  # Step 2: Filter by filenames BEFORE retrieving chunks (optimization)
  files_to_process = all_files
  if params.only_these_filenames:
    files_to_process = [f for f in all_files if get_filename_from_file(f) in params.only_these_filenames]
    print(f"    Filtered to {len(files_to_process)} file{'s' if len(files_to_process) != 1 else ''} matching filter: {params.only_these_filenames}")
  
  if not files_to_process:
    print(f"  No files to process.")
    if params.log_headers: log_function_footer(function_name, start_time)
    return []
  
  # Step 3: Retrieve chunks for each file with progress
  print(f"  Retrieving chunks for {len(files_to_process)} file{'s' if len(files_to_process) != 1 else ''}...")
  file_contents = []
  for file_idx, file in enumerate(files_to_process, 1):
    file_name = get_filename_from_file(file)
    print(f"    [ {file_idx} / {len(files_to_process)} ] Retrieving chunks for '{file_name}'...")
    chunks = get_vector_store_file_content(client, params.vector_store_id, file.id)
    chunk_count = len(chunks)
    total_chars = sum(len(c.text) if hasattr(c, 'text') else len(c.get('text', '')) for c in chunks)
    print(f"      {chunk_count} chunk{'s' if chunk_count != 1 else ''}, {total_chars:,} chars total")
    file_contents.append({"file": file, "chunks": chunks})
  
  file_count = len(file_contents)
  print(f"    {file_count} file{'s' if file_count != 1 else ''} retrieved with chunks.")
  
  # Step 3: Detect overlap from first file with 2+ chunks
  print(f"  Detecting overlap from first multi-chunk file...")
  overlap_info = ChunkOverlapInfo(overlap_chars=0, confidence="none")
  
  for item in file_contents:
    chunks = item.get('chunks', [])
    if len(chunks) >= 2:
      chunk_0_text = chunks[0].text if hasattr(chunks[0], 'text') else chunks[0].get('text', '')
      chunk_1_text = chunks[1].text if hasattr(chunks[1], 'text') else chunks[1].get('text', '')
      overlap_info = detect_chunk_overlap(chunk_0_text, chunk_1_text)
      filename = get_filename_from_file(item.get('file'))
      print(f"    Overlap detected from '{filename}': {overlap_info.overlap_chars} chars (confidence: {overlap_info.confidence})")
      if overlap_info.confidence == "normalized":
        print(f"    WARNING: Overlap detected via whitespace normalization. Results may have minor duplicates.")
      break
  
  if overlap_info.overlap_chars == 0:
    print(f"    No multi-chunk files found or no overlap detected. Proceeding without overlap removal.")
    print(f"    NOTE: If files have different chunking strategies, some may have duplicated content.")
  
  # Step 4: Create output folder if needed
  if not os.path.exists(params.output_folder):
    os.makedirs(params.output_folder)
    print(f"  Created output folder: '{params.output_folder}'")
  
  # Step 5: Process each file
  results = []
  total_chunks = 0
  total_bytes = 0
  
  print(f"  Processing {len(file_contents)} file{'s' if len(file_contents) != 1 else ''}...")
  
  for idx, item in enumerate(file_contents, 1):
    file_obj = item.get('file')
    chunks = item.get('chunks', [])
    filename = get_filename_from_file(file_obj)
    file_id = getattr(file_obj, 'id', UNKNOWN) if file_obj else UNKNOWN
    
    # Stitch chunks together
    reconstructed_text = stitch_chunks(chunks, overlap_info.overlap_chars)
    reconstructed_bytes = len(reconstructed_text.encode('utf-8'))
    
    # Determine output filename
    output_filename = filename + params.output_suffix
    output_path = os.path.join(params.output_folder, output_filename)
    
    # Write reconstructed content
    with open(output_path, 'w', encoding='utf-8') as f:
      f.write(reconstructed_text)
    
    # Track results
    result = ReconstructionResult(
      filename=filename,
      original_file_id=file_id,
      chunk_count=len(chunks),
      reconstructed_bytes=reconstructed_bytes,
      output_path=output_path
    )
    results.append(result)
    total_chunks += len(chunks)
    total_bytes += reconstructed_bytes
    
    # NOTE: PDF/DOCX quality depends on OpenAI's text extraction [RAGTR-RV-006]
    file_ext = os.path.splitext(filename)[1].lower() if filename != UNKNOWN else ''
    quality_warning = ' (text extraction quality may vary)' if file_ext in ['.pdf', '.docx', '.pptx', '.doc'] else ''
    print(f"    [ {idx} / {len(file_contents)} ] '{filename}': {len(chunks)} chunk{'s' if len(chunks) != 1 else ''} -> {reconstructed_bytes:,} bytes -> '{output_path}'{quality_warning}")
  
  # Summary
  print(f"  Summary: {len(results)} file{'s' if len(results) != 1 else ''}, {total_chunks} chunk{'s' if total_chunks != 1 else ''}, {total_bytes:,} bytes reconstructed")
  
  if params.log_headers: log_function_footer(function_name, start_time)
  return results

# ----------------------------------------------------- END: Main Functions --------------------------------------------------------


# ----------------------------------------------------- START: Main ----------------------------------------------------------------

if __name__ == '__main__':
  openai_service_type = os.getenv("OPENAI_SERVICE_TYPE", "openai")
  if openai_service_type == "openai":
    client = create_openai_client()
  elif openai_service_type == "azure_openai":
    azure_openai_use_key_authentication = os.getenv("AZURE_OPENAI_USE_KEY_AUTHENTICATION", "false").lower() in ['true']
    client = create_azure_openai_client(azure_openai_use_key_authentication)

  params = RAGTextRetrievalParams(
    vector_store_id="<vs_id>"
    ,only_these_filenames=[]  # Empty = all files, or specify: ["file1.pdf", "file2.md"]
    ,output_folder="./downloaded_rag_texts"
    ,output_suffix=".reconstructed.md"
    ,log_headers=True
  )

  # Run reconstruction
  results = retrieve_and_reconstruct_files(client, params)
  
  # Print final summary
  print("-"*140)
  if results:
    print(f"Reconstruction complete. {len(results)} file{'s' if len(results) != 1 else ''} written to '{params.output_folder}'")
    for r in results:
      print(f"  - '{r.filename}' ({r.chunk_count} chunk{'s' if r.chunk_count != 1 else ''}, {r.reconstructed_bytes:,} bytes)")
  else:
    print("No files reconstructed.")

# ----------------------------------------------------- END: Main ------------------------------------------------------------------
