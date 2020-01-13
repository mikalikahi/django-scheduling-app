# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-11-12 01:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher_billing', '0004_teachertotalbillinghours'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teachertotalbillinghours',
            name='total_billed_inside_hours',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='teachertotalbillinghours',
            name='total_billed_outside_hours',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
