from decimal import Decimal
from django.db import models

class userstocks(models.Model):
    # This creates a one-to-one link to the built-in User model
    username = models.CharField(
        max_length=150,     # Set a reasonable maximum length
        
        blank=False,        # The field must be filled out
        null=False,         # Cannot be NULL in the databas
    )
    
    
    price = models.DecimalField(
        default=Decimal('0.00'),
        max_digits=12,           
        decimal_places=2         
    )
    
    symbol = models.CharField(
        max_length=15,     # Set a reasonable maximum length
         default='NON',
        blank=False,        # The field must be filled out
        null=False,         # Cannot be NULL in the databas
    )
    
    qty = models.IntegerField(
         default=0
    )
    
    
   