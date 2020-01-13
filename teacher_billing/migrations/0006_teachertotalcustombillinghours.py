# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-11-12 07:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacher_billing', '0005_auto_20191112_0159'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeacherTotalCustomBillingHours',
            fields=[
                ('teacher_custom_billing_hours', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='teacher_billing.TeacherCustomBillingHours')),
                ('total_billed_custom_hours', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
