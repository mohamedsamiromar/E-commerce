from django.test import TestCase
from catalog.models import Category, Item


class CategoryModelTest(TestCase):
    def test_create_category(self):
        category = Category.objects.create(name="Electronics", slug="electronics")
        self.assertEqual(str(category), "Electronics")


class ItemModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Books", slug="books")

    def test_create_item(self):
        item = Item.objects.create(
            title="Test Item", price=10.99, slug="test-item",
            description="A test item", category=self.category,
        )
        self.assertEqual(str(item), "Test Item")
        self.assertEqual(item.final_price, 10.99)
        self.assertFalse(item.has_discount)

    def test_item_with_discount(self):
        item = Item.objects.create(
            title="Discounted Item", price=20.00, discount_price=15.00,
            slug="discounted-item", description="On sale",
        )
        self.assertTrue(item.has_discount)
        self.assertEqual(item.final_price, 15.00)

    def test_item_default_in_stock(self):
        item = Item.objects.create(
            title="In Stock Item", price=5.00, slug="in-stock",
            description="Default stock",
        )
        self.assertTrue(item.in_stock)
