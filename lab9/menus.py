from models.Inventory import Inventory
from models.Product import Product
from models.Supplier import Supplier
from models.ProductFactory import ProductFactory
from input_helpers import get_positive_float, get_non_negative_int

## functions to add, update, and search
def add_product_menu(inventory: Inventory) -> None:
    print("\nAdd New Product")
    print("1. Physical product")
    print("2. Digital product")
    choice = input("Choose product type: ")
    if choice not in ("1", "2"):
        print("Invalid product type.")
        return
    product_type = "physical" if choice == "1" else "digital"

    p_id = input("Product ID: ")
    name = input("Product Name: ")
    s_id = input("Supplier ID: ")
    s_name = input("Supplier Name: ")
    s_email = input("Supplier Email: ")
    supplier = Supplier(s_id, s_name, s_email)

    price = get_positive_float("Price: ")
    stock = get_non_negative_int("Stock Quantity: ")
    if product_type == "physical":
        extra = get_positive_float("Weight (kg): ")
    else:
        extra = get_positive_float("Download size (MB): ")

    product = ProductFactory.create(product_type, p_id, name, price, stock, supplier, extra)
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
    
    new_stock = get_non_negative_int("New Stock Quantity: ")
    product.update_stock(new_stock)
    print("\nStock updated successfully!")
 
 
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
