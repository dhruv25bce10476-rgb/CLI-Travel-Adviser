# auth.py
import json
import os
import getpass
import hashlib

FILE = "users.json"
#functions to access users file and make sure to access if any user has signed up beforehand
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return {}

def save_users(users):
    with open(FILE, "w") as f:
        json.dump(users, f, indent=4)
#Signup function asking user to enter basic information
def signup():
    users = load_users()
    print("\n" + "─" * 45)
    print("  SIGN UP")
    print("─" * 45)

    email = input("  Email        : ").strip()
    first = input("  First name   : ").strip()
    last  = input("  Last name    : ").strip()

    while True:
        username = input("  Username     : ").strip()
        if username in users:
            print("  ✗ Username already taken. Try another.")
        elif not username:
            print("  ✗ Username cannot be empty.")
        else:
            break

    password = hash_password(getpass.getpass("  Password     : "))

    users[username] = {
        "username":   username,
        "password":   password,
        "first_name": first,
        "last_name":  last,
        "email":      email,
    }
    save_users(users)
    print("\n  ✓ Account created! You can now log in.\n")
#Login function to get in the application
def login():
    users = load_users()
    print("\n" + "─" * 45)
    print("  LOGIN")
    print("─" * 45)
    #To ensure safety for user by providing only 3 attempts while password is incorrect
    for attempt in range(3):
        username = input("  Username : ").strip()
        password = hash_password(getpass.getpass("  Password : "))

        if username in users and users[username]["password"] == password:
            print(f"\n  ✓ Welcome back, {users[username]['first_name']}!\n")
            return users[username]
        else:
            remaining = 2 - attempt
            if remaining > 0:
                print(f"  ✗ Invalid credentials. {remaining} attempt(s) left.")
            else:
                print("  ✗ Too many failed attempts.")
    return None
