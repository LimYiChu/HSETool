# Generated by Django 3.1.5 on 2021-07-08 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userT', '0007_auto_20210709_0609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='disipline',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='fullname',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='organisation',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='subdisipline',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]
