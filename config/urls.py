from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="El Royale API",
        default_version='v1',
        description="Gerenciamento de cadastro de hotéis",
        terms_of_service="https://opensource.org/licenses/MIT",
        contact=openapi.Contact(email="robsonsilv410@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('users.urls')),
    path('api/v1/', include('hotels.urls')),
    path('api/v1/docs/', schema_view.with_ui('swagger',
                                             cache_timeout=0), name='swagger'),
]
