# Generated by Django 4.0 on 2023-12-13 23:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_rename_notes_customuser_selectedtopic_project_week_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='SelectedTopic',
            new_name='Topic',
        ),
    ]