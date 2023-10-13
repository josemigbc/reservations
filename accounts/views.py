from authentication.views import UserGoogleLoginCallback,UserDetailsUpdateView
from django.conf import settings
from django.shortcuts import redirect
from rest_framework.exceptions import MethodNotAllowed

class GoogleAuthCallback(UserGoogleLoginCallback):
    def get(self, request):
        redirect_uri = settings.GOOGLE_AUTHENTICATION_REDIRECT
        response = super().get(request)
        data_str = '&'.join([f"{key}={value}" for key,value in response.data.items()])
        return redirect(f"{redirect_uri}#{data_str}")

class UserDetailsView(UserDetailsUpdateView):
    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed  