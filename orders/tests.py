from django.test import TestCase
from django.contrib.auth.models import User
from .models import Order, OrderItem
from products.models import Product, Category

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john', password='pass')
        self.category = Category.objects.create(name="Books", slug="books")
        self.product = Product.objects.create(
            name="Django for Beginners",
            description="Learn Django",
            price=49.99,
            stock=20,
            category=self.category
        )
        self.order = Order.objects.create(user=self.user)
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=2)

    def test_order_created(self):
        self.assertEqual(self.order.user.username, "john")
        self.assertEqual(self.order_item.quantity, 2)
