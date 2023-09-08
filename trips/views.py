from rest_framework.generics import ListAPIView
from django.utils import timezone
from .serializers import TripSerializer
from .models import Trip

# Create your views here.
class TripWithSeatNoTaken(ListAPIView):
    serializer_class = TripSerializer
    queryset = Trip.objects.all()
    
    def get_queryset(self):
        date = self.request.GET["date"]
        origin = self.request.GET["origin"]
        destination = self.request.GET["destination"]
        now = timezone.now()
        
        queryset = self.queryset.filter(
            seat__taken=False, origin=origin, destination=destination, 
            datetime__date=date).distinct()
        
        if queryset:
            return queryset
        
        queryset = self.queryset.filter(
            seat__taken=False, origin=origin, destination=destination,
            datetime__gt=now).distinct()
        
        return queryset