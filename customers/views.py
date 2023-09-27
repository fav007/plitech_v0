from django.shortcuts import render
from django.http import HttpResponse
from customers.models import Customers

from django.views.generic import TemplateView,ListView,DetailView

class HomePageView(TemplateView):
    template_name = "customers/home.html"
    
    
class ListCustomers(ListView):
    model = Customers
    template_name = 'Customers/list_client.html'
    context_object_name = 'customers'
    
class AboutPageView(TemplateView):
    template_name = 'customers/about.html'
    
class CustomersDetailView(DetailView):
    model = Customers
    template_name = 'customers/customer_detail.html'
    context_object_name = 'customer'
    
# views.py
from django.views.generic.edit import CreateView
from .forms import CustomerForm

class CustomerCreateView(CreateView):
    model = Customers
    form_class = CustomerForm
    template_name = 'customers/customer_form.html'
    success_url = '/customers/list/'  # Redirect URL after successful form submission
