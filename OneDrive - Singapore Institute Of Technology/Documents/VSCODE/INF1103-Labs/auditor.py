

inventory = 0
while inventory == 0:
    userinput = input("Enter the quantity of stock to add: ")

    if userinput == "quit":
        break

    if not userinput.isdigit():
        print("Please enter a valid number")
        invalidcount = 0
        invaidcount=invalidcount + 1
        continue

    userinput = int(userinput)
    if userinput < 0:
        print("Please enter a positive number")
        continue
    invalidcount = invalidcount + 1
    if userinput > 500:
        print("Alert: Stock level is high!")
        break

    inventory = userinput
    print("Inventory updated to:", inventory)