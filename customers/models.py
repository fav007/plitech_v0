from django.db import models

class Customers(models.Model):
    name = models.CharField(max_length=200,unique=True)
    company = models.CharField(max_length=200,null=True,blank=True)
    contact = models.CharField(max_length=10,unique=True,null=True,blank=True)
    location = models.CharField(max_length=100,null=True,blank=True)
    
    def __str__(self) -> str:
        return f"{self.name} by {self.location}"
    
    
