# step 1, initialising variables
inventory=0
failed_entry=0
#while loop for iteration
while True:
    new_stock=input("How many stocks to add, or type 'quit' to leave:")
    #step 2 & 8, quit logic
    if new_stock.lower() == "quit":
        print('Total inventory:',inventory)
        print('failed entries:', failed_entry)
        break
    #step 3 to 5, rejecting negative and letters
    if not new_stock.isdigit():
        print("please type a positive integer.")
        failed_entry+=1
        continue
    #step 6, managing state
    new_stock= int(new_stock)

    #reporting
    inventory+= new_stock
    print('new stock accepted')
    print('Total inventory:',inventory)
    print('failed entries:', failed_entry)

    #step 7, overstocking
    if inventory==500:
        print("full stock")
        break
    elif inventory>500:
        print('stock overload')
        break
