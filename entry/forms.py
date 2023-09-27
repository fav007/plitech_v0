from django import forms
from .models import BE

class BEForm(forms.ModelForm):
    class Meta:
        model = BE
        fields = '__all__'