from django.shortcuts import render
# You need to import the DoesNotExist exception to catch when the object is not found
from .models import userstocks 
from django.core.exceptions import ObjectDoesNotExist
# Import for atomic operations (highly recommended for financial data)
from django.db import transaction

class A:
    """
    A utility class to handle stock addition logic.
    Assumes userstocks model has fields: username (str), symbol (str), price (Decimal), qty (int)
    """
    
    # We assume 'usera' is the username string.
    def addstock(usera: str, sym: str, pric: float, qty: int):
        
                stock = userstocks(username=usera, symbol=sym, price=pric, qty=qty)
                stock.save()
    def sellstock(usera: str, sym: str, pric: float, qty: int):
        
                stock = userstocks(username=usera, symbol=sym, price=pric, qty=qty*(-1))
                stock.save()
    
