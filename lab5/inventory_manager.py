import json

inventory = [
    {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
    {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
    {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25}
]


def display_all(inventory_list):
    print("\nCurrent Inventory")
    print("-----------------------------------------")
    if not inventory_list:
        print("No products in inventory.")
    for item in inventory_list:
        print(f"ID: {item['id']} | Name: {item['name']} | Price: ${item['price']:.2f} | Stock: {item['stock']}")
    print("-----------------------------------------")

def add_product(inventory_list):
    print("\nAdd New Product")
    p_id = input("Product ID: ")
    name = input("Product Name: ")
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("Invalid price or stock amount.")
        return

    inventory_list.append({
        "id": p_id,
        "name": name,
        "price": price,
        "stock": stock
    })
    print("Product added successfully!")

def update_stock(inventory_list):
    print("\nUpdate Stock")
    p_id = input("Enter Product ID: ")
    for item in inventory_list:
        if item["id"] == p_id:
            print(f"\nProduct Found:")
            print(f"Name: {item['name']}")
            print(f"Current Stock: {item['stock']}\n")
            try:
                new_stock = int(input("New Stock Quantity: "))
                item["stock"] = new_stock
                print("\nStock updated successfully!")
            except ValueError:
                print("Invalid stock number.")
            return
    print("Product not found.")

def search_product(inventory_list):
    print("\nSearch Product")
    p_id = input("Enter Product ID: ")
    for item in inventory_list:
        if item["id"] == p_id:
            print("\nProduct Found")
            print("-----------------------------------------")
            print(f"ID: {item['id']}")
            print(f"Name: {item['name']}")
            print(f"Price: ${item['price']:.2f}")
            print(f"Stock: {item['stock']}")
            print("-----------------------------------------")
            return
    print("Product not found.")

def load_inventory():
    filename = "inventory.json"
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            print("\ninventory.json found.")
            print("Inventory loaded successfully.")
            return data
    except FileNotFoundError:
        print("\ninventory.json not found. Using default inventory.")
        return inventory
    except Exception as e:
        print(f"\nError reading file: {e}. Using default inventory.")
        return inventory

def save_inventory(inventory_list):
    print("\nSaving inventory...")
    try:
        with open("inventory.json", "w") as file:
            json.dump(inventory_list, file, indent=4)
        print("Inventory saved successfully to inventory.json.")
    except Exception as e:
        print(f"Error saving inventory: {e}")


print("=========================================")
print("INVENTORY MANAGEMENT SYSTEM")
print("=========================================")

current_inventory = load_inventory()


while True:
    print("\n--------- MENU ---------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("------------------------")

    option = input("\nEnter option: ")

    if option == "1":
        display_all(current_inventory)
    elif option == "2":
        add_product(current_inventory)
    elif option == "3":
        update_stock(current_inventory)
    elif option == "4":
        search_product(current_inventory)
    elif option == "5":
        save_inventory(current_inventory)
    elif option == "6":
        save_inventory(current_inventory)
        print("Exiting program.")
        break
    else:
        print("Invalid option. Please choose between 1 and 6.")