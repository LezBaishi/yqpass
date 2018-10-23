from django.db import models


class Workflow(models.Model):
    """
    工作流
    """
    name = models.CharField("名称", max_length=50)
    description = models.CharField("描述", max_length=256)
    flowchart = models.FileField("流程图", upload_to='flowchart', blank=True, help_text="工作流的流程图")
    view_permission_check = models.BooleanField("查看权限校验", default=True,
                                                help_text="开启后，只允许工单的关联人创建人、曾经的处理人)有权限查看工单")
    display_form_str = models.CharField("展现表单字段", max_length=10000, default='[]', blank=True,
                                        help_text="默认'[]',用户只有工单查看权限时显示的字段，field_key的list"
                                                  "如 ['days','sn'],内置特殊字段： "
                                                  "participant_info.participant_name:当前处理人信息(部门名称、角色名称), "
                                                  "state.state_name：当前状态的状态名"
                                                  "workflow.workflow_name:工作流名称")

    creator = models.CharField('创建人', max_length=50, default='admin')
    gmt_created = models.DateTimeField('创建时间', auto_now_add=True)
    modifier = models.CharField('修改人', max_length=50, default='admin')
    gmt_modified = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField("已删除", default=False)

    class Meta:
        verbose_name = "工作流"
        verbose_name_plural = "工作流"


class State(models.Model):
    """
    状态记录, 变量支持通过脚本获取
    """
    name = models.CharField("名称", max_length=50)
    workflow_id = models.IntegerField("工作流")
    sub_workflow_id = models.IntegerField("子工作流id", default=0, blank=True,
                                          help_text="如果需要在此状态启用子工单,请填写对应的工作流id")
    is_hidden = models.BooleanField("是否隐藏", default=False,
                                    help_text="设置为True时,获取工单处理步骤信息中不显示此状态(当前处于此状态时除外)")
    order_id = models.IntegerField("状态顺序", default=0, help_text="用于工单步骤接口时,step上状态的顺序,值越小越靠前")
    type_id = models.IntegerField("状态类型id", default=0,
                                  help_text="0.普通类型 1.初始状态(用于新建工单时,获取对应的字段必填及transition信息) "
                                            "2.结束状态(此状态下的工单不得再处理，即没有对应的transition)")

    participant_type_id = models.IntegerField("参与者类型id", default=1, blank=True,
                                              help_text="0.无处理人、1.个人、2.多人、3.部门、4.角色、"
                                                        "5.变量(工单创建人,创建人的leader)、6.脚本、7.工单的字段内容、"
                                                        "8.父工单的字段内容")
    participant = models.CharField("参与者", default='', blank=True, max_length=100,
                                   help_text="可以为空(无处理人的情况，如结束状态)、username\多个username(以,隔开)\
                                   部门id\角色id\变量(creator,creator_tl)\脚本文件名(不包含上传后的路径)等，"
                                             "包含子工作流的需要设置处理人为robot")
    distribute_type_id = models.IntegerField("分配方式", default=1,
                                             help_text="1.主动接单(如果当前处理人实际为多人的时候，需要先接单才能处理)"
                                                       "2.直接处理(即使当前处理人实际为多人，也可以直接处理) ")
    state_field_str = models.TextField("表单字段", default='{}',
                                       help_text="json格式,包括读写属性1：只读，2：必填，3：可选. 示例："
                                                 "{'created_at':1,'title':2, 'sn':1} "
                                                 "内置特殊字段："
                                                 "participant_info.participant_name:当前处理人信息(部门名称、角色名称)，"
                                                 "state.state_name:当前状态的状态名,"
                                                 "workflow.workflow_name:工作流名称")
    label = models.CharField("状态标签", max_length=1000, default='{}',
                             help_text="json格式,由调用方根据实际定制需求自行确定,如状态下需要显示哪些前端组件:"
                                       "{'components':[{'AppList':1, 'ProjectList':7}]}")

    creator = models.CharField('创建人', max_length=50, default='admin')
    gmt_created = models.DateTimeField('创建时间', auto_now_add=True)
    modifier = models.CharField('修改人', max_length=50, default='admin')
    gmt_modified = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField("已删除", default=False)

    class Meta:
        verbose_name = "工作流状态"
        verbose_name_plural = "工作流状态"


