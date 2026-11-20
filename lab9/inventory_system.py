from models.Supplier import Supplier
from models.Inventory import Inventory
from storage import load_inventory_data, save_inventory
from menus import add_product_menu, update_stock_menu, search_product_menu
from models.ProductFactory import ProductFactory

def main() ->None:
    print("=========================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=========================================")
    
    inventory = Inventory()
    default_supplier = Supplier("S001", "TechSource Ltd", "sales@techsource.com")
    data = load_inventory_data()

    if data is None:
        inventory.add_product(ProductFactory.create("physical", "P001", "Laptop", 1200.00, 15, default_supplier, 2.2))
        inventory.add_product(ProductFactory.create("physical", "P002", "Mouse", 25.50, 40, default_supplier, 0.1))
        inventory.add_product(ProductFactory.create("physical", "P003", "Keyboard", 45.00, 25, default_supplier, 0.8))
    else:
        for item in data:
            try:
                supplier = Supplier(item["supplier_id"], item["supplier_name"], item["supplier_email"])
                extra = item["weight"] if item["type"] == "physical" else item["download_size"]
                inventory.add_product(ProductFactory.create(
                    item["type"], item["id"], item["name"], item["price"],
                    item["stock"], supplier, extra))
            except (KeyError, ValueError) as e:
                print(f"Skipping invalid item in inventory.json: {e}")
    
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