from django.db import models
from django.contrib.auth.models import User



class Order(models.Model):
	customer_id = models.IntegerField(default = 0)
	customer_username = models.CharField(max_length = 100)
	customer_phone = models.CharField(max_length = 30)
	customer_location = models.JSONField(default = dict)
	customer_name = models.CharField(max_length = 100)

	order = models.JSONField(default = list)
	source = models.CharField(max_length = 10, default = 'cash-register')
	price = models.FloatField(max_length = 30)
	status = models.CharField(max_length = 10, default = 'pending')
	date = models.DateTimeField()
	executor = models.ForeignKey(User, on_delete = models.PROTECT)

	def __str__(self):
		return f'{str(self.price)} uzs - {self.customer_name} ({self.date.date()}) || {self.status}'