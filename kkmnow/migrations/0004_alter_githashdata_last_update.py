# Generated by Django 4.0.6 on 2022-10-01 18:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('kkmnow', '0003_alter_githashdata_last_update'),
    ]

    operations = [
        migrations.AlterField(
            model_name='githashdata',
            name='last_update',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]