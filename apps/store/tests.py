from django.test import TestCase, Client
from django.urls import reverse
from apps.store.models import Category, Product
from decimal import Decimal


class StoreViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name='Celestial Rings',
            slug='celestial-rings',
            description='Test category',
            is_featured=True
        )
        self.product = Product.objects.create(
            category=self.category,
            name='Nebula Test Ring',
            slug='nebula-test-ring',
            sku='AJ-TEST-01',
            price=Decimal('150000.00'),
            stock=5,
            is_available=True,
            is_featured=True,
            is_bestseller=True,
            metal_karat='18K Yellow Gold',
            gemstone_type='Natural Diamond',
            image_url='https://example.com/test.jpg'
        )

    def test_homepage(self):
        response = self.client.get(reverse('store:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'AETHER')
        self.assertContains(response, 'Nebula Test Ring')

    def test_product_list(self):
        response = self.client.get(reverse('store:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nebula Test Ring')

    def test_product_detail(self):
        response = self.client.get(reverse('store:product_detail', args=[self.category.slug, self.product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'AJ-TEST-01')
        self.assertContains(response, '18K Yellow Gold')

    def test_search_filter(self):
        response = self.client.get(reverse('store:product_list') + '?q=Nebula')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nebula Test Ring')
