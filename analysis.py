import os
import django

# Set the settings module for your Django project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atelier.settings')

# Initialize Django
django.setup()

# Now you can safely import models
from entry.models import Invoice, InvoiceLine


# Fetch all invoices with their associated invoice lines
invoices = Invoice.objects.prefetch_related('invoice_lines')
