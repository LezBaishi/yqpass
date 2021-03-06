# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-08-06 10:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workflow_id', models.IntegerField(verbose_name='工作流id')),
                ('field_type_id', models.IntegerField(help_text='5.字符串，10.整形，15.浮点型，20.布尔，25.日期，30.日期时间，35.单选框，40.多选框，45.下拉列表，50.多选下拉列表，55.文本域，60.用户名, 70.多选的用户名', verbose_name='类型')),
                ('field_key', models.CharField(help_text='尽量特殊,避免冲突', max_length=50, verbose_name='字段标识')),
                ('field_name', models.CharField(max_length=50, verbose_name='字段名称')),
                ('order_id', models.IntegerField(default=0, help_text='工单基础字段在表单中排序为:流水号0,标题20,状态id40,状态名41,创建人80,创建时间100,更新时间120.前端展示工单信息的表单可以根据这个id顺序排列', verbose_name='排序')),
                ('default_value', models.CharField(blank=True, default='', help_text='前端展示时，可以将此内容作为表单中的该字段的默认值', max_length=512, verbose_name='默认值')),
                ('description', models.CharField(blank=True, default='', help_text='字段的描述信息，对于非文本域字段可以将此内容作为placeholder', max_length=512, verbose_name='描述')),
                ('field_template', models.TextField(blank=True, default='', help_text='字段的描述信息，对于非文本域字段可以将此内容作为placeholder', verbose_name='文本域模板')),
                ('boolean_field_display', models.CharField(blank=True, default='', help_text="当为布尔类型时候，可以支持自定义显示形式。{'1':'是',0:'否'}或{'1':'需要','0':'不需要'}，注意数字也需要引号", max_length=100, verbose_name='布尔类型显示名')),
                ('field_choice', models.CharField(blank=True, default='{}', help_text="radio,checkbox,select,multiselect类型可供选择的选项，格式为json如:{'1':'中国', '2':'美国'},注意数字也需要引号", max_length=1000, verbose_name='radio, checkbox, select的选项')),
                ('creator', models.CharField(default='admin', max_length=50, verbose_name='创建人')),
                ('gmt_created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('gmt_modified', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='已删除')),
            ],
            options={
                'verbose_name': '工作流自定义字段',
                'verbose_name_plural': '工作流自定义字段',
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='名称')),
                ('workflow_id', models.IntegerField(verbose_name='工作流')),
                ('sub_workflow_id', models.IntegerField(blank=True, default=0, help_text='如果需要在此状态启用子工单,请填写对应的工作流id', verbose_name='子工作流id')),
                ('is_hidden', models.BooleanField(default=False, help_text='设置为True时,获取工单步骤api中不显示此状态(当前处于此状态时除外)', verbose_name='是否隐藏')),
                ('order_id', models.IntegerField(default=0, help_text='用于工单步骤接口时,step上状态的顺序,值越小越靠前', verbose_name='状态顺序')),
                ('type_id', models.IntegerField(default=0, help_text='0.普通类型 1.初始状态(用于新建工单时,获取对应的字段必填及transition信息) 2.结束状态(此状态下的工单不得再处理，即没有对应的transition)', verbose_name='状态类型id')),
                ('participant_type_id', models.IntegerField(blank=True, default=1, help_text="0.无处理人,1.个人,2.多人,3.部门,4.角色,5.变量(支持工单创建人,创建人的leader),6.脚本,7.工单的字段内容(如表单中的'测试负责人'，需要为用户名或者逗号隔开的多个用户名),8.父工单的字段内容", verbose_name='参与者类型id')),
                ('participant', models.CharField(blank=True, default='', help_text='可以为空(无处理人的情况，如结束状态)、username\\多个username(以,隔开)                                   部门id\\角色id\\变量(creator,creator_tl)\\脚本文件名(不包含上传后的路径)等，包含子工作流的需要设置处理人为loonrobot', max_length=100, verbose_name='参与者')),
                ('distribute_type_id', models.IntegerField(default=1, help_text='1.主动接单(如果当前处理人实际为多人的时候，需要先接单才能处理)2.直接处理(即使当前处理人实际为多人，也可以直接处理) ', verbose_name='分配方式')),
                ('state_field_str', models.TextField(default='{}', help_text="json格式,包括读写属性1：只读，2：必填，3：可选. 示例：{'created_at':1,'title':2, 'sn':1}, 内置特殊字段participant_info.participant_name:当前处理人信息(部门名称、角色名称)，state.state_name:当前状态的状态名,workflow.workflow_name:工作流名称", verbose_name='表单字段')),
                ('label', models.CharField(default='{}', help_text="json格式,由调用方根据实际定制需求自行确定,如状态下需要显示哪些前端组件:{'components':[{'AppList':1, 'ProjectList':7}]}", max_length=1000, verbose_name='状态标签')),
                ('creator', models.CharField(default='admin', max_length=50, verbose_name='创建人')),
                ('gmt_created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('gmt_modified', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='已删除')),
            ],
            options={
                'verbose_name': '工作流状态',
                'verbose_name_plural': '工作流状态',
            },
        ),
        migrations.CreateModel(
            name='Transition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='操作')),
                ('workflow_id', models.IntegerField(verbose_name='工作流id')),
                ('transition_type_id', models.IntegerField(default=1, help_text='1.常规流转', verbose_name='流转类型')),
                ('source_state_id', models.IntegerField(verbose_name='源状态id')),
                ('destination_state_id', models.IntegerField(verbose_name='目的状态id')),
                ('field_require_check', models.BooleanField(default=True, help_text="默认在用户点击操作的时候需要校验工单表单的必填项,如果设置为否则不检查。用于如'退回'属性的操作，不需要填写表单内容", verbose_name='是否校验必填项')),
                ('alert_enable', models.BooleanField(default=False, verbose_name='点击弹窗提示')),
                ('alert_text', models.CharField(blank=True, default='', max_length=100, verbose_name='弹窗内容')),
                ('creator', models.CharField(default='admin', max_length=50, verbose_name='创建人')),
                ('gmt_created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('gmt_modified', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='已删除')),
            ],
            options={
                'verbose_name': '工作流流转',
                'verbose_name_plural': '工作流流转',
            },
        ),
        migrations.CreateModel(
            name='Workflow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='名称')),
                ('description', models.CharField(max_length=256, verbose_name='描述')),
                ('flowchart', models.FileField(blank=True, help_text='工作流的流程图', upload_to='flowchart', verbose_name='流程图')),
                ('view_permission_check', models.BooleanField(default=True, help_text='开启后，只允许工单的关联人创建人、曾经的处理人)有权限查看工单', verbose_name='查看权限校验')),
                ('display_form_str', models.CharField(blank=True, default='[]', help_text="默认'[]',用于用户只有对应工单查看权限时显示哪些字段，field_key的list的json如['days','sn'],内置特殊字段participant_info.participant_name:当前处理人信息(部门名称、角色名称), state.state_name：当前状态的状态名workflow.workflow_name:工作流名称", max_length=10000, verbose_name='展现表单字段')),
                ('creator', models.CharField(default='admin', max_length=50, verbose_name='创建人')),
                ('gmt_created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('gmt_modified', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='已删除')),
            ],
            options={
                'verbose_name': '工作流',
                'verbose_name_plural': '工作流',
            },
        ),
        migrations.CreateModel(
            name='WorkflowScript',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='名称')),
                ('saved_name', models.FileField(help_text='请上传python脚本', upload_to='workflow_script', verbose_name='存储的文件名')),
                ('description', models.CharField(blank=True, default='', max_length=100, verbose_name='描述')),
                ('is_active', models.BooleanField(default=True, help_text='勾选时，才允许实际操作', verbose_name='是否可用')),
                ('creator', models.CharField(default='admin', max_length=50, verbose_name='创建人')),
                ('gmt_created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('gmt_modified', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='已删除')),
            ],
            options={
                'verbose_name': '工作流脚本',
                'verbose_name_plural': '工作流脚本',
            },
        ),
    ]
