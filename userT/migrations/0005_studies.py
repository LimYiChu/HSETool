# Generated by Django 3.1.5 on 2021-04-17 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userT', '0004_auto_20210416_0747'),
    ]

    operations = [
        migrations.CreateModel(
            name='Studies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StudyName', models.CharField(max_length=200, null=True)),
                ('ProjectPhase', models.CharField(max_length=200, null=True)),
            ],
        ),
    ]
