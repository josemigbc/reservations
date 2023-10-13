from rest_framework import serializers, exceptions
from .models import Reservation,Passenger,Seat


class PassengerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Passenger
        fields = "__all__"
        
class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = "__all__"
        depth = 1
        
class ReservationSerializer(serializers.ModelSerializer):
    
    passenger_id = serializers.IntegerField(write_only=True)
    seat_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Reservation
        fields = "__all__"
        read_only_fields = ("payment_status","charge_id","datetime","passenger_id","seat_id")
        depth = 2
            
    def is_valid(self, *, raise_exception=False):
        error = {}
        try:
            seat_id = self.initial_data["seat_id"]
            seat = Seat.objects.get(id=seat_id)
            if seat.taken:
                error = {'error':{'seat': ['The seat must not be taken.']}}
        except KeyError:
            error = {'error':{'seat': ['The seat is a required field.']}}
        except:
            error = {'error':{'seat': ['The seat given does not exist']}}
        
        if error:
            if raise_exception:
                raise exceptions.ValidationError(error)
            return False
        
        return super().is_valid(raise_exception=raise_exception)
        