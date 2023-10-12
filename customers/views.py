from django.shortcuts import render
from django.http import HttpResponse
from customers.models import Customers
from entry.models import Invoice
from entry.models import BE_line,BE
from django.views.generic.edit import CreateView
from .forms import CustomerForm
from django.urls import reverse_lazy
from django.db.models import Sum, F
from django.utils import timezone
from datetime import datetime

from django.views.generic import TemplateView,ListView,DetailView,UpdateView,DeleteView

class HomePageView(TemplateView):
    template_name = "customers/home.html"
    
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        
        
        current_month = datetime.now().month
        current_year = datetime.now().year
        start_date = datetime(current_year, current_month, 1)
        if current_month == 12:
            end_date = datetime(current_year + 1, 1, 1)
        else:
            end_date = datetime(current_year, current_month + 1, 1)

        # Query the sum of sm_eqv for BE objects with date_entry within the current month
        # be_this_month = BE.objects.filter(date_entry__gte=start_date, date_entry__lt=end_date)

        # sum_sm_eqv = be_this_month.objects.aggregate(Sum('sm_eqv'))['sm_eqv__sum']

        context['client_unique_values_count'] = Customers.objects.values('name').distinct().count()
        context['sm_pcs'] = BE_line.objects.aggregate(Sum('qty'))['qty__sum']
        context['sm_eqv'] = BE_line.objects.aggregate(Sum('sm_eqv'))['sm_eqv__sum']
        context['amount'] = Invoice.objects.aggregate(Sum('total'))['total__sum'] + Invoice.objects.aggregate(Sum('total_sm'))['total_sm__sum']
        # context['total_sm_current_month'] = sum_sm_eqv
        return context
    
class AboutPageView(TemplateView):
    template_name = 'customers/about.html'
    

class CustomerCreateView(CreateView):
    model = Customers
    form_class = CustomerForm
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('customer-list')  # Redirect URL after successful form submission

class ListCustomers(ListView):
    model = Customers
    template_name = 'customers/list_client.html'
    context_object_name = 'customers'
    
class CustomersDetailView(DetailView):
    model = Customers
    template_name = 'customers/customer_detail.html'
    context_object_name = 'customer'
    
class CustomersUpdateView(UpdateView):
    model = Customers
    form_class = CustomerForm
    template_name = 'customers/customer_form.html'
    context_object_name = 'customer'
    success_url = reverse_lazy('customer-list')
    
class CustomersDeleteView(DeleteView):
    model = Customers
    template_name = 'customers/customer_confirm_delete.html'
    context_object_name = 'customer'
    success_url = reverse_lazy('customer-list')