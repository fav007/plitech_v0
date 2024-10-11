from django.shortcuts import render
from django.views.generic import CreateView,ListView,UpdateView
from .models import Expense,Jirama
from .forms import ExpenseForm,JiramaForm
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
    
class JiramaCreateView(CreateView):
    model = Jirama
    form_class = JiramaForm
    template_name = 'expense/create_jirama.html'
    success_url = reverse_lazy('jirama-list')
    
class JiramaListView(ListView):
    model = Jirama
    template_name = 'expense/list_jirama.html'
    context_object_name = 'jiramas'
    ordering = '-date'