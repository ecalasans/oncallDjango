# Generated by Django 2.2.1 on 2019-07-14 21:21

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_remove_setor_from_paciente'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paciente_leito',
            name='id',
        ),
        migrations.RemoveField(
            model_name='paciente_leito',
            name='pac',
        ),
        migrations.AddField(
            model_name='paciente_leito',
            name='paciente_ptr',
            field=models.OneToOneField(auto_created=True, default=1, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.Paciente'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ocorrencia',
            name='data_add',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 14, 21, 20, 29, 423741, tzinfo=utc), editable=False),
        ),
        migrations.AlterField(
            model_name='ocorrencia',
            name='data_modif',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 14, 21, 20, 29, 423787, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='paciente_leito',
            name='leito',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.DO_NOTHING, to='dashboard.Leito'),
        ),
    ]