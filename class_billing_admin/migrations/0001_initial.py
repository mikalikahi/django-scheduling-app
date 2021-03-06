# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-09-22 06:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0002_auto_20190908_0840'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentBilling',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchased_class_hours', models.DecimalField(decimal_places=2, max_digits=5)),
                ('student_account', models.ManyToManyField(related_name='student_account', to='accounts.Profile')),
            ],
        ),
    ]
