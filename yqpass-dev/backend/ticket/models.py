import datetime

from django.db import models


class TicketRecord(models.Model):
    """
    工单记录
    """
    title = models.CharField("标题", max_length=128, default='', help_text="工单的标题")
    workflow_id = models.IntegerField("关联的流程id", help_text="与 workflow.Workflow 流程关联")
    sn = models.CharField("流水号", max_length=25, help_text="工单编号")
    state_id = models.IntegerField("当前状态", help_text="与 workflow.State 关联")
    parent_ticket_id = models.IntegerField("父工单id", default=0, help_text="与 ticket.TicketRecord 关联")
    parent_ticket_state_id = models.IntegerField("对应父工单状态id", default=0,
                                                 help_text="与 workflow.State 关联, 子工单是关联到父工单的某个状态下的")
    participant = models.CharField("当前处理人", max_length=128, default='', blank=True,
                                   help_text="可以为空(无处理人的情况，如结束状态)、username\多个username(以,隔开)\
                                   部门id\角色id\变量(creator,creator_tl)\脚本文件名(不包含上传后的路径)")
    participant_type_id = models.IntegerField("当前处理人类型", default=0,
                                              help_text="0.无处理人、1.个人、2.多人、3.部门、4.角色、"
                                                        "5.变量(工单创建人,创建人的leader)、6.脚本、7.工单的字段内容、"
                                                        "8.父工单的字段内容")
    relation = models.CharField("工单关联人", max_length=1024, default='', blank=True,
                                help_text="工单流转过程中将保存所有相关的人(包括创建人、曾经的待处理人)，用于查询")
    in_add_node = models.BooleanField("加签状态中", default=False, help_text="是否处于加签状态中")
    add_node_man = models.CharField("加签人", max_length=128, default='', blank=True,
                                    help_text="加签操作的人, 工单当前处理人处理完成后会回到该处理人, 当处于加签状态下才有效")

    creator = models.CharField("创建人", max_length=50, default='admin')
    gmt_created = models.DateTimeField("创建时间", auto_now_add=True)
    gmt_modified = models.DateTimeField("修改时间", auto_now=True)
    is_deleted = models.BooleanField("已删除", default=False)

    class Meta:
        verbose_name = "工单记录"
        verbose_name_plural = "工单记录"


class TicketFlowLog(models.Model):
    """
    工单流转日志
    """
    ticket_id = models.IntegerField("工单id")
    transition_id = models.IntegerField("流转id", help_text="与workflow.Transition关联")
    suggestion = models.CharField("处理意见", max_length=1000, default='', blank=True)
    state_id = models.IntegerField("当前状态id", default=0, blank=True)

    participant_type_id = models.IntegerField("处理人类型")
    participant = models.CharField("处理人", max_length=50, default='', blank=True)
    intervene_type_id = models.IntegerField("干预类型", default=0,
                                            help_text="0.非人为干预的流转、1.转交操作、2.加签操作、3.加签完成")
    ticket_data = models.CharField("工单数据", max_length=10000, default='', blank=True,
                                   help_text="可以用于记录当前表单数据，json")

    creator = models.CharField("创建人", max_length=50, default='admin')
    gmt_created = models.DateTimeField("创建时间", auto_now_add=True)
    gmt_modified = models.DateTimeField("修改时间", auto_now=True)
    is_deleted = models.BooleanField("已删除", default=False)

    class Meta:
        verbose_name = "工单流转记录"
        verbose_name_plural = "工单流转记录"


class TicketCustomField(models.Model):
    """
    工单自定义字段，实际的值
    """
    name = models.CharField("字段名", max_length=50)
    field_key = models.CharField("字段标识", max_length=50)
    ticket_id = models.IntegerField("工单id")
    field_type_id = models.IntegerField("字段类型", help_text="5.字符串、10.整形、15.浮点型、20.布尔、25.日期、"
                                                          "30.日期时间、35.单选框、40.多选框、45.下拉列表、"
                                                          "50.多选下拉列表、55.文本域、60.用户名、70.多选的用户名")
    char_value = models.CharField("字符串值", max_length=1000, default='', blank=True)
    int_value = models.IntegerField("整型值", default=0, blank=True)
    float_value = models.FloatField("浮点数", default=0.0, blank=True)
    bool_value = models.BooleanField("布尔值", default=False, blank=True)
    date_value = models.DateField("日期值", default=datetime.datetime.strptime('1970-01-01', "%Y-%m-%d"), blank=True)
    datetime_value = models.DateTimeField("日期时间值", default=datetime.datetime.strptime('1970-01-01 00:00:01',
                                                                                      '%Y-%m-%d %H:%M:%S'), blank=True)
    time_value = models.TimeField("时间值", default=datetime.datetime.strptime('00:00:01', '%H:%M:%S'), blank=True)
    radio_value = models.CharField("radio值", default='', max_length=50, blank=True)
    checkbox_value = models.CharField("checkbox值", default='', max_length=50, blank=True, help_text="逗号隔开多个选项")
    select_value = models.CharField("下拉列表值", default='', max_length=50, blank=True)
    multi_select_value = models.CharField("多选下拉列表值", default='', max_length=50, blank=True, help_text="逗号隔开多个选项")
    text_value = models.TextField("文本值", default='', blank=True)
    username_value = models.CharField("用户名", max_length=50, default='', blank=True)
    multi_username_value = models.CharField("多选用户名", max_length=1000, default='', blank=True)

    creator = models.CharField("创建人", max_length=50, default='admin')
    gmt_created = models.DateTimeField("创建时间", auto_now_add=True)
    gmt_modified = models.DateTimeField("修改时间", auto_now=True)
    is_deleted = models.BooleanField("已删除", default=False)

    class Meta:
        verbose_name = "工单自定义字段"
        verbose_name_plural = "工单自定义字段"
