# Generated by Django 3.1.5 on 2021-01-28 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UploadExcel', '0010_auto_20210124_1030'),
    ]

    operations = [
        migrations.AddField(
            model_name='actionitems',
            name='Attachment',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='actionitems',
            name='Response',
            field=models.TextField(null=True),
        ),
    ]