from django.urls import path
from .views import HomePageView, AboutPageView, ListCustomers,CustomersDetailView,CustomerCreateView

urlpatterns = [
path('', HomePageView.as_view(), name='home'),
path('about/', AboutPageView.as_view(),name='about'),
path('list/' ,ListCustomers.as_view(),name='list-customers'),
path('<int:pk>/', CustomersDetailView.as_view(), name='customer-detail'),
path('create/', CustomerCreateView.as_view(), name='customer-create'),
]