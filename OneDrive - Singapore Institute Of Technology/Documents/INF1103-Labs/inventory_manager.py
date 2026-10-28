import json
import os

FILENAME = "inventory.json"


def load_inventory():
    """Load products and transaction history from inventory.json."""
    if not os.path.exists(FILENAME):
        print("No inventory.json found. Starting with an empty inventory.\n")
        return {"products": [], "transactions": []}

    try:
        with open(FILENAME, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Allow either the full format or a JSON file containing just a product list.
        if isinstance(data, list):
            return {"products": data, "transactions": []}

        if isinstance(data, dict):
            products = data.get("products", [])
            transactions = data.get("transactions", [])

            if isinstance(products, list) and isinstance(transactions, list):
                return {"products": products, "transactions": transactions}

    except (json.JSONDecodeError, OSError):
        print(f"Could not read {FILENAME}. Starting with an empty inventory.\n")

    return {"products": [], "transactions": []}


def save_inventory(inventory):
    """Save products and transaction history to inventory.json."""
    try:
        with open(FILENAME, "w", encoding="utf-8") as file:
            json.dump(inventory, file, indent=4)

        print(f"Inventory saved successfully to {FILENAME}.\n")
    except OSError as error:
        print(f"Could not save inventory: {error}\n")


def find_product(products, product_id):
    """Find and return a product by ID, ignoring ID letter case."""
    for product in products:
        if product["id"].lower() == product_id.lower():
            return product
    return None


def display_product(product):
    """Print one product's details."""
    print(f"ID: {product['id']}")
    print(f"Name: {product['name']}")
    print(f"Price: ${product['price']:.2f}")
    print(f"Stock: {product['stock']}")


def display_all(inventory):
    """Display all products."""
    products = inventory["products"]

    print("\nCurrent Inventory")
    print("-" * 60)

    if not products:
        print("No products in inventory.")
    else:
        for product in products:
            print(
                f"ID: {product['id']} | "
                f"Name: {product['name']} | "
                f"Price: ${product['price']:.2f} | "
                f"Stock: {product['stock']}"
            )

    print("-" * 60 + "\n")


def add_product(inventory):
    """Ask for product details and add a product to inventory."""
    print("\nAdd New Product")

    product_id = input("Product ID: ").strip()
    if not product_id:
        print("Product ID cannot be empty.\n")
        return

    if find_product(inventory["products"], product_id):
        print("A product with that ID already exists.\n")
        return

    name = input("Product Name: ").strip()
    if not name:
        print("Product name cannot be empty.\n")
        return

    try:
        price = float(input("Price: ").strip())
        if price < 0:
            print("Price cannot be negative.\n")
            return
    except ValueError:
        print("Please enter a valid price.\n")
        return

    try:
        stock = int(input("Stock Quantity: ").strip())
        if stock < 0:
            print("Stock cannot be negative.\n")
            return
    except ValueError:
        print("Please enter a whole number for stock.\n")
        return

    product = {
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock,
    }
    inventory["products"].append(product)

    # Record the monetary value of the stock added.
    inventory["transactions"].append(
        {
            "type": "add_product",
            "product_id": product_id,
            "amount": price * stock,
        }
    )

    print("\nProduct added successfully!\n")


def update_stock(inventory):
    """Find a product and replace its stock quantity."""
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()

    product = find_product(inventory["products"], product_id)
    if product is None:
        print("Product not found.\n")
        return

    print("\nProduct Found:")
    print(f"Name: {product['name']}")
    print(f"Current Stock: {product['stock']}")

    try:
        new_stock = int(input("\nNew Stock Quantity: ").strip())
        if new_stock < 0:
            print("Stock cannot be negative.\n")
            return
    except ValueError:
        print("Please enter a whole number for stock.\n")
        return

    old_stock = product["stock"]
    stock_change = new_stock - old_stock
    transaction_amount = stock_change * product["price"]

    product["stock"] = new_stock

    inventory["transactions"].append(
        {
            "type": "update_stock",
            "product_id": product["id"],
            "amount": transaction_amount,
        }
    )

    print("\nStock updated successfully!\n")


def search_product(inventory):
    """Search for and display a product by ID."""
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()

    product = find_product(inventory["products"], product_id)
    if product is None:
        print("\nProduct not found.\n")
        return

    print("\nProduct Found")
    print("-" * 40)
    display_product(product)
    print("-" * 40 + "\n")


def show_menu():
    """Display the menu options."""
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40 + "\n")

    inventory = load_inventory()

    if os.path.exists(FILENAME):
        print(f"{FILENAME} found.")
        print("Inventory loaded successfully.\n")

    while True:
        show_menu()
        option = input("Enter option: ").strip()

        if option == "1":
            display_all(inventory)
        elif option == "2":
            add_product(inventory)
        elif option == "3":
            update_stock(inventory)
        elif option == "4":
            search_product(inventory)
        elif option == "5":
            print("\nSaving inventory...")
            save_inventory(inventory)
        elif option == "6":
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 6.\n")


if __name__ == "__main__":
    main()