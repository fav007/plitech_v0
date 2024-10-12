from collections.abc import Iterable
from django.db import models
from customers.models import Customers
from django.utils import timezone
from django.db.models import Sum, F

class BE(models.Model):
    STATUS_CHOICES = [
    ('E', 'Entry'),
    ('B', 'Billed'),
    ('I', 'In progress'),
    ('C', 'Completed'),
    ('O','Out')
]
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_entry = models.DateField("Entry Date",default=timezone.now)
    time_entry = models.TimeField("Entry Time",default=timezone.now)
    status = models.CharField(max_length=1,choices=STATUS_CHOICES,default='E')
    customers = models.ForeignKey(Customers,on_delete=models.CASCADE,related_name='bes')
    
    def __str__(self) -> str:
        return f"ref bl-{self.pk} date:{self.date_entry} for customers:{self.customers.name}"

class BE_line(models.Model):
    METAL_TYPE_CHOICES = [
        ('TPN','TPN'),
        ('TPG','TPG'),
        ('TPI','TPI'),
        ('TPP','TPP'),
    ]
    
    OWNER_CHOICES = [
        ('Client','Client'),
        ('Hanitra','Hanitra'),
        ('Tojo','Tojo'),
        ('Plitech','Plitech')
    ]
    
    THICKNESS_CHOICES = [
        ('30/100', '30/100'),
        ('40/100', '40/100'),
        ('50/100', '50/100'),
        ('60/100', '60/100'),
        ('7/10', '7/10'),
        ('8/10', '8/10'),
        ('9/10', '9/10'),
        ('10/10', '10/10'),
        ('11/10', '11/10'),
        ('12/10', '12/10'),
        ('15/10', '15/10'),
        ('2 mm', '2 mm'),
        ('3 mm','3 mm'),
        ('4 mm','4 mm')
        ]
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    qty = models.IntegerField(default=1)
    type = models.CharField(max_length=3,choices=METAL_TYPE_CHOICES,default='TPN')
    length = models.IntegerField(default=2000)
    width = models.IntegerField(default=1000)
    thickness = models.CharField(max_length=6,choices=THICKNESS_CHOICES,default='8/10')
    owner = models.CharField(max_length=10,choices=OWNER_CHOICES,default='Client')
    be = models.ForeignKey(BE,on_delete=models.CASCADE,related_name='be_lines')
    sm_eqv = models.DecimalField(default=0,decimal_places=6,max_digits=10)
    
    def save(self,*args,**kwargs) :
        self.sm_eqv = self.qty * self.length * self.width / 2_000_000     
        return super(BE_line,self).save(*args,**kwargs)
    
    def __str__(self) -> str:
        return f'{self.qty} {self.type} {self.thickness} {self.length}x{self.width} BE-{self.be.pk}'
    

    
class Invoice(models.Model):
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    number = models.IntegerField(unique=True)
    date = models.DateField(default=timezone.now)
    total = models.IntegerField('Total machine fees',default=0)
    total_sm = models.IntegerField('Total metal price',default=0)
    discount = models.IntegerField('discount',default=0)
    metal_scrap = models.DecimalField("Metal SCRAP",max_digits=10,decimal_places=5,default=0)
    be = models.OneToOneField(BE,on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        # Update the BE status to 'I' when an invoice is created
        self.be.status = 'B'
        self.be.save()

        super(Invoice, self).save(*args, **kwargs)

    def __str__(self):
        return f'Inv{self.number} dated {self.date}'

 
class InvoiceLine(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    qty = models.IntegerField(default=1)
    item = models.CharField(max_length=20)
    unit_price = models.IntegerField()
    fini = models.IntegerField()
    dvlp = models.IntegerField()
    height = models.IntegerField()
    description = models.CharField(max_length=200,null=True,blank=True)
    invoice = models.ForeignKey(Invoice,on_delete=models.CASCADE,related_name='invoice_lines')  
    be_line = models.ForeignKey(BE_line,on_delete=models.CASCADE) 
    
    
class Banknote(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date = models.DateField(default=timezone.now)
    b_20_000 = models.IntegerField("20 000 MGA",default=0)
    b_10_000 = models.IntegerField("10 000 MGA",default=0)
    b_5_000 = models.IntegerField("5 000 MGA",default=0)
    b_2_000 = models.IntegerField("2 000 MGA",default=0)
    b_1_000 = models.IntegerField("1 000 MGA",default=0)
    b_500 = models.IntegerField("500 MGA",default=0)
    b_200 = models.IntegerField("200 MGA" ,default=0)
    b_100 = models.IntegerField("100 MGA",default=0)
    total = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        self.total = (
            self.b_20_000 * 20_000 +
            self.b_10_000 * 10_000 +
            self.b_5_000 * 5_000 +
            self.b_2_000 * 2_000 +
            self.b_1_000 * 1_000 +
            self.b_500 * 500 +
            self.b_200 * 200 +
            self.b_100 * 100
        )
        super(Banknote, self).save(*args, **kwargs)
        
