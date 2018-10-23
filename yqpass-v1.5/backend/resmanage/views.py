#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date: 2018/9/4 14:20
import json

from django.http import HttpResponse
from backend.resmanage.view_models import ViewOcableSection, ViewOfiberCore, ViewUsingCircuit
from django.core import serializers

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View

from service.common.format_response import api_response
from service.resmanage.base_service import BuildingBaseService, BuildingRoomBaseService, OcableSectionBaseService, \
    OfiberCoreBaseService, UsingCircuitBaseService

__author__ = 'mc'


# Create your views here.
def mysql_view_test(request):
    # temp = ViewOcableSection.objects.all()
    temp = ViewOfiberCore.objects.all()
    # tempa = ViewOcableSection.objects.values_list('name_A')
    data = serializers.serialize("json", temp)
    return HttpResponse(data)


class BuildingListView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """
        获取楼栋信息列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        building = request_data.get('building', '')
        reverse = int(request_data.get('reverse', 0))
        per_page = int(request_data.get('per_page', 10))
        page = int(request_data.get('page', 1))

        building_result_restful_list, msg = BuildingBaseService.get_building_list(building=building,
                                                                                  reverse=reverse,
                                                                                  per_page=per_page,
                                                                                  page=page)
        data = {}
        if building_result_restful_list is False:
            code, msg = 0, msg
        else:
            data = dict(value=building_result_restful_list,
                        per_page=msg['per_page'], page=msg['page'], total=msg['total'])
            code, msg = 1, ''
        return api_response(code, msg, data)


class BuildingRoomListView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """
        获取楼栋机房信息列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        building = request_data.get('building', '')
        room = request_data.get('room', '')
        description = request_data.get('description', '')
        room_id = int(request_data.get('room_id', 0))
        reverse = int(request_data.get('reverse', 0))
        per_page = int(request_data.get('per_page', 10))
        page = int(request_data.get('page', 1))

        building_room_result_restful_list, msg = BuildingRoomBaseService.get_building_room_list(
            building=building,
            room=room,
            room_id=room_id,
            description=description,
            reverse=reverse,
            per_page=per_page,
            page=page)
        data = {}
        if building_room_result_restful_list is False:
            code, msg = 0, msg
        else:
            data = dict(value=building_room_result_restful_list,
                        per_page=msg['per_page'], page=msg['page'], total=msg['total'])
            code, msg = 1, ''
        return api_response(code, msg, data)


class OcableSectionListView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """
        获取光缆段（视图）列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        username = request.user.username
        # building_A = request_data.get('building_A', '')
        # room_A = request_data.get('room_A', '')
        # building_Z = request_data.get('building_Z', '')
        # room_Z = request_data.get('room_Z', '')
        building = request_data.get('building', '')
        room = request_data.get('room', '')
        ocable_name = request_data.get('ocable_name', '')
        reverse = int(request_data.get('reverse', 0))
        per_page = int(request_data.get('per_page', 10))
        page = int(request_data.get('page', 1))

        ocable_section_result_restful_list, msg = OcableSectionBaseService.get_ocable_section_list(
            # building_A=building_A,
            # room_A=room_A,
            # building_Z=building_Z,
            # room_Z=room_Z,
            building=building,
            room=room,
            ocable_name=ocable_name,
            reverse=reverse,
            per_page=per_page,
            page=page)
        data = {}
        if ocable_section_result_restful_list is False:
            code, msg = 0, msg
        else:
            data = dict(value=ocable_section_result_restful_list,
                        per_page=msg['per_page'], page=msg['page'], total=msg['total'])
            code, msg = 1, ''
        return api_response(code, msg, data)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """
        新建光缆段
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data_dict = json.loads(request.body.decode('utf-8'))
        if not request_data_dict:
            return api_response(0, "post 参数为空", "")
        request_data_dict['username'] = request.user.username
        create_result, msg = OcableSectionBaseService.new_ocable_section(request_data_dict)
        if create_result is False:
            code, data = 0, ''
        else:
            code, data = 1, create_result
        return api_response(code, msg, data)


class OcableSectionDetailView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        request_data = request.GET
        username = request.user.username
        pk = kwargs.get('pk', 0)
        ocable_detail, msg = OcableSectionBaseService.get_ocable_section_detail(username, pk)
        if ocable_detail is False:
            code, data = 0, ''
        else:
            code, data = 1, ocable_detail
        return api_response(code, msg, data)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        request_data_dict = json.loads(request.body.decode('utf-8'))
        if not request_data_dict:
            return api_response(0, "post 参数为空", "")
        pk = kwargs.get('pk', 0)

        username = request.user.username
        request_data_dict['username'] = username
        ocable_result, msg = OcableSectionBaseService.change_ocable_section(pk, request_data_dict)
        if ocable_result is False:
            code, data = 0, ''
        else:
            code, data = 1, ocable_result
        return api_response(code, msg, data)


