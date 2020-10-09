from django.contrib.auth.models import User
from django.db import models

class Shop(models.Model):
	address = models.CharField(max_length = 200)
	name = models.CharField(max_length = 100)
	user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "user_shop", null = False)

	def __str__(self):
		return self.name

class Order(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "user_order", null = False)
	cat_1 = models.PositiveIntegerField(default = 0)
	cat_2 = models.PositiveIntegerField(default = 0)
	cat_3 = models.PositiveIntegerField(default = 0)
	cat_4 = models.PositiveIntegerField(default = 0)

	def __str__(self):
		return str(self.id)
	