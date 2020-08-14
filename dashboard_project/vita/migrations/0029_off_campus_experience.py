# Generated by Django 2.2.13 on 2020-07-21 00:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vita', '0028_auto_20200626_1108'),
    ]

    operations = [
        migrations.CreateModel(
            name='Off_Campus_Experience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experince_type', models.CharField(choices=[('INT', 'Internship'), ('CBL', 'Community-Based Learning'), ('STA', 'Study Abroad'), ('REU', 'Research Esperience for Undergraduates')], max_length=20)),
                ('aproved', models.BooleanField(default=False)),
                ('completed', models.BooleanField(default=False)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]