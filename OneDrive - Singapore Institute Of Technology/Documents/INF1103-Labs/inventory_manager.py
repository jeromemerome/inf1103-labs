import json
import os

# The file where products and transaction history will be stored.
FILENAME = "inventory.json"


class Product:
    """Represents one product and controls its own information."""

    def __init__(self, product_id, name, price, stock):
        # Check that the information used to create the product is valid.
        if not product_id.strip():
            raise ValueError("Product ID cannot be empty.")
        if not name.strip():
            raise ValueError("Product name cannot be empty.")
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if not isinstance(stock, int) or isinstance(stock, bool) or stock < 0:
            raise ValueError("Stock must be a non-negative whole number.")

        # Double underscores indicate attributes intended to be private.
        self.__product_id = product_id.strip()
        self.__name = name.strip()
        self.__price = float(price)
        self.__stock = stock

    # These properties let other code read product details without
    # directly changing the private attributes.
    @property
    def product_id(self):
        return self.__product_id

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @property
    def stock(self):
        return self.__stock

    def update_stock(self, quantity):
        # Change stock through this method so the value can be checked first.
        # Here, quantity means the new total stock, not the amount to add.
        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise ValueError("Stock must be a whole number.")
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")

        self.__stock = quantity

    def display_information(self):
        # Print this product's information in a readable format.
        print(
            f"ID: {self.__product_id} | "
            f"Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | "
            f"Stock: {self.__stock}"
        )

    def to_dict(self):
        # Convert the object into a dictionary so json.dump can save it.
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }


class Inventory:
    """Manages a collection of Product objects."""

    def __init__(self):
        # The inventory keeps its own list of Product objects.
        self.__products = []

    def add_product(self, product):
        # Only Product objects should be added to the inventory.
        if not isinstance(product, Product):
            raise TypeError("Only Product objects can be added.")

        # Product IDs must be unique.
        if self.search_product(product.product_id) is not None:
            return False

        self.__products.append(product)
        return True

    def search_product(self, product_id):
        # Search IDs without distinguishing uppercase and lowercase letters.
        for product in self.__products:
            if product.product_id.lower() == product_id.strip().lower():
                return product

        # Return None when no matching product is found.
        return None

    def display_all(self):
        # Display all products in the inventory.
        print("\nCurrent Inventory")
        print("-" * 60)

        if not self.__products:
            print("No products in inventory.")
        else:
            # Ask each Product object to display its own information.
            for product in self.__products:
                product.display_information()

        print("-" * 60 + "\n")

    def get_products(self):
        # Return a copy of the list for saving.
        # A copy prevents outside code from replacing the inventory's list.
        return self.__products.copy()


def load_inventory():
    # Create an empty Inventory object and transaction list.
    inventory = Inventory()
    transactions = []

    # If the file does not exist yet, start with empty data.
    if not os.path.exists(FILENAME):
        print(f"{FILENAME} not found. Starting with an empty inventory.\n")
        return inventory, transactions

    try:
        # Open and read the JSON file.
        with open(FILENAME, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Support an older file that contains only a list of products.
        if isinstance(data, list):
            product_data = data

        # Current format stores products and transactions in a dictionary.
        elif isinstance(data, dict):
            product_data = data.get("products", [])
            transactions = data.get("transactions", [])

        else:
            raise ValueError("Unexpected JSON format.")

        # Turn each saved product dictionary back into a Product object.
        for item in product_data:
            product = Product(
                item["id"],
                item["name"],
                float(item["price"]),
                int(item["stock"]),
            )

            # Add the object to the inventory unless its ID is duplicated.
            if not inventory.add_product(product):
                print(f"Skipping duplicate product ID: {product.product_id}")

        # Make sure transaction history has the expected list format.
        if not isinstance(transactions, list):
            transactions = []

        print(f"{FILENAME} found.")
        print("Inventory loaded successfully.\n")

    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        # If the file is missing required data or cannot be read,
        # continue with an empty inventory.
        print(f"Could not load inventory: {error}")
        print("Starting with an empty inventory.\n")
        inventory = Inventory()
        transactions = []

    return inventory, transactions


def save_inventory(inventory, transactions):
    # Convert Product objects into dictionaries for JSON storage.
    data = {
        "products": [product.to_dict() for product in inventory.get_products()],
        "transactions": transactions,
    }

    try:
        # Write the data to the JSON file.
        with open(FILENAME, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        print(f"Inventory saved successfully to {FILENAME}.\n")

    except OSError as error:
        print(f"Could not save inventory: {error}\n")


def add_product(inventory, transactions):
    # Get product details from the user.
    print("\nAdd New Product")

    product_id = input("Product ID: ").strip()
    name = input("Product Name: ").strip()

    try:
        price = float(input("Price: ").strip())
        stock = int(input("Stock Quantity: ").strip())

        # Create a Product object using the user's details.
        product = Product(product_id, name, price, stock)

        # Ask the Inventory object to store the new Product object.
        if not inventory.add_product(product):
            print("A product with that ID already exists.\n")
            return

        # Record the value of the stock added.
        transactions.append(
            {
                "type": "add_product",
                "product_id": product.product_id,
                "amount": product.price * product.stock,
            }
        )

        print("\nProduct added successfully!\n")

    except ValueError as error:
        # This catches invalid numbers and invalid product details.
        print(f"Invalid product details: {error}\n")


def update_stock(inventory, transactions):
    # Find a product before asking for its new stock quantity.
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()

    product = inventory.search_product(product_id)

    if product is None:
        print("Product not found.\n")
        return

    print("\nProduct Found:")
    print(f"Name: {product.name}")
    print(f"Current Stock: {product.stock}")

    try:
        new_stock = int(input("\nNew Stock Quantity: ").strip())
        old_stock = product.stock

        # Update stock by calling the Product method.
        product.update_stock(new_stock)

        # Calculate the value change.
        # A negative amount means the stock value decreased.
        amount = (new_stock - old_stock) * product.price

        # Save this change in the transaction history.
        transactions.append(
            {
                "type": "update_stock",
                "product_id": product.product_id,
                "amount": amount,
            }
        )

        print("\nStock updated successfully!\n")

    except ValueError as error:
        print(f"Invalid stock quantity: {error}\n")


def search_product(inventory):
    # Ask the Inventory object to search for the requested ID.
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()

    product = inventory.search_product(product_id)

    if product is None:
        print("\nProduct not found.\n")
        return

    # The Product object displays its own information.
    print("\nProduct Found")
    print("-" * 40)
    product.display_information()
    print("-" * 40 + "\n")


def show_menu():
    # Print the available program actions.
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def main():
    # Display the program title.
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40 + "\n")

    # Load saved data before showing the menu.
    inventory, transactions = load_inventory()

    # Keep showing the menu until the user chooses Exit.
    while True:
        show_menu()
        option = input("Enter option: ").strip()

        if option == "1":
            inventory.display_all()

        elif option == "2":
            add_product(inventory, transactions)

        elif option == "3":
            update_stock(inventory, transactions)

        elif option == "4":
            search_product(inventory)

        elif option == "5":
            print("\nSaving inventory...")
            save_inventory(inventory, transactions)

        elif option == "6":
            # Save automatically before closing the program.
            print("\nSaving inventory before exit...")
            save_inventory(inventory, transactions)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break

        else:
            print("Invalid option. Please enter a number from 1 to 6.\n")


# Run main() only when this file is started directly.
if __name__ == "__main__":
    main()