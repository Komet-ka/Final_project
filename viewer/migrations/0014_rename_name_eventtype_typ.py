# Generated by Django 4.1.1 on 2024-10-01 06:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0013_rename_place_event_misto_rename_name_event_nazev'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventtype',
            old_name='name',
            new_name='typ',
        ),
    ]
