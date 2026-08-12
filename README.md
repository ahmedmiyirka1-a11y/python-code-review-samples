# Python Code Review Samples

Welcome to my repository of Python code reviews.

## Contents

There are three main directories:

- `examples/`
- `reviews/`
- `fixed/`

### examples/

This directory contains Python code examples that were submitted for
review. Most of them have issues: some have anti-patterns, some have
bugs, and some have security vulnerabilities.

### reviews/

This directory contains the reviews themselves. Each review documents
the issues found during the review of the corresponding example in
`examples/`.

### fixed/

This directory contains the fixed versions of the examples from
`examples/`. These represent production-ready versions of the reviewed
code.

## Index

| # | Example | Topic | Main issues |
|---|---------|-------|-------------|
| 01 | `01_insecure_login.py` | Authentication | SQL injection, plaintext passwords, hardcoded credentials |
| 02 | `02_buggy_data_processor.py` | Data processing | Silent failures, mutable default args, no validation |
| 03 | `03_buggy_file_handler.py` | File handling | Path traversal, unclosed files, no error handling |

## Why this repository?

The repository was created to showcase my code review skills.

By reviewing the code examples, you get a chance to see my Python
expertise. You can judge how well I find bugs, security issues, and
code smells. You can also see my understanding of code quality, code
conventions, and Python-specific best practices (PEP 8). By comparing
`examples/` with `fixed/`, and reading through `reviews/`, you can see
my writing skills: how I explain issues in English, and how I
structure reviews to make them easy to follow.
