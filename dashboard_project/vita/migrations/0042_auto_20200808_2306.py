# Generated by Django 2.2.13 on 2020-08-09 06:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vita', '0041_auto_20200804_1508'),
    ]

    operations = [
        migrations.RenameField(
            model_name='offcampusexperience',
            old_name='user',
            new_name='student',
        ),
    ]
