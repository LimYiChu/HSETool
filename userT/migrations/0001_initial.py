# Generated by Django 3.1.7 on 2021-05-16 04:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('fullname', models.CharField(max_length=254, null=True)),
                ('disipline', models.CharField(blank=True, max_length=254, null=True)),
                ('subdisipline', models.CharField(blank=True, max_length=254, null=True)),
                ('organisation', models.CharField(blank=True, max_length=254, null=True)),
                ('designation', models.CharField(blank=True, max_length=254, null=True)),
                ('expiration', models.DateTimeField(null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('admin', models.BooleanField(default=False)),
                ('staff', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RiskMatrix',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Consequence', models.CharField(blank=True, max_length=20, null=True)),
                ('Likelihood', models.CharField(blank=True, max_length=20, null=True)),
                ('Combined', models.CharField(blank=True, max_length=100, null=True)),
                ('Ranking', models.CharField(blank=True, max_length=100, null=True)),
                ('Colour', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name_plural': 'RiskMatrix',
            },
        ),
        migrations.CreateModel(
            name='Studies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StudyName', models.CharField(max_length=200, null=True)),
                ('ProjectPhase', models.CharField(max_length=200, null=True)),
                ('AttendanceList', models.CharField(max_length=1000, null=True)),
                ('DateConducted', models.DateField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Studies',
            },
        ),
        migrations.CreateModel(
            name='ActionRoutes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('Studies', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to='userT.studies')),
            ],
            options={
                'verbose_name_plural': 'ActionRoutes',
            },
        ),
    ]
