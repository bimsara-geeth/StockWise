import json

from django.http import HttpResponse
from django.shortcuts import render
from portfolio import views

from django.template import loader

def dashboard_view(request):
    template = loader.get_template('dashboard.html')
    
    context = {
        'holdings': views.get_consolidated_portfolio(request.user),
    }
    # print(context['holdings']['JKH.N0000']['name'])
    return HttpResponse(template.render(context,request))