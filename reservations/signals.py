from .models import Seat,Reservation
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver

@receiver(post_save,sender=Reservation)
def set_taken_true(sender,instance,created,**kwargs):
    if created:
        instance.seat.taken = True
        instance.seat.save()
        
@receiver(post_delete,sender=Reservation)
def set_taken_false(sender,instance,**kwargs):
    instance.seat.taken = False
    instance.seat.save()