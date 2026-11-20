import inspect
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from models.Supplier import Supplier
from models.ProductFactory import ProductFactory
from models.PhysicalProduct import PhysicalProduct
from models.DigitalProduct import DigitalProduct
from models.Inventory import Inventory
from models.OrderLine import OrderLine
from models.Order import Order
from models.DiscountStrategy import DiscountStrategy
from models.PercentageDiscount import PercentageDiscount
from models.BulkDiscount import BulkDiscount
from models.StudentDiscount import StudentDiscount
from input_helpers import get_positive_float
from storage import load_products

CSV_TEXT = """product_type,product_id,name,price,stock_quantity
physical,P001,Desk Lamp,25.00,10
digital,D001,Photo Editor,49.90,100
service,S001,Installation,30.00,5
physical,P002,Office Chair,abc,3
physical,P003,Monitor Stand,39.50,7
"""


def make_supplier() -> Supplier:
    return Supplier("S001", "TechSource Ltd", "sales@techsource.com")


class TestDiscounts(unittest.TestCase):

    def setUp(self):
        product = ProductFactory.create("physical", "P001", "Desk", 250.0, 10, make_supplier(), 1.0)
        self.order = Order("O001", BulkDiscount(200, 20))
        self.order.add_order_line(product, 1)

    def test_default_is_no_discount(self):
        order = Order("O002")
        order.add_order_line(ProductFactory.create("digital", "D001", "App", 250.0, 5, make_supplier(), 1.0), 1)
        self.assertAlmostEqual(order.calculate_total(), 250.0)

    def test_bulk_discount_applied(self):
        self.assertAlmostEqual(self.order.calculate_total(), 230.0)

    def test_bulk_discount_below_threshold(self):
        self.assertAlmostEqual(BulkDiscount(200, 20).apply(150), 150)

    def test_set_discount_changes_strategy(self):
        self.order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(self.order.calculate_total(), 225.0)

    def test_student_discount(self):
        self.order.set_discount(StudentDiscount())
        self.assertAlmostEqual(self.order.calculate_total(), 237.5)

    def test_new_strategy_needs_no_change_to_order(self):
        class HalfPrice(DiscountStrategy):
            def apply(self, total: float) -> float:
                return total / 2
        self.order.set_discount(HalfPrice())
        self.assertAlmostEqual(self.order.calculate_total(), 125.0)

    def test_order_has_no_discount_elif_logic(self):
        self.assertNotIn("elif", inspect.getsource(Order))


class TestFactory(unittest.TestCase):

    def test_creates_physical(self):
        p = ProductFactory.create("physical", "P1", "Lamp", 10.0, 1, make_supplier(), 2.0)
        self.assertIsInstance(p, PhysicalProduct)

    def test_creates_digital(self):
        p = ProductFactory.create("digital", "D1", "App", 10.0, 1, make_supplier(), 2.0)
        self.assertIsInstance(p, DigitalProduct)

    def test_unknown_type_raises_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            ProductFactory.create("service", "S1", "Install", 10.0, 1, make_supplier())
        self.assertIn("Unknown product type: service", str(ctx.exception))


class TestValidation(unittest.TestCase):

    def test_price_must_be_positive(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P1", "Lamp", 0, 1, make_supplier(), 1.0)
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P1", "Lamp", -5, 1, make_supplier(), 1.0)

    def test_stock_cannot_be_negative(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D1", "App", 10.0, -1, make_supplier(), 1.0)

    def test_update_stock_cannot_be_negative(self):
        p = ProductFactory.create("digital", "D1", "App", 10.0, 1, make_supplier(), 1.0)
        with self.assertRaises(ValueError):
            p.update_stock(-3)

    def test_order_line_quantity_must_be_positive(self):
        p = ProductFactory.create("physical", "P1", "Lamp", 10.0, 5, make_supplier(), 1.0)
        with self.assertRaises(ValueError):
            OrderLine(p, 0)
        with self.assertRaises(ValueError):
            OrderLine(p, -2)


class TestUserInput(unittest.TestCase):

    def test_get_positive_float_asks_again(self):
        buffer = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
            with redirect_stdout(buffer):
                result = get_positive_float("Price: ")
        self.assertEqual(result, 12.5)
        self.assertIn("valid number", buffer.getvalue())
        self.assertIn("greater than zero", buffer.getvalue())


class TestLoadProducts(unittest.TestCase):

    def test_missing_file_is_handled(self):
        inventory = Inventory()
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            load_products("no_such_file.csv", inventory, make_supplier())
        self.assertIn("not found", buffer.getvalue())
        self.assertIn("Load attempt finished.", buffer.getvalue())
        self.assertEqual(len(inventory.get_products()), 0)

    def test_bad_rows_skipped_and_valid_rows_load(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "products.csv")
            with open(path, "w", newline="") as f:
                f.write(CSV_TEXT)
            inventory = Inventory()
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                load_products(path, inventory, make_supplier())
        self.assertEqual(len(inventory.get_products()), 3)
        self.assertIn("3 products loaded.", buffer.getvalue())
        self.assertIn("Load attempt finished.", buffer.getvalue())


if __name__ == "__main__":
    unittest.main()