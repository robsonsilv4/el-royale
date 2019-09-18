from rest_framework.serializers import ModelSerializer

from rooms.serializers import RoomSerializer

from .models import Hotel


class HotelSerializer(ModelSerializer):
    rooms = RoomSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = ('name',  'address', 'city', 'state', 'phone', 'rooms',)
