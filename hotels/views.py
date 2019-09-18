from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Hotel
from .serializers import HotelSerializer


class HotelViewSet(ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    def get_permissions(self):
        permission_classes = []

        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAuthenticated, ]
        elif self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny, ]
        elif self.action == 'destroy':
            permission_classes = [IsAdminUser, ]

        return [permission() for permission in permission_classes]
