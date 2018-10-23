from django.db import models
from backend.ticket.models import TicketRecord


# Create your models here.

class ApplicationDetail(models.Model):
    """
    工单明细表
    """
    SINGLE = '单模'
    MULTI = '多模'
    PORT_TYPE = (
        (SINGLE, "单模"),
        (MULTI, "多模"),
    )
    BANDWIDTH_TYPE = (
        ("155M", "155M"),
        ("GE", "GE"),
        ("2.5GE", "2.5GE"),
        ("10GE", "10GE"),
        ("40GE", "40GE"),
        ("100GE", "100GE"),
    )
    MAIN = '主用'
    SPARE = '备用'
    MAIN_OR_SPARE_TYPE = (
        (MAIN, "主用"),
        (SPARE, "备用")
    )

    ticket_id = models.IntegerField("工单id", default=0)
    field_num = models.IntegerField("申请电路序号", default=0)
    bus_sys_name = models.CharField("业务系统", max_length=50, help_text="如南方基地信息支撑平台", default='')

    department1_A = models.CharField("A端设备移动维护部门", help_text="如XX中心", max_length=20, default='')
    person1_A = models.CharField("移动负责人", help_text='请填写姓名', max_length=10, default='')
    phone1_A = models.CharField("移动负责人联系方式", help_text='请填写手机号', max_length=20, default='')
    department2_A = models.CharField("A端设备维护合作单位", help_text='如XX公司', max_length=20, default='')
    person2_A = models.CharField("合作单位负责人", help_text='请填写姓名', max_length=10, default='')
    phone2_A = models.CharField("合作单位联系方式", help_text='请填写手机号', max_length=20, default='')
    fk_rid_A = models.IntegerField("A端业务设备所在楼栋机房ID",
                                   help_text="A端排序规则：（1）不同楼宇：3.1--2.3--2.2--1.3--1.2--1.1--2.1--6.1--6.2--4.1--4.2--4.3--4.4.1--4.4.2--4.5.1--4.5.2--园内（指挥部/保安亭/变电站/足球场）--出局；"
                                             "（2）相同楼宇：底层机房号数小的为A端，高层机房号数大为Z端。", default=0)
    rack_num_A = models.CharField("A端业务设备位置", max_length=20, help_text="请填写具体机架号，如A02架", default='')
    device_name_A = models.CharField("A端业务设备/网元名称", max_length=20, help_text="如S9303交换机或核心交换机", default='')
    port_name_A = models.CharField("A端业务设备端口", max_length=20, help_text="如POS 1/1/0或交换机端口-1", default='')
    port_type_A = models.CharField("A端业务设备端口类型", max_length=10, choices=PORT_TYPE, default='single')

    department1_Z = models.CharField("Z端设备移动维护部门", help_text="如XX中心", max_length=20, default='')
    person1_Z = models.CharField("移动负责人", help_text='请填写姓名', max_length=10, default='')
    phone1_Z = models.CharField("移动负责人联系方式", help_text='请填写手机号', max_length=20, default='')
    department2_Z = models.CharField("Z端设备维护合作单位", help_text='如XX公司', max_length=20, default='')
    person2_Z = models.CharField("合作单位负责人", help_text='请填写姓名', max_length=10, default='')
    phone2_Z = models.CharField("合作单位联系方式", help_text='请填写手机号', max_length=20, default='')
    fk_rid_Z = models.IntegerField("Z端业务设备所在楼栋机房ID",
                                   help_text="A端排序规则：（1）不同楼宇：3.1--2.3--2.2--1.3--1.2--1.1--2.1--6.1--6.2--4.1--4.2--4.3--4.4.1--4.4.2--4.5.1--4.5.2--园内（指挥部/保安亭/变电站/足球场）--出局；"
                                             "（2）相同楼宇：底层机房号数小的为A端，高层机房号数大为Z端。", default=0)
    rack_num_Z = models.CharField("Z端业务设备位置", max_length=20, help_text="请填写具体机架号，如A02架", default='')
    device_name_Z = models.CharField("Z端业务设备/网元名称", max_length=20, help_text="如S9303交换机或核心交换机", default='')
    port_name_Z = models.CharField("Z端业务设备端口", max_length=20, help_text="如POS 1/1/0或交换机端口-1", default='')
    port_type_Z = models.CharField("Z端业务设备端口类型", max_length=10, choices=PORT_TYPE, default='单模')

    bandwidth = models.CharField("需求带宽", max_length=10, choices=BANDWIDTH_TYPE, default='155M')
    main_or_spare = models.CharField("链路主备关系", max_length=10, choices=MAIN_OR_SPARE_TYPE, default='主用')
    route_info = models.CharField("路由信息", max_length=108, default='')
    notes = models.TextField("备注", default='')

    def __str__(self):
        ticket_sn = TicketRecord.objects.filter(id=self.ticket_id).first().sn
        return ticket_sn + ': ' + str(self.field_num) + '-' + self.bus_sys_name

    class Meta:
        verbose_name = "工单明细表"
        verbose_name_plural = "工单明细表"
