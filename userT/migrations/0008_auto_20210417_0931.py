# Generated by Django 3.1.5 on 2021-04-17 01:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userT', '0007_auto_20210417_0925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actionroutes',
            name='Studies',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to='userT.studies'),
        ),
    ]
