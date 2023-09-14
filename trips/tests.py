from rest_framework.test import APITestCase,APIRequestFactory
from trips.models import Trip,Bus
from reservations.models import Seat
from trips.views import TripWithSeatNoTaken
from trips.serializers import TripSerializer
from trips.exceptions import MissingParameters,BadDate
from django.utils import timezone
import datetime

# Create your tests here.


class TripViewTest(APITestCase):
    
    @classmethod
    def setUpTestData(cls) -> None:
        bus = Bus.objects.create(registration_number="B100000")
        Trip.objects.create(
            origin="A", destination="B",datetime=timezone.now() + datetime.timedelta(days=3),
            price=100,bus=bus
        )
        
        Trip.objects.create(
            origin="A", destination="B",datetime=timezone.now() - datetime.timedelta(days=1),
            price=100,bus=bus
        )
        
        Trip.objects.create(
            origin="A", destination="B",datetime=timezone.now() + datetime.timedelta(days=1),
            price=100,bus=bus
        )
        
        cls.view = TripWithSeatNoTaken()
        cls.factory = APIRequestFactory()

    def test_get_queryset_ok(self):
        data = {
            "origin": "A",
            "destination": "B",
            "date": (timezone.now().date()+datetime.timedelta(days=3)).isoformat(),
        }
        request = self.factory.get("/trip/",data=data)
        self.view.request = request
        queryset = self.view.get_queryset()
        expected_queryset = Trip.objects.filter(id=1)
        
        self.assertEqual(list(queryset),list(expected_queryset))
        
    def test_get_queryset_with_missing_params(self):
        data = {
            "origin": "A",
            "destination": "B",
        }
        request = self.factory.get("/trip/",data=data)
        self.view.request = request
        
        with self.assertRaises(MissingParameters):
            self.view.get_queryset()
            
    def test_get_queryset_with_date_before_now(self):
        data = {
            "origin": "A",
            "destination": "B",
            "date": (timezone.now().date()-datetime.timedelta(days=1)).isoformat(),
        }
        request = self.factory.get("/trip/",data=data)
        self.view.request = request
        
        with self.assertRaises(BadDate):
            self.view.get_queryset()
    
    def test_get_queryset_with_no_exact_day(self):
        data = {
            "origin": "A",
            "destination": "B",
            "date": (timezone.now().date()+datetime.timedelta(days=2)).isoformat(),
        }
        request = self.factory.get("/trip/",data=data)
        self.view.request = request
        queryset = self.view.get_queryset()
        expected_queryset = Trip.objects.filter(id__in=[1,3])
        
        self.assertEqual(list(queryset),list(expected_queryset))
    
    def test_list_with_trips(self):
        data = {
            "origin": "A",
            "destination": "B",
            "date": (timezone.now().date()+datetime.timedelta(days=2)).isoformat(),
        }
        request = self.factory.get("/trip/",data=data)
        self.view.request = request
        serializer = TripSerializer(self.view.get_queryset(),many=True)
        response = self.client.get("/trip/",data=data)
        self.assertEqual(response.data,serializer.data)
    
    def test_list_trips_with_no_trips(self):
        data = {
            "origin": "A",
            "destination": "B",
            "date": timezone.now().date().isoformat(),
        }
        Trip.objects.all().delete()
        response = self.client.get("/trip/",data=data)
        serializer = TripSerializer(Trip.objects.all(),many=True)
        self.assertEqual(len(serializer.data),1)
        self.assertEqual(response.data,serializer.data)
        
class SignalsTest(APITestCase):
    def test_create(self):
        bus = Bus.objects.create(registration_number="B100000")
        Trip.objects.create(
            origin="A", destination="B",datetime=timezone.now() + datetime.timedelta(days=3),
            price=100,bus=bus
        )
        seats_number = Seat.objects.all().count()
        self.assertEqual(seats_number,36)