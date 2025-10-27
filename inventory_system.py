"""
INVENTORY MANAGEMENT SYSTEM - PROFESSIONAL VERSION

MAJOR IMPROVEMENTS MADE:
1. Security vulnerabilities eliminated
2. Critical bugs fixed
3. Proper error handling implemented
4. Input validation added
5. Code quality significantly enhanced
6. All style issues resolved
"""
import json
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any


# Global variable for stock data
stock_data: Dict[str, int] = {}


def add_item(
    item: str = "default",
    quantity: int = 0,
    logs: Optional[List[str]] = None
) -> bool:
    """
    Add items to inventory with comprehensive validation.

    FIXED: Mutable default argument bug
    ORIGINAL: logs=[] - Same list shared across all function calls!
    FIXED: logs=None - New list created for each call

    Args:
        item: Name of the item to add
        quantity: Quantity to add (must be positive)
        logs: Optional list to store log messages

    Returns:
        bool: True if successful, False otherwise
    """
    if logs is None:
        logs = []

    # Input validation
    if not item:
        logging.warning("Attempted to add item with empty name")
        return False

    if not isinstance(item, str):
        logging.error("Item name must be a string")
        return False

    if not isinstance(quantity, int):
        logging.error("Quantity must be an integer")
        return False

    if quantity < 0:
        logging.warning("Attempted to add negative quantity")
        return False

    # Update stock data
    stock_data[item] = stock_data.get(item, 0) + quantity

    # Modern string formatting
    log_message = f"{datetime.now()}: Added {quantity} of {item}"
    logs.append(log_message)
    logging.info(log_message)
    return True


def remove_item(item: str, quantity: int) -> bool:
    """
    Remove items from inventory with proper error handling.

    FIXED: Dangerous bare except clause
    ORIGINAL: except: pass - Hides ALL errors including serious ones!
    FIXED: Specific exception handling with proper logging

    Args:
        item: Name of the item to remove
        quantity: Quantity to remove (must be positive)

    Returns:
        bool: True if successful, False otherwise
    """
    # Input validation
    if not isinstance(item, str):
        logging.error("Item name must be a string")
        return False

    if not isinstance(quantity, int) or quantity <= 0:
        logging.error("Quantity must be a positive integer")
        return False

    # Check item existence before try block
    if item not in stock_data:
        logging.warning("Item '%s' not found in inventory", item)
        return False

    if stock_data[item] < quantity:
        logging.warning("Insufficient stock for '%s'", item)
        return False

    try:
        # Perform removal operation
        stock_data[item] -= quantity
        if stock_data[item] <= 0:
            del stock_data[item]
            msg = "Item '%s' completely removed from inventory"
            logging.info(msg, item)
        else:
            logging.info("Removed %d of '%s'", quantity, item)
        return True

    # Specific exception handling instead of bare except
    except KeyError as error:
        msg = "Unexpected error removing item '%s': %s"
        logging.error(msg, item, error)
        return False
    except ValueError as error:
        msg = "Invalid operation for item '%s': %s"
        logging.error(msg, item, error)
        return False


def get_quantity(item: str) -> int:
    """
    Safely get quantity of an item.

    FIXED: Safer dictionary access
    ORIGINAL: return stock_data[item] - Would crash if item doesn't exist!
    FIXED: Uses .get() with default value

    Args:
        item: Name of the item to query

    Returns:
        int: Quantity of the item, 0 if not found
    """
    return stock_data.get(item, 0)


