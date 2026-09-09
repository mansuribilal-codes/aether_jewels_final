from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from apps.store.models import Category, Product
from apps.cart.models import Coupon, Cart
from decimal import Decimal


class CartTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testclient', password='password123')
        self.category = Category.objects.create(name='Rings', slug='rings')
        self.product = Product.objects.create(
            category=self.category,
            name='Test Celestial Solitaire',
            slug='test-celestial-solitaire',
            sku='AJ-CART-01',
            price=Decimal('100000.00'),
            stock=10,
            is_available=True,
            image_url='https://example.com/test.jpg'
        )
        self.coupon = Coupon.objects.create(
            code='AETHER10',
            description='10% discount',
            discount_percent=10,
            min_purchase=Decimal('50000.00')
        )

    def test_add_to_cart_and_coupon(self):
        # Add item to cart
        res = self.client.post(reverse('cart:add_to_cart', args=[self.product.id]), {'quantity': 1, 'size': '9'})
        self.assertEqual(res.status_code, 302)

        # Apply coupon
        res = self.client.post(reverse('cart:apply_coupon'), {'coupon_code': 'AETHER10'})
        self.assertEqual(res.status_code, 302)

        # View Cart
        res = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Test Celestial Solitaire')
        self.assertContains(res, 'AETHER10')
