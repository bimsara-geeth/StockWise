import datetime
from decimal import ROUND_HALF_UP, Decimal
from StockWise import stock
from StockWise.portfolio.models import myportfolio

def get_portfolio(user):
    return myportfolio.objects.filter(user=user)

def get_consolidated_portfolio(user):
    portfolio = get_portfolio(user)
    consolidated = {}

    for position in portfolio:
        symbol = position.stock_symbol
        qty = position.quantity
        price_paid = position.purchase_price
        date_purchased = position.date_purchased
        
        if isinstance(date_purchased, datetime):
            purchase_date = date_purchased.date()

            days_held = (datetime.date.today() - purchase_date).days if purchase_date else 0

            stock_days = days_held * qty
 

        
        
        if symbol not in consolidated:
            consolidated[symbol] = {
                'total_qty': 0,
                'total_cost': Decimal('0.00'),
                'current_price': Decimal('0.00'),
                'stock_days': 0
            }

        consolidated[symbol]['total_qty'] += qty
        consolidated[symbol]['total_cost'] += qty * price_paid
        consolidated[symbol]['stock_days'] += stock_days

    
    for symbol in consolidated.keys():
        current_price = stock.get_current_price(symbol)
        consolidated[symbol]['current_price'] = current_price

    return consolidated
