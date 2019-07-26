# Generated by Django 2.2.1 on 2019-07-11 01:13

import datetime
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0008_change_user_id_medicos'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='medico',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterModelManagers(
            name='medico',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='medico',
            name='id',
        ),
        migrations.RemoveField(
            model_name='medico',
            name='user_id',
        ),
        migrations.AddField(
            model_name='medico',
            name='user_ptr',
            field=models.OneToOneField(auto_created=True, default=0, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='medico',
            name='crm',
            field=models.CharField(default='0000', max_length=6),
        ),
        migrations.AlterField(
            model_name='ocorrencia',
            name='data_add',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 11, 1, 13, 25, 863373, tzinfo=utc), editable=False),
        ),
        migrations.AlterField(
            model_name='ocorrencia',
            name='data_modif',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 11, 1, 13, 25, 863412, tzinfo=utc)),
        ),
    ]
