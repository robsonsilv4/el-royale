from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Hotel
from .serializers import HotelSerializer


class HotelViewSet(ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    filterset_fields = ('name', 'address', 'city', 'state',)

    def get_permissions(self):
        permission_classes = []

        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny, ]
        elif self.action == 'destroy':
            permission_classes = [IsAdminUser, ]
        else:
            permission_classes = [IsAuthenticated, ]

        return [permission() for permission in permission_classes]

    @method_decorator(cache_page(60))
    def dispatch(self, *args, **kwargs):
        return super(HotelViewSet, self).dispatch(*args, **kwargs)
