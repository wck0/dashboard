# Generated by Django 2.2.13 on 2020-10-09 08:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vita', '0046_student_shared_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='shared_url',
        ),
    ]
