# Generated by Django 3.2.7 on 2021-10-20 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UploadExcel', '0008_auto_20210922_0945'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='actionitems',
            index=models.Index(fields=['QueSeries', 'Organisation', 'Disipline', 'Subdisipline'], name='UploadExcel_QueSeri_9f4706_idx'),
        ),
    ]
