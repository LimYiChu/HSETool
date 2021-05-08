# Generated by Django 3.1.7 on 2021-05-08 05:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('UploadExcel', '0018_actionitems_queseriestarget'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalActionItems',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('StudyActionNo', models.CharField(blank=True, max_length=100, null=True)),
                ('StudyName', models.CharField(blank=True, max_length=255, null=True)),
                ('Facility', models.CharField(blank=True, max_length=255, null=True)),
                ('ProjectPhase', models.CharField(blank=True, max_length=255, null=True)),
                ('Cause', models.TextField(blank=True, null=True)),
                ('Safeguard', models.TextField(blank=True, null=True)),
                ('Consequence', models.TextField(blank=True, null=True)),
                ('Recommendations', models.TextField(blank=True, null=True)),
                ('InitialRisk', models.CharField(blank=True, max_length=10, null=True)),
                ('ResidualRisk', models.CharField(blank=True, max_length=10, null=True)),
                ('Response', models.TextField(blank=True, null=True)),
                ('Organisation', models.CharField(blank=True, max_length=100, null=True)),
                ('Disipline', models.CharField(blank=True, max_length=100, null=True)),
                ('Subdisipline', models.CharField(blank=True, max_length=100, null=True)),
                ('FutureAction', models.TextField(blank=True, null=True)),
                ('DueDate', models.DateField(blank=True, editable=False, null=True)),
                ('QueSeries', models.IntegerField(blank=True, default=0, null=True)),
                ('QueSeriesTarget', models.IntegerField(blank=True, default=0, null=True)),
                ('Guidewords', models.TextField(blank=True, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical action items',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
