#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-11 16:44:21
import datetime
import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import IntegrityError
from django.db.models import Q

from backend.fielddiy.models import ApplicationDetail
from backend.resmanage.models import BuildingInfo, BuildingRoomInfo, OcableSection, OfiberCore, RouteInfo
from backend.resmanage.view_models import ViewOcableSection, ViewOfiberCore
from backend.ticket.models import TicketRecord

from service.common.base_services import BaseService
from service.common.constant_service import CONSTANT_SERVICE
from service.common.log_service import auto_log
from service.resmanage.orm_tools import OrmToolsService

__author__ = 'mc'


class BuildingBaseService(BaseService):
    """
    楼栋信息的基础服务
    """

    def __init__(self):
        pass

    @classmethod
    @auto_log
    def get_building_list(cls, building='', reverse=1, per_page=10, page=1):
        """
        获取楼栋信息列表
        :param building: 楼栋号
        :param reverse: 按照ID倒序（False:0和True:1）,默认1
        :param per_page: 每页显示个数，默认10
        :param page: 页码，默认1
        :return:
        """
        query_params = Q(is_deleted=0)
        if building:
            query_params &= Q(building=building)
        if reverse:
            order_by_str = '-id'
        else:
            order_by_str = 'id'

        building_objects = BuildingInfo.objects.filter(query_params).order_by(order_by_str)
        paginator = Paginator(building_objects, per_page)
        try:
            building_result_paginator = paginator.page(page)
        except PageNotAnInteger:
            building_result_paginator = paginator.page(1)
        except EmptyPage:
            building_result_paginator = paginator.page(paginator.num_pages)

        # 分页后要显示的楼栋信息列表
        building_result_object_list = building_result_paginator.object_list
        building_result_restful_list = []

        for building_result_object in building_result_object_list:
            building_result_restful_list.append(dict(id=building_result_object.id,
                                                     building=building_result_object.building)
                                                )
        return building_result_restful_list, dict(per_page=per_page, page=page, total=paginator.count)


class BuildingRoomBaseService(BaseService):
    """
    楼栋机房信息的基础服务
    """

    def __init__(self):
        pass

    @classmethod
    @auto_log
    def get_building_room_list(cls, building='', room='', description='', room_id=0,
                               reverse=1, per_page=10, page=1):
        """
        获取楼栋机房信息列表
        :param building: 楼栋号
        :param room: 机房号
        :param reverse: 按照ID倒序（False:0和True:1）,默认1
        :param per_page: 每页显示个数，默认10
        :param page: 页码，默认1
        :return:
        """
        query_params = Q(is_deleted=0)
        if room_id:
            query_params &= Q(id=room_id)
        if building:
            # building_info_id = BuildingInfo.objects.filter(building=building).first().id
            building_info = BuildingInfo.objects.filter(building=building).first()
            if building_info:
                query_params &= Q(building_info_id=building_info.id)
        if room:
            query_params &= Q(room=room)
        if description:
            query_params &= Q(description__contains=description)
        if reverse:
            order_by_str = '-id'
        else:
            order_by_str = 'id'

        building_room_objects = BuildingRoomInfo.objects.filter(query_params).order_by(order_by_str)
        paginator = Paginator(building_room_objects, per_page)
        try:
            building_room_result_paginator = paginator.page(page)
        except PageNotAnInteger:
            building_room_result_paginator = paginator.page(1)
        except EmptyPage:
            building_room_result_paginator = paginator.page(paginator.num_pages)

        # 分页后要显示的楼栋机房信息列表
        building_room_result_object_list = building_room_result_paginator.object_list
        building_room_result_restful_list = []

        for building_room_result_object in building_room_result_object_list:
            # building_id = building_room_result_object.building_info_id
            # building = BuildingInfo.objects.filter(id=building_id).first().building
            building_name, msg = OrmToolsService.get_building_by_room_id(building_room_result_object.id)
            building_room_result_restful_list.append(dict(id=building_room_result_object.id,
                                                          building=building_name,
                                                          room=building_room_result_object.room,
                                                          description=building_room_result_object.description)
                                                     )
        return building_room_result_restful_list, dict(per_page=per_page, page=page, total=paginator.count)


