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
        read_only_fields = ("payment_status","charge_id","datetime")
        
    def is_valid(self, *, raise_exception=False):
        valid = super().is_valid(raise_exception=raise_exception)
        
        seat = self.validated_data.get('seat')
        if seat.taken:
            valid = False
            self.errors['seat'] = ['The seat must not be taken.']
        
        return valid