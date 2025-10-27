import json
from datetime import datetime

# Global variable to store inventory data
stock_data = {}

def add_item(item="default", qty=0, logs=None):
    """Add an item and quantity to the inventory."""
    if logs is None:
        logs = []

    # Validate types
    if not isinstance(item, str) or not isinstance(qty, (int, float)):
        print("Error: Invalid types for item or quantity.")
        return

    if not item:
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")


def remove_item(item, qty):
    """Remove a quantity of an item from the inventory."""
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError:
        print(f"Warning: Item '{item}' not found, cannot remove.")


def get_qty(item):
    """Return the quantity of the given item."""
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """Load inventory data from a JSON file without using global variables."""
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            stock_data.clear()
            stock_data.update(data)
    except FileNotFoundError:
        print(f"File '{file}' not found. Starting with empty inventory.")
        stock_data.clear()


def save_data(file="inventory.json"):
    """Save the inventory data to a JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(stock_data, f, indent=4)


def print_data():
    """Print all items and their quantities."""
    print("\nItems Report")
    for item, qty in stock_data.items():
        print(f"{item} -> {qty}")


def check_low_items(threshold=5):
    """Return a list of items with quantity below the threshold."""
    return [item for item, qty in stock_data.items() if qty < threshold]


def main():
    """Main function for testing inventory operations."""
    add_item("apple", 10)
    add_item("banana", -2)
    add_item(123, "ten")  # invalid types, will show error
    remove_item("apple", 3)
    remove_item("orange", 1)
    print("Apple stock:", get_qty("apple"))
    print("Low items:", check_low_items())
    save_data()
    load_data()
    print_data()
    print("Execution completed safely.")


if _name_ == "_main_":
    main()
