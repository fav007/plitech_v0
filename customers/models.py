from django.db import models

class Customers(models.Model):
    name = models.CharField(max_length=200,unique=True)
    company = models.CharField(max_length=200)
    contact = models.CharField(max_length=10,unique=True)
    address = models.CharField(max_length=100)
    


# Create your models here.
