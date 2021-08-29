from django.contrib.auth.models import User
from django.db import models
from item.models import Item


class User_Type(models.Model):
    privilege = models.BooleanField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_priv", null=False
    )

    def __str__(self):
        return str(self.user)


class Shop(models.Model):
    address = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_shop", null=False
    )

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_order", null=False
    )
    items = models.ManyToManyField(Item, through="Order_Item", related_name="ord_item")
    cost = models.FloatField(default=0, null=False)
    paid = models.BooleanField(default=False, null=False)
    delivered = models.BooleanField(default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class Order_Item(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()

    def __str__(self):
        return str(self.id)


class Test_Model(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)
