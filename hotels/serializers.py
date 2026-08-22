from rest_framework.serializers import ModelSerializer

from .models import Hotel


class HotelSerializer(ModelSerializer):
    class Meta:
        model = Hotel
        fields = (
            "id",
            "name",
            "address",
            "city",
            "state",
            "phone",
        )
