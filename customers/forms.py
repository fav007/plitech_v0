# forms.py
from django import forms
from .models import Customers
import re

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = '__all__'
    
    def clean_name(self):
        # Get the cleaned data from the form
        cleaned_name = self.cleaned_data.get('name')
        
        # Check if the cleaned_name is not None
        if cleaned_name:
            # Convert the name to uppercase
            cleaned_name = cleaned_name.upper()
        else:
            raise forms.ValidationError("Give a name please")
        
        return cleaned_name
    
    def clean_contact(self):
        # Get the cleaned data from the form
        cleaned_contact = self.cleaned_data.get('contact')

        # Define the pattern you want to match
        pattern = r'^\d{10}$'  # Matches exactly 10 digits

        # Use regular expression to check if it matches the pattern
        if not re.match(pattern, cleaned_contact):
            raise forms.ValidationError("Contact must be in 10 digits.")

        return cleaned_contact


