from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from trips.models import Trip

User = get_user_model()

# Create your models here.
class Passenger(models.Model):

    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    full_name = models.CharField(_("Full Name"), max_length=150)
    dni = models.CharField(_("DNI"), max_length=11)

    class Meta:
        verbose_name = _("Passenger")
        verbose_name_plural = _("Passengers")

    def __str__(self):
        return self.full_name

class Seat(models.Model):

    trip = models.ForeignKey(Trip, verbose_name=_("Trip"), on_delete=models.CASCADE)
    number = models.IntegerField(_("NUmber"))
    taken = models.BooleanField(_("Taken"))

    class Meta:
        verbose_name = _("Seat")
        verbose_name_plural = _("Seats")

    def __str__(self):
        return f"{str(self.trip)} A{self.number}"
    
class Reservation(models.Model):

    passenger = models.ForeignKey(Passenger, verbose_name=_("Passenger"), on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, verbose_name=_(""), on_delete=models.CASCADE)
    charge_token = models.CharField(_("Payment ID"), max_length=100,null=True,blank=True)
    payment_status = models.CharField(_("Payment Status"), max_length=50)
    datetime = models.DateTimeField(_("Datetime"), auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _("Reservation")
        verbose_name_plural = _("Reservations")

    def __str__(self):
        return str(self.seat)