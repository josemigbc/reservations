from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API Rest of Bus Reservations",
        default_version='v0.1',
        description="API Rest of Bus Reservations",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)