# Generated by Django 2.1.1 on 2020-05-07 02:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vita', '0024_student_prmeeting_complete'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='EDmeeting_complete',
            new_name='ED_meeting_complete',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='PRmeeting_complete',
            new_name='PR_meeting_complete',
        ),
    ]
