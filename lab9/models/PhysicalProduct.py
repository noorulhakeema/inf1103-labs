from models.Product import Product
from models.CanBeShipped import CanBeShipped
from models.Supplier import Supplier

#create PhysicalProduct that inherits from Product
class PhysicalProduct(Product, CanBeShipped):

    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier, weight: float):
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight: float = weight

    def display_information(self) -> None:
        super().display_information()
        print(f"Weight: {self.__weight} kg")
        print("-----------------------------------------")

    def get_fulfilment_info(self) -> str:
        return "This product requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        return 5.00 * self.__weight

    def get_weight(self) -> float:
        return self.__weight