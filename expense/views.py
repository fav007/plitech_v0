from django.shortcuts import render
from django.views.generic import CreateView,ListView,UpdateView,DeleteView
from .models import Expense,Jirama
from .forms import ExpenseForm,JiramaForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class ExpenseCreateView(LoginRequiredMixin,CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expense/create_form.html' 
    success_url = reverse_lazy('expense-list')
    
class ExpenseListView(LoginRequiredMixin,ListView):
    model = Expense
    template_name = 'expense/list_view.html'
    context_object_name = 'expenses'
    
class ExpenseUpdateView(LoginRequiredMixin,UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expense/create_form.html'
    success_url = reverse_lazy('expense-list')
    
class JiramaCreateView(LoginRequiredMixin,CreateView):
    model = Jirama
    form_class = JiramaForm
    template_name = 'expense/create_jirama.html'
    success_url = reverse_lazy('jirama-list')
    
class JiramaListView(LoginRequiredMixin, ListView):
    model = Jirama
    template_name = 'expense/list_jirama.html'
    context_object_name = 'jiramas'
    ordering = '-date'
    
    
# Update view to edit existing Jirama entry
class JiramaUpdateView(LoginRequiredMixin,UpdateView):
    model = Jirama
    form_class = JiramaForm
    template_name = 'expense/create_jirama.html'
    success_url = reverse_lazy('jirama-list')  # Redirect after successful update
    
class JiramaDeleteView(LoginRequiredMixin,DeleteView):
    model = Jirama
    success_url = reverse_lazy('jirama-list')
    
    