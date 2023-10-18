from django.shortcuts import render
from django.views.generic import CreateView,ListView,UpdateView
from .models import Expense
from .forms import ExpenseForm
from django.urls import reverse_lazy

class ExpenseCreateView(CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expense/create_form.html' 
    success_url = reverse_lazy('expense-list')
    
class ExpenseListView(ListView):
    model = Expense
    template_name = 'expense/list_view.html'
    context_object_name = 'expenses'
    
class ExpenseUpdateView(UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expense/create_form.html'
    success_url = reverse_lazy('expense-list')