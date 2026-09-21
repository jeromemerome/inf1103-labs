def get_valid_input():
    userinput = input("Enter the inventory to add: ")

    if userinput.lower() == "quit":
        return "quit"
    
    if userinput.isdigit():
        return int(userinput)
    
    else:
        print("Invalid input. Please enter a valid non-negative number.")
        return "invalid"


def process_delivery(current_total, new_value):
    return current_total + new_value


def calculate_tax(amount):
    return amount * 0.10


def generate_report(total_units, failed_attempts, total_tax, deliveries_count):
    print("Total units processed:", total_units)
    print("Total tax calculated: $" + str(total_tax))
    print("Total Deliveries Processed:", deliveries_count)
    print("failed entries:", failed_attempts)



inventory = 0
invalidcount = 0
total_tax = 0
deliveries_count = 0

while True:
    entry = get_valid_input()

    if entry == "quit":
        generate_report(inventory, invalidcount, total_tax, deliveries_count)
        break
    elif entry == "invalid":
        invalidcount += 1
        continue
    else:
        inventory = process_delivery(inventory, entry)
        print("Units added: " + str(entry))
        print("Current inventory: " + str(inventory))
        print("tax calculated for this entry: $" + str(calculate_tax(entry)))
        total_tax += calculate_tax(entry)
        deliveries_count += 1

    if inventory > 500:
        print("Inventory limit exceeded! Current total "+ str(inventory) +" is over 500. Stopping program...")
        generate_report(inventory, invalidcount, total_tax, deliveries_count)
        break

