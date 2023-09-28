from django.db import models
from customers.models import Customers
from django.utils import timezone

class BE(models.Model):
    STATUS_CHOICES = [
    ('E', 'Entry'),
    ('B', 'Billed'),
    ('I', 'In progress'),
    ('C', 'Completed'),
    ('O','Out')
]
    
    date_entry = models.DateField(default=timezone.now)
    time_entry = models.TimeField(default=timezone.now)
    status = models.CharField(max_length=1,choices=STATUS_CHOICES,default='E')
    customers = models.ForeignKey(Customers,on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"id:{self.pk} date:{self.date_entry} customers:{self.customers.name}"

class BE_line(models.Model):
    METAL_TYPE_CHOICES = [
        ('TPN','TPN'),
        ('TPG','TPG'),
        ('TPI','TPI'),
        ('TPP','TPP'),
    ]
    
    qty = models.IntegerField(default=1)
    type = models.CharField(max_length=3,choices=METAL_TYPE_CHOICES)
    be = models.ForeignKey(BE,on_delete=models.CASCADE,related_name='be_lines')
    
    def __str__(self) -> str:
        return f'{self.qty} {self.type} BE N° :{self.be.pk}'