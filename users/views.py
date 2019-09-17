from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from .permissions import UpdateOwnProfile
from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = []

        if self.action == 'update' or self.action == 'partial_update':
            permission_classes = [UpdateOwnProfile, ]
        elif self.action == 'list' or self.action == 'retrieve' or self.action == 'destroy':
            permission_classes = [IsAdminUser, ]

        return [permission() for permission in permission_classes]
