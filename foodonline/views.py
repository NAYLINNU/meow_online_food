from django.shortcuts import render 
from django.http import HttpResponse

from vendor.models import Vendor


def home(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]#Take care double underscore front is_active
    context = {
        'vendors': vendors
    }
    return render(request,'home.html', context)