from django.urls import path
from rest_framework import routers

from .views import RoomViewSet

router = routers.DefaultRouter()
router.register('rooms', RoomViewSet, 'rooms')

app_name = 'rooms'
urlpatterns = router.urls
