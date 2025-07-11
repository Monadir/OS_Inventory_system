import unittest
from datetime import date


# Mock functions extracted and adapted from Bakery_Inventory.py
# You can import from your actual code if functions are modularized.

class TestBakeryInventory(unittest.TestCase):

    def setUp(self):
        # Start each test with a clean mock inventory
        self.inventory = {
            "Flour": {"quantity": 10, "unit": "kg", "expiry": "2025-08-01"},
            "Milk": {"quantity": 3, "unit": "litres", "expiry": "2023-08-01"}
        }

    def test_add_ingredient(self):
        name = "Sugar"
        self.inventory[name] = {"quantity": 5, "unit": "kg", "expiry": "2025-12-01"}
        self.assertIn(name, self.inventory)
        self.assertEqual(self.inventory[name]["quantity"], 5)

    def test_update_ingredient_use(self):
        name = "Flour"
        used = 2
        original = self.inventory[name]["quantity"]
        self.inventory[name]["quantity"] -= used
        self.assertEqual(self.inventory[name]["quantity"], original - used)

    def test_update_ingredient_restock(self):
        name = "Milk"
        added = 2
        original = self.inventory[name]["quantity"]
        self.inventory[name]["quantity"] += added
        self.assertEqual(self.inventory[name]["quantity"], original + added)

    def test_low_stock_alert(self):
        low_stock_items = []
        min_threshold = 5
        for item, info in self.inventory.items():
            if info["quantity"] < min_threshold:
                low_stock_items.append(item)
        self.assertIn("Milk", low_stock_items)

    def test_expiry_check(self):
        today = date.today()
        expired_items = []
        for name, info in self.inventory.items():
            expiry_date = date.fromisoformat(info["expiry"])
            if expiry_date < today:
                expired_items.append(name)
        self.assertIn("Milk", expired_items)

    def test_search_ingredient(self):
        name = "Flour"
        self.assertTrue(name in self.inventory)
        self.assertEqual(self.inventory[name]["unit"], "kg")

    def test_invalid_ingredient(self):
        name = "Oil"
        self.assertNotIn(name, self.inventory)

if __name__ == '__main__':
    unittest.main()
