# Generated by Django 3.0.5 on 2020-04-29 00:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0017_altera_model_Medico_hospital'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medico',
            name='crm',
            field=models.CharField(max_length=6),
        ),
        migrations.AlterField(
            model_name='ocorrencia',
            name='data_add',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 29, 0, 59, 5, 7291, tzinfo=utc), editable=False),
        ),
        migrations.AlterField(
            model_name='ocorrencia',
            name='data_modif',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 29, 0, 59, 5, 7329, tzinfo=utc)),
        ),
    ]