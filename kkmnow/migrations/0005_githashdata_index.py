# Generated by Django 4.0.6 on 2022-10-01 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kkmnow', '0004_alter_githashdata_last_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='githashdata',
            name='index',
            field=models.CharField(default='HASH_DATA', max_length=200),
        ),
    ]
