import os

FILENAME = "inventory.txt"


def get_valid_input():
    product_name = input("Enter Product Name: ")

    if product_name.lower() == "quit":
        return "quit", "quit"

    # Allow spaces in product names (e.g., "Laptop Stand")
    valid_name = len(product_name.strip()) > 0 and product_name.replace(
        " ", ""
    ).isalpha()

    if not valid_name:
        print("Invalid product name. Please enter a valid name.\n")
        return "invalid", "invalid"

    userinput = input("Enter Quantity: ")
    if userinput.lower() == "quit":
        return "quit", "quit"

    valid_number = userinput.isdigit() and int(userinput) >= 0

    if not valid_number:
        print(
            "Invalid quantity value. Please enter a valid non-negative number.\n"
        )
        return "invalid", "invalid"

    return product_name.strip(), int(userinput)


def load_inventory():
    """Loads existing inventory from inventory.txt into an in-memory list."""
    product_list = []
    next_id = 1001
    inventory = 0

    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r") as file:
                for line in file:
                    line = line.strip()
                    if line:
                        parts = line.split(",")
                        item_id = int(parts[0].strip())
                        name = parts[1].strip()
                        qty = int(parts[2].strip())

                        product_list.append(
                            {"id": item_id, "name": name, "quantity": qty}
                        )

                        inventory += qty
                        if item_id >= next_id:
                            next_id = item_id + 1
        except (ValueError, IndexError):
            print(f"Error reading {FILENAME}. Starting fresh.\n")

    return product_list, next_id, inventory


def save_inventory(product_list):
    """Saves the current in-memory array list to inventory.txt."""
    with open(FILENAME, "w") as file:
        for item in product_list:
            file.write(f"{item['id']},{item['name']},{item['quantity']}\n")


def add_to_inventory_list(product_list, item_id, name, qty):
    """Appends a new order to the temporary array list in memory."""
    product_list.append({"id": item_id, "name": name, "quantity": qty})


def process_delivery(current_total, new_value):
    return current_total + new_value


def calculate_tax(amount):
    return amount * 0.10


def generate_report(
    product_list, total_units, failed_attempts, total_tax, deliveries_count
):
    print("Current Orders:")
    if not product_list:
        print("  (No orders placed yet)")
    else:
        for item in product_list:
            print(f" {item['id']} ,  {item['name']} , {item['quantity']}")
    print()


invalidcount = 0
total_tax = 0
deliveries_count = 0

# Load existing orders from file at startup into array list
product_list, next_id, inventory = load_inventory()

while True:
    # Print current orders before asking for product input
    generate_report(
        product_list, inventory, invalidcount, total_tax, deliveries_count
    )

    prod_name, entry = get_valid_input()

    if prod_name == "quit" or entry == "quit":
        # Save to inventory.txt ONLY when quitting
        save_inventory(product_list)
        break

    if prod_name == "invalid" or entry == "invalid":
        invalidcount += 1
        continue

    # Store order temporarily in the in-memory array list
    add_to_inventory_list(product_list, next_id, prod_name, entry)

    print("\nNew Order Added:")
    print(f"{next_id},{prod_name},{entry}\n")

    next_id += 1
    inventory = process_delivery(inventory, entry)
    total_tax += calculate_tax(entry)
    deliveries_count += 1

    if inventory > 500:
        print(
            f"Inventory limit exceeded! Current total {inventory} is over 500. Stopping program..."
        )
        save_inventory(product_list)
        break