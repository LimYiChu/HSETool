# Generated by Django 3.1.5 on 2021-03-25 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UploadExcel', '0005_auto_20210321_0708'),
    ]

    operations = [
        migrations.AddField(
            model_name='actionitems',
            name='Comments',
            field=models.TextField(blank=True, null=True),
        ),
    ]
