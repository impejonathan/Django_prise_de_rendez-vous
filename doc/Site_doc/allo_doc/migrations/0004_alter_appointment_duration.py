# Generated by Django 4.1 on 2023-02-08 18:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allo_doc', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='duration',
            field=models.DurationField(default=datetime.timedelta(seconds=3000)),
        ),
    ]
