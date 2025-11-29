from django.urls import reverse
from decimal import Decimal
from django.test import TestCase
from .models import Product, Order
from django.utils.html import escape

class OrderSuccessPageTest(TestCase):

    def setUp(self):
        # vytvoříme produkt
        self.product = Product.objects.create(
            nazev_produktu="Test Produkt",
            cena_bez_dph=Decimal('100.00'),
            dph=21,
        )

        # vytvoříme objednávku
        self.order = Order.objects.create(
            jmeno="Jan Novák",
            email="jan@example.com",
            telefon="123456789",
            produkt=self.product,
            pocet=2,
            addresa="Testovací ulice 1",
            celkem_cena=self.product.cena_z_dph * 2
        )

        # URL stránky potvrzení
        self.success_url = reverse('order_success', kwargs={'objednavka_id': self.order.id})

    def test_order_success_page_status_code(self):
        response = self.client.get(self.success_url)
        self.assertEqual(response.status_code, 200)

    def test_order_success_page_contains_order_data(self):
        response = self.client.get(self.success_url)
        # formátujeme na dvě desetinná místa
        formatted_cena = f"{self.order.celkem_cena:.2f}"
        self.assertContains(response, escape(formatted_cena))

    def test_redirect_from_order_submit(self):
        response = self.client.post(
            reverse('order_submit'),
            data={
                'jmeno': 'Anna',
                'email': 'anna@example.com',
                'telefon': '987654321',
                'produkt': self.product.id,
                'pocet': 1,
                'addresa': 'Nová 2'
            }
        )
        self.assertEqual(response.status_code, 302)  # redirect po odeslání
