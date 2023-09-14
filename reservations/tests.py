from rest_framework.test import APITestCase,APIRequestFactory
from rest_framework import exceptions
from django.contrib.auth import get_user_model
from django.utils import timezone
from reservations.views import PassengerViewset,ReservationViewset,SeatListView
from reservations.models import Passenger,Reservation,Seat
from reservations.serializers import ReservationSerializer
from trips.models import Trip,Bus
import datetime

User = get_user_model()

# Create your tests here.
class PassengerViewsetTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="test",password="testing1234")
        user2 = User.objects.create_user(username="test2",password="testing1234")
        cls.user = user
        cls.passenger = Passenger.objects.create(user=user,full_name="Test",dni="00000000000")
        cls.passenger = Passenger.objects.create(user=user2,full_name="Test",dni="00000000111")
        cls.viewset = PassengerViewset()
        cls.factory = APIRequestFactory()
        
    def test_get_queryset_in_list(self):
        request = self.factory.get("/passenger/")
        request.user =  self.user
        self.viewset.request = request
        queryset = self.viewset.get_queryset()
        expected_queryset = Passenger.objects.filter(id=1)
        
        self.assertEqual(list(queryset),list(expected_queryset))
        
class SeatViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.view = SeatListView()
        bus = Bus.objects.create(registration_number="B100000")
        Trip.objects.create(
            origin="A", destination="B",datetime=timezone.now() + datetime.timedelta(days=3),
            price=100,bus=bus
        )
    
    def test_get_queryset(self):
        seat = Seat.objects.get(id=1)
        seat.taken = True
        seat.save()
        self.view.kwargs = {"pk": 1}
        count = self.view.get_queryset().count()
        
        self.assertEqual(count,35)
        
        
class ReservationViewsetTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="test",password="testing1234")
        user2 = User.objects.create_user(username="test2",password="testing1234")
        passenger = Passenger.objects.create(user=user,full_name="Test",dni="00000000000")
        passenger2 = Passenger.objects.create(user=user2,full_name="Test",dni="00000000111")
        cls.user = user
        bus = Bus.objects.create(registration_number="B100000")
        Trip.objects.create(
            origin="A", destination="B",datetime=timezone.now() + datetime.timedelta(days=3),
            price=100,bus=bus
        )
        cls.reservation = Reservation.objects.create(passenger=passenger,seat=Seat.objects.get(id=1))
        Reservation.objects.create(passenger=passenger2,seat=Seat.objects.get(id=2))
        cls.viewset = ReservationViewset()
        cls.factory = APIRequestFactory()
        
    def test_get_queryset_in_list(self):
        request = self.factory.get("/reservation/")
        request.user =  self.user
        self.viewset.request = request
        queryset = self.viewset.get_queryset()
        expected_queryset = Reservation.objects.filter(id=1)
        
        self.assertEqual(list(queryset),list(expected_queryset))
    
    def test_create_ok(self):
        data = {"seat": 3, "passenger": 1}
        self.client.login(username="test",password="testing1234")
        response = self.client.post("/reservation/",data=data)
        self.assertEqual(response.status_code,201)
    
    def test_create_with_no_passenger(self):
        data = {"seat": 3}
        self.client.login(username="test",password="testing1234")
        response = self.client.post("/reservation/",data=data)
        self.assertEqual(response.status_code,400)
    
    def test_create_with_passenger_does_not_exist(self):
        data = {"seat": 3,"passenger": 10}
        self.client.login(username="test",password="testing1234")
        response = self.client.post("/reservation/",data=data)
        self.assertEqual(response.status_code,404)
    
    def test_create_with_passenger_does_not_belong_user(self):
        data = {"seat": 3,"passenger": 2}
        self.client.login(username="test",password="testing1234")
        response = self.client.post("/reservation/",data=data)
        self.assertEqual(response.status_code,403)
    
    def test_update(self):
        request = self.factory.patch(f"/reservation/{self.reservation.pk}/")
        request.user = self.user
        response = self.viewset.update(request)
        
        self.assertEqual(response.status_code,405)
    
    def test_destroy_with_payment_status_1(self):
        self.reservation.payment_status = "1"
        self.reservation.save()
        self.client.login(username="test",password="testing1234")
        response = self.client.delete(f"/reservation/{self.reservation.pk}/")
        self.assertEqual(response.status_code,400)

    def test_destroy_with_payment_status_0(self):
        self.client.login(username="test",password="testing1234")
        response = self.client.delete(f"/reservation/{self.reservation.pk}/")
        self.assertEqual(response.status_code,204)
        
class SignalsTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        user = User.objects.create_user(username="test",password="testing1234")
        passenger = Passenger.objects.create(user=user,full_name="Test",dni="00000000000")
        cls.user = user
        bus = Bus.objects.create(registration_number="B100000")
        Trip.objects.create(
            origin="A", destination="B",datetime=timezone.now() + datetime.timedelta(days=3),
            price=100,bus=bus
        )
        cls.reservation = Reservation.objects.create(passenger=passenger,seat=Seat.objects.get(id=1))
    
    def test_created(self):
        seat=Seat.objects.get(id=1)
        self.assertTrue(seat.taken)
        
    def test_modify(self):
        seat = Seat.objects.get(id=1)
        seat.taken = False
        seat.save()
        self.reservation.charge_id = "id"
        self.reservation.save()
        seat = Seat.objects.get(id=1)
        self.assertFalse(seat.taken)
        
    def test_delete(self):
        self.reservation.delete()
        self.assertFalse(self.reservation.seat.taken)
        
class ReservationSerializerTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        bus = Bus.objects.create(registration_number="B100000")
        Trip.objects.create(
            origin="A", destination="B",datetime=timezone.now() + datetime.timedelta(days=3),
            price=100,bus=bus
        )
        seat = Seat.objects.get(id=1)
        cls.seat = seat
        user = User.objects.create_user(username="test",password="testing1234")
        passenger = Passenger.objects.create(user=user,full_name="Test",dni="00000000000")
        
    
    def test_with_ok(self):
        serializer = ReservationSerializer(data={"seat": 1, "passenger": 1})
        valid =  serializer.is_valid()
        self.assertTrue(valid)
    
    def test_with_seat_taken(self):
        self.seat.taken = True
        self.seat.save()
        serializer = ReservationSerializer(data={"seat": 1, "passenger": 1})
        valid =  serializer.is_valid()
        self.assertFalse(valid)
        with self.assertRaises(exceptions.ValidationError):
            serializer.is_valid(raise_exception=True)
    
    def test_is_valid_with_seat_does_not_exist(self):
        serializer = ReservationSerializer(data={"seat": 100, "passenger": 1})
        valid =  serializer.is_valid()
        self.assertFalse(valid)
        
    def test_is_valid_with_no_seat(self):
        serializer = ReservationSerializer(data={"passenger": 1})
        valid = serializer.is_valid()
        self.assertFalse(valid)