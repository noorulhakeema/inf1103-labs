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
