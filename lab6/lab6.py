import json

## create product class
class Product:
 
    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock
 
    def get_product_id(self):
        return self.__product_id
 
    def get_name(self):
        return self.__name
 
    def get_price(self):
        return self.__price
 
    def get_stock(self):
        return self.__stock
 
    def update_stock(self, quantity):
        self.__stock = quantity
 
    def display_information(self):
        print("-----------------------------------------")
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")
        print("-----------------------------------------")

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
            data.append({
                "id": product.get_product_id(),
                "name": product.get_name(),
                "price": product.get_price(),
                "stock": product.get_stock()
            })
        with open("inventory.json", "w") as file:
            json.dump(data, file, indent=4)
        print("Inventory saved successfully to inventory.json.")
    except Exception as e:
        print(f"Error saving inventory: {e}")

## functions to add, update, and search
def add_product_menu(inventory):
    print("\nAdd New Product")
    p_id = input("Product ID: ")
    name = input("Product Name: ")
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("Invalid price or stock amount.")
        return
 
    product = Product(p_id, name, price, stock)
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

