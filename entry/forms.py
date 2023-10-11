from django import forms
from .models import BE,BE_line,Invoice,InvoiceLine,Banknote
from django.utils import timezone
from django.forms import inlineformset_factory
from datetime import datetime


# class DateInput(forms.DateInput):
#     input_type = 'date'

class BEForm(forms.ModelForm):
    class Meta:
        model = BE
        exclude = ['status']
        
    date_entry = forms.DateField(
        label='Date',
        widget=forms.DateInput(attrs={'type': 'date'}),  # Utilisation d'un widget datepicker en HTML
        input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'],  # Formats de date acceptés
        initial=timezone.now
    )
    time_entry = forms.TimeField(
        label='Time of Entry',
        widget=forms.TimeInput(attrs={'type':'time'}),
        input_formats=['%H:%M'],
        initial=datetime.now().strftime('%H:%M'),
    )
    

class LineBEForm(forms.ModelForm):
    class Meta:
        model = BE_line
        exclude = ['eq_sm']
        
    type = forms.ChoiceField(
        choices=BE_line.METAL_TYPE_CHOICES,
        initial='TPN')
        
LineBEFormSet = inlineformset_factory(BE, BE_line, form=LineBEForm, extra=1 ,can_delete=True)

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        #exclude = ['be']
        fields = '__all__'
        
    date = forms.DateField(
        label='Date',
        widget=forms.DateInput(attrs={'type': 'date'}),  # Utilisation d'un widget datepicker en HTML
        input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'],  # Formats de date acceptés
        initial=timezone.now)
    
    # be = forms.ModelChoiceField(
    #                          widget=forms.Select(attrs={'disabled':'disabled'})
    #                             )

class InvoiceLineForm(forms.ModelForm):
    class Meta:
        model = InvoiceLine
        fields = '__all__'
        
class BanknoteForm(forms.ModelForm):
    class Meta:
        model = Banknote
        exclude = ['total']