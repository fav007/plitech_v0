from django.urls import path
from .views import (BECreateView,BEListView,BEUpdateView,AddLinesBEView,BEDetailsView,add_lines_be_view,
                    InvoiceCreateView,InvoiceListView,BanknoteCreateView,InvoiceDetailView,InvoiceAddLineView,
                    InvoiceDetailSearchView,BEListNoInvView,InvoiceMakePaymentView,invoice_pay_balance,
                    invoice_exit,
                    )

urlpatterns = [
    
    path('create/', BECreateView.as_view(),name='be-create'),
    path('list/<int:pk>/add_lines/', AddLinesBEView.as_view(), name='be-add_lines'),
    path('list/', BEListView.as_view(),name='be-list'),
    path('list_no_inv/', BEListNoInvView.as_view(),name='be-list-no-inv'),
    path('list/<int:pk>/',BEDetailsView.as_view(),name='be-details'),
    path('list/<int:pk>/update/',BEUpdateView.as_view(),name='be-update'),
    path('list/<int:pk>/create_invoice/', InvoiceCreateView.as_view(),name='invoice-create'),
    path('invoice/<int:pk>/make_payment/', InvoiceMakePaymentView.as_view(),name='invoice-make-payment'),
    path('list_invoice/', InvoiceListView.as_view(),name='invoice-list'),
    path('list/<int:pk>/detail_invoice/', InvoiceDetailView.as_view(),name='invoice-detail'),
    path('invoice/<int:pk>/add_lines',InvoiceAddLineView.as_view(),name = 'invoice-add_lines'),
    path('banknote/create',BanknoteCreateView.as_view(),name='banknote-create'), 
    path('search-invoice/', InvoiceDetailSearchView.as_view(), name='search-invoice'),   
    path('invoice/<int:pk>/pay_balance',invoice_pay_balance,name="pay-balance"),
    path('invoice/<int:pk>/exit',invoice_exit,name='invoice-exit'),
    
    ]