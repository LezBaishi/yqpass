from django.db import models

__author__ = 'mc'


# Create your models here.
class BuildingInfo(models.Model):
    """
    楼栋信息表
    """
    building = models.CharField("楼栋", max_length=50)

    creator = models.CharField('创建人', max_length=50, default='admin')
    gmt_created = models.DateTimeField('创建时间', auto_now_add=True)
    modifier = models.CharField('修改人', max_length=50, default='admin')
    gmt_modified = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField("已删除", default=False)

    def __str__(self):
        return self.building

    class Meta:
        verbose_name = "楼栋信息"
        verbose_name_plural = "楼栋信息"


class BuildingRoomInfo(models.Model):
    """
    楼栋机房信息表
    """
    building_info = models.ForeignKey('BuildingInfo', on_delete=models.CASCADE, related_name='BuildingRoomInfos',
                                      help_text='所在楼栋')
    room = models.CharField("机房号", max_length=50, help_text='F表示楼层，R表示弱电间，S表示南边，N表示北边，-1表示负一层')
    description = models.CharField("备注", max_length=100, help_text='有英文标注请详细说明')

    creator = models.CharField('创建人', max_length=50, default='admin')
    gmt_created = models.DateTimeField('创建时间', auto_now_add=True)
    modifier = models.CharField('修改人', max_length=50, default='admin')
    gmt_modified = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField("已删除", default=False)

    def __str__(self):
        building_name = self.building_info.building
        return building_name + '_' + self.room

    class Meta:
        verbose_name = "楼栋机房信息"
        verbose_name_plural = "楼栋机房信息"


class OcableSection(models.Model):
    """
    光缆段表
    """
    bri_A = models.ForeignKey('BuildingRoomInfo', on_delete=models.CASCADE, related_name='OcableSectionsA',
                              help_text='A端楼栋机房号，A端排序规则：（1）不同楼宇：3.1--2.3--2.2--1.3--1.2--1.1--2.1--6.1--6.2--4.1--4.2--4.3--4.4.1--4.4.2--4.5.1--4.5.2--园内（指挥部/保安亭/变电站/足球场）--出局；'
                                        + '（2）相同楼宇：底层机房号数小的为A端，高层机房号数大为Z端。F表示楼层，R表示弱电间，S表示南边，N表示北边，-1表示负一。')
    name_A = models.CharField('A端名称', max_length=50, unique=True,
                              help_text='命名格式参考：3.1栋101数据机房路由1-1或1.1栋1楼南塔弱电间')
    bri_Z = models.ForeignKey('BuildingRoomInfo', on_delete=models.CASCADE, related_name='OcableSectionsZ',
                              help_text='Z端楼栋机房号，A端排序规则：（1）不同楼宇：3.1--2.3--2.2--1.3--1.2--1.1--2.1--6.1--6.2--4.1--4.2--4.3--4.4.1--4.4.2--4.5.1--4.5.2--园内（指挥部/保安亭/变电站/足球场）--出局；'
                                        + '（2）相同楼宇：底层机房号数小的为A端，高层机房号数大为Z端。F表示楼层，R表示弱电间，S表示南边，N表示北边，-1表示负一。')
    name_Z = models.CharField('Z端名称', max_length=50, unique=True,
                              help_text='命名格式参考：3.1栋101数据机房路由1-1或1.1栋1楼南塔弱电间')
    ocable_name = models.CharField('光缆段名称', max_length=100)
    core_num = models.PositiveSmallIntegerField('纤芯数')
    ocable_length = models.DecimalField('光缆长度（皮长公里）', max_digits=5, decimal_places=2)

    SINGLE_MODE = '单模'
    MULTIMODE = '多模'
    OCABLE_TYPE_CHOICES = (
        (SINGLE_MODE, '单模'),
        (MULTIMODE, '多模'),
    )
    ocable_type = models.CharField('光缆类型', max_length=10, choices=OCABLE_TYPE_CHOICES, default=SINGLE_MODE)

    GANXIAN = '干线'
    BENDIWANG = '广州本地网'
    YUANQU = '南方基地园区'
    YUANQU2 = '南方基地园区（CMNET网络成端）'
    OCABLE_LEVEL_CHOICES = (
        (GANXIAN, '干线'),
        (BENDIWANG, '广州本地网'),
        (YUANQU, '南方基地园区'),
        (YUANQU2, '南方基地园区（CMNET网络成端）'),
    )
    ocable_level = models.CharField('光缆等级', max_length=20, choices=OCABLE_LEVEL_CHOICES)

    OFIBER_TYPE1 = 'G652'
    OFIBER_TYPE2 = 'G655'
    OFIBER_TYPE_CHOICES = (
        (OFIBER_TYPE1, 'G652'),
        (OFIBER_TYPE2, 'G655'),
    )
    ofiber_type = models.CharField('光纤型号', max_length=10, choices=OFIBER_TYPE_CHOICES)
    notes = models.TextField('备注', null=True, blank=True)

    creator = models.CharField('创建人', max_length=50, default='admin')
    gmt_created = models.DateTimeField('创建时间', auto_now_add=True)
    modifier = models.CharField('修改人', max_length=50, default='admin')
    gmt_modified = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField("已删除", default=False)

    def __str__(self):
        return self.ocable_name

    class Meta:
        verbose_name = "光缆段"
        verbose_name_plural = "光缆段"


