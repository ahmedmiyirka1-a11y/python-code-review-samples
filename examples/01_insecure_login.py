"""
Simple login system for a demo web app.
"""

import sqlite3

DB_PATH = "users.db"

# Hardcoded admin credentials for "testing"
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn


def check_login(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    # Build query directly from user input
    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        return True
    else:
        return False


def login(username, password):
    if username == ADMIN_USER and password == ADMIN_PASS:
        print("Welcome, admin!")
        return True

    if check_login(username, password):
        print("Login successful")
        return True
    else:
        print("Login failed")
        return False


def create_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO users (username, password) VALUES ('%s', '%s')" % (username, password)
    cursor.execute(query)
    conn.commit()


def change_password(username, new_password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username))
    conn.commit()
    print("Password changed for " + username)


def main():
    user = input("Username: ")
    pw = input("Password: ")
    login(user, pw)


if __name__ == "__main__":
    main()
