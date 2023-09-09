from rest_framework.test import APITestCase,APIRequestFactory
from unittest.mock import MagicMock,patch
from payments.views import proccess_payment,PaymentView
from django.contrib.auth import get_user_model
from reservations.models import Passenger,Reservation,Seat
from trips.models import Bus,Trip
import datetime
import stripe
import freezegun

User = get_user_model()

# Create your tests here.
class PaymentsTest(APITestCase):
    
    @classmethod
    def setUpTestData(cls) -> None:
        user = User.objects.create_user(username="test",password="testing1234")
        cls.passenger = Passenger.objects.create(user=user,full_name="Test",dni="00000000000")
        cls.user = user
        cls.bus = Bus.objects.create(registration_number="B100000")
        cls.view = PaymentView()
        cls.factory = APIRequestFactory()
    
    def setUp(self) -> None:
        Trip.objects.create(
            origin="A", destination="B",datetime=datetime.datetime.now() + datetime.timedelta(days=3),
            price=100,bus=self.bus
        )
        self.reservation = Reservation.objects.create(passenger=self.passenger,seat=Seat.objects.get(id=1))
    
    @patch('stripe.Charge.create')
    def test_process_payment(self,mock:MagicMock):
        mock.return_value = "Charge"
        charge = proccess_payment("token",100)
        mock.assert_called_once()
        self.assertEqual(charge,"Charge")
    
    @patch('stripe.Charge.create')
    def test_view_with_ok(self,mock:MagicMock):
        mock_charge = MagicMock()
        mock_charge.id = "id"
        mock_charge.to_dict.return_value = {"info":"test"}
        mock.return_value = mock_charge
        
        response = self.client.post("/payment/",data={"charge_token":"tok","reservation_id":self.reservation.id})
        reservation = Reservation.objects.get(id=1)
        
        self.assertEqual(response.json(),{"info":"test"})
        self.assertEqual(reservation.charge_id,"id")
        self.assertEqual(reservation.payment_status,"1")
    
    def test_view_with_missing_params(self):
        response = self.client.post("/payment/",data={"charge_token":"tok"})
        self.assertEqual(response.status_code,400)
        
    def test_view_with_reservation_does_not_exist(self):
        response = self.client.post("/payment/",data={"charge_token":"tok","reservation_id":2000})
        print(response.json())
        self.assertEqual(response.status_code,404)
    
    @patch('stripe.Charge.create')
    def test_view_with_bad_token(self,mock:MagicMock):
        mock.side_effect = stripe.error.CardError(message="Error",code="card_decline",param="number")
        response = self.client.post("/payment/",data={"charge_token":"tok","reservation_id":self.reservation.id})
        mock.assert_called_once()
        self.assertEqual(response.status_code,401)
    
    def test_reservation_timeout(self):
        reservation = Reservation.objects.create(passenger=self.passenger,seat=Seat.objects.get(id=2))
        freeze = reservation.datetime + datetime.timedelta(minutes=11)
        with freezegun.freeze_time(freeze):
            response = self.client.post("/payment/",data={"charge_token":"tok","reservation_id":reservation.id})
            self.assertEqual(response.status_code,404)
        
        with self.assertRaises(Exception):
            Reservation.objects.get(id=reservation.id)