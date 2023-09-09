from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from reservations.models import Reservation
from django.conf import settings
from django.utils import timezone
import stripe
from .exceptions import ReservationTimeOut

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



class PaymentView(APIView):
    
    def post(self,request):
        try:
            charge_token = request.data['charge_token']
            reservation_id = request.data['reservation_id']
            reservation = Reservation.objects.get(id=reservation_id)
            spent = timezone.now() - reservation.datetime
            
            if spent.seconds > 600:
                reservation.delete()
                raise ReservationTimeOut
            
            charge = proccess_payment(charge_token,reservation.seat.trip.price)
        
        except KeyError:
            return Response(
                data={"message": "The charge token and reservation id must be given."},
                status=status.HTTP_400_BAD_REQUEST
            )

        except stripe.error.CardError as e:
            return Response(data={"message":str(e)},status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as e:
            return Response(data={"message": str(e)},status=status.HTTP_404_NOT_FOUND)
        
        reservation.payment_status = "1"
        reservation.charge_id = charge.id
        reservation.save()
        
        return Response(data=charge.to_dict())