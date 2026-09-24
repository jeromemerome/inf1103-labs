def get_valid_input():
    product_name = input("Enter Product Name: ")
    
    if product_name.lower() == "quit":
        return "quit", "quit"
    
    valid_name = product_name.isalpha() and len(product_name) > 0
   
  
    if not valid_name:
        print("Invalid product name. Please enter a valid name.")
        return "invalid", "invalid"  
    
    userinput = input("Enter Inventory: ")
    valid_number = userinput.isdigit() and int(userinput) >= 0
    if userinput.lower() == "quit":
        return "quit", "quit"

    
    if not valid_number:
        print("Invalid inventory value. Please enter a valid non-negative number.")
        return "invalid", "invalid"
    
    return product_name, int(userinput)

def load_inventory():
    product_list=[]
    next_id = 1001
    inventory = 0
    return product_list, next_id, inventory

def save_inventory(product_list, item_id, name, qty):
    product_list.append({
        "id": item_id,
        "name": name,
        "quantity": qty
    })


def process_delivery(current_total, new_value):
    return current_total + new_value


def calculate_tax(amount):
    return amount * 0.10


def generate_report(total_units, failed_attempts, total_tax, deliveries_count):
    print("Current Orders: ")
    for item in product_list:
            print(f" {item['id']} ,  {item['name']} , {item['quantity']}")




invalidcount = 0
total_tax = 0
deliveries_count = 0
product_list , next_id , inventory = load_inventory()

while True:
    prod_name,entry = get_valid_input()
    if prod_name == "quit":
        generate_report(inventory, invalidcount, total_tax, deliveries_count)
        break

    if entry == "quit":
        generate_report(inventory, invalidcount, total_tax, deliveries_count)
        break

    if prod_name == "invalid" or entry == "invalid":
        invalidcount += 1
        continue
   
    else:
        save_inventory(product_list, next_id, prod_name, entry)
        next_id +=1
        
        inventory = process_delivery(inventory, entry)
        print("Product added: " + str(prod_name))
        print("Stock added: " + str(entry))
        print("Current inventory: " + str(inventory))
        total_tax += calculate_tax(entry)
        deliveries_count += 1

    if inventory > 500:
        print("Inventory limit exceeded! Current total "+ str(inventory) +" is over 500. Stopping program...")
        generate_report(inventory, invalidcount, total_tax, deliveries_count)
        break

