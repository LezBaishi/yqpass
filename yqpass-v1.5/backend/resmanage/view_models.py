from backend.resmanage.models import *

__author__ = 'mc'

class ViewOcableSection(models.Model):
    """
    光缆段视图
    """
    building_A = models.CharField(max_length=50)
    room_A = models.CharField(max_length=50)
    name_A = models.CharField(max_length=50)
    building_Z = models.CharField(max_length=50)
    room_Z = models.CharField(max_length=50)
    name_Z = models.CharField(max_length=50)
    ocable_name = models.CharField(max_length=100)
    core_num = models.CharField(max_length=50)
    used_core_num = models.CharField(max_length=50)
    core_occ = models.CharField(max_length=50)
    unused_core_num = models.CharField(max_length=50)
    ocable_length = models.CharField(max_length=50)
    core_kilo = models.CharField(max_length=50)
    used_core_kilo = models.CharField(max_length=50)
    core_usage = models.CharField(max_length=50)
    ocable_type = models.CharField(max_length=50)
    ocable_level = models.CharField(max_length=50)
    ofiber_type = models.CharField(max_length=50)
    notes = models.TextField()
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'resmanage_view_ocablesection'


class ViewOfiberCore(models.Model):
    """
    纤芯视图
    """
    ocable_section_id = models.IntegerField()
    core_no = models.IntegerField()
    ocable_odf_A = models.CharField(max_length=50)
    switch_dport_A = models.CharField(max_length=50)
    ocable_cor = models.CharField(max_length=100)
    ocable_odf_Z = models.CharField(max_length=50)
    switch_dport_Z = models.CharField(max_length=50)
    core_quality = models.CharField(max_length=50)
    circuit_num = models.CharField(max_length=50)
    occ_business = models.CharField(max_length=128)
    sn = models.CharField(max_length=25)
    notes = models.TextField()
    is_deleted_of_oc = models.BooleanField(default=False)
    is_deleted_of_os = models.BooleanField(default=False)

    class Meta:
        db_table = 'resmanage_view_ofibercore'

class ViewUsingCircuit(models.Model):
    """
    在用电路视图
    """
    project_name = models.CharField(max_length=128)
    name_A = models.CharField(max_length=100)
    name_Z = models.CharField(max_length=100)
    circuit_num = models.CharField(max_length=10)
    state = models.CharField(max_length=10)
    sn = models.CharField(max_length=20)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'resmanage_view_usingcircuit'