
invalidcount = 0
inventory = 0
while inventory <=500:
    userinput = input("Enter the inventory to add: ")
    stock = 0
    
    if userinput == "quit":
        print("Total units processed: ", inventory)
        print("failed entries: ", invalidcount)
        break

    elif not userinput.isdigit():
        print("Invalid input. Please enter a valid number.")
        invalidcount += 1
        continue
    elif stock < 0:
        print("Inventory cannot be negative. Please enter a valid number.")
        invalidcount += 1
        continue
    else:
        stock = int(userinput)
        print ("Units added:" + str(stock))
        inventory += stock
        if inventory > 500:
            print("Inventory limit exceeded. Current inventory: " + str(inventory))
            break
        else:
            continue
 
    

    