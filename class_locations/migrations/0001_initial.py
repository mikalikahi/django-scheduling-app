# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-06-29 09:33
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClassLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_name', models.CharField(max_length=200)),
                ('address_line_1', models.CharField(max_length=120)),
                ('address_line_2', models.CharField(max_length=120)),
                ('classroom', models.CharField(blank=True, default='', max_length=10, null=True)),
                ('district', models.CharField(choices=[('beitou', 'Beitou'), ('daan', 'Daan'), ('datong', 'Datong'), ('nangang', 'Nangang'), ('neihu', 'Neihu'), ('shilin', 'Shilin'), ('songshan', 'Songshan'), ('wanhua', 'Wanhua'), ('wenshan', 'Wenshan'), ('xinyi', 'Xinyi'), ('zhongshang', 'Zhongshan'), ('zhongzheng', 'Zhongzheng'), ('banqiao', 'Banqiao'), ('zhonghe', 'Zhonghe'), ('yonghe', 'Yonghe'), ('tucheng', 'Tucheng'), ('shulin', 'Shulin'), ('sanxia', 'Sanxia'), ('yingge', 'Yingge'), ('xinzhuang', 'Xinzhuang'), ('sanchong', 'Sanchong'), ('luzhou', 'Luzhou'), ('wugu', 'Wugu'), ('taishan', 'Taishan'), ('linkou', 'Linkou'), ('tamsui', 'Tamsui'), ('bali', 'Bali'), ('sanzhi', 'Sanzhi'), ('shimen', 'Shimen'), ('jinshan', 'Jinshan'), ('wanli', 'Wanli'), ('xizhi', 'Xinzhi'), ('ruifang', 'Ruifang'), ('gongliao', 'Gongliao'), ('pinxi', 'Pinxi'), ('shangxi', 'Shuangxi'), ('xindian', 'Xindian'), ('shenkeng', 'Shenkeng'), ('shiding', 'Shiding'), ('pinglin', 'Pinglin'), ('wulai', 'Wulai'), ('other', 'Other')], max_length=120)),
                ('city', models.CharField(choices=[('new_taipei_city', 'New Taipei City'), ('taipei_city', 'Taipei City')], max_length=120)),
                ('contact_name', models.CharField(blank=True, max_length=120, null=True)),
                ('contact_phone', models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator(code='Invalid number', message='Length has to be 10', regex='^\\d{10}$')])),
                ('contact_phone_extension', models.CharField(blank=True, max_length=5, null=True)),
                ('other_information', models.TextField(blank=True, default='')),
            ],
        ),
    ]
