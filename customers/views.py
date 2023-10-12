from django.shortcuts import render
from django.http import HttpResponse
from customers.models import Customers
from entry.models import Invoice
from entry.models import BE_line,BE
from django.views.generic.edit import CreateView
from .forms import CustomerForm
from django.urls import reverse_lazy
from django.db.models import Sum, F,Q,ExpressionWrapper, DecimalField
from django.utils import timezone
from datetime import datetime,timedelta

from django.views.generic import TemplateView,ListView,DetailView,UpdateView,DeleteView

class HomePageView(TemplateView):
    template_name = "customers/home.html"
    
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)

        now = timezone.now()

        start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = now.replace(day=now.day, hour=23, minute=59, second=59, microsecond=999999)
        total_sm_eqv_in_current_month = BE_line.objects.filter(be__date_entry__gte=start_date, be__date_entry__lte=end_date).aggregate(Sum('sm_eqv'))['sm_eqv__sum']
        total_sm_eqv = total_sm_eqv_in_current_month
        
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        today_sum = BE_line.objects.filter(be__date_entry__range=(today_start, today_end)).aggregate(Sum('sm_eqv'))['sm_eqv__sum']

        last_month_start = now - timedelta(days=now.day)
        last_month_start = last_month_start.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_month_end = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(microseconds=1)
        total_sm_last_month = BE_line.objects.filter(be__date_entry__range=(last_month_start, last_month_end)).aggregate(Sum('sm_eqv'))['sm_eqv__sum']

        
        context['client_unique_values_count'] = Customers.objects.values('name').distinct().count()
        context['sm_pcs'] = BE_line.objects.aggregate(Sum('qty'))['qty__sum']
        context['sm_eqv'] = BE_line.objects.aggregate(Sum('sm_eqv'))['sm_eqv__sum']
        context['amount'] = Invoice.objects.aggregate(Sum('total'))['total__sum'] + Invoice.objects.aggregate(Sum('total_sm'))['total_sm__sum']
        context['total_sm_current_month'] = total_sm_eqv
        context['total_sm_current_day'] = today_sum
        context['total_sm_last_month'] = total_sm_last_month
        
        TARGET = 120
        JOUR_OUVRABLE = 26
        context['indicator'] = int(float(total_sm_eqv)*JOUR_OUVRABLE/(TARGET*now.day)*100)
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