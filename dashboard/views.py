
from django.db.models.functions import TruncMonth

from django.shortcuts import render
from django.db.models import Count, Sum, F,Min,Max,ExpressionWrapper, FloatField,IntegerField
from customers.models import Customers
from entry.models import BE,Invoice,BE_line,InvoiceLine
from expense.models import Jirama

from django.db.models.functions import TruncMonth
from datetime import date, timedelta,datetime

def dashboard_overview(request):
    # General Metrics
    total_customers = Customers.objects.count()
    total_invoices = Invoice.objects.count()
    total_bes = BE.objects.count()
    total_revenue = Invoice.objects.aggregate(total=Sum('total'))['total']
    total_metal_revenue = Invoice.objects.aggregate(total_sm=Sum('total_sm'))['total_sm']
    total_sheet_metal = BE_line.objects.aggregate(total_sheet_metal=Sum('sm_eqv'))['total_sheet_metal']
    
    #####################
    # Markting indicator
    #AVO - Panier moyen
    average_order_value = total_revenue / total_invoices
    purchase_frequency = total_invoices / total_customers
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
        'average_order_value':average_order_value,
        'purchase_frequency':purchase_frequency
    }

    return render(request, 'dashboard/overview.html', context)



def dashboard_utilities_view(request):
    # 1. Monthly SM_EQV (Sum from BE_line)
    monthly_sm_eqv = (
        BE_line.objects.annotate(
            month=TruncMonth('be__date_entry')  # Extract month from BE's entry date
        )
        .values('month')  # Group by month
        .annotate(total_sm_eqv=Sum('sm_eqv'))  # Sum sm_eqv
        .order_by('month')  # Order by year and month
    )

    # 2. Electricity consumption (from Jirama)
    monthly_electricity = (
        Jirama.objects.annotate(
            month=TruncMonth('date')  # Extract month from the date field
        )
        .values('month')  # Group by month
        .annotate(
            first_index=Min('index'),  # Minimum index for the month
            last_index=Max('index'),  # Maximum index for the month
            consumption=F('last_index') - F('first_index')  # Difference = consumption
        )
        .values('month', 'consumption')  # Select only month and consumption
        .order_by('month')  # Order by year and month
    )

    # 3. Monthly Invoice Summary (Sum of qty * unit_price from InvoiceLine)
    monthly_invoice_summary = (
        InvoiceLine.objects.annotate(
            month=TruncMonth('invoice__date'),  # Extract month from related Invoice date
            total_price=ExpressionWrapper(
                F('qty') * F('unit_price'),  # Calculate total price per line
                output_field=IntegerField()
            )
        )
        .values('month')  # Group by month
        .annotate(total_invoice_sum=Sum('total_price'))  # Sum of all totals
        .order_by('month')  # Order by year and month
    )

    # Combine the data into a single dictionary keyed by month
    monthly_data = {}

    # Process monthly SM_EQV data
    for entry in monthly_sm_eqv:
        month_key = entry['month'].strftime('%B %Y')  # Format: "Month Year"
        monthly_data.setdefault(month_key, {'sm_eqv': 0, 'consumption': 0, 'total_invoice_sum': 0})
        monthly_data[month_key]['sm_eqv'] = entry['total_sm_eqv']

    # Process electricity consumption data
    for entry in monthly_electricity:
        month_key = entry['month'].strftime('%B %Y')  # Format: "Month Year"
        monthly_data.setdefault(month_key, {'sm_eqv': 0, 'consumption': 0, 'total_invoice_sum': 0})
        monthly_data[month_key]['consumption'] = entry['consumption']

    # Process monthly Invoice Summary data
    for entry in monthly_invoice_summary:
        month_key = entry['month'].strftime('%B %Y')  # Format: "Month Year"
        monthly_data.setdefault(month_key, {'sm_eqv': 0, 'consumption': 0, 'total_invoice_sum': 0})
        monthly_data[month_key]['total_invoice_sum'] = entry['total_invoice_sum']

    # Format the data for rendering in the template
    formatted_data = [
    {
        'month': month,
        'sm_eqv': values['sm_eqv'],
        'consumption': values['consumption'],
        'total_invoice_sum': values['total_invoice_sum']
    }
    for month, values in sorted(
        monthly_data.items(),
        key=lambda x: datetime.strptime(x[0], '%B %Y')  # Convert "Month Year" back to a date
    )
]

    # Pass the formatted data to the template
    context = {
        'monthly_data': formatted_data
    }
    return render(request, 'dashboard/utilities.html', context)
