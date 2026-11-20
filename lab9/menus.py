from models.Inventory import Inventory
from models.Product import Product
from models.Supplier import Supplier
from models.ProductFactory import ProductFactory

## functions to add, update, and search
def add_product_menu(inventory: Inventory) -> None:
    print("\nAdd New Product")
    print("1. Physical product")
    print("2. Digital product")
    choice = input("Choose product type: ")
    if choice not in ("1", "2"):
        print("Invalid product type.")
        return

    p_id = input("Product ID: ")
    name = input("Product Name: ")
    s_id = input("Supplier ID: ")
    s_name = input("Supplier Name: ")
    s_email = input("Supplier Email: ")
    supplier = Supplier(s_id, s_name, s_email)
    
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
        if choice == "1":
            weight = float(input("Weight (kg): "))
            product = ProductFactory.create("physical", p_id, name, price, stock, supplier, weight)
        else:
            size = float(input("Download size (MB): "))
            product = ProductFactory.create("digital", p_id, name, price, stock, supplier, size)
    except ValueError as e:
        print(f"Invalid input: {e}")
        return

    inventory.add_product(product)
    print("Product added successfully!")
 
def update_stock_menu(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    p_id = input("Enter Product ID: ")
    product = inventory.find_product(p_id)
    if product is None:
        print("Product not found.")
        return
 
    print("\nProduct Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}\n")
    try:
        new_stock = int(input("New Stock Quantity: "))
        product.update_stock(new_stock)
        print("\nStock updated successfully!")
    except ValueError:
        print("Invalid stock number.")
 
 
def search_product_menu(inventory: Inventory) -> None:
    print("\nSearch Product")
    p_id = input("Enter Product ID: ")
    product = inventory.find_product(p_id)
    if product is None:
        print("Product not found.")
    else:
        print("\nProduct Found")
        product.display_information()
        product.get_supplier().display_information()

def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())
