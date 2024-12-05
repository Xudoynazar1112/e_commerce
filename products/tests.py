from django.test import TestCase

from products.models import Product


# Create your tests here.
class ProductTests(TestCase):
    def test_string_representation(self):
        product = Product.objects.create(name="My Product", price=100.00,
                                         description="My Product Description", stock=10)
        self.assertEqual(product.name, "My Product")
        self.assertEqual(product.price, 100.00)
        self.assertEqual(product.description, "My Product Description")
        self.assertEqual(product.stock, 10)
