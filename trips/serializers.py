from rest_framework import serializers
from .models import Trip,Bus

class BusSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Bus
        fields = "__all__"
        
class TripSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Trip
        fields = "__all__"