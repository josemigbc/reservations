"""
URL configuration for bus_reservations project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from trips.views import TripWithSeatNoTaken
from reservations import views as reservation_views
from payments.views import PaymentView
from accounts.views import GoogleAuthCallback
from authentication.views import UserGoogleLogin

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('',include('authentication.urls')),
    path('auth/',include('accounts.urls')),
    path("trip/", TripWithSeatNoTaken.as_view(), name="trip-list"),
    path("seat/<int:pk>/", reservation_views.SeatListView.as_view(), name="seat-list"),
    path("payment/",PaymentView.as_view(),name="payment"),
]

urlpatterns += reservation_views.reservation_router.urls + reservation_views.passenger_router.urls
