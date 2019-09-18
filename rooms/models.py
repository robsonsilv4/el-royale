from uuid import uuid4

from django.core.validators import MinValueValidator
from django.db import models

from hotels.models import Hotel


class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    number = models.IntegerField(
        'Número', validators=[MinValueValidator(1, message='Permitido apenas números positivos.')])
    description = models.CharField('Descrição', max_length=100, null=True)
    hotel = models.ForeignKey(
        Hotel, related_name='rooms', on_delete=models.CASCADE)

    class Meta:
        ordering = ['number', ]
        verbose_name = 'Quarto'
        verbose_name_plural = 'Quartos'
        unique_together = ['number', 'hotel', ]

    def __str__(self):
        return f'{str(self.number)} - {self.hotel.name}'
