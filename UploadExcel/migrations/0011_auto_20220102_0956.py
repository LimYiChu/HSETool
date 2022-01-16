# Generated by Django 3.1.5 on 2022-01-02 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UploadExcel', '0010_auto_20211018_0614'),
    ]

    operations = [
        migrations.AddField(
            model_name='actionitems',
            name='MitigativeSafeguard',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='actionitems',
            name='NodeDescription',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='actionitems',
            name='NodeNo',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='actionitems',
            name='PreventiveSafeguard',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalactionitems',
            name='MitigativeSafeguard',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalactionitems',
            name='NodeDescription',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalactionitems',
            name='NodeNo',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='historicalactionitems',
            name='PreventiveSafeguard',
            field=models.TextField(blank=True, null=True),
        ),
    ]