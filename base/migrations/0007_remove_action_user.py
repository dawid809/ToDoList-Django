# Generated by Django 4.0.2 on 2022-03-06 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_action_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='action',
            name='user',
        ),
    ]