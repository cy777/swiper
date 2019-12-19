# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-12-19 13:36
from __future__ import unicode_literals

from django.db import migrations, models
import lib.mixins


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=128, verbose_name='目标城市')),
                ('min_distance', models.IntegerField(default=0, verbose_name='最小查找范围')),
                ('max_distance', models.IntegerField(default=100, verbose_name='最大查找范围')),
                ('min_dating_age', models.IntegerField(default=18, verbose_name='最小交友年龄')),
                ('max_dating_age', models.IntegerField(default=50, verbose_name='最大交友年龄')),
                ('dating_sex', models.CharField(choices=[('female', 'female'), ('male', 'male')], default='female', max_length=8, verbose_name='匹配的性别')),
                ('vibration', models.BooleanField(default=True, verbose_name='开启震动')),
                ('only_matche', models.BooleanField(default=True, verbose_name='不让为匹配的人看我的相册')),
                ('auto_play', models.BooleanField(default=True, verbose_name='自动播放视频')),
            ],
            options={
                'db_table': 'profile',
            },
            bases=(models.Model, lib.mixins.ModelMixin),
        ),
    ]
