# app_name/services.py (Place this in your Django app's directory)
import requests
from django.db import transaction
from .models import StockData
from decimal import Decimal

# --- API Configuration ---
BASE_URL = "https://www.cse.lk/api/"
ENDPOINT = "tradeSummary"
API_URL = BASE_URL + ENDPOINT

def fetch_stock_data():
    """Fetches the latest stock data from the external API."""
    try:
        response = requests.post(API_URL)
        
        # The API documentation implies a POST request without a specific body for all data
        #response = requests.post(API_URL, timeout=10)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching stock data: {e}")
        return None

def transform_stock_data(data):
    """
    Transforms the API data structure to match the StockData model fields.
    Handles data type conversions (floats/ints from JSON to Decimal/Int in Django).
    """
    try:
        return {
            'stock_id': data['id'],
            'name': data['name'],
            'symbol': data['symbol'],
            'issue_date': data['issueDate'],
            'price': Decimal(str(data['price'])),
            # 'price': Decimal(data['price']),
            'quantity': data['quantity'],
            'percentage_change': Decimal(str(data['percentageChange'])),
            'change': Decimal(str(data['change'])),
            'previous_close': Decimal(str(data['previousClose'])),
            'high': Decimal(str(data['high'])),
            'low': Decimal(str(data['low'])),
            'open': Decimal(str(data['open'])),
            'closing_price': Decimal(str(data['closingPrice'])),
            'turnover': Decimal(str(data['turnover'])),
            
            # 'percentage_change': Decimal(data['percentageChange']),
            # 'change': Decimal(data['change']),
            # 'previous_close': Decimal(data['previousClose']),
            # 'high': Decimal(data['high']),
            # 'low': Decimal(data['low']),
            # 'open': Decimal(data['open']),
            # 'closing_price': Decimal(data['closingPrice']),
            # 'turnover': Decimal(data['turnover']),
            
            
            'share_volume': data['sharevolume'],
            'trade_volume': data['tradevolume'],
            'crossing_volume': data['crossingVolume'],
            'crossing_trade_vol': data['crossingTradeVol'],
            'market_cap': Decimal(str(data['marketCap'])),
            'market_cap_percentage': Decimal(str(data['marketCapPercentage'])),
            # 'market_cap': Decimal(data['marketCap']),
            # 'market_cap_percentage': Decimal(data['marketCapPercentage']),
            
            
            #'market_cap': Decimal(str(data['marketCap'])),
            #'market_cap_percentage': Decimal(str(data['marketCapPercentage'])),
            
            
            'status': data['status'],
            'last_traded_time': data['lastTradedTime'],
        }
    except KeyError as e:
        #print(f"Missing key in API data: {e} for symbol {data.get('symbol', 'Unknown')}")
        return None
    except Exception as e:
        #print(f"Error transforming data for symbol {data.get('symbol', 'Unknown')}: {e}")
        return None

def update_or_create_stock_data_daily():
    """
    Primary method to fetch, transform, and update/create stock records in the database.
    This method should be called daily (e.g., via a management command or scheduled task).
    """
    stock_list = fetch_stock_data()
    if stock_list is None:
        print("Update failed: Could not fetch stock data.")
        return 0

    update_count = 0
    create_count = 0

    # Use a transaction for atomicity: all updates/creates succeed or none of them do
    with transaction.atomic():
        for stock_data in stock_list:
            transformed_data = transform_stock_data(stock_data)
            if transformed_data:
                # Get the primary key (stock_id) to check for existence
                stock_id = transformed_data.pop('stock_id')

                # Use update_or_create to handle both new and existing stocks efficiently
                # The 'symbol' is the unique field we would use if 'stock_id' wasn't present
                # Here, we use the primary key 'stock_id' for lookup
                try:
                    obj, created = StockData.objects.update_or_create(
                        stock_id=stock_id, 
                        defaults=transformed_data
                    )
                    
                    if created:
                        create_count += 1
                        print(f"Created new record for: {obj.symbol}")
                    else:
                        update_count += 1
                        print(f"Updated record for: {obj.symbol}")
                except Exception as e:
                    # In case of database error (e.g., Decimal precision, integrity error)
                    print(f"Database error for stock ID {stock_id}: {e}")
        
    print(f"\n--- Daily Stock Data Update Complete ---")
    print(f"Records created: {create_count}")
    print(f"Records updated: {update_count}")
    return update_count + create_count

# Example usage (for testing/immediate run)
# if __name__ == '__main__':
#     # This block would only run if you execute services.py directly, 
#     # which is usually not how Django works, but useful for initial testing.
#     # You would typically call update_or_create_stock_data_daily() from 
#     # a Django management command or a scheduled task (like Celery/Cron job).
#     pass