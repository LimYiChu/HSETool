# Generated by Django 3.1.5 on 2021-01-23 22:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UploadExcel', '0007_auto_20210122_1931'),
    ]

    operations = [
        migrations.RenameField(
            model_name='uploadexl',
            old_name='filename',
            new_name='filoename',
        ),
    ]
