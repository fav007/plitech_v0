from django.db import models
from django.utils import timezone

class Expense(models.Model):
    
    CATEGORY_CHOICES = [
        ('AT',"Achat Tôle"),
        ('FAA',"Frais accesoires d'achat"),
        ('FR',"Frais Roulage"),
        ("AM","Achat de marchandises"),
        ("RRROA","RRR obtenus sur achats"),
        ("AMET","Achats de matériels,équipements et travaux"),
        ("AEPS","Achat d'études et de préstation de service"),
        ("FPT", "Frais postaux et de télécommunications"),
        ("PPRP","Publicité, publication, relations publiques"),
        ('ANSMF',"Achat non stockés de matières et fournitures"),
        ('AEPS',"Achat d'études et de préstation de service"),
        ('RP',"Rémunérations du personnel"),
        ('RD',"Rémunération des dirigeants"),
        ('RIH',"Rémunérations d'intermédiaires et honoraires"),
        ('CBA',"Services bancaires et assimilés"),
        ('ERM',"Entretien, réparation et maintenance"),
        ('CD',"Cotisations et divers"),
        ('TBCP',"Transport de biens et transport collectif du personnel"),
        ('CI',"Charges d'intérêts"),
        ('IT',"impôts et taxes"),
        ('AA',"Autres approvisionnements"),
        ('VS',"Variation des stocks"),
        ('PCI',"Pertes sur créances irrécouvrables"),
        ]
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date = models.DateField(default=timezone.now)
    category = models.CharField(max_length=5,choices=CATEGORY_CHOICES)
    acn = models.CharField('Accounting Document Number',max_length=50)
    description = models.CharField(max_length=200)
    total = models.IntegerField("Total Amount")
    
    def __str__(self) -> str:
        return f'{self.category} dated {self.date} amount:{self.total} MGA'