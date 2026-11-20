from models.DiscountStrategy import DiscountStrategy


class PercentageDiscount(DiscountStrategy):

    def __init__(self, percentage: float):
        self.__percentage: float = percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.__percentage / 100)