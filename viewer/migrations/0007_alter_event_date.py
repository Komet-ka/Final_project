# Generated by Django 4.1.1 on 2024-09-30 23:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0006_alter_event_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
