# Generated by Django 3.1.5 on 2021-07-08 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userT', '0006_auto_20210708_2028'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]