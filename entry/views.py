from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from django.views.generic import CreateView, ListView ,UpdateView , DetailView
from .models import BE,BE_line,Customers,Invoice,InvoiceLine,Banknote
from .forms import BEForm,LineBEForm,LineBEFormSet,InvoiceForm,InvoiceLineForm,BanknoteForm
from django.urls import reverse_lazy

class BECreateView(CreateView):
    model = BE
    form_class = BEForm
    template_name = 'entry/be_form.html'
    success_url = reverse_lazy('be-list')  # Redirect URL after successful form submission
    
class BEListView(ListView):
    model = BE
    template_name = 'entry/be_list.html'
    context_object_name = 'bes'
    
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
      # Redirigez ici après l'ajout de lignes
    
    
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
        # Save the form and get the BE instance
        self.object = form.save()
        # Get the 'pk' of the related BE instance
        pk = self.object.be.pk
        # Use reverse_lazy to generate the 'be-details' URL with the 'pk' argument
        # self.success_url = reverse_lazy('be-details', kwargs={'pk': pk})
        self.success_url = reverse_lazy('be-add_lines', kwargs={'pk': pk})
        return super().form_valid(form)
    
    
    
def add_lines_be_view(request,pk):
    be = BE.objects.get(pk=pk)
    context={'be':be}
    return render(request,template_name='entry/try.html',context=context)


class InvoiceCreateView(CreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'entry/invoice_form.html'
    success_url = reverse_lazy('invoice-list')
    
    # def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        
    #     pk = self.kwargs.get('pk')
    #     be = get_object_or_404(BE, pk=pk)
    #     context = super().get_context_data(**kwargs)
    #     context['be'] = be
        
    
        # context['form'] = InvoiceForm(initial={'be' : be })
        # return context
    # def form_valid(self, form):
    #     be_id = self.kwargs['pk']
    #     be = BE.objects.get(pk=be_id)
    #     form.instance.be = be
    #     return super().form_valid(form)
    
    # def get_initial(self):
        
    #     pk = self.kwargs.get('pk')
    #     be = get_object_or_404(BE, pk=pk)
    #     initial = super().get_initial()
        
    #     initial['be'] = be  # 'be' should match the field name in your InvoiceForm
    #     return initial
    def get_initial(self):
        initial = super().get_initial()
        pk = self.kwargs.get('pk')
        be = get_object_or_404(BE, pk=pk)
        initial['be'] = be
        return initial

    def form_valid(self, form):
        # Get the ModelA instance based on the ID from the URL
        be = get_object_or_404(BE, pk=self.kwargs['pk'])
        # Associate the ModelA instance with ModelB and save
        form.object = form.save()
        return super().form_valid(form)
    
class InvoiceListView(ListView):
    model = Invoice
    template_name = 'entry/invoice_list.html'
    context_object_name = 'invoices'

class InvoiceAddLineView(CreateView):
    model = InvoiceLine
    form_class = InvoiceLineForm
    template_name = 'entry/invoice_add_lines.html'
    success_url = reverse_lazy('invoice-list')

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        invoice = get_object_or_404(Invoice, pk=pk)

        be = invoice.be
        be_line = BE_line.objects.filter(be=be)
        context = super().get_context_data(**kwargs)
        context['form'] = InvoiceLineForm(initial={'invoice':invoice})
        context['items'] = invoice.invoice_lines.all()  # Replace this with your actual query
        context['invoice'] = invoice
        return context
    
    
    def form_valid(self, form):

        self.object = form.save()
        pk = self.object.invoice.pk
        self.success_url = reverse_lazy('invoice-add_lines', kwargs={'pk': pk})
        return super().form_valid(form)
    
class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = 'entry/invoice_details.html'
    context_object_name = 'invoice'

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