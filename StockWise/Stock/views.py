
import requests
from django.http import HttpResponse
from django.template import loader

from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from UserProfile.models import userprofile
from django.contrib.auth.decorators import login_required
from decimal import Decimal
@login_required
def dashboard(request) :
    #username = request.user.username
    asipchange = requests.post("https://www.cse.lk/api/aspiData").json().get('change')
    sppchange = requests.post("https://www.cse.lk/api/snpData").json().get('change')
    asip = requests.post("https://www.cse.lk/api/aspiData").json().get('value')
    spp = requests.post("https://www.cse.lk/api/snpData").json().get('value')
    template = loader.get_template('dashboard.html')
    
    if (asipchange < 0) :
        asipmark = 'negetive'
    else :
        asipmark = "positive"
        
    if (sppchange < 0) :
        sppmark = 'negetive'
    else :
        sppmark = "positive"
    
    if request.method == 'POST':
       
        if (request.POST.get('wi') == "Deposit") :
            
            new = userprofile.objects.get(username=request.user.username).cash_balance  + Decimal(request.POST.get('am').strip())
            user = userprofile.objects.get(username=request.user.username)
           
            user.cash_balance = new
            user.save()
            return redirect('/dashboard/')
        if (request.POST.get('wi') == "Withdraw") :
            
            new = userprofile.objects.get(username=request.user.username).cash_balance  - Decimal(request.POST.get('am').strip())
            user = userprofile.objects.get(username=request.user.username)
           
            user.cash_balance = new
            user.save()
            return redirect('/dashboard/')
    # Render the registration page template (GET request)
    context = {
        'asipchange' : asipchange,
        'sppchange' : sppchange,
        'asip' : asip ,
        'asipmark' : asipmark,
        'spp' : spp ,
        'sppmark' : sppmark,
        'bal' : userprofile.objects.get(username=request.user.username).cash_balance ,
    }    
    
    return HttpResponse(template.render(context,request))
    
    