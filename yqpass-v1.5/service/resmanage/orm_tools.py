#!usr/bin/env python  
# -*- coding:utf-8 _*-  
""" 
@author: x-zj
@file: orm_tools.py 
@version:
@time: 2018/10/15 11:49
"""
from backend.fielddiy.models import ApplicationDetail
from backend.resmanage.models import BuildingInfo, BuildingRoomInfo
from service.common.base_services import BaseService
from service.common.log_service import auto_log


class OrmToolsService(BaseService):
    """
    常用查询函数
    """

    def __init__(self):
        pass

    @classmethod
    @auto_log
    def get_building_by_room_id(cls, room_id):
        """
        获取楼栋信息
        :param room_id:
        :return:
        """
        room_info = BuildingRoomInfo.objects.filter(id=room_id).first()
        if not room_info:
            return '', "该机房无记录"
        building_name = room_info.building_info.building
        return building_name, ''

    @classmethod
    @auto_log
    def get_route_info_by_detail_id(cls, application_detail_id):
        """
        获取每条线路的路由信息
        :param application_detail_id:
        :return:
        """
        app_detail_obj = ApplicationDetail.objects.filter(id=application_detail_id).first()
        if not app_detail_obj:
            return '', '该明细表无对应路由信息'
        route_info = app_detail_obj.ad_routeinfos.all()
        return route_info, ''
