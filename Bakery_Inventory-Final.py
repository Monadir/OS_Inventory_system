# Bakery Inventory System with Menu, Validation, and Interaction

import json
from datetime import date, datetime

# Constants
MIN_THRESHOLD = 5
EXPIRY_CHECK_ENABLED = True
INVENTORY_FILE = "inventory.json"

# Permissions
ADMIN_PERMISSIONS = ["view", "edit", "add", "update", "search", "check_expiry"]
STAFF_PERMISSIONS = ["view", "update", "search"]


# User setup
userRole = input("Enter your role (Admin/Staff): ").capitalize()
permissions = ADMIN_PERMISSIONS if userRole == "Admin" else STAFF_PERMISSIONS
print(f"Welcome, {userRole}! Permissions granted: {', '.join(permissions)}")

# Load or initialize inventory
"""Load the inventory from the JSON file."""
try:
    with open(INVENTORY_FILE, "r") as f:
        inventory = json.load(f)
except FileNotFoundError:
    print("File Not Found. Starting with empty inventory.")
    inventory = {}

def save_inventory():
    """Save the inventory to the JSON file."""
    with open(INVENTORY_FILE, "w") as F:
        json.dump(inventory, F, indent=4)


def validate_expiry_date(date_str):
    """Validate an expiry date format and ensure it's not in the past."""
    try:
        expiry_date = datetime.strptime(date_str, "%Y-%m-%d")
        if expiry_date.date() < date.today():
            return False, "Expiry date cannot be in the past."
        return True, "Valid expiry date."
    except ValueError:
        return False, "Invalid date format. Please use YYYY-MM-DD."


def low_stock_alert():
    """Alert if any item is below the minimum threshold."""
    print("\n--- Low Stock Check ---")
    low_stock_items = []
    for item, info in inventory.items():
        qty = info['quantity']
        if qty < MIN_THRESHOLD:
            low_stock_items.append((item, qty, info['unit']))
    if low_stock_items:
        for item, qty, unit in low_stock_items:
            print(f"ALERT: Low stock on {item} — Only {qty} {unit} left!")
    else:
        print("All items are above the minimum threshold.")

# Menu functions

def add_ingredient():
    """Add a new ingredient with validation."""
    name = input("Enter ingredient name: ").title()
    if name in inventory:
        print("Ingredient already exists.")
        return
    try:
        quantity = float(input("Enter quantity: "))
        if quantity <= 0:
            print("Quantity must be positive.")
            return
        unit = input("Enter unit (e.g., kg, litres): ").strip()
        if not unit:
            print("Unit cannot be empty.")
            return
        while True:
            expiry = input("Enter expiry date (YYYY-MM-DD): ")
            valid, message = validate_expiry_date(expiry)
            print(message)
            if valid:
                break
        inventory[name] = {"quantity": quantity, "unit": unit, "expiry": expiry}
        save_inventory()
        print(f"Added {name} successfully.")
    except ValueError:
        print("Invalid input. Please enter numeric values for quantity.")


def check_ingredients():
    """Display all ingredients and their details."""
    print("\n--- Current Inventory ---")
    if not inventory:
        print("Inventory is empty.")
        return
    for name, info in inventory.items():
        print(f"{name}: {info['quantity']} {info['unit']} (Expires: {info['expiry']})")


def update_ingredient():
    """Update an ingredient by usage or restock, with validation."""
    name = input("Enter ingredient name: ").title()
    if name not in inventory:
        print("Ingredient not found.")
        return
    action = input("Type 'use' to deduct or 'restock' to add: ").lower()
    if action not in ["use", "restock"]:
        print("Invalid action.")
        return
    try:
        amount = float(input(f"Enter amount to {action} for {name}: "))
        if amount <= 0:
            print("Amount must be positive.")
            return
        if action == "use":
            if amount > inventory[name]["quantity"]:
                print("Not enough in stock.")
                return
            confirm = input(f"Confirm using {amount} from {name}? (y/n): ").lower()
            if confirm != 'y':
                print("Cancelled.")
                return
            inventory[name]["quantity"] -= amount
        elif action == "restock":
            inventory[name]["quantity"] += amount
        save_inventory()
        print(f"{name} updated. New quantity: {inventory[name]['quantity']} {inventory[name]['unit']}")
        low_stock_alert()  # Alert after use/restock
    except ValueError:
        print("Invalid input. Please enter a valid number.")


def search_ingredient():
    """Search for an ingredient by name."""
    name = input("Search for ingredient: ").title()
    if name in inventory:
        info = inventory[name]
        print(f"{name}: {info['quantity']} {info['unit']} (Expires: {info['expiry']})")
    else:
        print("Ingredient not found.")
        low_stock_alert()  # Alert after check


def check_expiry():
    """Check for expired ingredients."""
    today = date.today()
    expired = [
        name for name, info in inventory.items()
        if datetime.strptime(info["expiry"], "%Y-%m-%d").date() < today
    ]
    if expired:
        print("\n--- Expired Ingredients ---")
        for name in expired:
            print(f"{name} expired on {inventory[name]['expiry']}")
    else:
        print("\nNo expired items.")


def main_menu():
    """Display the main menu and handle user choices."""
    while True:
        print("\n-- Sweet Surrender Bakery --")
        print("--- Inventory Menu ---")
        print("1. Add New Ingredients")
        print("2. Check All Stock Levels")
        print("3. Update Ingredients")
        print("4. Search Ingredients")
        print("5. Check For Expired Ingredients")
        print("6. Exit")
        low_stock_alert()  # Alert after print
        choice = input("Enter your choice (1-6): ")
        if choice == '1':
            if "add" in permissions:
                add_ingredient()
            else:
                print("Access Denied: You do not have permission to add ingredients.")
        elif choice == '2':
            if "view" in permissions:
                check_ingredients()
            else:
                print("Access Denied: You do not have permission to view inventory.")
        elif choice == '3':
            if "update" in permissions:
                update_ingredient()
            else:
                print("Access Denied: You do not have permission to update ingredients.")
        elif choice == '4':
            if "search" in permissions:
                search_ingredient()
            else:
                print("Access Denied: You do not have permission to search ingredients.")
        elif choice == '5':
            if "check_expiry" in permissions:
                check_expiry()
            else:
                print("Access Denied: You do not have permission to check expiry.")
        elif choice == '6':
            print("Exiting Bakery Inventory System.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


# Run the program
main_menu()
