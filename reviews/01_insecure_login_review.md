# Code Review: 01_insecure_login.py

## Summary

This file contains a simple implementation of a login system, but has numerous
security issues and code quality problems. The most serious issue is an
SQL injection vulnerability, which could allow an attacker to log in as any

user, including admin, without knowing their password. This document describes
all issues in detail, and provides suggestions for fixing them.
---

## 1. SQL Injection in `check_login`
Code:
```python
query = "SELECT FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
cursor.execute(query)
```
Issue:
The SQL query is constructed from strings and variables using concatenation.
Why it is bad:
An attacker could inject arbitrary SQL code by entering something like
`' OR '1'='1' --` as the username, thus bypassing authentication. This is one of
the most common and dangerous vulnerabilities in web applications
(see [OWASP Top 10: SQL Injection](https://owasp.org/www-project-cheat-sheets/#sql-injection-cheat-sheet)).
Fix:
Use parameterized queries instead of building queries from strings:
```python
query = "SELECT FROM users WHERE username = ? AND password = ?"
cursor.execute(query, (username, password))
```
---
## 2. Plaintext Passwords
Code:
The passwords are compared as plain text.
Issue:
The passwords are stored and compared as plain text.
Why it is bad:
If the database is compromised, all the users' passwords will be exposed.
Fix:
Store and compare hashed passwords using a secure algorithm such as
`bcrypt`.
---
## 3. Hardcoded Admin Credentials
Code:
```python
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"
```
Issue:
The admin user and password are hardcoded in the source code.
Why it is bad:
If the source code gets exposed somehow, the attacker will be able to log in
as the admin user.
Fix:
Do not store admin credentials in the source code at all. The admin user
account should be stored in the database as any other user.
---
## 4. SQL Injection in `create_user`
Code:
```python
query = "INSERT INTO users (username, password) VALUES ('%s', '%s')" % (username, password)
```
Issue:
The SQL query is built using string formatting, which is also vulnerable to
SQL injection.
Fix:
Use parameterized queries.
---
## 5. No Input Validation
Code:
The `username` and `password` parameters are not validated.
Issue:
The parameters are not validated and may be `None` or empty string.
Fix:
Check that the `username` and `password` are not empty:
```python
if not username or not password:
raise ValueError("Username and password are required")
```
---
## 6. No Error Handling
Code:
None of the database operations are wrapped in `try/except` blocks.
Issue:
The code will crash on any database error.
Fix:
Wrap database operations in `try/except` and handle the errors.
---
## 7. Connections Are Not Closed
Code:
The `get_connection` function opens a connection every time it is called, but
it is never closed.
Issue:
The connection is opened, but never closed, which will eventually lead to a
database connection limit being reached.
Fix:
Use a context manager to ensure that the connection is closed:
```python
with sqlite3.connect(DATABASE_FILENAME) as conn:
...
```
---
## 8. `check_login` Returns Only `True`/`False`
Code:
The `check_login` function returns `True`/`False`, but does not provide any
information about why the login failed.
Issue:
If the login fails, the function returns `False`. However, there might be
different reasons for that, such as invalid credentials or database error.
Fix:
Return a custom object that indicates the reason for failure.
---
## 9. No Docstrings or Type Hints
Code:
None of the functions have docstrings or type hints.
Issue:
The code is not well-documented and lacks type hints.
Fix:
Add docstrings and type hints to all functions:
```python
def check_login(username: str, password: str) -> bool:
"""Verify a username/password pair against the users table."""
...
```
---
## Priority List
| Priority | Issue |
|----------|-------|
| Critical | SQL injection in `check_login` and `create_user` |
| Critical | Storing passwords as plain text |
| High | Hardcoded admin credentials |
| Medium | No input validation |
| Medium | No error handling |
| Medium | Connections are not closed |
| Low | `check_login` returns only `True`/`False` |
| Low | No docstrings or type hints |
---

See `fixed/01_insecure_login.py` for the fixed version of this file.
