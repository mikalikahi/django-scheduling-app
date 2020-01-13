from django.shortcuts import render, get_object_or_404

from .models import StudentBilling

def low_hours_list_view(request):
    qs = StudentBilling.custom_query.under_two_hours()
    heading = 'Student Accounts with Pending Updates'
    context = {
        'heading': heading,
        'queryset': qs,
    }
    template = "class_billing_admin/billing_account_list.html"
    return render(request, template, context)

def billing_accounts_list_view(request):
    qs = StudentBilling.objects.all()
    heading = "Student Accounts Information"
    context = {
        'heading': heading,
        'queryset': qs,
    }
    template = "class_billing_admin/billing_account_list.html"
    return render(request, template, context)

def class_billing_detail_view(request, slug=None):
    object = get_object_or_404(StudentBilling, slug=slug)
    context = {
        'object': object,
    }
    template = "class_billing_admin/class_billing_account_detail.html"
    return render(request, template, context)

