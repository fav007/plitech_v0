from django.shortcuts import render

from django.shortcuts import render
from django.db.models import Count, Sum, F
from customers.models import Customers
from entry.models import BE,Invoice,BE_line,InvoiceLine

from django.db.models.functions import TruncMonth
from datetime import date, timedelta

def dashboard_overview(request):
    # General Metrics
    total_customers = Customers.objects.count()
    total_invoices = Invoice.objects.count()
    total_bes = BE.objects.count()
    total_revenue = Invoice.objects.aggregate(total=Sum('total'))['total']
    total_metal_revenue = Invoice.objects.aggregate(total_sm=Sum('total_sm'))['total_sm']
    total_sheet_metal = BE_line.objects.aggregate(total_sheet_metal=Sum('sm_eqv'))['total_sheet_metal']
    
    # BE Status Breakdown
    be_statuses = BE.objects.values('status').annotate(count=Count('status'))

    # Customer Location Distribution
    customer_locations = Customers.objects.values('location').annotate(count=Count('location'))

    # Latest BE Entries
    latest_be_entries = BE.objects.order_by('-date_entry')[:5]  # Last 5 entries

    # Calculate sm_eqv data grouped by month and year for the past two years
    today = date.today()
    two_years_ago = today - timedelta(days=730)
    
    sm_eqv_by_month = (
        BE_line.objects.filter(be__date_entry__gte=two_years_ago)
        .annotate(month=TruncMonth('be__date_entry'))
        .values('month')
        .annotate(total_sm_eqv=Sum('sm_eqv'))
        .order_by('month')
    )

    # Format data for Chart.js
    chart_labels = [data['month'].strftime('%b-%Y') for data in sm_eqv_by_month]
    chart_data = [int(data['total_sm_eqv']) for data in sm_eqv_by_month]
    
    # Query to group data by month-year and calculate total revenue
    invoice_line_data = (
    InvoiceLine.objects.annotate(month_year=TruncMonth('invoice__date'))  # Group by month-year
    .values('month_year')  # Select month-year
    .annotate(total_revenue=Sum(F('unit_price') * F('qty')))  # Sum(unit_price * qty)
    .order_by('month_year')  # Sort by date
    )

    # Prepare data for the chart
    revenue_chart_labels = [item['month_year'].strftime('%b %Y') for item in invoice_line_data]  # E.g., 'Jan 2025'
    revenue_chart_data = [item['total_revenue'] for item in invoice_line_data]

    # Context Data
    context = {
        'total_customers': total_customers,
        'total_invoices': total_invoices,
        'total_bes': total_bes,
        'total_revenue': total_revenue,
        'total_metal_revenue': total_metal_revenue,
        'be_statuses': be_statuses,
        'customer_locations': customer_locations,
        'latest_be_entries': latest_be_entries,
        'total_sheet_metal': total_sheet_metal,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'revenue_chart_labels': revenue_chart_labels,
        'revenue_chart_data': revenue_chart_data,
    }

    return render(request, 'dashboard/overview.html', context)
