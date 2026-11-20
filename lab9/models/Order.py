from models.Product import Product
from models.OrderLine import OrderLine
from models.DiscountStrategy import DiscountStrategy
from models.NoDiscount import NoDiscount

## Order creates and manages its own OrderLine objects
class Order:

    def __init__(self, order_id: str, discount: DiscountStrategy | None = None):
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []
        self.__discount: DiscountStrategy = discount if discount is not None else NoDiscount()

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.__discount = discount  

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
        total: float = sum(line.calculate_subtotal() for line in self.__order_lines)
        return self.__discount.apply(total)
    