# Generated by Django 3.1.5 on 2021-01-24 00:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UploadExcel', '0008_auto_20210124_0656'),
    ]

    operations = [
        migrations.RenameField(
            model_name='uploadexl',
            old_name='filoename',
            new_name='file_id',
        ),
    ]