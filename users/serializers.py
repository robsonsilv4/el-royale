from django.contrib.auth import get_user_model
from rest_framework.serializers import CharField, ModelSerializer

from .models import User


class UserSerializer(ModelSerializer):
    password = CharField(min_length=8, max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ('name', 'email', 'password')

    # Para encriptar a senha
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
