from rest_framework import viewsets
from rest_framework import permissions
from django.conf import settings
import stripe

# Create your views here.
def proccess_payment(charge_token,price):
    """
    Args:
        charge_token (str): Token generated in fronted using information of card.
        price (int): price of product

    Returns:
        Charge: Object Charge returned by creation of charge. 
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY
    charge = stripe.Charge.create(
        amount=price,
        currency="usd",
        description="Purchase of a ticket",
        source=charge_token
    )
    
    return charge

class PassengerViewset(viewsets.ModelViewSet):
    serializer_class = 

