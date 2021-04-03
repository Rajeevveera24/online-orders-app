from django.db import models

class Item(models.Model):
	name = models.CharField(max_length = 50, unique = True)
	desc = models.CharField(max_length = 100)
	unit = models.CharField(max_length = 10, default = "No.s")
	price = models.FloatField(null=True)

	def __str__(self):
		return self.name