class OcableSectionBaseService(BaseService):
    """
    光缆段的基础服务
    """

    def __init__(self):
        pass

    @classmethod
    @auto_log
    def get_ocable_section_list(cls, building='', room='', ocable_name='',
                                reverse=1, per_page=10, page=1):
        """
        获取光缆段（视图）列表
        :param building: 端点楼栋
        :param room: 端点机房号
        :param ocable_name: 光缆名称
        :param reverse: 按照光缆段ID倒序（False:0和True:1）,默认1
        :param per_page: 每页显示个数，默认10
        :param page: 页码，默认1
        :return:
        """
        query_params = Q(is_deleted=0)
        if building:
            query_params &= (Q(building_A__contains=building) | Q(building_Z__contains=building))
        if room:
            query_params &= (Q(room_A__contains=room.upper()) | Q(room_Z__contains=room.upper()))
        # if building_A:
        #     query_params &= Q(building_A__contains=building_A)
        # if room_A:
        #     query_params &= Q(room_A__contains=room_A)
        # if building_Z:
        #     query_params &= Q(building_Z__contains=building_Z)
        # if room_Z:
        #     query_params &= Q(room_Z__contains=room_Z)
        if ocable_name:
            query_params &= Q(ocable_name__contains=ocable_name)
        if reverse:
            order_by_str = '-id'
        else:
            order_by_str = 'id'

        ocable_section_objects = ViewOcableSection.objects.filter(query_params).order_by(order_by_str)
        paginator = Paginator(ocable_section_objects, per_page)
        try:
            ocable_section_result_paginator = paginator.page(page)
        except PageNotAnInteger:
            ocable_section_result_paginator = paginator.page(1)
        except EmptyPage:
            ocable_section_result_paginator = paginator.page(paginator.num_pages)

        # 分页后要显示的光缆段列表
        ocable_section_result_object_list = ocable_section_result_paginator.object_list
        ocable_section_result_restful_list = []

        for ocable_section_result_object in ocable_section_result_object_list:
            ocable_section_result_restful_list.append(dict(id=ocable_section_result_object.id,
                                                           building_A=ocable_section_result_object.building_A,
                                                           room_A=ocable_section_result_object.room_A,
                                                           name_A=ocable_section_result_object.name_A,
                                                           building_Z=ocable_section_result_object.building_Z,
                                                           room_Z=ocable_section_result_object.room_Z,
                                                           name_Z=ocable_section_result_object.name_Z,
                                                           ocable_name=ocable_section_result_object.ocable_name,
                                                           core_num=ocable_section_result_object.core_num,
                                                           used_core_num=str(
                                                               ocable_section_result_object.used_core_num),
                                                           core_occ=_decimal2percentage(
                                                               ocable_section_result_object.core_occ),
                                                           unused_core_num=str(
                                                               ocable_section_result_object.unused_core_num),
                                                           ocable_length=str(
                                                               ocable_section_result_object.ocable_length),
                                                           core_kilo=str(ocable_section_result_object.core_kilo),
                                                           used_core_kilo=str(
                                                               ocable_section_result_object.used_core_kilo),
                                                           core_usage=_decimal2percentage(
                                                               ocable_section_result_object.core_usage),
                                                           ocable_type=ocable_section_result_object.ocable_type,
                                                           ocable_level=ocable_section_result_object.ocable_level,
                                                           ofiber_type=ocable_section_result_object.ofiber_type,
                                                           notes=ocable_section_result_object.notes)
                                                      )
        return ocable_section_result_restful_list, dict(per_page=per_page, page=page, total=paginator.count)

    @classmethod
    @auto_log
    def get_ocable_section_detail(cls, username, ocable_id):
        """
        光缆段详情
        :param username:
        :param ocable_id:
        :return:
        """
        ocable_view_obj = ViewOcableSection.objects.filter(id=ocable_id, is_deleted=0).first()
        if not ocable_view_obj:
            return False, "无相应光缆段信息"
        ocable_restful_dict = dict(id=ocable_view_obj.id,
                                   building_A=ocable_view_obj.building_A,
                                   room_A=ocable_view_obj.room_A,
                                   name_A=ocable_view_obj.name_A,
                                   building_Z=ocable_view_obj.building_Z,
                                   room_Z=ocable_view_obj.room_Z,
                                   name_Z=ocable_view_obj.name_Z,
                                   ocable_name=ocable_view_obj.ocable_name,
                                   core_num=ocable_view_obj.core_num,
                                   used_core_num=str(
                                       ocable_view_obj.used_core_num),
                                   core_occ=_decimal2percentage(
                                       ocable_view_obj.core_occ),
                                   unused_core_num=str(
                                       ocable_view_obj.unused_core_num),
                                   ocable_length=str(
                                       ocable_view_obj.ocable_length),
                                   core_kilo=str(ocable_view_obj.core_kilo),
                                   used_core_kilo=str(
                                       ocable_view_obj.used_core_kilo),
                                   core_usage=_decimal2percentage(
                                       ocable_view_obj.core_usage),
                                   ocable_type=ocable_view_obj.ocable_type,
                                   ocable_level=ocable_view_obj.ocable_level,
                                   ofiber_type=ocable_view_obj.ofiber_type,
                                   notes=ocable_view_obj.notes)
        return ocable_restful_dict, ''

    @classmethod
    @auto_log
    def new_ocable_section(cls, request_data_dict):
        """
        新建光缆段
        :param request_data_dict:
        :return:
        """
        # bri_a_id = request_data_dict.setdefault('bri_A_id', 0)
        name_a = request_data_dict.setdefault('name_A', '')
        # bri_z_id = request_data_dict.setdefault('bri_Z_id', 0)
        name_z = request_data_dict.setdefault('name_Z', '')
        ocable_name = '{}-{}'.format(name_a, name_z)
        core_num = request_data_dict.setdefault('core_num', 0)
        ocable_length = request_data_dict.setdefault('ocable_length', 0.0)
        ocable_type = request_data_dict.setdefault('ocable_type', '')
        ocable_level = request_data_dict.setdefault('ocable_level', '')
        ofiber_type = request_data_dict.setdefault('ofiber_type', '')
        notes = request_data_dict.setdefault('notes', '')
        building_a = request_data_dict.setdefault('building_A', '')
        building_z = request_data_dict.setdefault('building_Z', '')
        room_a = request_data_dict.setdefault('room_A', '')
        room_z = request_data_dict.setdefault('room_Z', '')

        missing_params = []
        for data in request_data_dict:
            if not (request_data_dict[data] or data == 'notes'):
                missing_params.append(data)
        if missing_params:
            return False, "缺少参数：" + ','.join(missing_params)

        bri_a_obj, msg = cls.get_building_room_by_brinfo(building_a, room_a)
        bri_z_obj, msg = cls.get_building_room_by_brinfo(building_z, room_z)

        if not (bri_a_obj and bri_z_obj):
            return False, msg
        if not (ocable_type in CONSTANT_SERVICE.OCABLE_TYPE and
                ocable_level in CONSTANT_SERVICE.OCABLE_LEVEL and
                ofiber_type in CONSTANT_SERVICE.OFIBER_TYPE):
            return False, "光缆类型、等级或光纤型号有误"

        # 检查是否有已删除的电缆，name_A和name_Z与新建的电缆冲突
        params = Q(is_deleted=True) & (Q(name_A=name_a) | Q(name_Z=name_z))
        bool_ocable = OcableSection.objects.filter(params)
        if bool_ocable:
            for ocable in bool_ocable:
                ocable.delete()

        try:
            new_ocable_section = OcableSection(bri_A=bri_a_obj,
                                               name_A=name_a,
                                               bri_Z=bri_z_obj,
                                               name_Z=name_z,
                                               ocable_name=ocable_name,
                                               core_num=core_num,
                                               ocable_length=ocable_length,
                                               ocable_type=ocable_type,
                                               ocable_level=ocable_level,
                                               ofiber_type=ofiber_type,
                                               notes=notes,
                                               creator=request_data_dict.get('username', 'admin'))
            new_ocable_section.save()
        except IntegrityError as error:
            if "key 'name_A'" in str(error):
                return False, "A端名称已存在"
            elif "key 'name_Z" in str(error):
                return False, "Z端名称已存在"
            else:
                return False, str(error)
        return dict(ocable_section_id=new_ocable_section.id), ''

    @classmethod
    @auto_log
    def change_ocable_section(cls, pk, request_data_dict):
        # bri_a_id = request_data_dict.get('bri_A_id', 0)
        name_a = request_data_dict.get('name_A', '')
        # bri_z_id = request_data_dict.get('bri_Z_id', 0)
        name_z = request_data_dict.get('name_Z', '')
        ocable_name = '{}-{}'.format(name_a, name_z)
        core_num = request_data_dict.get('core_num', 0)
        ocable_length = request_data_dict.get('ocable_length', 0.0)
        ocable_type = request_data_dict.get('ocable_type', '')
        ocable_level = request_data_dict.get('ocable_level', '')
        ofiber_type = request_data_dict.get('ofiber_type', '')
        notes = request_data_dict.get('notes', '')
        building_a = request_data_dict.setdefault('building_A', '')
        building_z = request_data_dict.setdefault('building_Z', '')
        room_a = request_data_dict.setdefault('room_A', '')
        room_z = request_data_dict.setdefault('room_Z', '')

        missing_params = []
        for data in request_data_dict:
            if not (request_data_dict[data] or data == 'notes'):
                missing_params.append(data)
        if missing_params:
            return False, "缺少参数：" + ','.join(missing_params)

        bri_a_obj, msg = cls.get_building_room_by_brinfo(building_a, room_a)
        bri_z_obj, msg = cls.get_building_room_by_brinfo(building_z, room_z)

        if not (bri_a_obj and bri_z_obj):
            return False, msg
        if not (ocable_type in CONSTANT_SERVICE.OCABLE_TYPE and
                ocable_level in CONSTANT_SERVICE.OCABLE_LEVEL and
                ofiber_type in CONSTANT_SERVICE.OFIBER_TYPE):
            return False, "光缆类型、等级或光纤型号有误"
        try:
            OcableSection.objects.filter(id=pk, is_deleted=0).update(
                bri_A=bri_a_obj,
                name_A=name_a,
                bri_Z=bri_z_obj,
                name_Z=name_z,
                ocable_name=ocable_name,
                core_num=core_num,
                ocable_length=ocable_length,
                ocable_type=ocable_type,
                ocable_level=ocable_level,
                ofiber_type=ofiber_type,
                notes=notes,
                modifier=request_data_dict.get(
                    'username', 'admin'))
        except IntegrityError as error:
            if "key 'name_A'" in str(error):
                return False, "A端名称已存在"
            elif "key 'name_Z" in str(error):
                return False, "Z端名称已存在"
            else:
                return False, str(error)

        return dict(ocable_section_id=pk), ''

    @classmethod
    @auto_log
    def delete_ocable_section(cls, username, delete_str):
        """
        删除光缆段信息
        :param username:
        :param delete_str:
        :return:
        """
        delete_list = [x for x in delete_str.strip().split(',') if x]
        ocable_sections = OcableSection.objects.filter(id__in=delete_list, is_deleted=0).all()
        if not ocable_sections:
            return False, "请提供有效的光缆段id"
        delete_info = []
        for ocable in ocable_sections:
            ocable.is_deleted = True
            ocable.save()
            if ocable.OfiberCores.all():
                ocable.OfiberCores.update(is_deleted=True)
            delete_info.append(str(ocable.id))
        return ','.join(delete_info), '删除光缆段成功'

    @classmethod
    def get_building_room_by_brinfo(cls, building, room):
        building_room_obj = BuildingRoomInfo.objects.filter(building_info__building=building,
                                                            room=room,
                                                            is_deleted=0).first()
        if not building_room_obj:
            return False, "无该楼栋机房信息"
        else:
            return building_room_obj, ''


