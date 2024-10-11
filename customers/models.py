from django.db import models

class Customers(models.Model):
    
    TITLE_CHOICES = [
        ('M.', 'Monsieur'),
        ('Mme', 'Madame'),
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=3,choices=TITLE_CHOICES)
    name = models.CharField(max_length=200,unique=True)
    company = models.CharField(max_length=200)
    contact = models.CharField(max_length=10)
    location = models.CharField(max_length=100)
        
    def __str__(self) -> str:
        return f"{self.name} by {self.location}"
    
class Customers_t(models.Model):
    
    TITLE_CHOICES = [
        ('M.', 'Monsieur'),
        ('Mme', 'Madame'),
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=3,choices=TITLE_CHOICES)
    name = models.CharField(max_length=200,unique=True)
    company = models.CharField(max_length=200)
    contact = models.CharField(max_length=10)
    location = models.CharField(max_length=100)
        
    def __str__(self) -> str:
        return f"{self.name} by {self.location}"
    
    
