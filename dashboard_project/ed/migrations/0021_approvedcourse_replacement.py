# Generated by Django 2.1.1 on 2020-04-01 23:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ed', '0020_remove_approvedcourse_replacement'),
    ]

    operations = [
        migrations.AddField(
            model_name='approvedcourse',
            name='replacement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ed.EDCourse'),
        ),
    ]