class Transition(models.Model):
    """
    工作流流转
    """
    name = models.CharField("操作", max_length=50)
    workflow_id = models.IntegerField("工作流id")
    transition_type_id = models.IntegerField("流转类型", default=1, help_text="1.常规流转")
    source_state_id = models.IntegerField("源状态id")
    destination_state_id = models.IntegerField("目的状态id")
    field_require_check = models.BooleanField("是否校验必填项", default=True,
                                              help_text="默认在用户点击操作的时候需要校验工单表单的必填项,"
                                                        "如果设置为否则不检查。用于如'退回'属性的操作，不需要填写表单内容")
    alert_enable = models.BooleanField("点击弹窗提示", default=False)
    alert_text = models.CharField("弹窗内容", max_length=100, default='', blank=True)

    creator = models.CharField('创建人', max_length=50, default='admin')
    gmt_created = models.DateTimeField('创建时间', auto_now_add=True)
    modifier = models.CharField('修改人', max_length=50, default='admin')
    gmt_modified = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField("已删除", default=False)

    class Meta:
        verbose_name = "工作流流转"
        verbose_name_plural = "工作流流转"


class CustomField(models.Model):
    """
    自定义字段, 设定某个工作流有哪些自定义字段
    """
    workflow_id = models.IntegerField("工作流id")
    field_type_id = models.IntegerField("类型", help_text="5.字符串、10.整形、15.浮点型、20.布尔、25.日期、"
                                                        "30.日期时间、35.单选框、40.多选框、45.下拉列表、"
                                                        "50.多选下拉列表、55.文本域、60.用户名、70.多选的用户名")
    field_key = models.CharField("字段标识", max_length=50, help_text="尽量特殊,避免冲突")
    field_name = models.CharField("字段名称", max_length=50)
    order_id = models.IntegerField("排序", default=0,
                                   help_text="工单基础字段在表单中排序为:流水号0、标题20、状态id40、状态名41、创建人80、"
                                             "创建时间100、更新时间120、前端展示工单信息的表单可以根据这个id顺序排列")
    default_value = models.CharField("默认值", default='', blank=True, max_length=512,
                                     help_text="前端展示时，可以将此内容作为表单中的该字段的默认值")
    description = models.CharField("描述", max_length=512, blank=True, default='',
                                   help_text="字段的描述信息，对于非文本域字段可以将此内容作为placeholder")
    field_template = models.TextField("文本域模板", default='', blank=True,
                                      help_text="字段的描述信息，对于非文本域字段可以将此内容作为placeholder")
    boolean_field_display = models.CharField("布尔类型显示名", max_length=100, default='', blank=True,
                                             help_text="当为布尔类型时候，可以支持自定义显示形式。"
                                                       "{'1':'是',0:'否'}或{'1':'需要','0':'不需要'}，注意数字也需要引号")
    field_choice = models.CharField("radio, checkbox, select的选项", max_length=1000, default='{}', blank=True,
                                    help_text="radio,checkbox,select,multiselect类型可供选择的选项，"
                                              "格式为json如:{'1':'中国', '2':'美国'},注意数字也需要引号")

    creator = models.CharField('创建人', max_length=50, default='admin')
    gmt_created = models.DateTimeField('创建时间', auto_now_add=True)
    modifier = models.CharField('修改人', max_length=50, default='admin')
    gmt_modified = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField("已删除", default=False)

    class Meta:
        verbose_name = "工作流自定义字段"
        verbose_name_plural = "工作流自定义字段"


class WorkflowScript(models.Model):
    """
    流程中执行的脚本
    """
    name = models.CharField("名称", max_length=50)
    saved_name = models.FileField("存储的文件名", upload_to='workflow_script',
                                  help_text="请上传python脚本")
    description = models.CharField("描述", max_length=100, default='', blank=True)
    is_active = models.BooleanField("是否可用", default=True, help_text="勾选时，才允许实际操作")

    creator = models.CharField('创建人', max_length=50, default='admin')
    gmt_created = models.DateTimeField('创建时间', auto_now_add=True)
    modifier = models.CharField('修改人', max_length=50, default='admin')
    gmt_modified = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField("已删除", default=False)

    class Meta:
        verbose_name = "工作流脚本"
        verbose_name_plural = "工作流脚本"
