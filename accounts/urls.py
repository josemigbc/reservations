from authentication.views import UserCreationView, UserGoogleLogin
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from django.urls import path

from accounts.views import GoogleAuthCallback,UserDetailsView

urlpatterns = [
    path("register/", UserCreationView.as_view(), name="user-create"),
    path("user/", UserDetailsView.as_view(), name="user-details"),
    path("token/", TokenObtainPairView.as_view(), name="token-obtain"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path('google/',UserGoogleLogin.as_view(),name="google"),
    path("google/callback/", GoogleAuthCallback.as_view(), name="google-callback"),
]
