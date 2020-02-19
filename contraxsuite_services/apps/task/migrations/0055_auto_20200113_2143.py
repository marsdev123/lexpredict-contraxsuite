# Generated by Django 2.2.8 on 2020-01-13 21:43

import apps.common.model_utils.hr_django_json_encoder
import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0054_auto_remove_args_index'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='args',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, encoder=apps.common.model_utils.hr_django_json_encoder.HRDjangoJSONEncoder, null=True),
        ),
    ]