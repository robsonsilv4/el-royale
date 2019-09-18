from django.urls import path
from rest_framework import routers

from .views import HotelViewSet

router = routers.DefaultRouter()
router.register('hotels', HotelViewSet, 'hotels')

app_name = 'hotels'
urlpatterns = router.urls
