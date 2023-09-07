from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Bus(models.Model):

    registration_number = models.CharField(_("Registration Number"), max_length=50)

    class Meta:
        verbose_name = _("Bus")
        verbose_name_plural = _("Buses")

    def __str__(self):
        return self.registration_number


class Trip(models.Model):

    origin = models.CharField(_("Origin"), max_length=50)
    destination = models.CharField(_("Destination"), max_length=50)
    bus = models.ForeignKey(Bus, verbose_name=_("Bus"), on_delete=models.CASCADE)
    price = models.IntegerField(_("Price"))
    datetime = models.DateTimeField(_("Datetime"), auto_now=False, auto_now_add=False)
    
    class Meta:
        verbose_name = _("Trip")
        verbose_name_plural = _("Trips")

    def __str__(self):
        return f"{self.origin} - {self.destination} {self.datetime}"