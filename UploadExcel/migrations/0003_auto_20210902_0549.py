# Generated by Django 3.1.5 on 2021-09-01 21:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UploadExcel', '0002_auto_20210901_0606'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actionitems',
            name='StudyName_fk',
        ),
        migrations.RemoveField(
            model_name='historicalactionitems',
            name='StudyName_fk',
        ),
    ]