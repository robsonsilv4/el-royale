from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Room


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = ("id", "number", "description", "hotel")
        read_only_fields = ("hotel",)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        hotel_id = self.context["view"].kwargs["hotel_pk"]
        number = attrs.get("number")
        if number is not None:
            rooms = Room.objects.filter(hotel_id=hotel_id, number=number)
            if self.instance is not None:
                rooms = rooms.exclude(pk=self.instance.pk)
            if rooms.exists():
                raise serializers.ValidationError(
                    {"number": "Já existe um quarto com este número neste hotel."}
                )
        return attrs
