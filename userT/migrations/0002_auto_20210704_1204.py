# Generated by Django 3.1.5 on 2021-07-04 04:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userT', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='user_permissions',
        ),
    ]
