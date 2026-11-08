import json
from abc import ABC, abstractmethod

# created supplier class
class Supplier:

    def __init__(self, supplier_id: str, name: str, contact_email: str):
        self.__supplier_id: str = supplier_id
        self.__name: str = name
        self.__contact_email: str = contact_email

    def get_supplier_id(self) -> str:
        return self.__supplier_id

    def get_name(self) -> str:
        return self.__name

    def get_contact_email(self) -> str:
        return self.__contact_email

    def display_information(self) -> None:
        print(f"Supplier ID: {self.__supplier_id}")
        print(f"Name: {self.__name}")
        print(f"Contact Email: {self.__contact_email}")

## create product class
class Product(ABC):
 
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier):
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock
        self.__supplier: Supplier = supplier
 
    def get_product_id(self):
        return self.__product_id
 
    def get_name(self):
        return self.__name
 
    def get_price(self):
        return self.__price
 
    def get_stock(self):
        return self.__stock

    def get_supplier(self) -> Supplier:
        return self.__supplier
    
    def update_stock(self, quantity):
        self.__stock = quantity
 
    def display_information(self):
        print("-----------------------------------------")
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")

    @abstractmethod
    def get_fulfilment_info(self):
        pass

class CanBeShipped(ABC):

    @abstractmethod
    def calculate_shipping_cost(self):
        pass

#create PhysicalProduct that inherits from Product
class PhysicalProduct(Product, CanBeShipped):

    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier, weight: float):
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight: float = weight

    def display_information(self):
        super().display_information()
        print(f"Weight: {self.__weight} kg")
        print("-----------------------------------------")

    def get_fulfilment_info(self):
        return "This product requires physical shipping."

    def calculate_shipping_cost(self):
        return 5.00 * self.__weight

    def get_weight(self):
        return self.__weight
            
#create Digitalproduct that inherits from Product
class DigitalProduct(Product):

    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier, download_size: float):
        super().__init__(product_id, name, price, stock, supplier)
        self.__download_size: float = download_size

    def display_information(self):
        super().display_information()
        print(f"Download size: {self.__download_size} MB")
        print("-----------------------------------------")

    def get_fulfilment_info(self):
        return "This product is delivered digitally."

    def get_download_size(self):
        return self.__download_size
        
## inventory class 
class Inventory:
 
    def __init__(self):
        self.__products = []
 
    def add_product(self, product):
        self.__products.append(product)
 
    def search_product(self, product_id):
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None
 
    def display_all(self):
        print("\nCurrent Inventory")
        print("-----------------------------------------")
        if not self.__products:
            print("No products in inventory.")
        for product in self.__products:
            print(f"ID: {product.get_product_id()} | Name: {product.get_name()} | "
                  f"Price: ${product.get_price():.2f} | Stock: {product.get_stock()}")
        print("-----------------------------------------")
 
    def get_products(self):
        return self.__products


##file handling by loading and saving
def load_inventory_data():
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
 
 
def save_inventory(inventory):
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
def add_product_menu(inventory):
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
 
def update_stock_menu(inventory):
    print("\nUpdate Stock")
    p_id = input("Enter Product ID: ")
    product = inventory.search_product(p_id)
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
 
 
def search_product_menu(inventory):
    print("\nSearch Product")
    p_id = input("Enter Product ID: ")
    product = inventory.search_product(p_id)
    if product is None:
        print("Product not found.")
    else:
        print("\nProduct Found")
        product.display_information()
        product.get_supplier().display_information()

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