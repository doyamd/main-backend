# Generated by Django 5.1.3 on 2025-05-18 11:20

import legalUser.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legalUser', '0004_attorney_expertise_delete_attorneyexpertise_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attorney',
            name='expertise',
            field=models.JSONField(blank=True, default=list, validators=[legalUser.models.validate_expertise_list]),
        ),
    ]
