from django.shortcuts import render
from requests.api import request


def staff_dashboard(request):
    return render(request, 'staff_template/home_content.html')