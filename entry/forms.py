from django import forms
from .models import BE,BE_line
from django.utils import timezone
from django.forms import inlineformset_factory


# class DateInput(forms.DateInput):
#     input_type = 'date'

class BEForm(forms.ModelForm):
    class Meta:
        model = BE
        exclude = ['status']
        
    date_entry = forms.DateField(
        label='Date of Entry',
        widget=forms.DateInput(attrs={'type': 'date'}),  # Utilisation d'un widget datepicker en HTML
        input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'],  # Formats de date acceptés
        initial=timezone.now
    )
    

class LineBEForm(forms.ModelForm):
    class Meta:
        model = BE_line
        fields = '__all__'
    type = forms.ChoiceField(
        choices=BE_line.METAL_TYPE_CHOICES,
        initial='TPN')
        
LineBEFormSet = inlineformset_factory(BE, BE_line, form=LineBEForm, extra=1 ,can_delete=True)



        