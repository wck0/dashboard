# Generated by Django 2.1.1 on 2020-04-28 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ed', '0021_approvedcourse_replacement'),
    ]

    operations = [
        migrations.AddField(
            model_name='approvedcourse',
            name='edcourseID',
            field=models.IntegerField(default=-1),
        ),
    ]
