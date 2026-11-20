from models.Product import Product
from models.Supplier import Supplier

#create Digitalproduct that inherits from Product
class DigitalProduct(Product):

    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier, download_size: float):
        super().__init__(product_id, name, price, stock, supplier)
        self.__download_size: float = download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"Download size: {self.__download_size} MB")
        print("-----------------------------------------")

    def get_fulfilment_info(self) -> str:
        return "This product is delivered digitally."

    def get_download_size(self) -> float:
        return self.__download_size