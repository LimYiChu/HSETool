# Generated by Django 3.1.5 on 2021-07-04 03:54

from django.db import migrations, models
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActionItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('DueDate', models.DateField(blank=True, null=True)),
                ('QueSeries', models.IntegerField(blank=True, default=0, null=True)),
                ('QueSeriesTarget', models.IntegerField(blank=True, default=0, null=True)),
                ('Guidewords', models.TextField(blank=True, null=True)),
                ('Deviation', models.TextField(blank=True, null=True)),
                ('Revision', models.IntegerField(blank=True, default=0, null=True)),
                ('DateCreated', models.DateField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Attachments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Username', models.CharField(blank=True, max_length=255, null=True)),
                ('Attachment', models.FileField(blank=True, max_length=500, null=True, upload_to='attachments')),
                ('DateAdded', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Attachments',
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Username', models.CharField(blank=True, max_length=255, null=True)),
                ('Reason', models.TextField(blank=True, null=True)),
                ('Attachment', models.FileField(blank=True, max_length=500, null=True, upload_to='comments')),
                ('DateAdded', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Comments',
            },
        ),
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
                ('DueDate', models.DateField(blank=True, null=True)),
                ('QueSeries', models.IntegerField(blank=True, default=0, null=True)),
                ('QueSeriesTarget', models.IntegerField(blank=True, default=0, null=True)),
                ('Guidewords', models.TextField(blank=True, null=True)),
                ('Deviation', models.TextField(blank=True, null=True)),
                ('Revision', models.IntegerField(blank=True, default=0, null=True)),
                ('DateCreated', models.DateField(blank=True, editable=False, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical action items',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='UploadExl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Filename', models.FileField(max_length=500, upload_to='excelUpload')),
                ('DateAdded', models.DateTimeField(auto_now_add=True)),
                ('Username', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
