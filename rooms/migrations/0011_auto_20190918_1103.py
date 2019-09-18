# Generated by Django 2.2.5 on 2019-09-18 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0004_auto_20190918_0933'),
        ('rooms', '0010_auto_20190918_1102'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['number'], 'verbose_name': 'Quarto', 'verbose_name_plural': 'Quartos'},
        ),
        migrations.AlterUniqueTogether(
            name='room',
            unique_together={('number', 'hotel')},
        ),
        migrations.RemoveField(
            model_name='room',
            name='floor',
        ),
    ]