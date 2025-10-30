import datetime
from decimal import ROUND_HALF_UP, Decimal
from stock import views
from portfolio.models import myportfolio

def get_portfolio(user):
    return myportfolio.objects.filter(user=user)

def get_consolidated_portfolio(user):
    portfolio = get_portfolio(user)
    raw_positions = get_portfolio(user)
    # consolidated_portfolio = {}

    # for position in portfolio:
    #     symbol = str(position.stock_symbol)
    #     try:
    #         qty = int(position.quantity)
    #     except (TypeError, ValueError):
    #         qty = 0
    #     try:
    #         price_paid = Decimal(str(position.purchase_price))
    #     except Exception:
    #         price_paid = Decimal('0.00')
    #     date_purchased = position.date_purchased

    #     # if isinstance(date_purchased, datetime):
    #     #     purchase_date = date_purchased.date()

    #     #     days_held = (datetime.date.today() - purchase_date).days if purchase_date else 0

    #     #     stock_days = days_held * qty
 

        
        
    #     if symbol not in consolidated_portfolio:
    #         consolidated_portfolio[symbol] = {
    #             'symbol': symbol,
    #             'name' : views.get_name(symbol),
    #             'total_qty': 0,
    #             'total_cost': Decimal('0.00'),
    #             'current_price': Decimal('0.00'),
    #             'stock_days': 0,
    #             'ave_price' : Decimal('0.00')
    #         }

    #     consolidated_portfolio[symbol]['total_qty'] += qty
    #     consolidated_portfolio[symbol]['total_cost'] += Decimal(qty) * price_paid
    #     # consolidated_portfolio[symbol]['stock_days'] += stock_days
    #     if consolidated_portfolio[symbol]['total_qty'] > 0:
    #         consolidated_portfolio[symbol]['ave_price'] = (consolidated_portfolio[symbol]['total_cost'] / Decimal(consolidated_portfolio[symbol]['total_qty'])).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    #     else:
    #         consolidated_portfolio[symbol]['ave_price'] = Decimal('0.00')
   

        
    # return consolidated_portfolio
    
    """
    Takes raw database results (QuerySet or list) and consolidates them
    by symbol to calculate the weighted average cost basis.
    """
    # Use a dictionary to hold consolidated data {symbol: data}
    consolidated = {}
    
    for position in raw_positions:
        symbol = position.stock_symbol  # Assuming 'position' is a model instance
        qty = position.quantity
        price_paid = position.purchase_price
        
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
    totalinvestment = 0
    totalvalue = 0
    for data in consolidated.values():
        data['name'] = views.get_name(data['symbol'])
        total_cost = data['total_cost']
        total_qty = data['total_qty']
     
        data['value'] =  round(total_qty * views.get_price(data['symbol']), 2)
        data['avg_cost'] = round(total_cost / total_qty, 2) if total_qty > 0 else 0
        
        # Placeholder for real-time data integration
        data['current_price'] = round(views.get_price(data['symbol']), 2)
        # data['current_value'] = round(total_qty * data['current_price'], 2)
        # data['gain_loss_percent'] = round((data['current_value'] - total_cost) / total_cost * 100, 2) if total_cost > 0 else 0


        final_portfolio.append(data)
        final_portfolio.sort(key=lambda x: x['symbol'], reverse=True)

        totalinvestment += total_cost
        totalvalue += data['value']
        
    
    return final_portfolio
