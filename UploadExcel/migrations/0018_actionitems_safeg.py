# Generated by Django 3.1.5 on 2021-03-02 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UploadExcel', '0017_remove_actionitems_safeguard2'),
    ]

    operations = [
        migrations.AddField(
            model_name='actionitems',
            name='SafeG',
            field=models.TextField(null=True),
        ),
    ]
