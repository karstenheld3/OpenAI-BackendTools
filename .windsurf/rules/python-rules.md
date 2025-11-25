---
trigger: model_decision
description: Apply to Python code
---

## Code formatting
- 2 spaces for indenting
- if less than 200 chars, put on single line

## Imports
- imports always on single line
- all imports at the top of the file; all members of a library in a single row
- standard / core libraries first (top), only then 3rd party libraries

## Code generation
- *Never change existing names*: The existing code base is holy. Only change stuff if you have been asked to do so.
- *Principle Of Least Surprise*: Write simple, idiomatic code. Things should work exactly as a standard programmer would assume them to work.
- *Use Minimal Explicit Consistent Terminology*: Use clear, fully written-out names over abbreviations. Stick to the naming patterns of the existing code base. Avoid ambiguous, generic, shortened names.
- *Write readable code*: Optimize for maintainability, not performance
- *Write concise code*: Put multiple variable inits, function definitions / calls, data classes on a single line. Group lines of code into logical intention blocks.
- *No unnecessary comments": Comments replicating readable code are noise. Use comments to document the overall intention or expected outcome.
- *No lambdas and iterators*: Lambda and array-iteration functions can't easily be debugged. Use classic for loops instead.
- *No unnecessary libraries*: Prefer core Python libraries over 3rd party sources. Before using 3rd party libraries, check if the task can be accomplished with explicit helper functions.
- *No docstrings for smaller functions*: Stick to the documentation pattern of the existing code base. No comments for simple functions. Simple one-line comments if function intention is ambiguous.
- *Use docstring execptions*: FastAPI endpoints, complex / multi-purpose functions and return types
- dont use emojis in logs. exception for ui text: ✅=OK, ❌=FAIL

### Write single intentions on single line even if the line gets very long
*BAD*:
```
content_page = client.vector_stores.files.content(
  vector_store_id=vector_store_id,
  file_id=file_id
)
```
*GOOD*:
```
content_page = client.vector_stores.files.content(vector_store_id=vector_store_id, file_id=file_id)
```
*BAD*:
```
if not vector_store_id:
  raise ValueError(f"Expected a non-empty value for 'vector_store_id' but received {vector_store_id!r}")
```
*GOOD*:
```
if not vector_store_id: raise ValueError(f"Expected a non-empty value for 'vector_store_id' but received {vector_store_id!r}")
```

### Console and internal log formatting
- Indent subactions with 2 spaces
- Put OK / ERROR / FAIL / WARNING on indented separate lines
- `OK` = action succeeded. `ERROR` = intermediate or final error occurred. `FAIL` = action failed even after error mitigation. `WARNING` = intermediate error that will be mitigated
- Put file paths, names and IDs in single quotes
- Log action / subaction description before executing action
- For iterations, ùse `[ x / n ]` format at the beginning of a line where x = current item number, n = total items.
- For retries use `( x / n )` inline where x = current retry, n = max retries.

*BAD*:
```
Uploading item 1/2 Example.docx to vs_62573645276345
SUCCESS: Verified uploaded file.
Uploading item 1/2 Test.docx to vs_62573645276345
ERROR: BlockingIOError: [Errno 11] Resource temporarily unavailable
```
*GOOD*:
```
[ 1 / 2 ] Uploading file 'C:\Example.docx' to vector store ID='vs_62573645276345'...
  Verifying uploaded file ID='file_923748237'...
  OK.
[ 2 / 2 ] Uploading file 'C:\Test.docx' to vector store ID='vs_62573645276345'...
  WARNING: File could not be opened. Maybe it's locked. -> BlockingIOError: [Errno 11] Resource temporarily unavailable
  Waiting 5 seconds ( 1 / 2 ) for retry...
  Uploading file...
  Verifying uploaded file ID='file_238756235'...
  OK.
```