from django.db import models
from apps.accounts.models import Client

class Item(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    description = models.TextField()
    in_stock = models.PositiveIntegerField()
    category_id = models.ForeignKey('Category')

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    status = models.PositiveIntegerField(default=0)
    status_change_date = models.DateTimeField()
    payment_status = models.PositiveIntegerField()
    client_id = models.ForeignKey(Client)

class Order_Item(models.Model):
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    order_id = models.ForeignKey('Order')
    item_id = models.ForeignKey('Item')

class Invoice(models.Model):
    unique_no = models.PositiveIntegerField(unique=True)
    order_id = models.OneToOneField('Order',
                                    primary_key=True)

class Review(models.Model):
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    client_id = models.ForeignKey(Client)
    item_id = models.ForeignKey('Item')
