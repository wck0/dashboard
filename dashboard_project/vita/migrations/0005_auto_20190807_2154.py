# Generated by Django 2.1.1 on 2019-08-08 04:54

from django.db import migrations
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
        ('vita', '0004_auto_20190806_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='zip_code',
            field=localflavor.us.models.USZipCodeField(blank=True, max_length=10, null=True),
        ),
    ]
