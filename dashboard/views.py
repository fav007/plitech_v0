from django.shortcuts import render

from django.shortcuts import render
from django.db.models import Count, Sum
from customers.models import Customers
from entry.models import BE,Invoice

def dashboard_overview(request):
    # General Metrics
    total_customers = Customers.objects.count()
    total_invoices = Invoice.objects.count()
    total_bes = BE.objects.count()
    total_revenue = Invoice.objects.aggregate(total=Sum('total'))['total']
    total_metal_revenue = Invoice.objects.aggregate(total_sm=Sum('total_sm'))['total_sm']
    
    # BE Status Breakdown
    be_statuses = BE.objects.values('status').annotate(count=Count('status'))

    # Customer Location Distribution
    customer_locations = Customers.objects.values('location').annotate(count=Count('location'))

    # Latest BE Entries
    latest_be_entries = BE.objects.order_by('-date_entry')[:5]  # Last 5 entries

    # Data for Chart.js
    context = {
        'total_customers': total_customers,
        'total_invoices': total_invoices,
        'total_bes': total_bes,
        'total_revenue': total_revenue,
        'total_metal_revenue': total_metal_revenue,
        'be_statuses': be_statuses,
        'customer_locations': customer_locations,
        'latest_be_entries': latest_be_entries,
    }

    return render(request, 'dashboard/overview.html', context)

