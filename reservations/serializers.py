from rest_framework import serializers
from .models import Reservation,Passenger,Seat

class PassengerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Passenger
        fields = "__all__"
        
class SeatSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Seat
        fields = "__all__"
        
class ReservationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Reservation
        fields = "__all__"
        read_only_fields = ("payment_status","datetime")