from uuid import uuid4

from django.db import models


class Hotel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField('Nome', max_length=100)
    address = models.CharField('Endereço', max_length=255)
    city = models.CharField('Cidade', max_length=100)
    state = models.CharField('Estado', max_length=100)
    phone = models.CharField('Telefone', max_length=15)

    class Meta:
        ordering = ['name', ]
        verbose_name = 'Hotel'
        verbose_name_plural = 'Hotéis'
        unique_together = ['name', 'city', ]

    def __str__(self):
        return self.name
