import json
from models.Inventory import Inventory
from models.PhysicalProduct import PhysicalProduct
from models.DigitalProduct import DigitalProduct
import csv
from models.Supplier import Supplier
from models.ProductFactory import ProductFactory

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

def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    loaded = 0
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            next(reader, None)  # skip the header row
            for row_number, row in enumerate(reader, start=2):
                try:
                    product_type, product_id, name, price, stock = row
                    product = ProductFactory.create(product_type, product_id, name,
                                                    float(price), int(stock), supplier)
                    inventory.add_product(product)
                    loaded += 1
                except ValueError as e:
                    print(f"Skipping row {row_number}: {e}")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")