
import requests
from django.http import HttpResponse
from django.template import loader
from userstocks.views import A
from django.shortcuts import render, redirect
from userstocks.models import userstocks
from django.contrib.auth.decorators import login_required
import collections
from UserProfile.models import userprofile
from django.contrib.auth.decorators import login_required
from decimal import Decimal , ROUND_HALF_UP
# Assuming you have a Stock model and the necessary imports
from django.shortcuts import render
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
# from .models import Stock # Your Stock model import

# --- Integration of Aggregation Logic ---

def consolidate_portfolio_data(raw_positions):
    """
    Takes raw database results (QuerySet or list) and consolidates them
    by symbol to calculate the weighted average cost basis.
    """
    # Use a dictionary to hold consolidated data {symbol: data}
    consolidated = {}
    
    for position in raw_positions:
        symbol = position.symbol  # Assuming 'position' is a model instance
        qty = position.qty
        price_paid = position.price
        
        # Calculate the total cost of this specific trade
        trade_cost = qty * price_paid
        
        if symbol not in consolidated:
            # Initialize if this is the first time we see the symbol
            consolidated[symbol] = {
                'symbol': symbol,
                'total_qty': 0,
                'total_cost': 0.0,
                'current_price': 0.0, # You will fetch this later or it's on the model
            }

        # Add to the running totals
        consolidated[symbol]['total_qty'] += qty
        trade_cost =Decimal(trade_cost)
        consolidated[symbol]['total_cost'] = Decimal(consolidated[symbol]['total_cost'] )
        consolidated[symbol]['total_cost']  += trade_cost

    # Finalize the average cost calculation
    final_portfolio = []
    
    # NOTE: You will need to fetch the 'current_price' for each symbol here 
    # from a financial API before calculating the final metrics (Market Value, Gain/Loss).
    # For now, we only calculate the Avg Cost Basis:
    
    for data in consolidated.values():
        total_cost = data['total_cost']
        total_qty = data['total_qty']
        
        
        base_url = "https://www.cse.lk/api/"
        endpoint = "companyInfoSummery"
        #data = {"symbol": "LOLC.N0000"}
       # data = {"symbol": data['symbol']}

        response = requests.post(base_url + endpoint, data=data)

        
        
        
        
        
        # Weighted Average Cost Basis calculation
        data['avg_cost'] = round(total_cost / total_qty, 2) if total_qty > 0 else 0
        
       
        response_data = response.json()


        symbol_info = response_data.get('reqSymbolInfo')
        TWO_PLACES = Decimal("0.00")

        if symbol_info:
            last_traded_price = symbol_info.get('lastTradedPrice')
            a=Decimal(last_traded_price)
            rounded_price = a.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)
   
            data['current_price'] =  rounded_price
      





        data['current_value'] = round(total_qty * data['current_price'], 2)
        data['gain_loss_percent'] = round((data['current_value'] - total_cost) / total_cost * 100, 2) if total_cost > 0 else 0


        final_portfolio.append(data)
        
    return final_portfolio


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
    user_stocks_list = userstocks.objects.filter(username=request.user.username)
    

    final_portfolio = consolidate_portfolio_data(user_stocks_list)

    
    context = {
        'user_stocks': final_portfolio,
        'asipchange' : asipchange,
        'sppchange' : sppchange,
        'asip' : asip ,
        'asipmark' : asipmark,
        'spp' : spp ,
        'sppmark' : sppmark,
        'bal' : userprofile.objects.get(username=request.user.username).cash_balance ,
    }    
    
    return HttpResponse(template.render(context,request))
