from django.db import models
import requests
# Create your models here.
#from UserProfile.models import userprofile
from django.contrib.auth.decorators import login_required
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class userprofile(models.Model):
    # This creates a one-to-one link to the built-in User model
    username = models.CharField(
        max_length=150,     # Set a reasonable maximum length
        unique=True,        # Ensure no two profiles have the same custom username
        blank=False,        # The field must be filled out
        null=False,         # Cannot be NULL in the databas
    )
    
    # The Cash Balance Field
    # max_digits is the total number of digits (including decimal places)
    # decimal_places is the number of digits to store after the decimal point
    cash_balance = models.DecimalField(
        default=Decimal('0.00'), # Always start at 0.00
        max_digits=12,           # Allows values up to 9,999,999,999.99
        decimal_places=2         # Stores two decimal places for currency
    )

    @login_required
    def deposit(a, amount):
        
        """Method to safely add funds to the balance."""
        new = amount + userprofile.objects.get(a).cash_balance 
        print(new)
    def withdraw(self, amount):
    
        self.cash_balance -= Decimal(amount)
        self.save()
        return True
        
    def __str__(self):
        return self.username