# Generated by Django 2.2.13 on 2020-07-31 09:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vita', '0038_auto_20200731_0216'),
    ]

    operations = [
        migrations.RenameField(
            model_name='offcampusexperience',
            old_name='aproved',
            new_name='approved',
        ),
    ]
