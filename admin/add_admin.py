"""
add_admin.py
------------
Run this script once to create your first admin account.
Usage: python admin/add_admin.py

You will be prompted for a username and password.
The password is stored hashed (SHA-256).
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.admin_model import create_admin, get_admin_by_username

print("=== Blood Bank Portal - Create Admin ===")
print("")

username = input("Enter admin username: ").strip()
password = input("Enter admin password: ").strip()

if not username or not password:
    print("Error: Username and password cannot be empty.")
    sys.exit(1)

# Check if admin with this username already exists
existing = get_admin_by_username(username)
if existing:
    print("Error: An admin with this username already exists.")
    sys.exit(1)

create_admin(username, password)
print("")
print("Admin account created successfully.")
print("Username: " + username)
print("You can now log in at /admin/login")
