
import requests
from django.http import HttpResponse
from django.template import loader
from userstocks.views import A
from django.shortcuts import render, redirect
from userstocks.models import userstocks
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
    # try:
    #     user_stocks_list = userstocks.objects.get(username=request.user.username)
    # # Logic if the object is found
    # except userstocks.DoesNotExist:
    # # Logic if the object is NOT found (e.g., create a default)
   
   
    #      user_stocks_list = userstocks.objects.create(username=request.user, qty=0,price=0.0,symbol='non')
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
        if (request.POST.get('bs') == "Buy") :
            A.addstock(request.user.username, request.POST.get('sym') ,Decimal(request.POST.get('price').strip()), int(request.POST.get('qty').strip()) )
           
           
        if (request.POST.get('bs') == "Sell") :
            A.sellstock(request.user.username, request.POST.get('sym') ,Decimal(request.POST.get('price').strip()), int(request.POST.get('qty').strip()) )
           
    # Render the registration page template (GET request)
   # user_stocks_list = userstocks.objects.filter(username=request.user.username)
    context = {
        #'user_stocks': user_stocks_list,
        'asipchange' : asipchange,
        'sppchange' : sppchange,
        'asip' : asip ,
        'asipmark' : asipmark,
        'spp' : spp ,
        'sppmark' : sppmark,
        'bal' : userprofile.objects.get(username=request.user.username).cash_balance ,
    }    
    
    return HttpResponse(template.render(context,request))
