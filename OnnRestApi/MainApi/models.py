from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=50, blank=False, default="")
    price = models.DecimalField(max_digits=19, decimal_places=2, blank=False, default=0)
    stock = models.IntegerField(blank=False, default=0)
    description = models.CharField(max_length=300, blank=False, default="")


class Order(models.Model):
    product = models.ForeignKey(
        Product, related_name="orders", on_delete=models.CASCADE, default=""
    )
    address = models.CharField(max_length=300, blank=False, default="")
