# Generated by Django 5.1.2 on 2024-10-27 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emp', '0002_employee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='user',
        ),
    ]
