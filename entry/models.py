from django.db import models
from customers.models import Customers

class BE(models.Model):
    date_entry = models.DateField(auto_now_add=True)
    time_entry = models.TimeField(auto_now_add=True)
    customers = models.ForeignKey(Customers,on_delete=models.DO_NOTHING)
