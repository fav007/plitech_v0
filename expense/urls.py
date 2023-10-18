from django.urls import path
from .views import ExpenseCreateView,ExpenseListView,ExpenseUpdateView

urlpatterns = [
    path('create/',ExpenseCreateView.as_view(),name='expense-create'),
    path('list/',ExpenseListView.as_view(),name='expense-list'),
    path('list/<int:pk>/update',ExpenseUpdateView.as_view(),name='expense-update')
]