class OcableSectionDeleteView(View):

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """
        删除纤芯表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data_dict = json.loads(request.body.decode('utf-8'))
        username = request.user.username
        delete_str = request_data_dict.get('delete_str', '')

        delete_result, msg = OcableSectionBaseService.delete_ocable_section(username, delete_str)
        if delete_result is False:
            code, data = 0, ''
        else:
            code, data = 1, delete_result
        return api_response(code, msg, data)


class OfiberCoreListView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """
        获取纤芯（视图）列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        ocable_section_id = request_data.get('ocable_section_id', '')
        # ocable_odf_A = request_data.get('ocable_odf_A', '')
        # switch_dport_A = request_data.get('switch_dport_A', '')
        # ocable_odf_Z = request_data.get('ocable_odf_Z', '')
        # switch_dport_Z = request_data.get('switch_dport_Z', '')
        ocable_odf = request_data.get('ocable_odf', '')
        switch_dport = request_data.get('switch_dport', '')
        ocable_cor = request_data.get('ocable_cor', '')
        core_quality = request_data.get('core_quality', '')
        circuit_num = request_data.get('circuit_num', '')
        occ_business = request_data.get('occ_business', '')
        sn = request_data.get('sn', '')
        building = request_data.get('building', 0)
        room = request_data.get('room', 0)
        reverse = int(request_data.get('reverse', 0))
        per_page = int(request_data.get('per_page', 10))
        page = int(request_data.get('page', 1))

        ofiber_core_result_restful_list, msg = OfiberCoreBaseService.get_ofiber_core_list(
            ocable_section_id=ocable_section_id,
            ocable_odf=ocable_odf,
            switch_dport=switch_dport,
            ocable_cor=ocable_cor,
            core_quality=core_quality,
            circuit_num=circuit_num,
            occ_business=occ_business,
            sn=sn,
            building=building,
            room=room,
            reverse=reverse,
            per_page=per_page,
            page=page)
        data = {}
        if ofiber_core_result_restful_list is False:
            code, msg = 0, msg
        else:
            data = dict(value=ofiber_core_result_restful_list,
                        per_page=msg['per_page'], page=msg['page'], total=msg['total'])
            code, msg = 1, ''
        return api_response(code, msg, data)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """
        新增纤芯
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data_dict = json.loads(request.body.decode('utf-8'))
        username = request.user.username
        request_data_dict['username'] = username

        new_ofiber_core, msg = OfiberCoreBaseService.new_ofiber_core(request_data_dict)
        if new_ofiber_core is False:
            code, data = 0, ''
        else:
            code, data = 1, new_ofiber_core
        return api_response(code, msg, data)


class OfiberCoreDetailView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """
        获取纤芯电路详情
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        username = request.user.username
        pk = kwargs.get('pk', 0)
        ofiber_core, msg = OfiberCoreBaseService.get_ofiber_core_detail(username, pk)
        if ofiber_core is False:
            code, data = 0, ''
        else:
            code, data = 1, ofiber_core
        return api_response(code, msg, data)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """
        修改纤芯电路详情
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data_dict = json.loads(request.body.decode('utf-8'))
        pk = kwargs.get('pk', '')
        username = request.user.username
        request_data_dict['username'] = username

        change_ofiber_result, msg = OfiberCoreBaseService.change_ofiber_core(pk, request_data_dict)
        if change_ofiber_result is False:
            code, data = 0, ''
        else:
            code, data = 1, change_ofiber_result
        return api_response(code, msg, data)


class OfiberCoreDeleteView(View):

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """
        删除纤芯表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data_dict = json.loads(request.body.decode('utf-8'))
        username = request.user.username
        delete_str = request_data_dict.get('delete_str', '')
        delete_ofiber_result, msg = OfiberCoreBaseService.delete_ofiber_core(username, delete_str)
        if delete_ofiber_result is False:
            code, data = 0, ''
        else:
            code, data = 1, delete_ofiber_result
        return api_response(code, msg, data)


class UsingCircuitListView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """
        获取在用电路列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET

        request_params = dict(project_name=request_data.get('project_name', ''),
                              name_az=request_data.get('name_az', ''),
                              # name_Z=request_data.get('name_Z', ''),
                              circuit_num=request_data.get('circuit_num', ''),
                              state=request_data.get('state', ''),
                              sn=request_data.get('sn', ''),
                              reverse=int(request_data.get('reverse', 1)),
                              per_page=int(request_data.get('per_page', 10)),
                              page=int(request_data.get('page', 1)))

        using_circuit_result_restful_list, msg = UsingCircuitBaseService.get_using_circuit_list(**request_params)
        if using_circuit_result_restful_list is False:
            code, data = 0, ''
        else:
            data = dict(value=using_circuit_result_restful_list,
                        per_page=msg['per_page'], page=msg['page'], total=msg['total'])
            code, msg = 1, ''
        return api_response(code, msg, data)


class UsingCircuitDeleteView(View):

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """
        停闭电路
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data_dict = json.loads(request.body.decode('utf-8'))
        username = request.user.username
        delete_str = request_data_dict.get('delete_str', '')
        delete_ofiber_result, msg = UsingCircuitBaseService.delete_using_circuit(username, delete_str)
        if delete_ofiber_result is False:
            code, data = 0, ''
        else:
            code, data = 1, delete_ofiber_result
        return api_response(code, msg, data)
