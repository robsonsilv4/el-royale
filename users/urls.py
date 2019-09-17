from django.urls import path
from rest_framework import routers

from .views import UserViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet, 'users')

app_name = 'users'
urlpatterns = router.urls
