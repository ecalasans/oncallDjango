# Generated by Django 2.2.1 on 2019-05-29 17:36

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(default='', max_length=250)),
                ('sigla', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='leito',
            name='numero',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ocorrencia',
            name='data_add',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 29, 17, 36, 37, 379727, tzinfo=utc), editable=False),
        ),
        migrations.AlterField(
            model_name='ocorrencia',
            name='data_modif',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 29, 17, 36, 37, 379750, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='leito',
            name='hospital',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.DO_NOTHING, to='dashboard.Hospital'),
        ),
    ]
