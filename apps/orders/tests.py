from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from apps.store.models import Category, Product
from apps.orders.models import Order
from decimal import Decimal


class OrdersTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='vipbuyer', password='password123', email='buyer@luxury.in')
        self.category = Category.objects.create(name='Earrings', slug='earrings')
        self.product = Product.objects.create(
            category=self.category,
            name='Test Starlight Drops',
            slug='test-starlight-drops',
            sku='AJ-EAR-TEST',
            price=Decimal('75000.00'),
            stock=5,
            is_available=True,
            image_url='https://example.com/test.jpg'
        )

    def test_checkout_flow(self):
        self.client.login(username='vipbuyer', password='password123')
        
        # Add to cart
        self.client.post(reverse('cart:add_to_cart', args=[self.product.id]), {'quantity': 1, 'size': 'Standard'})

        # Post checkout form
        checkout_data = {
            'full_name': 'Aarav VIP',
            'email': 'buyer@luxury.in',
            'phone': '+91 98201 54321',
            'address_line1': '101 Altamount Road',
            'address_line2': 'Cumballa Hill',
            'landmark': 'Near Tower',
            'city': 'Mumbai',
            'state': 'Maharashtra',
            'pincode': '400026',
            'payment_method': 'UPI',
        }
        res = self.client.post(reverse('orders:checkout'), checkout_data)
        self.assertEqual(res.status_code, 302)

        order = Order.objects.filter(user=self.user).first()
        self.assertIsNotNone(order)
        self.assertEqual(order.full_name, 'Aarav VIP')
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.items.first().product_sku, 'AJ-EAR-TEST')