class OfiberCoreBaseService(BaseService):
    """
    纤芯的基础服务
    """

    def __init__(self):
        pass

    @classmethod
    @auto_log
    def get_ofiber_core_list(cls, ocable_section_id='', ocable_odf='',
                             switch_dport='', ocable_cor='', core_quality='', circuit_num='',
                             occ_business='', sn='', building='', room='', reverse=1, per_page=10, page=1):
        """
        获取纤芯（视图）列表
        :param room: 机房信息
        :param building: 楼栋信息
        :param ocable_section_id: 光缆段ID
        :param ocable_odf: 光缆ODF
        :param switch_dport: 转接设备端口
        :param ocable_cor: 光缆对应
        :param core_quality: 纤芯质量 
        :param circuit_num: 电路编号
        :param occ_business: 占用业务
        :param sn: 施工单号
        :param reverse: 按照纤芯序号倒序（False:0和True:1），默认1
        :param per_page: 每页显示个数，默认10
        :param page: 页码，默认1
        :return:
        """
        query_params = Q(is_deleted_of_oc=0) & Q(is_deleted_of_os=0)
        if ocable_section_id:
            query_params &= Q(ocable_section_id=ocable_section_id)
        if ocable_odf:
            query_params &= Q(ocable_odf_A__contains=ocable_odf) | Q(ocable_odf_Z__contains=ocable_odf)
        if switch_dport:
            query_params &= Q(switch_dport_A__contains=switch_dport) | Q(switch_dport_Z__contains=switch_dport)
        # if ocable_odf_A:
        #     query_params &= Q(ocable_odf_A__contains=ocable_odf_A)
        # if switch_dport_A:
        #     query_params &= Q(switch_dport_A__contains=switch_dport_A)
        # if ocable_odf_Z:
        #     query_params &= Q(ocable_odf_Z__contains=ocable_odf_Z)
        # if switch_dport_Z:
        #     query_params &= Q(switch_dport_Z__contains=switch_dport_Z)
        if ocable_cor:
            query_params &= Q(ocable_cor__contains=ocable_cor)
        if core_quality:
            query_params &= Q(core_quality__contains=core_quality)
        if circuit_num:
            query_params &= Q(circuit_num__contains=circuit_num)
        if occ_business:
            query_params &= Q(occ_business__contains=occ_business)
        if sn:
            query_params &= Q(sn__contains=sn)

        if building:
            # building_info_id = BuildingInfo.objects.filter(building=building).first().id
            building_info = BuildingInfo.objects.filter(building=building, is_deleted=0).first()
            ocable_id_list = []
            if building_info:
                room_info = building_info.BuildingRoomInfos.all()
                if room_info:
                    for room_obj in room_info:
                        ocable_info = room_obj.OcableSectionsA.all() | room_obj.OcableSectionsZ.all()
                        ocable_id_list += [ocable.id for ocable in ocable_info if ocable]
            query_params &= Q(ocable_section_id__in=ocable_id_list)

        if room:
            room_info = BuildingRoomInfo.objects.filter(room=room, is_deleted=0)
            ocable_id_list = []
            if room_info:
                for room in room_info:
                    ocable_info = room.OcableSectionsA.all() | room.OcableSectionsZ.all()
                    ocable_id_list += [ocable.id for ocable in ocable_info if ocable]
            query_params &= Q(ocable_section_id__in=ocable_id_list)

        if reverse:
            order_by_str = '-core_no'
        else:
            order_by_str = 'core_no'

        ofiber_core_objects = ViewOfiberCore.objects.filter(query_params).order_by(order_by_str)
        paginator = Paginator(ofiber_core_objects, per_page)
        try:
            ofiber_core_result_paginator = paginator.page(page)
        except PageNotAnInteger:
            ofiber_core_result_paginator = paginator.page(1)
        except EmptyPage:
            ofiber_core_result_paginator = paginator.page(paginator.num_pages)

        # 分页后要显示的工单列表
        ofiber_core_result_object_list = ofiber_core_result_paginator.object_list
        ofiber_core_result_restful_list = []

        for ofiber_core_result_object in ofiber_core_result_object_list:
            ofiber_core_result_restful_list.append(dict(id=ofiber_core_result_object.id,
                                                        ocable_section_id=ofiber_core_result_object.ocable_section_id,
                                                        core_no=ofiber_core_result_object.core_no,
                                                        ocable_odf_A=ofiber_core_result_object.ocable_odf_A,
                                                        switch_dport_A=ofiber_core_result_object.switch_dport_A,
                                                        ocable_cor=ofiber_core_result_object.ocable_cor,
                                                        ocable_odf_Z=ofiber_core_result_object.ocable_odf_Z,
                                                        switch_dport_Z=ofiber_core_result_object.switch_dport_Z,
                                                        core_quality=ofiber_core_result_object.core_quality,
                                                        circuit_num=ofiber_core_result_object.circuit_num,
                                                        occ_business=ofiber_core_result_object.occ_business,
                                                        sn=ofiber_core_result_object.sn,
                                                        notes=ofiber_core_result_object.notes)
                                                   )

        return ofiber_core_result_restful_list, dict(per_page=per_page, page=page, total=paginator.count)

    @classmethod
    @auto_log
    def new_ofiber_core(cls, request_data_dict):
        # 两部分新建和修改都没有优化下代码，有点冗余，后续再处理。
        # core_no = request_data_dict.get('core_no', 0)
        ocable_section_id = request_data_dict.get('ocable_section_id', 0)
        ocable_odf_A = request_data_dict.get('ocable_odf_A', '')
        ocable_odf_Z = request_data_dict.get('ocable_odf_Z', '')
        core_quality = request_data_dict.get('core_quality', '')
        notes = request_data_dict.get('notes', '')
        username = request_data_dict.get('username', '')

        if not (ocable_odf_A and ocable_odf_Z and ocable_section_id):
            return False, "必须参数数据：ocable_section_id, ocable_odf_A, ocable_odf_Z"

        ocable_section_obj = OcableSection.objects.filter(id=ocable_section_id).first()
        if not ocable_section_obj:
            return False, "纤芯对应光缆段不存在。"

        # bool_ofiber = OfiberCore.objects.filter(ocable_section=ocable_section_obj, core_no=core_no).first()
        # if bool_ofiber:
        #     if bool_ofiber.is_deleted:
        #         bool_ofiber.delete()
        #     else:
        #         return False, "该纤芯段已存在，请核实后再添加。"
        bool_ofiber = OfiberCore.objects.filter(Q(ocable_section=ocable_section_obj) &
                                                (Q(ocable_odf_A__in=(ocable_odf_A, ocable_odf_Z)) |
                                                 Q(ocable_odf_Z__in=(ocable_odf_A, ocable_odf_Z))) &
                                                Q(is_deleted=0))
        conflict_ofiber = [str(ofiber.id) for ofiber in bool_ofiber if ofiber]
        if conflict_ofiber:
            return False, "该纤芯段ODF架与纤芯段：{}，冲突，请核实后再添加".format(','.join(conflict_ofiber))

        # 生成纤芯序号, 自增1, 如果存在某条纤芯被删除, 自动补上, 比如存在： 1, 2, 4, 5那么新增的序号将为3
        ofiber_objs = OfiberCore.objects.filter(ocable_section=ocable_section_obj, is_deleted=0).order_by('-core_no')
        core_no = 1
        if ofiber_objs:
            ofiber_core_nos = [ofiber.core_no for ofiber in ofiber_objs if ofiber]
            if len(ofiber_objs) < ofiber_core_nos[0]:
                for i in range(1, ofiber_core_nos[0]):
                    if i not in ofiber_core_nos:
                        core_no = i
                        break
            else:
                core_no = ofiber_core_nos[0] + 1
        # 光缆对应，不需填写，自动拼凑（光缆名称+纤芯数+'芯之'+纤芯序号）
        ocable_cor = '{}-{}芯之{}'.format(ocable_section_obj.ocable_name,
                                        str(ocable_section_obj.core_num),
                                        str(core_no))

        new_ofiber_core = OfiberCore(core_no=core_no,
                                     ocable_section=ocable_section_obj,
                                     ocable_odf_A=ocable_odf_A,
                                     ocable_odf_Z=ocable_odf_Z,
                                     ocable_cor=ocable_cor,
                                     core_quality=core_quality,
                                     notes=notes,
                                     creator=username)
        new_ofiber_core.save()
        return dict(ofiber_core_id=new_ofiber_core.id), '新建纤芯成功'

    @classmethod
    @auto_log
    def get_ofiber_core_detail(cls, username, pk):

        ofiber_core = ViewOfiberCore.objects.filter(id=pk).first()
        if not ofiber_core:
            return False, "查无相应纤芯端"
        ofiber_core_rest_result = dict(id=ofiber_core.id,
                                       ocable_section_id=ofiber_core.ocable_section_id,
                                       core_no=ofiber_core.core_no,
                                       ocable_odf_A=ofiber_core.ocable_odf_A,
                                       switch_dport_A=ofiber_core.switch_dport_A,
                                       ocable_cor=ofiber_core.ocable_cor,
                                       ocable_odf_Z=ofiber_core.ocable_odf_Z,
                                       switch_dport_Z=ofiber_core.switch_dport_Z,
                                       core_quality=ofiber_core.core_quality,
                                       circuit_num=ofiber_core.circuit_num,
                                       occ_business=ofiber_core.occ_business,
                                       sn=ofiber_core.sn,
                                       notes=ofiber_core.notes)
        return ofiber_core_rest_result, ''

    @classmethod
    @auto_log
    def change_ofiber_core(cls, pk, request_data_dict):
        # core_no = request_data_dict.get('core_no', 0)
        # ocable_section_id = request_data_dict.get('ocable_section_id', 0)
        ocable_odf_A = request_data_dict.get('ocable_odf_A', '')
        ocable_odf_Z = request_data_dict.get('ocable_odf_Z', '')
        core_quality = request_data_dict.get('core_quality', '')
        notes = request_data_dict.get('notes', '')
        username = request_data_dict.get('username', '')

        if not (ocable_odf_A and ocable_odf_Z):
            return False, "必须的参数数据：ocable_odf_A, ocable_odf_Z"

        # ocable_section_obj = OcableSection.objects.filter(id=ofiber_obj.ocable_section).first()
        # if not ocable_section_obj:
        #     return False, "纤芯对应光缆不存在"

        ofiber_obj = OfiberCore.objects.filter(id=pk).first()
        if ofiber_obj:
            if ofiber_obj.is_deleted:
                return False, "该纤芯不存在或已被删除"
        if (not ofiber_obj.ocable_section) or ofiber_obj.ocable_section.is_deleted:
            return False, "该纤芯对应光缆不存在"

        # 光缆对应，不需填写，自动拼凑（光缆名称+纤芯数+'芯之'+纤芯序号）
        ocable_cor = '{}-{}芯之{}'.format(ofiber_obj.ocable_section.ocable_name,
                                        str(ofiber_obj.ocable_section.core_num),
                                        str(ofiber_obj.core_no))

        OfiberCore.objects.filter(id=pk, is_deleted=0).update(
            # core_no=core_no,
            # ocable_section=ocable_section_obj,
            ocable_odf_A=ocable_odf_A,
            ocable_odf_Z=ocable_odf_Z,
            ocable_cor=ocable_cor,
            core_quality=core_quality,
            notes=notes,
            modifier=username
        )

        return dict(ofiber_core_id=pk), '编辑纤芯成功'

    @classmethod
    @auto_log
    def delete_ofiber_core(cls, username, delete_str):
        """
        删除纤芯段信息
        :param username:
        :param delete_str:
        :return:
        """
        delete_list = [x for x in delete_str.strip().split(',') if x]
        ofibers = OfiberCore.objects.filter(id__in=delete_list, is_deleted=0).all()
        if not ofibers:
            return False, "该纤芯段被删除或不存在"
        delete_info = []
        for ofiber in ofibers:
            ofiber.is_deleted = True
            ofiber.save()
            delete_info.append(str(ofiber.id))
        return ','.join(delete_info), "删除纤芯段成功"


