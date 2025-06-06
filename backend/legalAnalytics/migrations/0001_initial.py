# Generated by Django 5.1.3 on 2025-05-25 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DailyAnalytics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_users', models.PositiveIntegerField(default=0)),
                ('attorney_users', models.PositiveIntegerField(default=0)),
                ('client_users', models.PositiveIntegerField(default=0)),
                ('pending_approval', models.PositiveIntegerField(default=0)),
                ('active_requests', models.PositiveIntegerField(default=0)),
                ('pending_requests', models.PositiveIntegerField(default=0)),
                ('approved_requests', models.PositiveIntegerField(default=0)),
                ('rejected_requests', models.PositiveIntegerField(default=0)),
                ('document_uploads', models.JSONField(default=dict)),
                ('case_requests', models.JSONField(default=dict)),
                ('date', models.DateField(unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LifetimeAnalytics',
            fields=[
                ('total_users', models.PositiveIntegerField(default=0)),
                ('attorney_users', models.PositiveIntegerField(default=0)),
                ('client_users', models.PositiveIntegerField(default=0)),
                ('pending_approval', models.PositiveIntegerField(default=0)),
                ('active_requests', models.PositiveIntegerField(default=0)),
                ('pending_requests', models.PositiveIntegerField(default=0)),
                ('approved_requests', models.PositiveIntegerField(default=0)),
                ('rejected_requests', models.PositiveIntegerField(default=0)),
                ('document_uploads', models.JSONField(default=dict)),
                ('case_requests', models.JSONField(default=dict)),
                ('id', models.PositiveSmallIntegerField(default=1, primary_key=True, serialize=False)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MonthlyAnalytics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_users', models.PositiveIntegerField(default=0)),
                ('attorney_users', models.PositiveIntegerField(default=0)),
                ('client_users', models.PositiveIntegerField(default=0)),
                ('pending_approval', models.PositiveIntegerField(default=0)),
                ('active_requests', models.PositiveIntegerField(default=0)),
                ('pending_requests', models.PositiveIntegerField(default=0)),
                ('approved_requests', models.PositiveIntegerField(default=0)),
                ('rejected_requests', models.PositiveIntegerField(default=0)),
                ('document_uploads', models.JSONField(default=dict)),
                ('case_requests', models.JSONField(default=dict)),
                ('month', models.DateField(unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
