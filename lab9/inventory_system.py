import json
from models.Supplier import Supplier
from models.Product import Product
from models.PhysicalProduct import PhysicalProduct
from models.DigitalProduct import DigitalProduct
        
## inventory class 
# Inventory groups Product objects, but the products can exist independently of the inventory
class Inventory:

    def __init__(self):
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> None:
        self.__products.append(product)

    def remove_product(self, product_id: str) -> None:
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def display_all(self) -> None:
        print("\nCurrent Inventory")
        print("-----------------------------------------")
        if not self.__products:
            print("No products in inventory.")
        for product in self.__products:
            print(f"ID: {product.get_product_id()} | Name: {product.get_name()} | "
                  f"Price: ${product.get_price():.2f} | Stock: {product.get_stock()}")
        print("-----------------------------------------")

    def get_products(self) -> list[Product]:
        return self.__products

## OrderLine represents one product and the quantity of that product requested in an order
class OrderLine:

    def __init__(self, product: Product, quantity: int):
        self.__product: Product = product
        self.__quantity: int = quantity

    def get_product(self) -> Product:
        return self.__product

    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity

    def display_information(self) -> None:
        print(f"{self.__product.get_name()} x {self.__quantity} = ${self.calculate_subtotal():.2f}")

## Order creates and manages its own OrderLine objects
class Order:

    def __init__(self, order_id: str):
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> None:
        for line in self.__order_lines:
            if line.get_product().get_product_id() == product_id:
                self.__order_lines.remove(line)
                return

    def get_order_lines(self) -> list[OrderLine]:
        return self.__order_lines

    def calculate_total(self) -> float:
        total: float = 0.0
        for line in self.__order_lines:
            total += line.calculate_subtotal()
        return total
    
##file handling by loading and saving
def load_inventory_data() -> list | None:
    try:
        with open("inventory.json", "r") as file:
            data = json.load(file)
        print("\ninventory.json found.")
        print("Inventory loaded successfully.")
        return data
    except FileNotFoundError:
        print("\ninventory.json not found. Using default inventory.")
        return None
    except Exception as e:
        print(f"\nError reading file: {e}. Using default inventory.")
        return None
 
def save_inventory(inventory: Inventory) -> None:
    print("\nSaving inventory...")
    try:
        data = []
        for product in inventory.get_products():
            supplier = product.get_supplier()
            item = {
                "id": product.get_product_id(),
                "name": product.get_name(),
                "price": product.get_price(),
                "stock": product.get_stock(),
                "supplier_id": supplier.get_supplier_id(),
                "supplier_name": supplier.get_name(),
                "supplier_email": supplier.get_contact_email()
            }
            if isinstance(product, PhysicalProduct):
                item["type"] = "physical"
                item["weight"] = product.get_weight()
            elif isinstance(product, DigitalProduct):
                item["type"] = "digital"
                item["download_size"] = product.get_download_size()
            data.append(item)
        with open("inventory.json", "w") as file:
            json.dump(data, file, indent=4)
        print("Inventory saved successfully to inventory.json.")
    except Exception as e:
        print(f"Error saving inventory: {e}")

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
            product = PhysicalProduct(p_id, name, price, stock, supplier, weight)
        else:
            size = float(input("Download size (MB): "))
            product = DigitalProduct(p_id, name, price, stock, supplier, size)
    except ValueError:
        print("Invalid number entered.")
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

def main() ->None:
    print("=========================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=========================================")
    
    # create the inventory object and fill it with product details
    inventory = Inventory()
    data = load_inventory_data()

    if data is None:
        default_supplier = Supplier("S001", "TechSource Ltd", "sales@techsource.com")
        inventory.add_product(PhysicalProduct("P001", "Laptop", 1200.00, 15, default_supplier, 2.2))
        inventory.add_product(PhysicalProduct("P002", "Mouse", 25.50, 40, default_supplier, 0.1))
        inventory.add_product(PhysicalProduct("P003", "Keyboard", 45.00, 25, default_supplier, 0.8))
    else:
        for item in data:
            supplier = Supplier(item["supplier_id"], item["supplier_name"], item["supplier_email"])
            if item["type"] == "physical":
                inventory.add_product(PhysicalProduct(item["id"], item["name"], item["price"], item["stock"], supplier, item["weight"]))
            elif item["type"] == "digital":
                inventory.add_product(DigitalProduct(item["id"], item["name"], item["price"], item["stock"], supplier, item["download_size"]))            

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
            inventory.display_all()
        elif option == "2":
            add_product_menu(inventory)
        elif option == "3":
            update_stock_menu(inventory)
        elif option == "4":
            search_product_menu(inventory)
        elif option == "5":
            save_inventory(inventory)
        elif option == "6":
            save_inventory(inventory)
            print("Exiting program.")
            break
        else:
            print("Invalid option. Please choose between 1 and 6.")

if __name__ == "__main__":
    main()