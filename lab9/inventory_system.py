from models.Supplier import Supplier
from models.PhysicalProduct import PhysicalProduct
from models.DigitalProduct import DigitalProduct
from models.Inventory import Inventory
from storage import load_inventory_data, save_inventory
from menus import add_product_menu, update_stock_menu, search_product_menu

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