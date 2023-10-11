from django.shortcuts import render
from django.http import HttpResponse
from customers.models import Customers
from entry.models import Invoice
from entry.models import BE_line,BE
from django.views.generic.edit import CreateView
from .forms import CustomerForm
from django.urls import reverse_lazy
from django.db.models import Sum, F


from django.views.generic import TemplateView,ListView,DetailView,UpdateView,DeleteView

class HomePageView(TemplateView):
    template_name = "customers/home.html"
    
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)

        context['client_unique_values_count'] = Customers.objects.values('name').distinct().count()
        context['sm_pcs'] = BE_line.objects.aggregate(Sum('qty'))['qty__sum']
        context['sm_eqv'] = BE_line.objects.aggregate(Sum('sm_eqv'))['sm_eqv__sum']
        context['amount'] = Invoice.objects.aggregate(Sum('total'))['total__sum'] + Invoice.objects.aggregate(Sum('total_sm'))['total_sm__sum']
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