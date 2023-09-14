from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, exceptions, status
from rest_framework.generics import ListAPIView
from rest_framework.routers import SimpleRouter
from rest_framework.response import Response
from django.utils import timezone
from .models import Passenger, Seat, Reservation
from .serializers import PassengerSerializer, SeatSerializer, ReservationSerializer
import datetime


class PassengerViewset(ModelViewSet):
    serializer_class = PassengerSerializer
    queryset = Passenger.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class SeatListView(ListAPIView):
    serializer_class = SeatSerializer
    queryset = Seat.objects.filter(taken=False)

    def get_queryset(self):
        trip_id = self.kwargs['pk']
        return self.queryset.filter(trip=trip_id)


class ReservationViewset(ModelViewSet):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        to_delete = self.queryset.filter(payment_status="0",
                                         datetime__lt=timezone.now()-datetime.timedelta(minutes=10)
                                         )
        to_delete.delete()
        return self.queryset.filter(passenger__user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            passenger = Passenger.objects.get(
                id=self.request.data['passenger'])
        except KeyError:
            raise exceptions.ValidationError(
                detail={'error': 'That passenger field is a required field.'})
        except Exception as exc:
            raise exceptions.NotFound(detail={"passenger": str(exc)})
        if passenger.user != self.request.user:
            raise exceptions.AuthenticationFailed(
                detail={"error": "Passenger does not belong to user"})
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def destroy(self, request, *args, **kwargs):
        reservation = self.get_object()
        if reservation.payment_status == "1":
            raise exceptions.ValidationError(detail={"payment_status":["This reservation is payed and it can not be deleted."]})
        return super().destroy(request, *args, **kwargs)


passenger_router = SimpleRouter()
passenger_router.register(r"passenger", PassengerViewset)

reservation_router = SimpleRouter()
reservation_router.register(r"reservation", ReservationViewset)
