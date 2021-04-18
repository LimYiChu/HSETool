# Generated by Django 3.1.5 on 2021-04-17 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userT', '0005_studies'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Workshops',
        ),
        migrations.AlterModelManagers(
            name='actionroutes',
            managers=[
            ],
        ),
        migrations.AddField(
            model_name='studies',
            name='AttendanceList',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='studies',
            name='DateConducted',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
