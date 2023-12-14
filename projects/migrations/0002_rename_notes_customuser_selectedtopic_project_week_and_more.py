# Generated by Django 4.0 on 2023-12-13 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='notes',
            new_name='SelectedTopic',
        ),
        migrations.AddField(
            model_name='project',
            name='week',
            field=models.IntegerField(choices=[(1, 'Week 1'), (2, 'Week 2'), (3, 'Week 3'), (4, 'Week 4'), (5, 'Week 5'), (6, 'Week 6'), (7, 'Week 7'), (8, 'Week 8'), (9, 'Week 9'), (10, 'Week 10')], null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(max_length=100),
        ),
    ]