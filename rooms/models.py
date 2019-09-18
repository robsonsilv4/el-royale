from django.db import models

from hotels.models import Hotel


class Room(models.Model):
    number = models.IntegerField('Número')
    floor = models.IntegerField('Piso')
    hotel = models.ForeignKey(
        Hotel, related_name='rooms', on_delete=models.CASCADE)

    class Meta:
        ordering = ['floor', ]
        verbose_name = 'Quarto'
        verbose_name_plural = 'Quartos'

    def __str__(self):
        return f'{str(self.number)} - {self.hotel.name}'
