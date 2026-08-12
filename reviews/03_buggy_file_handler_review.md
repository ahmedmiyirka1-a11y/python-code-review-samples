# Code Review: 03_buggy_file_handler.py

## Summary

This script reads uploaded files, backs them up, logs activity, and
deletes empty files. It has a critical path traversal vulnerability, as
well as resource leaks, missing error handling, and a destructive
default behavior that could cause unintended data loss.

---

## 1. Path Traversal Vulnerability

**Issue:**
```python
path = UPLOAD_DIR + "/" + filename
```
`filename` is used directly to build a file path with no sanitization.

**Why it matters:**
If `filename` ever comes from user input and contains something like
`../../etc/passwd`, this code will read, back up, or delete files
outside of `uploads/` — a serious security vulnerability known as path
traversal.

**Fix:**
```python
import os

def safe_path(base_dir, filename):
    full_path = os.path.abspath(os.path.join(base_dir, filename))
    if not full_path.startswith(os.path.abspath(base_dir) + os.sep):
        raise ValueError(f"Invalid filename: {filename}")
    return full_path
```

---

## 2. File Handles Never Closed

**Issue:** `read_file` and `write_log` both call `open()` but never
close the file handle.

**Why it matters:** Every call leaks a file descriptor, which can
exhaust the OS limit during large batches.

**Fix:**
```python
def read_file(filename):
    path = safe_path(UPLOAD_DIR, filename)
    with open(path, "r") as f:
        return f.read()
```

---

## 3. No Error Handling for Missing/Unreadable Files

**Issue:** None of the functions handle missing files, permission
errors, or missing directories.

**Why it matters:** A single bad file crashes the entire batch,
aborting processing for all remaining files.

**Fix:** Wrap file operations in try/except and continue processing
other files, logging failures instead of crashing.

---

## 4. Destructive Default Behavior (`process_upload`)

**Issue:**
```python
if word_count == 0:
    delete_file(filename)
```

**Why it matters:** Silently deleting a file because it's empty is a
surprising, destructive side effect for a function whose name doesn't
suggest deletion at all.

**Fix:** Make deletion an explicit, opt-in parameter, e.g.
`process_upload(filename, delete_if_empty=False)`.

---

## 5. `write_log` Uses Hardcoded Relative Path

**Issue:**
```python
f = open("activity.log", "a")
```

**Why it matters:** The log path depends on the current working
directory, leading to logs written to unexpected locations.

**Fix:** Use an absolute or configurable path.

---

## 6. `BACKUP_DIR` Assumed to Already Exist

**Issue:** `backup_file` assumes `BACKUP_DIR` exists, with no check or
creation step.

**Fix:**
```python
os.makedirs(BACKUP_DIR, exist_ok=True)
```

---

## 7. Word Count Logic Is Naive

**Issue:**
```python
word_count = len(content.split(" "))
```
Splitting only on single spaces miscounts words separated by tabs or
multiple spaces.

**Fix:**
```python
word_count = len(content.split())
```

---

## Priority Summary

| Priority | Issue |
|----------|-------|
| Critical | Path traversal vulnerability |
| High     | No error handling around file operations |
| High     | Destructive silent delete on empty files |
| Medium   | File handles never closed |
| Medium   | `BACKUP_DIR` not guaranteed to exist |
| Low      | Hardcoded log path |
| Low      | Naive word-count logic |

See `fixed/03_buggy_file_handler.py` for the corrected version.
