from django.urls import path
from .views import (HomePageView, AboutPageView, ListCustomers,CustomersDetailView,CustomerCreateView,CustomersUpdateView,CustomersDeleteView,
                    PricingPageView,DashBoardPageView)

urlpatterns = [
path('', HomePageView.as_view(), name='home'),
path('about/', AboutPageView.as_view(),name='about'),
path('dashboard/', DashBoardPageView.as_view(),name='dashboard'),
path('pricing/', PricingPageView.as_view(),name='price-list'),
path('create/', CustomerCreateView.as_view(), name='customer-create'),
path('list/' ,ListCustomers.as_view(),name='customer-list'),
path('list/<int:pk>/', CustomersDetailView.as_view(), name='customer-detail'),
path('list/<int:pk>/update/', CustomersUpdateView.as_view(), name='customer-update'),
path('list/<int:pk>/delete/', CustomersDeleteView.as_view(), name='customer-delete'),





]