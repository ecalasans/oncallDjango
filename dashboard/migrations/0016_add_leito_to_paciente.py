# Generated by Django 2.2.1 on 2019-08-01 21:45

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0015_drop_paciente_leito'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='leito',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='dashboard.Leito'),
        ),
        migrations.AlterField(
            model_name='ocorrencia',
            name='data_add',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 1, 21, 45, 11, 508442, tzinfo=utc), editable=False),
        ),
        migrations.AlterField(
            model_name='ocorrencia',
            name='data_modif',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 1, 21, 45, 11, 508493, tzinfo=utc)),
        ),
    ]