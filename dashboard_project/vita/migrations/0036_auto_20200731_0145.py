# Generated by Django 2.2.13 on 2020-07-31 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vita', '0035_auto_20200731_0133'),
    ]

    operations = [
        migrations.RenameField(
            model_name='offcampusexperience',
            old_name='director_notes',
            new_name='council_notes',
        ),
    ]
