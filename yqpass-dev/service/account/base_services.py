#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date: 2018/6/1 11:11
from backend.account.models import User, Department, Role, UserRole
from service.common.base_services import BaseService
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
        username_queryset = User.objects.filter(id__in=(user_id_list)).all()
        username_list = []
        for username in username_queryset:
            username_list.append(username)
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
