# Generated by Django 4.0.6 on 2022-10-01 18:16

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('kkmnow', '0002_githashdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='githashdata',
            name='last_update',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 1, 18, 16, 22, 778839, tzinfo=utc)),
        ),
    ]
