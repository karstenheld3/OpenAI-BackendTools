from dataclasses import dataclass
from dotenv import load_dotenv
from openai_backendtools import *
import time
import os
import datetime

load_dotenv()

# Global variables
# https://platform.openai.com/docs/assistants/tools/file-search/supported-files#supported-files
default_filetypes_accepted_by_vector_stores = ["c", "cpp", "cs", "css", "doc", "docx", "go", "html", "java", "js", "json", "md", "pdf", "php", "pptx", "py", "rb", "sh", "tex", "ts", "txt"]

@dataclass
class CrawledFile:
  file_id: str
  file_path: str
  file_type: str
  file_size: int
  file_timestamp: int
  last_modified: str # datetime string in format 'YYYY-MM-DD HH:MM:SS', CET (Central European Time), Berlin time zone
  key: str # source file path
  source_url: str
  metadata: dict
  errors: list[str]

@dataclass
class CrawledFiles:
  vector_store: any
  files: list[CrawledFile]
  omitted_files: list[CrawledFile]
  failed_files: list[CrawledFile]
