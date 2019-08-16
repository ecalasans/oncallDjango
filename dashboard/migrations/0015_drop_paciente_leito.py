# Generated by Django 2.2.1 on 2019-08-01 21:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0014_create_hospitais_on_medico'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medico',
            name='hospital',
        ),
        migrations.AlterField(
            model_name='ocorrencia',
            name='data_add',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 1, 21, 41, 38, 397430, tzinfo=utc), editable=False),
        ),
        migrations.AlterField(
            model_name='ocorrencia',
            name='data_modif',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 1, 21, 41, 38, 397474, tzinfo=utc)),
        ),
        migrations.DeleteModel(
            name='Paciente_Leito',
        ),
    ]