from django.db import models


class Hotel(models.Model):
    name = models.CharField('Nome', max_length=100)
    address = models.CharField('Endereço', max_length=255)
    city = models.CharField('Cidade', max_length=100)
    state = models.CharField('Estado', max_length=100)
    phone = models.CharField('Telefone', max_length=15)

    class Meta:
        unique_together = ['name', 'city', ]
        ordering = ['name', ]
        verbose_name = 'Hotel'
        verbose_name_plural = 'Hotéis'

    def __str__(self):
        return self.name
