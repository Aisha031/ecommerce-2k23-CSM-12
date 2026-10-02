from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from api.models import Product, WellnessTag

User = get_user_model()

class ProductAdminTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.seller = User.objects.create_user(username='seller1', password='password123')
        self.client.force_authenticate(user=self.seller)
        self.tag = WellnessTag.objects.create(name='Sleep')

    def test_negative_stock_rejection(self):
        product = Product.objects.create(
            seller=self.seller,
            name='Chamomile Tea',
            ingredients='Dried chamomile flowers',
            price=12.99,
            stock_quantity=10
        )
        url = f'/api/v1/admin/products/{product.id}/'
        payload = {'stock_quantity': -5}
        response = self.client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response.json()['detail'], "Stock cannot be negative")