def load_data(file_path: str = "inventory.json") -> bool:
    """
    Load inventory data from file safely.

    FIXED: Unsafe file operations
    ORIGINAL: Manual file open/close - Could leak file descriptors!
    FIXED: Context manager ensures proper cleanup

    Args:
        file_path: Path to the inventory JSON file

    Returns:
        bool: True if loaded successfully, False otherwise
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            loaded_data = json.load(file)

        # Validate loaded data structure
        if not isinstance(loaded_data, dict):
            logging.error("Invalid data format in file: expected dict")
            return False

        # Validate all values are integers
        if not all(isinstance(val, int) for val in loaded_data.values()):
            logging.error("Invalid data types: values must be integers")
            return False

        # Update global stock data
        global stock_data
        stock_data = loaded_data
        logging.info("Data successfully loaded from %s", file_path)
        return True

    except FileNotFoundError:
        msg = "File %s not found, starting with empty inventory"
        logging.warning(msg, file_path)
        return True  # Not an error - start fresh
    except json.JSONDecodeError as error:
        logging.error("Error reading JSON file %s: %s", file_path, error)
        return False
    except (PermissionError, OSError) as error:
        logging.error("Error accessing file %s: %s", file_path, error)
        return False


def save_data(file_path: str = "inventory.json") -> bool:
    """
    Save inventory data to file safely.

    FIXED: Safe file operations with proper error handling
    ORIGINAL: Manual file handling with no encoding specified

    Args:
        file_path: Path to save the inventory file

    Returns:
        bool: True if saved successfully, False otherwise
    """
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(stock_data, file, indent=4, sort_keys=True)

        logging.info("Data successfully saved to %s", file_path)
        return True

    except (IOError, OSError) as error:
        logging.error("Error saving data to %s: %s", file_path, error)
        return False


def print_data() -> None:
    """
    Print all inventory data in a formatted, readable way.

    FIXED: Better variable names and output formatting
    """
    print("\n" + "=" * 40)
    print("          INVENTORY REPORT")
    print("=" * 40)

    if not stock_data:
        print("No items in inventory")
        return

    total_items = sum(stock_data.values())
    print(f"Total items: {total_items}")
    print(f"Unique items: {len(stock_data)}")
    print("-" * 40)

    # Sort items for consistent output
    for item, quantity in sorted(stock_data.items()):
        status = "LOW STOCK" if quantity < 5 else "OK"
        print(f"  {item:<15} -> {quantity:>3} units [{status}]")

    print("=" * 40)


def check_low_items(threshold: int = 5) -> List[str]:
    """
    Check for items with stock below threshold.

    FIXED: Better variable names and type hints

    Args:
        threshold: Minimum quantity threshold

    Returns:
        List of item names below threshold
    """
    return [
        item for item, quantity in stock_data.items()
        if quantity < threshold
    ]


def get_inventory_summary() -> Dict[str, Any]:
    """
    Get comprehensive inventory summary.

    NEW: Added for better functionality
    """
    return {
        "total_items": sum(stock_data.values()),
        "unique_items": len(stock_data),
        "low_stock_items": check_low_items(),
        "all_items": dict(stock_data)
    }


def main() -> None:
    """
    Main function to demonstrate system functionality.

    FIXED: Proper logging configuration and structure
    ORIGINAL: Had dangerous eval() function
    """
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    logging.info("Starting inventory system demonstration")

    # Test with valid data
    test_operations = [
        ("apple", 10),
        ("banana", 5),
        ("orange", 3),
        (123, "ten"),  # Should fail - invalid types
        ("test", -5),  # Should fail - negative quantity
        ("", 5)  # Should fail - empty item name
    ]

    for item, qty in test_operations:
        success = add_item(item, qty)
        if not success:
            debug_msg = "Expected failure for item=%s, quantity=%s"
            logging.debug(debug_msg, item, qty)

    # Test removal operations
    removal_operations = [
        ("apple", 3),  # Should succeed
        ("orange", 1),  # Should succeed
        ("nonexistent", 1),  # Should fail
        ("banana", 10)  # Should fail - insufficient stock
    ]

    for item, qty in removal_operations:
        success = remove_item(item, qty)
        if not success:
            debug_msg = "Expected removal failure for item=%s, quantity=%s"
            logging.debug(debug_msg, item, qty)

    # Display results
    print("\n" + "=" * 50)
    print("            DEMONSTRATION RESULTS")
    print("=" * 50)

    print(f"Apple stock: {get_quantity('apple')}")
    print(f"Low stock items: {check_low_items()}")

    summary = get_inventory_summary()
    total_msg = f"Total items in inventory: {summary['total_items']}"
    print(total_msg)
    print(f"Unique items: {summary['unique_items']}")

    # Save and load data
    if save_data():
        logging.info("Data saved successfully")

    if load_data():
        logging.info("Data loaded successfully")

    print_data()
    logging.info("Inventory system demonstration completed successfully")


if __name__ == "__main__":
    main()

