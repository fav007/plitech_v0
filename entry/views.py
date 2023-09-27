from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import BE
from .forms import BEForm

class CustomerCreateView(CreateView):
    model = BE
    form_class = BEForm
    template_name = 'entry/be_form.html'
    success_url = '/'  # Redirect URL after successful form submission

