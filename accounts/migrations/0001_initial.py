# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-06-29 09:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_email', models.EmailField(blank=True, max_length=200, null=True)),
                ('surname', models.CharField(blank=True, max_length=120, null=True)),
                ('given_name', models.CharField(blank=True, max_length=120, null=True)),
                ('teacher', models.BooleanField(default=False)),
                ('student', models.BooleanField(default=False)),
                ('course_content_preferences', models.TextField(blank=True, default='')),
                ('other_personal_information', models.TextField(blank=True, default='')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
