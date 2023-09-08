from django.contrib import admin
from .models import Reservation,Seat,Passenger

# Register your models here.
admin.site.register(Reservation)
admin.site.register(Seat)
admin.site.register(Passenger)