from django.db import models
from decimal import Decimal, ROUND_HALF_UP
from django.core.validators import RegexValidator




# Create your models here.
class Product(models.Model):
    nazev_produktu = models.CharField(max_length=100)
    cena_bez_dph = models.DecimalField(max_digits=10, decimal_places=2)
    dph = models.DecimalField(max_digits=4, decimal_places=2, default=21.00)
    popis = models.TextField()

    @property
    def cena_z_dph(self):
        cena = self.cena_bez_dph * (Decimal('1') + Decimal(self.dph) / Decimal('100'))
        return cena.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


    def __str__(self):
        return self.nazev_produktu


class Order(models.Model):
    jmeno = models.CharField(max_length=100)
    email = models.EmailField()
    telefon = models.CharField(max_length=15)
    produkt = models.ForeignKey(Product, on_delete=models.CASCADE)
    pocet = models.IntegerField()
    addresa = models.TextField()
    order_date = models.DateTimeField(auto_now_add=True)
    celkem_cena = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order #{self.id} by {self.jmeno}"