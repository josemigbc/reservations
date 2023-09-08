from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.routers import SimpleRouter
from .models import Passenger, Seat, Reservation
from .serializers import PassengerSerializer, SeatSerializer, ReservationSerializer

# Create your views here
class PassengerViewset(ModelViewSet):
    serializer_class = PassengerSerializer
    queryset = Passenger.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.action != "list":
            return super().get_queryset()
        return self.queryset.filter(user=self.request.user)
    
class SeatListView(ListAPIView):
    serializer_class = SeatSerializer
    queryset = Seat.objects.all()
    
    def get_queryset(self):
        trip_id = self.kwargs['pk']
        return self.queryset.filter(trip=trip_id)
    
class ReservationViewset(ModelViewSet):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.action != "list":
            return super().get_queryset()
        return self.queryset.filter(passenger__user=self.request.user)
    
passenger_router = SimpleRouter()
passenger_router.register(r"passenger",PassengerViewset)

reservation_router = SimpleRouter()
reservation_router.register(r"reservation",ReservationViewset)
