# Generated by Django 2.1.1 on 2019-05-31 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ed', '0006_auto_20190405_0010'),
    ]

    operations = [
        migrations.AddField(
            model_name='educationalgoal',
            name='courses',
            field=models.ManyToManyField(to='ed.EDCourse'),
        ),
    ]
