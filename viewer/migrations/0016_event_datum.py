# Generated by Django 4.1.1 on 2024-10-01 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0015_event_vstupne'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='datum',
            field=models.DateField(auto_now=True),
        ),
    ]
