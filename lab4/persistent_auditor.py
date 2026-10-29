filename = "inventory.txt"
failed_attempts = 0
deliveries_processed = 0


def load_inventory():
    orders = []
    file = open(filename, "a")
    file.close()

    file = open(filename, "r")
    lines = file.readlines()
    file.close()

    for line in lines:
        line = line.strip()
        if line != "":
            parts = line.split(",")
            orders.append(parts)

    return orders

def save_inventory(orders):
    file = open(filename, "w")
    for item in orders:
        file.write(item[0] + "," + item[1] + "," + item[2] + "\n")
    file.close()
    
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

orders = load_inventory()

print("Current Orders:\n")
if len(orders) == 0:
    print("No orders found in inventory.txt")
else:
    for item in orders:
        print(item[0] + ", " + item[1] + ", " + item[2])
    print()

while True:
    product_name = input(
        "Enter Product Name (or type 'quit' to exit): "
    ).strip()

    if product_name.lower() == "quit":
        save_inventory(orders)
        generate_report(deliveries_processed, failed_attempts)
        break

    while True:
        quantity_input = input("Enter Quantity: ").strip()

        if quantity_input.lower() == "quit":
            product_name = "quit"
            break

        if not quantity_input.isdigit():
            print("type a valid integer.")
            failed_attempts += 1
            continue

        quantity = int(quantity_input)
        break

    if product_name.lower() == "quit":
        save_inventory(orders)
        generate_report(deliveries_processed, failed_attempts)
        break

    next_id = str(1001 + len(orders))

    new_order = [next_id, product_name, str(quantity)]
    orders.append(new_order)

    tax = calculate_tax(quantity)
    deliveries_processed += 1

    print("\nNew Order Added:")
    print(new_order[0] + ", " + new_order[1] + ", " + new_order[2])
    print("Tax for this entry: {:.2f}\n".format(tax))