# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-08-16 10:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketcustomfield',
            name='field_type_id',
            field=models.IntegerField(help_text='5.字符串、10.整形、15.浮点型、20.布尔、25.日期、30.日期时间、35.单选框、40.多选框、45.下拉列表、50.多选下拉列表、55.文本域、60.用户名、70.多选的用户名', verbose_name='字段类型'),
        ),
        migrations.AlterField(
            model_name='ticketflowlog',
            name='intervene_type_id',
            field=models.IntegerField(default=0, help_text='0.非人为干预的流转、1.转交操作、2.加签操作、3.加签完成', verbose_name='干预类型'),
        ),
        migrations.AlterField(
            model_name='ticketrecord',
            name='add_node_man',
            field=models.CharField(blank=True, default='', help_text='加签操作的人, 工单当前处理人处理完成后会回到该处理人, 当处于加签状态下才有效', max_length=128, verbose_name='加签人'),
        ),
        migrations.AlterField(
            model_name='ticketrecord',
            name='parent_ticket_state_id',
            field=models.IntegerField(default=0, help_text='与 workflow.State 关联, 子工单是关联到父工单的某个状态下的', verbose_name='对应父工单状态id'),
        ),
        migrations.AlterField(
            model_name='ticketrecord',
            name='participant',
            field=models.CharField(blank=True, default='', help_text='可以为空(无处理人的情况，如结束状态)、username\\多个username(以,隔开)                                   部门id\\角色id\\变量(creator,creator_tl)\\脚本文件名(不包含上传后的路径)', max_length=128, verbose_name='当前处理人'),
        ),
        migrations.AlterField(
            model_name='ticketrecord',
            name='participant_type_id',
            field=models.IntegerField(default=0, help_text='0.无处理人、1.个人、2.多人、3.部门、4.角色、5.变量(工单创建人,创建人的leader)、6.脚本、7.工单的字段内容、8.父工单的字段内容', verbose_name='当前处理人类型'),
        ),
        migrations.AlterField(
            model_name='ticketrecord',
            name='sn',
            field=models.CharField(help_text='工单编号', max_length=25, verbose_name='流水号'),
        ),
    ]
