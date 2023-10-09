from django.urls import path
from .views import (BECreateView,BEListView,BEUpdateView,AddLinesBEView,BEDetailsView,add_lines_be_view,
                    InvoiceCreateView,InvoiceListView)

urlpatterns = [
    path('create/', BECreateView.as_view(),name='be-create'),
    path('list/<int:pk>/add_lines/', AddLinesBEView.as_view(), name='be-add_lines'),
    path('list/', BEListView.as_view(),name='be-list'),
    path('list/<int:pk>/',BEDetailsView.as_view(),name='be-details'),
    path('list/<int:pk>/update/',BEUpdateView.as_view(),name='be-update'),
    path('list/<int:pk>/create_invoice/', InvoiceCreateView.as_view(),name='invoice-create'),
    path('list_invoice/', InvoiceListView.as_view(),name='invoice-list'),
]