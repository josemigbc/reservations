from .models import Trip
from reservations.models import Seat
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save,sender=Trip)
def create_seats(sender,instance,created,**kwargs):
    if created:
        [Seat.objects.create(number=i+1,trip=instance,taken=False) for i in range(instance.bus.capacity)]