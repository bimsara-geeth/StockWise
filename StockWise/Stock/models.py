

#import Stock.models
from django.db import models
from django.utils import timezone

class StockData(models.Model):
   
    # Primary Key and Identifiers
    # We set id as the primary key since it is unique and provided by the API
    stock_id = models.IntegerField(primary_key=True, verbose_name="ID from API")
    name = models.CharField(max_length=255)
    # symbol is set to be unique for easy lookup
    symbol = models.CharField(max_length=50, unique=True)
    # Storing as CharField as per the "DD/MMM/YYYY" format in the sample data
    issue_date = models.CharField(max_length=50) 

    # Trading Metrics
    price = models.DecimalField(max_digits=15, decimal_places=2, help_text="Last Traded Price")
    quantity = models.IntegerField(help_text="Quantity")
    percentage_change = models.DecimalField(max_digits=10, decimal_places=5)
    change = models.DecimalField(max_digits=10, decimal_places=2)
    previous_close = models.DecimalField(max_digits=15, decimal_places=2)
    high = models.DecimalField(max_digits=15, decimal_places=2)
    low = models.DecimalField(max_digits=15, decimal_places=2)
    open = models.DecimalField(max_digits=15, decimal_places=2)
    closing_price = models.DecimalField(max_digits=15, decimal_places=2)

    # Volume and Turnover
    turnover = models.DecimalField(max_digits=20, decimal_places=2)
    share_volume = models.IntegerField()
    trade_volume = models.IntegerField()
    crossing_volume = models.IntegerField()
    crossing_trade_vol = models.IntegerField()

    # Market Data
    market_cap = models.DecimalField(max_digits=25, decimal_places=2)
    market_cap_percentage = models.DecimalField(max_digits=10, decimal_places=5)
    
    # Status and Time
    status = models.IntegerField(help_text="Status code from API")
    # Store timestamp as BigIntegerField and convert to datetime when needed
    last_traded_time = models.BigIntegerField(help_text="Last Traded Time (milliseconds since epoch)")

    # Metadata for tracking updates
    # auto_now=True updates the time every time the object is saved
    updated_at = models.DateTimeField(auto_now=True) 
    # auto_now_add=True sets the time only when the object is created
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Stock Data"
        verbose_name_plural = "Stock Data"
        # Ordering by symbol makes it easy to view/debug
        ordering = ['symbol']

    def __str__(self):
        return f"{self.name} ({self.symbol}) - Price: {self.price}"

    def get_last_traded_datetime(self):
        """Converts the BigIntegerField timestamp (milliseconds) to a timezone-aware datetime object."""
        # Convert milliseconds to seconds, then to a timezone-aware datetime
        return timezone.datetime.fromtimestamp(self.last_traded_time / 1000.0, tz=timezone.utc)