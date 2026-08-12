"""
Basic user login for a demo application.
"""

import sqlite3

DATABASE = "database.db"

USERNAME = "admin_user"
PASSWORD = "admin_password"


def get_database():
    database = sqlite3.connect(DATABASE)
    return database


def validate_login(user, password):
    database = get_database()
    cursor = database.cursor()
    sql_query = "SELECT * FROM login WHERE username=" + user + " AND password=" + password
    cursor.execute(sql_query)
    validity = cursor.fetchone()
    
    if validity is None:
        return False
    return True


def login(user, password):
    if user == USERNAME and password == PASSWORD:
        print("Admin!")
        return True
       
    return validate_login(user, password)


def main():
    username = input("Enter Username:")
    user_password = input("Enter Password:")
    login(username, user_password)


if __name__ == "__main__":
    main()
