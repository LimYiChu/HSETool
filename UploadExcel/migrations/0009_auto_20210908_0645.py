# Generated by Django 3.1.5 on 2021-09-07 22:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userT', '0013_phases'),
        ('UploadExcel', '0008_auto_20210907_0626'),
    ]

    operations = [
        migrations.RenameField(
            model_name='actionitems',
            old_name='ProjectPhase',
            new_name='ProjectPhase_backup'
        ),
        migrations.RenameField(
            model_name='historicalactionitems',
            old_name='ProjectPhase',
            new_name='ProjectPhase_backup'
        ),
        
        migrations.RenameField(
            model_name='actionitems',
            old_name='ProjectPhase_fk',
            new_name = 'ProjectPhase'
           
        ),
        migrations.RenameField(
            model_name='historicalactionitems',
            old_name='ProjectPhase_fk',
            new_name='ProjectPhase'
        ),
    ]
