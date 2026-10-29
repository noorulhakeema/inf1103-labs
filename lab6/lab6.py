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
