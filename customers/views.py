from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from customers.models import Customers,Customers_t
from entry.models import Invoice
from entry.models import BE_line,BE
from django.views.generic.edit import CreateView
from .forms import CustomerForm
from django.urls import reverse_lazy
from django.db.models import Sum,Count, F,Q,ExpressionWrapper, DecimalField
from django.utils import timezone
from datetime import datetime,timedelta

from django.views.generic import TemplateView,ListView,DetailView,UpdateView,DeleteView


class HomePageView(LoginRequiredMixin,TemplateView):
    
    template_name = "customers/home.html"
    
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)

        now = timezone.now()
        
        current_month = datetime.now().month
        current_year = datetime.now().year

        start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = now.replace(day=now.day, hour=23, minute=59, second=59, microsecond=999999)
        total_sm_eqv_in_current_month = BE_line.objects.filter(be__date_entry__gte=start_date, be__date_entry__lte=end_date).aggregate(Sum('sm_eqv'))['sm_eqv__sum']
        total_sm_eqv = total_sm_eqv_in_current_month or 0
        
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        today_sum = BE_line.objects.filter(be__date_entry__range=(today_start, today_end)).aggregate(Sum('sm_eqv'))['sm_eqv__sum']

        last_month_start = now - timedelta(days=now.day)
        last_month_start = last_month_start.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_month_end = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(microseconds=1)
        total_sm_last_month = BE_line.objects.filter(be__date_entry__range=(last_month_start, last_month_end)).aggregate(Sum('sm_eqv'))['sm_eqv__sum']

        distinct_client_count = Customers.objects.filter(bes__date_entry__month=current_month, bes__date_entry__year=current_year).values('name').distinct().count()
        
        context['client_unique_values_count'] = Customers.objects.values('name').distinct().count()
        context['sm_pcs'] = BE_line.objects.aggregate(Sum('qty'))['qty__sum']
        context['sm_eqv'] = BE_line.objects.aggregate(Sum('sm_eqv'))['sm_eqv__sum']
        context['amount'] = Invoice.objects.aggregate(Sum('total'))['total__sum'] + Invoice.objects.aggregate(Sum('total_sm'))['total_sm__sum']
        context['total_sm_current_month'] = total_sm_eqv
        context['total_sm_current_day'] = today_sum or 0
        context['total_sm_last_month'] = total_sm_last_month
        context['client_unique_this_month'] = distinct_client_count
        
        TARGET = 150
        JOUR_OUVRABLE = 30
        context['indicator'] = int(float(total_sm_eqv) *JOUR_OUVRABLE/(TARGET*now.day)*100)
        return context
    
class AboutPageView(TemplateView):
    template_name = 'customers/about.html'
    
class DashBoardPageView(TemplateView):
    template_name = 'customers/dashboard.html'
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        be_with_total_amounts = BE.objects.annotate(total_amount=Sum('be_lines__sm_eqv'))
        be_with_total_amounts
        context['be_with_total_amounts'] = be_with_total_amounts.order_by('-id')
        
        return context
    
class PricingPageView(TemplateView):
    template_name = 'customers/pricing.html'
    

class CustomerCreateView(CreateView):
    model = Customers
    form_class = CustomerForm
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('customer-list')  # Redirect URL after successful form submission

class ListCustomers(ListView):
    model = Customers
    template_name = 'customers/list_client.html'
    context_object_name = 'customers'
    
     # Override the get_queryset method to annotate customers with the BE count
    def get_queryset(self):
        return Customers.objects.annotate(be_count=Count('bes')).order_by('id')  # 'bes' is the related_name from BE model
    
class CustomersDetailView(DetailView):
    model = Customers
    template_name = 'customers/customer_detail.html'
    context_object_name = 'customer'
    
    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        customer = get_object_or_404(Customers, pk=pk)
        context = super().get_context_data(**kwargs)
        if customer.bes.order_by('-date_entry').first() is not None:
            context['last'] = (timezone.now().date() - customer.bes.order_by('-date_entry').first().date_entry).days
        else :
            context['last'] = '-9999'

        frequency = customer.bes.count()

        context["frequency"] = frequency if frequency is not None else 0
        total_sm_eqv = BE_line.objects.filter(be__customers=customer).aggregate(total=Sum('sm_eqv'))['total']
        context["total_sm_eqv"] = total_sm_eqv if total_sm_eqv is not None else 0
        return context
    
class CustomersUpdateView(UpdateView):
    model = Customers
    form_class = CustomerForm
    template_name = 'customers/customer_form.html'
    context_object_name = 'customer'
    success_url = reverse_lazy('customer-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Customer updated successfully.')
        return super().form_valid(form)
class CustomersDeleteView(DeleteView):
    model = Customers
    template_name = 'customers/customer_confirm_delete.html'
    context_object_name = 'customer'
    success_url = reverse_lazy('customer-list')
    
class TargetClientListView(ListView):
    model = Customers_t
    template_name = 'customers/list_t.html'
    context_object_name = 'customers_ts'
    ordering = ['-id']