class OfiberCore(models.Model):
    """
    纤芯表
    """
    core_no = models.PositiveSmallIntegerField('纤芯序号', help_text='在该光缆段中的纤芯序号')
    ocable_section = models.ForeignKey('OcableSection', on_delete=models.CASCADE, related_name='OfiberCores',
                                       help_text='对应光缆段名称')
    ocable_odf_A = models.CharField('A端光缆ODF', max_length=50,
                                    help_text='命名格式参考：1.1栋负1楼ODF01-1-A1或3.1栋103机房G101-1-A1')
    ocable_odf_Z = models.CharField('Z端光缆ODF', max_length=50,
                                    help_text='命名格式参考：1.1栋负1楼ODF01-1-A1或3.1栋103机房G101-1-A1')
    ocable_cor = models.CharField('光缆对应', max_length=100)
    core_quality = models.CharField('纤芯质量', max_length=50, null=True, blank=True)
    notes = models.TextField('备注', null=True, blank=True)

    creator = models.CharField('创建人', max_length=50, default='admin')
    gmt_created = models.DateTimeField('创建时间', auto_now_add=True)
    modifier = models.CharField('修改人', max_length=50, default='admin')
    gmt_modified = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField("已删除", default=False)

    def __str__(self):
        return self.ocable_cor

    class Meta:
        verbose_name = "纤芯"
        verbose_name_plural = "纤芯"


class RouteInfo(models.Model):
    """
    路由信息表
    根据两端业务设备信息生成电路路由-纤芯表关系
    """
    circuit_num = models.CharField('电路编号', max_length=10, help_text='命名格式：F+四位数字')
    ofiber_core = models.ForeignKey('OfiberCore', on_delete=models.CASCADE, related_name='oc_routeinfos',
                                    help_text='对应光缆纤芯')
    application_detail = models.ForeignKey('fielddiy.ApplicationDetail', on_delete=models.CASCADE,
                                           related_name='ad_routeinfos', help_text='工单明细')

    ONE = 'first'
    TWO = 'second'
    ROUTE_NO_CHOICES = (
        (ONE, '1'),
        (TWO, '2'),
    )
    route_no = models.CharField('路由序号(1或2)', max_length=10, choices=ROUTE_NO_CHOICES)

    route_where = models.PositiveSmallIntegerField('路由位置')

    ON = '在用'
    OFF = '停闭'
    STATE_CHOICES = (
        (ON, '在用'),
        (OFF, '停闭'),
    )
    state = models.CharField('状态', max_length=10, choices=STATE_CHOICES, default=ON)

    creator = models.CharField('创建人', max_length=50, default='admin')
    gmt_created = models.DateTimeField('创建时间', auto_now_add=True)
    modifier = models.CharField('修改人', max_length=50, default='admin')
    gmt_modified = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField("已删除", default=False)

    def __str__(self):
        return self.circuit_num + '-' + str(self.ofiber_core)

    class Meta:
        verbose_name = "路由信息"
        verbose_name_plural = "路由信息"
