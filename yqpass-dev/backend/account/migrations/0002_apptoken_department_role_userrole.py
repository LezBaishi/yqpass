# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-07-26 22:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(max_length=50, verbose_name='应用名称')),
                ('token', models.CharField(help_text='后端自动生成', max_length=257, verbose_name='签名令牌')),
                ('creator', models.CharField(max_length=50, verbose_name='创建人')),
                ('gmt_created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('gmt_modified', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='已删除')),
            ],
            options={
                'verbose_name': '调用token',
                'verbose_name_plural': '调用token',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='部门名称')),
                ('parent_dept_id', models.IntegerField(blank=True, default=0, verbose_name='上级部门id')),
                ('leader', models.CharField(blank=True, default='', help_text='部门leader, user表中的用户名', max_length=50, verbose_name='部门领导')),
                ('approver', models.CharField(blank=True, default='', help_text='user表中的用户名, 用逗号隔开多个user。', max_length=50, verbose_name='审批人')),
                ('label', models.CharField(blank=True, default='', max_length=50, verbose_name='标签')),
                ('creator', models.CharField(max_length=50, verbose_name='创建人')),
                ('gmt_created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('gmt_modified', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='已删除')),
            ],
            options={
                'verbose_name': '部门',
                'verbose_name_plural': '部门',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='名称')),
                ('description', models.CharField(default='', max_length=100, verbose_name='描述')),
                ('label', models.CharField(blank=True, default='', max_length=50, verbose_name='标签')),
                ('creator', models.CharField(max_length=50, verbose_name='创建人')),
                ('gmt_created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('gmt_modified', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='已删除')),
            ],
            options={
                'verbose_name': '角色',
                'verbose_name_plural': '角色',
            },
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(verbose_name='用户id')),
                ('role_id', models.IntegerField(verbose_name='角色id')),
                ('creator', models.CharField(max_length=50, verbose_name='创建人')),
                ('gmt_created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('gmt_modified', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='已删除')),
            ],
            options={
                'verbose_name': '用户角色',
                'verbose_name_plural': '用户角色',
            },
        ),
    ]
