from django.urls import path
from .views import dashboard_overview,dashboard_utilities_view

urlpatterns = [
    path('overview/',dashboard_overview,name='overview'),
    path('utilities/',dashboard_utilities_view,name='dashboard-utilities'),
]