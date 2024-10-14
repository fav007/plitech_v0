from django.contrib import admin
from django.urls import path,include
from customers import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls')),
    path('customers/', include('customers.urls')),
    path('',views.HomePageView.as_view(),name='home'),
    path('entry/', include('entry.urls')),
    path('expense/',include('expense.urls')),
    path('dashboard/',include('dashboard.urls'))
    
]

admin.site.site_header = 'Plitech Service Administration'
admin.site.site_title = 'PLITECH'