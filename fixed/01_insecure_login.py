"""
Simple login system for a demo web app (fixed / production-ready version).

Security fixes applied:
- Parameterized SQL queries (no SQL injection)
- Passwords hashed with bcrypt (never stored/compared in plaintext)
- No hardcoded credentials
- Input validation
- Proper error handling and logging
- Connections managed with context managers
"""

import logging
import sqlite3
from contextlib import contextmanager

import bcrypt

DB_PATH = "users.db"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@contextmanager
def get_connection():
"""Yield a database connection and guarantee it is closed afterward."""
conn = sqlite3.connect(DB_PATH)
try:
yield conn
finally:
conn.close()

def _validate_credentials(username: str, password: str) -> None:
"""Raise ValueError if username or password are missing/invalid."""
if not username or not username.strip():
raise ValueError("Username is required")
if not password:
raise ValueError("Password is required")

def hash_password(password: str) -> bytes:
"""Hash a plaintext password using bcrypt."""
return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def verify_password(password: str, hashed: bytes) -> bool:
"""Verify a plaintext password against a bcrypt hash."""
return bcrypt.checkpw(password.encode("utf-8"), hashed)

def check_login(username: str, password: str) -> bool:
"""
Verify a username/password pair against the users table.

Returns True if credentials are valid, False otherwise.
"""
_validate_credentials(username, password)

try:
with get_connection() as conn:
cursor = conn.cursor()
cursor.execute(
"SELECT password FROM users WHERE username = ?",
(username,),
)
result = cursor.fetchone()
except sqlite3.Error as e:
logger.error("Database error during login for %s: %s", username, e)
return False

if result is None:
return False

stored_hash = result[0]
return verify_password(password, stored_hash)

def login(username: str, password: str) -> bool:
"""Attempt to log in a user and print the result."""
try:
if check_login(username, password):
logger.info("Login successful for user: %s", username)
return True
logger.info("Login failed for user: %s", username)
return False
except ValueError as e:
logger.warning("Invalid login attempt: %s", e)
return False

def create_user(username: str, password: str) -> None:
"""Create a new user with a securely hashed password."""
_validate_credentials(username, password)
hashed = hash_password(password)

try:
with get_connection() as conn:
cursor = conn.cursor()
cursor.execute(
"INSERT INTO users (username, password) VALUES (?, ?)",
(username, hashed),
)
conn.commit()
except sqlite3.IntegrityError:
logger.warning("User already exists: %s", username)
raise
except sqlite3.Error as e:
logger.error("Database error creating user %s: %s", username, e)
raise

def change_password(username: str, new_password: str) -> None:
"""Change a user's password, storing it as a secure hash."""
_validate_credentials(username, new_password)
hashed = hash_password(new_password)

try:
with get_connection() as conn:
cursor = conn.cursor()
cursor.execute(
"UPDATE users SET password = ? WHERE username = ?",
(hashed, username),
)
conn.commit()
except sqlite3.Error as e:
logger.error("Database error changing password for %s: %s", username, e)
raise

logger.info("Password changed for user: %s", username)

def main() -> None:
user = input("Username: ")
pw = input("Password: ")
login(user, pw)

if __name__ == "__main__":
main()"""
Simple login system for a demo web app (fixed / production-ready version).

Security fixes applied:
- Parameterized SQL queries (no SQL injection)
- Passwords hashed with bcrypt (never stored/compared in plaintext)
- No hardcoded credentials
- Input validation
- Proper error handling and logging
- Connections managed with context managers
"""

import logging
import sqlite3
from contextlib import contextmanager

import bcrypt

DB_PATH = "users.db"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@contextmanager
def get_connection():
"""Yield a database connection and guarantee it is closed afterward."""
conn = sqlite3.connect(DB_PATH)
try:
yield conn
finally:
conn.close()

def _validate_credentials(username: str, password: str) -> None:
"""Raise ValueError if username or password are missing/invalid."""
if not username or not username.strip():
raise ValueError("Username is required")
if not password:
raise ValueError("Password is required")

def hash_password(password: str) -> bytes:
"""Hash a plaintext password using bcrypt."""
return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def verify_password(password: str, hashed: bytes) -> bool:
"""Verify a plaintext password against a bcrypt hash."""
return bcrypt.checkpw(password.encode("utf-8"), hashed)

def check_login(username: str, password: str) -> bool:
"""
Verify a username/password pair against the users table.

Returns True if credentials are valid, False otherwise.
"""
_validate_credentials(username, password)

try:
with get_connection() as conn:
cursor = conn.cursor()
cursor.execute(
"SELECT password FROM users WHERE username = ?",
(username,),
)
result = cursor.fetchone()
except sqlite3.Error as e:
logger.error("Database error during login for %s: %s", username, e)
return False

if result is None:
return False

stored_hash = result[0]
return verify_password(password, stored_hash)

def login(username: str, password: str) -> bool:
"""Attempt to log in a user and print the result."""
try:
if check_login(username, password):
logger.info("Login successful for user: %s", username)
return True
logger.info("Login failed for user: %s", username)
return False
except ValueError as e:
logger.warning("Invalid login attempt: %s", e)
return False

def create_user(username: str, password: str) -> None:
"""Create a new user with a securely hashed password."""
_validate_credentials(username, password)
hashed = hash_password(password)

try:
with get_connection() as conn:
cursor = conn.cursor()
cursor.execute(
"INSERT INTO users (username, password) VALUES (?, ?)",
(username, hashed),
)
conn.commit()
except sqlite3.IntegrityError:
logger.warning("User already exists: %s", username)
raise
except sqlite3.Error as e:
logger.error("Database error creating user %s: %s", username, e)
raise

def change_password(username: str, new_password: str) -> None:
"""Change a user's password, storing it as a secure hash."""
_validate_credentials(username, new_password)
hashed = hash_password(new_password)

try:
with get_connection() as conn:
cursor = conn.cursor()
cursor.execute(
"UPDATE users SET password = ? WHERE username = ?",
(hashed, username),
)
conn.commit()
except sqlite3.Error as e:
logger.error("Database error changing password for %s: %s", username, e)
raise

logger.info("Password changed for user: %s", username)

def main() -> None:
user = input("Username: ")
pw = input("Password: ")
login(user, pw)

if __name__ == "__main__":
main()
