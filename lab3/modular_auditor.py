inventory = 0
failed_attempts = 0
deliveries_processed = 0

def get_valid_input():
    global failed_attempts
    while True:
        new_stock = input("How many stocks to add, or type 'quit' to leave: ")

        if new_stock.lower() == "quit":
            return "quit"

        if not new_stock.isdigit():
            print("type a valid integer.")
            failed_attempts +=1
            continue

        return int(new_stock)

def process_delivery(current_total,new_value):
    new_total = current_total +new_value    
    return new_total

def calculate_tax(amount):
    tax = amount * 0.10
    return tax

def generate_report(total_units, failed_attempts):
    print('Final Summary:')
    print('Total deliveries processed:', total_units)
    print('number of failed entries:', failed_attempts)


while True:
    new_stock = get_valid_input()

    if new_stock =="quit":
        generate_report(deliveries_processed, failed_attempts)
        break

    inventory = process_delivery(inventory, new_stock)

    tax = calculate_tax(new_stock)

    print("new stock received")
    print("Total inventory:", inventory)
    print("Tax for this: {:.2f}".format(tax))

    deliveries_processed +=1