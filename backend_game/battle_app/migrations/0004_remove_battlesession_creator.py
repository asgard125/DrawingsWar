# Generated by Django 4.0.5 on 2022-07-08 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('battle_app', '0003_battlesession_creator_battlesession_started'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='battlesession',
            name='creator',
        ),
    ]
