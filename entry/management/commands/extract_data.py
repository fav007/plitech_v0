# myapp/management/commands/extract_data.py
from django.core.management.base import BaseCommand
from entry.data_extraction import extract_data  # Importez votre script

class Command(BaseCommand):
    help = 'Extract data and create a DataFrame'

    def handle(self, *args, **kwargs):
        extract_data()  # Appelez la fonction de votre script
        self.stdout.write(self.style.SUCCESS('Data extraction completed successfully'))
