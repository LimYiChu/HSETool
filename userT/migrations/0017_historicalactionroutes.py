# Generated by Django 3.1.5 on 2021-12-20 23:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('userT', '0016_auto_20211216_0647'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalActionRoutes',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('Organisation', models.CharField(max_length=100, null=True)),
                ('Disipline', models.CharField(max_length=100, null=True)),
                ('Subdisipline', models.CharField(max_length=100, null=True)),
                ('Actionee', models.CharField(max_length=100, null=True)),
                ('Approver1', models.CharField(blank=True, max_length=100, null=True)),
                ('Approver2', models.CharField(blank=True, max_length=100, null=True)),
                ('Approver3', models.CharField(blank=True, max_length=100, null=True)),
                ('Approver4', models.CharField(blank=True, max_length=100, null=True)),
                ('Approver5', models.CharField(blank=True, max_length=100, null=True)),
                ('Approver6', models.CharField(blank=True, max_length=100, null=True)),
                ('Approver7', models.CharField(blank=True, max_length=100, null=True)),
                ('Approver8', models.CharField(blank=True, max_length=100, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('ProjectPhase', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='userT.phases')),
                ('Studies', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='userT.studies')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical action routes',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
