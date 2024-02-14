# apps/legal/views.py
from django.shortcuts import render

def privacy_policy(request):
    return render(request, 'legal/privacy_policy.html')

def terms_of_service(request):
    return render(request, 'legal/terms_of_service.html')