class UsingCircuitBaseService(BaseService):
    """
    在用电路的基础服务
    """

    def __init__(self):
        pass

    @classmethod
    @auto_log
    def get_using_circuit_list(cls, project_name='', name_az='', circuit_num='', state='',
                               sn='', reverse=1, per_page=10, page=1):
        """
        获取在用电路列表
        :param project_name: 项目名称
        :param name_az: 在用电路端点名称
        :param circuit_num: 电路编号
        :param state: 状态(在用/停闭)
        :param sn: 施工单号
        :param reverse: 按照电路编号倒序（False:0和True:1），默认1
        :param per_page: 每页显示个数，默认10
        :param page: 页码，默认1
        :return:
        """

        app_detail_set = ApplicationDetail.objects.all()
        if not app_detail_set:
            return False, "没有在用电路"
        circuit_rest_list = []
        for app_detail in app_detail_set:
            # 找出各条在用电路的集合
            route_info_set = app_detail.ad_routeinfos.filter(is_deleted=0).all()
            if not route_info_set:
                continue
            # 每条电路包含两个路径
            circuit_one_set = route_info_set.filter(route_no='first').order_by('route_where')
            circuit_two_set = route_info_set.filter(route_no='second').order_by('route_where')
            circuit_one = [route_obj.ofiber_core for route_obj in circuit_one_set]
            format_circuit_one = [(ofiber.ocable_odf_A, ofiber.ocable_cor, ofiber.ocable_odf_Z) for
                                  ofiber in
                                  circuit_one]
            circuit_two = [route_obj.ofiber_core for route_obj in circuit_two_set]
            format_circuit_two = [(ofiber.ocable_odf_A, ofiber.ocable_cor, ofiber.ocable_odf_Z) for
                                  ofiber in
                                  circuit_two]
            ticket_obj = TicketRecord.objects.filter(id=app_detail.ticket_id, is_deleted=0).first()
            if not ticket_obj:
                continue

            build_room_a_obj = BuildingRoomInfo.objects.filter(id=app_detail.fk_rid_A, is_deleted=0).first()
            build_room_z_obj = BuildingRoomInfo.objects.filter(id=app_detail.fk_rid_Z, is_deleted=0).first()
            if not (build_room_a_obj and build_room_z_obj):
                continue

            if build_room_a_obj.id == circuit_one[0].ocable_section.bri_A_id:
                name_a = circuit_one[0].ocable_section.name_A
            else:
                name_a = circuit_one[0].ocable_section.name_Z
            if build_room_z_obj.id == circuit_one[-1].ocable_section.bri_A_id:
                name_z = circuit_one[-1].ocable_section.name_A
            else:
                name_z = circuit_one[-1].ocable_section.name_Z

            circuit_rest_list.append(dict(
                project_name=ticket_obj.title,
                name_A=name_a,
                name_Z=name_z,
                circuit_num=circuit_one_set.first().circuit_num,
                state=circuit_one_set.first().state,
                sn=ticket_obj.sn,
                route={'first': format_circuit_one,
                       'second': format_circuit_two},
            ))

        # 构造查询函数过滤电路
        query_dict = {'project_name': project_name,
                      'circuit_num': circuit_num,
                      'state': state,
                      'sn': sn}
        query_list = list(filter(lambda x: x[1] != '', query_dict.items()))
        circuit_rest_list = cls._recursion(query_list, circuit_rest_list)
        if name_az:
            circuit_rest_list = [circuit for circuit in circuit_rest_list if
                                 (name_az in circuit['name_A']) or (name_az in circuit['name_Z'])]

        circuit_rest_list = sorted(circuit_rest_list, key=lambda x: x['circuit_num'], reverse=bool(reverse))

        paginator = Paginator(circuit_rest_list, per_page)
        try:
            circuit_rest_paginator = paginator.page(page)
        except PageNotAnInteger:
            circuit_rest_paginator = paginator.page(1)
        except EmptyPage:
            circuit_rest_paginator = paginator.page(paginator.num_pages)

        circuit_final_rest_list = circuit_rest_paginator.object_list

        return circuit_final_rest_list, dict(per_page=per_page, page=page, total=paginator.count)

    @classmethod
    @auto_log
    def _recursion(cls, query_list, filter_list):
        """
        递归过滤
        :param query_list:
        :param filter_list:
        :return:
        """
        if not query_list:
            return filter_list
        else:
            circuit_list = []
            for circuit in filter_list:
                key_name = query_list[0][0]
                value_name = query_list[0][1]
                if str(circuit[key_name]).__contains__(str(value_name)):
                    circuit_list.append(circuit)
            return cls._recursion(query_list[1:], circuit_list)

    @classmethod
    @auto_log
    def delete_using_circuit(cls, username, delete_str):
        """
        停闭电路
        :param username:
        :param delete_str:
        :return:
        """
        delete_list = [x for x in delete_str.strip().split(',') if x]
        delete_circuit_info = RouteInfo.objects.filter(circuit_num__in=delete_list, is_deleted=0).all()
        delete_info = []
        for circuit_num in delete_list:
            route_info = delete_circuit_info.filter(circuit_num=circuit_num, is_deleted=0)
            if not route_info:
                continue
            route_info.update(state="停闭", is_deleted=True)
            delete_info.append(circuit_num)

        return ','.join(delete_info), "停闭电路成功"


def _decimal2percentage(num):
    """
    小数转换为百分比，并保留两位小数
    :param num:decimal
    :return:str
    """
    return "%.2f%%" % (num * 100)
