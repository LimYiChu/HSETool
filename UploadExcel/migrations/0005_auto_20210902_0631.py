# Generated by Django 3.1.5 on 2021-09-01 22:31

from django.db import migrations


def fill_studies_fk(apps, schema_editor):
  mdlAI = apps.get_model('UploadExcel', 'ActionItems')
  Studies = apps.get_model('userT', 'Studies')
  for actions in mdlAI.objects.all():
    actions.StudyName_fk, created = Studies.objects.get_or_create(StudyName=actions.StudyName)
    actions.save()

class Migration(migrations.Migration):

    dependencies = [
        ('UploadExcel', '0004_auto_20210902_0604'),
    ]

    operations = [

         migrations.RunPython(fill_studies_fk),
    ]