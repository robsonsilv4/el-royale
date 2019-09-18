from .models import Hotel
from rest_framework.serializers import ModelSerializer


class HotelSerializer(ModelSerializer):
    class Meta:
        model = Hotel
        fields = ('name', 'address', 'city', 'state', 'phone')
