from django.urls import path
from .views import (ExpenseCreateView,ExpenseListView,ExpenseUpdateView,
                    JiramaCreateView,JiramaListView)

urlpatterns = [
    path('create/',ExpenseCreateView.as_view(),name='expense-create'),
    path('list/',ExpenseListView.as_view(),name='expense-list'),
    path('list/<int:pk>/update',ExpenseUpdateView.as_view(),name='expense-update'),
    path('create_jirama/',JiramaCreateView.as_view(),name='jirama-create'),
    path('list_jirama/',JiramaListView.as_view(),name='jirama-list'),
]