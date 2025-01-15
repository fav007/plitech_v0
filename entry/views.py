from typing import Any
from django.utils import timezone

from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import CreateView, ListView ,UpdateView , DetailView
from .models import BE,BE_line,Customers,Invoice,InvoiceLine,Banknote
from .forms import BEForm,LineBEForm,LineBEFormSet,InvoiceForm,InvoiceLineForm,BanknoteForm,InvoiceSearchForm,InvoicePaymentForm
from django.urls import reverse_lazy
from django.db.models import Sum


class BECreateView(CreateView):
    model = BE
    form_class = BEForm
    template_name = 'entry/be_form.html'
    success_url = reverse_lazy('be-list')  # Redirect URL after successful form submission
    
class BEListView(ListView):
    model = BE
    template_name = 'entry/be_list.html'
    context_object_name = 'bes'
    ordering = ['-id']

    
class BEListNoInvView(ListView):
    model = BE
    template_name = 'entry/be_list_no_inv.html'
    context_object_name = 'bes'
    
    def get_queryset(self):
        return BE.objects.filter(invoice__isnull=True).order_by("-id")
    
        
class BEDetailsView(DetailView):
    model = BE
    template_name = 'entry/be_details.html'
    context_object_name = 'be'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        be = self.get_object()  # Get the 'be' object for this view
        context['pcs'] = sum(i.qty for i in be.be_lines.all())
        total_qty = sum(line.qty * line.width * line.length / 2_000_000 for line in be.be_lines.all())

        context['total_qty'] = total_qty
        return context


class BEUpdateView(UpdateView):
    model = BE
    form_class = BEForm
    template_name = 'entry/be_form.html'
    success_url = '/entry/list/'  # Redirigez ici après la mise à jour
    
class AddLinesBEView(CreateView):
    model = BE_line
    form_class = LineBEForm
    template_name = 'entry/be_add_lines.html'  # Créez ce template
    
    
    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        be = get_object_or_404(BE, pk=pk)
        context = super().get_context_data(**kwargs)
        context['form'] = LineBEForm(initial={'be':be})
        context['items'] = be.be_lines.all()  # Replace this with your actual query
        context['total'] = sum(i.qty * i.length * i.width / 2_000_000 for i in be.be_lines.all())
        context['be'] = be
        return context
    
    def form_valid(self, form):
        be_id = self.kwargs.get('pk')
        be = BE.objects.get(id=be_id)
        form.instance.be = be
        self.success_url = reverse_lazy('be-add_lines', kwargs={'pk': be_id})
        return super().form_valid(form)
    
    
    
def add_lines_be_view(request,pk):
    be = BE.objects.get(pk=pk)
    context={'be':be}
    return render(request,template_name='entry/try.html',context=context)

class InvoiceMakePaymentView(UpdateView): 
    model = Invoice 
    form_class = InvoicePaymentForm 
    template_name = 'entry/invoice_make_payment.html' 
    success_url = reverse_lazy('invoice-list')
    
    def form_valid(self, form): 
        response = super().form_valid(form) 
        invoice = self.object
        invoice.calculate_total() # Call calculate_total to update balanced_due return response
        return response
    
    

class InvoiceCreateView(CreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'entry/invoice_form.html'
    success_url = reverse_lazy('invoice-list')
    
    def get_initial(self):
        initial = super().get_initial()
        pk = self.kwargs.get('pk')
        be = get_object_or_404(BE, pk=pk)
        initial['be'] = be
        return initial

    def form_valid(self, form):
        # Get the ModelA instance based on the ID from the URL
        be = get_object_or_404(BE, pk=self.kwargs['pk'])
        
        if Invoice.objects.filter(be=be).exists():
            # Return a custom error page with a return button
            error_message = """
                <html>
                    <body>
                        <h2>This BE already has an associated Invoice.</h2>
                        <a href="/entry/list_invoice/">
                            <button>Return to Invoice List</button>
                        </a>
                    </body>
                </html>
            """
            return HttpResponse(error_message)
        
        
        # Associate the ModelA instance with ModelB and save
        form.instance.be = be
        return super().form_valid(form)
    



class InvoiceListView(ListView):
    model = Invoice
    template_name = 'entry/invoice_list.html'
    context_object_name = 'invoices'
    ordering = ['-id']

    

class InvoiceAddLineView(CreateView):
    model = InvoiceLine
    form_class = InvoiceLineForm
    template_name = 'entry/invoice_add_lines.html'
    success_url = reverse_lazy('invoice-list')

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        invoice = get_object_or_404(Invoice, pk=pk)
        
        context = super().get_context_data(**kwargs)
        context['form'] = InvoiceLineForm(initial={'invoice':invoice})
        context['items'] = invoice.invoice_lines.all()  # Replace this with your actual query
        context['invoice'] = invoice
        return context
      
    def form_valid(self, form):
        # Set the invoice explicitly if it's not set by the form
        invoice = get_object_or_404(Invoice, pk=self.kwargs['pk'])
        form.instance.invoice = invoice  # Associate this line with the correct invoice
        
        self.object = form.save()  # Save the new InvoiceLine

        # Redirect to add more lines for the same invoice
        self.success_url = reverse_lazy('invoice-add_lines', kwargs={'pk': self.object.invoice.pk})
        return super().form_valid(form)
    
class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = 'entry/invoice_details.html'
    context_object_name = 'invoice'
    
    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        invoice = get_object_or_404(Invoice, pk=pk)
        context = super().get_context_data(**kwargs)
        context['items'] = invoice.invoice_lines.all()  # Replace this with your actual query
        return context
    
class InvoiceDetailSearchView(DetailView):
    
    model = Invoice
    template_name = 'entry/invoice_search_details.html'
    context_object_name = 'invoice'
    
    def get_object(self):
        """
        Override get_object to search by invoice_number.
        """
        invoice_number = self.request.GET.get('invoice_number')
        if invoice_number:
            try:
                return Invoice.objects.get(number=invoice_number)
            except Invoice.DoesNotExist:
                return None
        return None

    def get_context_data(self, **kwargs):
        """
        Add the search form and invoice details to the context.
        """
        context = super().get_context_data(**kwargs)
        context['form'] = InvoiceSearchForm(self.request.GET or None)
        return context

def invoice_pay_balance(request, pk):
    # Retrieve the invoice
    invoice = get_object_or_404(Invoice, pk=pk)
    
    # Update the paid_status to "FP" (Fully Paid)
    invoice.paid_status = "FP"
    invoice.save()
    
    # Redirect to the invoice detail or list page
    return redirect('invoice-list')

def invoice_exit(request,pk):
    invoice = get_object_or_404(Invoice,pk=pk)
    invoice.exit_status = True
    invoice.exit_datetime = timezone.now()
    invoice.save()
    
    return redirect('invoice-detail',pk)

def banknote_form(request):
    context = {}
    return render(request, 'banknote_form.html',context)

class BanknoteCreateView(CreateView):
    model = Banknote
    form_class = BanknoteForm
    template_name = 'entry/banknote_form.html'
    success_url = reverse_lazy('home')
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        last_banknote = Banknote.objects.order_by('-id').first()
        context['last_banknote'] = last_banknote
        return context
    

    
