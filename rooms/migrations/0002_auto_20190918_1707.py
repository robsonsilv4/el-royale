# Generated by Django 2.2.5 on 2019-09-18 20:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='number',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1, message='Permitido apenas números positivos.')], verbose_name='Número'),
        ),
    ]