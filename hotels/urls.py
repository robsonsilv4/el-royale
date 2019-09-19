from django.urls import include, path
from rest_framework_nested import routers

from rooms.views import RoomViewSet

from .views import HotelViewSet

# Recursos de hotéis
hotel_router = routers.SimpleRouter()
hotel_router.register('hotels', HotelViewSet, 'hotels')

# Recursos aninhados de hotéis/quartos
room_router = routers.NestedSimpleRouter(
    hotel_router, 'hotels', lookup='hotel')
room_router.register('rooms', RoomViewSet, base_name='hotels')

app_name = 'hotels'
urlpatterns = (
    path('', include(hotel_router.urls)),
    path('', include(room_router.urls)),
)
