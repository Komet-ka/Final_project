# Generated by Django 4.1 on 2024-10-08 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0004_event_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventtype',
            options={'permissions': [('custom_add_eventtype', 'Can add event type')]},
        ),
    ]
