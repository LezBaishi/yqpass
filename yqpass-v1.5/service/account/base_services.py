#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date: 2018/6/1 11:11
import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from backend.account.models import User, Department, Role, UserRole
from service.common.base_services import BaseService
from service.common.format_response import DateEncoder
from service.common.log_service import auto_log

__author__ = 'x-zj'


class AccountBaseService(BaseService):
    """
    账户各种操作
    """

    @classmethod
    @auto_log
    def get_user_by_username(cls, username):
        """
        获取用户信息
        :param username:
        :return:
        """
        result = User.objects.filter(username=username, is_deleted=0).first()
        if result:
            return result, ''
        else:
            return False, "account:base_service: 用户名对应用户不存在"

    @classmethod
    @auto_log
    def get_user_role_id_list(cls, username):
        """
        获取用户角色id list
        :param username:
        :return:
        """
        user_obj = User.objects.filter(username=username, is_deleted=0).first()
        if not user_obj:
            return False, "account:base_service: 获取用户角色id列表时用户信息不存在"

        user_role_queryset = UserRole.objects.filter(user_id=user_obj.id,
                                                     is_deleted=0).all()
        user_role_id_list = [user_role.role_id for user_role in user_role_queryset]
        return user_role_id_list, ''

    @classmethod
    @auto_log
    def get_user_dept_id_list(cls, username):
        """
        获取用户的部门id list, 包括上级部门id
        :param username:
        :return:
        """
        dept_id_list = []
        user_obj = User.objects.filter(username=username, is_deleted=0).first()
        if not user_obj:
            return False, "account:base_service: 获取部门id列表时用户信息不存在"

        def iter_dept(dept_id):
            """
            迭代获取
            """
            dept_obj = Department.objects.filter(id=dept_id, is_deleted=0).first()
            if dept_obj:
                dept_id_list.append(dept_obj.id)
                if dept_obj.parent_dept_id:
                    iter_dept(dept_obj.parent_dept_id)

        iter_dept(user_obj.dept_id)
        return dept_id_list, ''

    @classmethod
    @auto_log
    def get_user_dept_approver(cls, username):
        """
        获取用户所在部门的审批人，优先获取审批人，如果没有则取leader
        :param username:
        :return:
        """
        user_obj = User.objects.filter(username=username, is_deleted=0).first()
        dept_obj = Department.objects.filter(id=user_obj.dept_id).first()
        if dept_obj.approver:
            return dept_obj.approver, ''
        elif dept_obj.leader:
            return dept_obj.leader, ''
        else:
            return False, "account:base_service: 刚用户对应部门没有审批人和领导 "

    @classmethod
    @auto_log
    def get_dept_sub_id_list(cls, dept_id):
        """
        获取部门所有子部门
        :param dept_id:
        :return:
        """
        dept_id_list = []
        dept_obj = Department.objects.filter(id=dept_id, is_deleted=0).first()
        if dept_obj:
            dept_id_list.append(dept_obj.id)
        else:
            return [], ''

        def iter_dept_id_list(_dept_id):
            _dept_obj = Department.objects.filter(id=_dept_id, is_deleted=0).first()
            if _dept_obj:
                sub_dept_queryset = Department.objects.filter(parent_dept_id=_dept_obj.id, is_deleted=0).all()
                for sub_dept in sub_dept_queryset:
                    if sub_dept:
                        dept_id_list.append(sub_dept.id)
                        iter_dept_id_list(sub_dept.id)

        iter_dept_id_list(dept_id)
        return dept_id_list, ''

    @classmethod
    @auto_log
    def get_dept_username_list(cls, dept_id):
        """
        获取部门下属用户的username_list
        :param dept_id:
        :return:
        """
        sub_dept_id_list, msg = cls.get_dept_sub_id_list(dept_id)
        user_name_list = []
        if sub_dept_id_list:
            user_queryset = User.objects.filter(dept_id__in=sub_dept_id_list).all()
            for user in user_queryset:
                user_name_list.append(user.username)
        return user_name_list, ''

    @classmethod
    @auto_log
    def get_role_username_list(cls, role_id):
        """
        获取角色对应的username_list
        :param role_id:
        :return:
        """
        user_role_queryset = UserRole.objects.filter(role_id=role_id).all()
        user_id_list = []
        for user_role in user_role_queryset:
            user_id_list.append(user_role.user_id)
        if not user_id_list:
            return [], ''
        username_queryset = User.objects.filter(id__in=user_id_list).all()
        username_list = []
        for user in username_queryset:
            username_list.append(user.username)
        return username_list, ''

    @classmethod
    @auto_log
    def get_dept_by_id(cls, dept_id):
        """
        获取部门信息
        :param dept_id:
        :return:
        """
        return Department.objects.filter(id=dept_id, is_deleted=False).first(), ''

    @classmethod
    @auto_log
    def get_role_by_id(cls, role_id):
        """
        获取角色信息
        :param role_id:
        :return:
        """
        return Role.objects.filter(id=role_id, is_deleted=False).first(), ''

    @classmethod
    @auto_log
    def get_user_list(cls, username='', email='', alias='',
                      per_page=10, page=1, category=''):
        """
        获取用户列表
        :param username:
        :param email:
        :param alias:
        :param per_page:
        :param page:
        :param category:
        :return:
        """

        category_tuple = ('all', 'general', 'admin', 'viewer')
        if category not in category_tuple:
            return False, "查询类别错误, 请重新选择"

        query_params = Q(is_deleted=0)
        if username:
            query_params &= Q(username__contains=username)
        if email:
            query_params &= Q(email__contains=email)
        if alias:
            query_params &= Q(alias__contains=alias)

        if category == 'general':
            query_params &= Q(is_admin=False)
            account_objects = User.objects.filter(query_params).order_by('-gmt_created')

        elif category == 'admin':
            query_params &= Q(is_admin=True)
            account_objects = User.objects.filter(query_params).order_by('-gmt_created')

        elif category == 'viewer':
            query_params &= Q(is_viewer=True)
            account_objects = User.objects.filter(query_params).order_by('-gmt_created')

        else:
            account_objects = User.objects.filter(query_params).order_by('-gmt_created')

        paginator = Paginator(account_objects, per_page)
        try:
            account_restful_paginator = paginator.page(page)
        except PageNotAnInteger:
            account_restful_paginator = paginator.page(1)
        except EmptyPage:
            account_restful_paginator = paginator.page(paginator.num_pages)

        account_result_object_list = account_restful_paginator.object_list
        account_restful_list = []

        for account_result_object in account_result_object_list:
            account_restful_list.append(dict(id=account_result_object.id,
                                             username=account_result_object.username,
                                             email=account_result_object.email,
                                             alias=account_result_object.alias,
                                             active=account_result_object.is_active,
                                             admin=account_result_object.is_admin,
                                             viewer=account_result_object.is_viewer))
        return account_restful_list, dict(per_page=per_page, page=page,
                                          total=paginator.count)

    @classmethod
    @auto_log
    def get_user_detail(cls, user_id):
        """
        获取用户信息
        :param user_id:
        :return:
        """
        user_obj = User.objects.filter(id=user_id, is_deleted=False).first()
        if not user_obj:
            return False, "对应用户不存在或已被删除"

        user_dict = user_obj.__dict__
        if user_dict.__contains__('_state'):
            user_dict.pop('_state')
        if user_dict.__contains__('password'):
            user_dict.pop('password')
        if user_dict.__contains__('_password'):
            user_dict.pop('_password')
        user_form_dict = json.dumps(user_dict, cls=DateEncoder, ensure_ascii=False)
        user_form_dict = json.loads(user_form_dict)
        user_role_info, msg = AccountBaseService.get_user_role(user_obj.id)
        user_form_dict['role_info'] = user_role_info
        return user_form_dict, ''

    @classmethod
    @auto_log
    def user_delete(cls, user_id):
        """
        删除用户
        :param user_id:
        :return:
        """
        user_obj = User.objects.filter(pk=user_id, is_deleted=False).first()
        if not user_obj:
            return False, "该用户不存在或已被删除"
        # user_form_obj, msg = cls.get_user_detail(user_id)
        username = user_obj.username
        User.objects.filter(pk=user_id, is_deleted=False).delete()
        UserRole.objects.filter(user_id=user_id, is_deleted=False).delete()
        return username, ''

    @classmethod
    @auto_log
    def get_role_list(cls, role_name, per_page, page):
        """
        获取用户角色列表
        :param role_name:
        :param per_page:
        :param page:
        :return:
        """
        query_params = Q(is_deleted=0)
        if role_name:
            query_params &= Q(name=role_name)

        role_objects = Role.objects.filter(query_params).order_by('-gmt_created')
        if not role_objects:
            return False, "没有角色"

        paginator = Paginator(role_objects, per_page)
        try:
            role_paginator = paginator.page(page)
        except PageNotAnInteger:
            role_paginator = paginator.page(1)
        except EmptyPage:
            role_paginator = paginator.page(paginator.num_pages)

        role_result_object_list = role_paginator.object_list
        role_restful_list = []

        for role in role_result_object_list:
            role_restful_list.append(dict(id=role.id,
                                          name=role.name,
                                          description=role.description,
                                          label=role.label,
                                          creator=role.creator,
                                          gmt_created=str(role.gmt_created)[0:19],
                                          gmt_modified=str(role.gmt_modified)[0:19]))
        return role_restful_list, dict(per_page=per_page, page=page,
                                       total=paginator.count)

    @classmethod
    @auto_log
    def get_role_detail(cls, role_id, per_page, page):
        """
        获取角色细节
        :param page:
        :param per_page:
        :param role_id:
        :return:
        """
        role_obj, msg = cls.get_role_by_id(role_id)
        if not role_obj:
            return False, "该角色不存在或已被删除"

        username_list, msg = cls.get_role_username_list(role_id)
        username_list_objects = User.objects.filter(username__in=username_list, is_deleted=False)

        paginator = Paginator(username_list_objects, per_page)
        try:
            account_restful_paginator = paginator.page(page)
        except PageNotAnInteger:
            account_restful_paginator = paginator.page(1)
        except EmptyPage:
            account_restful_paginator = paginator.page(paginator.num_pages)

        account_result_object_list = account_restful_paginator.object_list

        user_restful_list = []
        for user in account_result_object_list:
            user_restful_list.append(dict(id=user.id,
                                          username=user.username,
                                          email=user.email,
                                          alias=user.alias,
                                          active=user.is_active,
                                          admin=user.is_admin,
                                          viewer=user.is_viewer))

        user_list = dict(value=user_restful_list,
                         per_page=per_page,
                         page=page,
                         total=paginator.count)

        role_detail = dict(id=role_obj.id,
                           name=role_obj.name,
                           description=role_obj.description,
                           label=role_obj.label,
                           creator=role_obj.creator,
                           gmt_created=str(role_obj.gmt_created)[0:19],
                           gmt_modified=str(role_obj.gmt_modified)[0:19],
                           user_list=user_list)

        return role_detail, ''

    @classmethod
    @auto_log
    def role_delete(cls, role_id):
        role_obj, msg = cls.get_role_by_id(role_id)
        if not role_obj:
            return False, "该角色不存在或已被删除"
        role_name = role_obj.name
        Role.objects.filter(pk=role_id, is_deleted=False).delete()
        UserRole.objects.filter(role_id=role_id, is_deleted=False).delete()
        return role_name, ''

    @classmethod
    @auto_log
    def get_dept_list(cls, dept_name, per_page, page):
        """

        :param dept_name:
        :param per_page:
        :param page:
        :return:
        """
        query_params = Q(is_deleted=0)
        if dept_name:
            query_params &= Q(name=dept_name)

        dept_objects = Department.objects.filter(query_params).order_by('-gmt_created')
        if not dept_objects:
            return False, "没有部门"

        paginator = Paginator(dept_objects, per_page)
        try:
            dept_paginator = paginator.page(page)
        except PageNotAnInteger:
            dept_paginator = paginator.page(1)
        except EmptyPage:
            dept_paginator = paginator.page(paginator.num_pages)

        dept_result_object_list = dept_paginator.object_list
        dept_restful_list = []

        for dept_obj in dept_result_object_list:
            dept_restful_list.append(dict(id=dept_obj.id,
                                          name=dept_obj.name,
                                          parent_dept_id=dept_obj.parent_dept_id,
                                          leader=dept_obj.leader,
                                          approver=dept_obj.approver,
                                          label=dept_obj.label,
                                          creator=dept_obj.creator,
                                          gmt_created=str(dept_obj.gmt_created)[0:19],
                                          gmt_modified=str(dept_obj.gmt_modified)[0:19]))
        return dept_restful_list, dict(per_page=per_page, page=page,
                                       total=paginator.count)

    @classmethod
    @auto_log
    def get_dept_detail(cls, dept_id):
        dept_obj, msg = cls.get_dept_by_id(dept_id)
        if not dept_obj:
            return False, "对应部门不存在或已被删除"

        dept_dict = dept_obj.__dict__
        if dept_dict.__contains__('_state'):
            dept_dict.pop('_state')

        user_form_dict = json.dumps(dept_dict, cls=DateEncoder, ensure_ascii=False)
        user_form_dict = json.loads(user_form_dict)

        leader = user_form_dict.get('leader', '')
        approver = user_form_dict.get('approver', '')
        if leader:
            leader, msg = cls.get_user_list_by_str(leader)
        if approver:
            approver, msg = cls.get_user_list_by_str(approver)

        user_form_dict['leader'] = leader
        user_form_dict['approver'] = approver
        return user_form_dict, ''

    @classmethod
    @auto_log
    def get_user_list_by_str(cls, user_str):

        if not user_str:
            return False, "参数为空"

        user_list = user_str.split(',')
        user_restful_list = []
        if len(user_list) >= 1:
            user_objects = User.objects.filter(username__in=user_list).all()
            if not user_objects:
                return [], ''
            for user_obj in user_objects:
                user_restful_list.append(dict(id=user_obj.id,
                                              username=user_obj.username,
                                              email=user_obj.email,
                                              alias=user_obj.alias,
                                              active=user_obj.is_active,
                                              admin=user_obj.is_admin))
        return user_restful_list, ''

    @classmethod
    @auto_log
    def dept_delete(cls, dept_id):

        dept_obj, msg = cls.get_dept_by_id(dept_id)
        if not dept_obj:
            return False, "该部门不存在或已被删除"
        dept_name = dept_obj.name
        Department.objects.filter(pk=dept_id, is_deleted=False).delete()
        return dept_name, ''

    @classmethod
    @auto_log
    def deal_role_members(cls, role_id, user_info, command):
        if not cls.get_role_by_id(role_id):
            return False, "用户id错误"
        user_list = [x for x in user_info.split(',') if x]

        if command == 'append':
            user_objs = User.objects.filter(id__in=user_list)
            user_list = list(map(lambda x: x.id, user_objs))
            user_final_objs = UserRole.objects.filter(role_id=role_id, user_id__in=user_list)
            for user_role_obj in user_final_objs:
                user_list.remove(user_role_obj.user_id)

            if len(user_list) == 0:
                return False, "请提供有效的操作用户id"

            for user in user_list:
                UserRole.objects.create(user_id=user, role_id=role_id)
            return ','.join(map(lambda x: str(x), user_list)) + "已添加", ''

        elif command == 'delete':
            result = UserRole.objects.filter(role_id=role_id, user_id__in=user_list).delete()
            if result[0] == 0:
                return False, "请提供有效的操作用户id"
            else:
                return "已删除", ''
        else:
            return False, "请提供正确的指令"

    @classmethod
    @auto_log
    def get_user_role(cls, user_id):
        """
        获取用户角色信息
        :param username:
        :return:
        """
        user_role_list = UserRole.objects.filter(user_id=user_id, is_deleted=0).all()
        if not user_role_list:
            return '', '该用户无分配角色'
        role_id_list = list(user_role.id for user_role in user_role_list)
        role_objs = Role.objects.filter(id__in=role_id_list).all()
        if not role_objs:
            return '', '查无该用户对应角色'
        role_info = []
        for role in role_objs:
            role_info.append(dict(role_id=role.id,
                                  role_name=role.name))
        return role_info, ''
