inventory=0
failed_entry=0
while True:
    new_stock=input("How many stocks to add, or type 'quit' to leave:")
    if new_stock.lower() == "quit":
        print('Total inventory:',inventory)
        print('failed entries:', failed_entry)
        break
    
    if not new_stock.isdigit():
        print("please type a positive integer.")
        failed_entry+=1
        continue
    
    new_stock= int(new_stock)

    inventory+= new_stock
    print('new stock accepted')
    print('Total inventory:',inventory)
    print('failed entries:', failed_entry)


    if inventory==500:
        print("full stock")
        break
    elif inventory>500:
        print('stock overload')
        break
