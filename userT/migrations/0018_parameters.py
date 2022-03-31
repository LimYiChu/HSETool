# Generated by Django 3.1.5 on 2022-03-29 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userT', '0017_historicalactionroutes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parameters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Versioning', models.CharField(max_length=200, null=True)),
                ('Emailactionee', models.CharField(blank=True, max_length=200, null=True)),
                ('Emailapprover', models.CharField(blank=True, max_length=200, null=True)),
                ('Emailfrequency', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name_plural': 'Parameters',
            },
        ),
    ]
