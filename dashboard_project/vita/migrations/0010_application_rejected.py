# Generated by Django 2.1.1 on 2019-08-09 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vita', '0009_auto_20190808_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='rejected',
            field=models.BooleanField(default=False),
        ),
    ]
