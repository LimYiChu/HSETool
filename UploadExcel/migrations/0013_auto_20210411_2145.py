# Generated by Django 3.1.5 on 2021-04-11 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UploadExcel', '0012_auto_20210406_0724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actionitems',
            name='QueSeries',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
