# Generated by Django 2.1.1 on 2019-10-02 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vita', '0013_menu_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu_item',
            name='link',
            field=models.CharField(default='/', max_length=60),
            preserve_default=False,
        ),
    ]
