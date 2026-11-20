from models.Product import Product
from models.PhysicalProduct import PhysicalProduct
from models.DigitalProduct import DigitalProduct
from models.Supplier import Supplier


class ProductFactory:

    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock: int, supplier: Supplier, extra: float = 0.0) -> Product:
        # extra is the weight (physical) or the download size (digital)
        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock, supplier, extra)
        elif product_type == "digital":
            return DigitalProduct(product_id, name, price, stock, supplier, extra)
        else:
            raise ValueError(f"Unknown product type: {product_type}")