from .models import Expense,Jirama
from django import forms
from django.utils import timezone

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = '__all__'
        
    date = forms.DateField(
        label='Date',
        widget=forms.DateInput(attrs={'type': 'date'}),  # Utilisation d'un widget datepicker en HTML
        input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'],  # Formats de date acceptés
        initial=timezone.now)
    
    description = forms.CharField(max_length=200,widget=forms.Textarea())
    
class JiramaForm(forms.ModelForm):
    class Meta:
        model = Jirama
        fields = '__all__'
        
    date = forms.DateField(
        label='Date',
        widget=forms.DateInput(attrs={'type': 'date'}),  # Utilisation d'un widget datepicker en HTML
        input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'],  # Formats de date acceptés
        initial=timezone.now)
        