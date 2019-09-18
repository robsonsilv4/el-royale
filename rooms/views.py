from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Room
from .serializers import RoomSerializer


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_permissions(self):
        permission_classes = []

        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny, ]
        elif self.action == 'destroy':
            permission_classes = [IsAdminUser, ]
        else:
            permission_classes = [IsAuthenticated, ]

        return [permission() for permission in permission_classes]
