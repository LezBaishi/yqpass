#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth import login as _login
from django.contrib.auth import logout as _logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.middleware import csrf
from django.shortcuts import redirect, get_object_or_404
from backend.account.forms import RegisterForm, AccountChangeForm
from backend.account.models import User
from service.account.base_services import AccountBaseService
from service.common.format_response import api_response, DateEncoder
from service.common.permission_check import admin_permission_check


def index(request):
    return api_response(1, "Listen to the party's command", 'both socialist-minded and professionally qualified')


def register(request):
    # get 请求中，next 通过 url 传递，即 /?next=value
    # post 请求中，next 通过表单传递，即 <input type="hidden" name="next" value="{{ next }}"/>
    # redirect_to = request.POST.get('next', request.GET.get('next', ''))

    if request.method == 'POST':
        user_data_dict = json.loads(request.body.decode('utf-8'))
        form = RegisterForm(user_data_dict)
        if form.is_valid():
            form.save()
            return api_response(1, "用户注册成功", {"username": form.cleaned_data['username']})
            # if redirect_to:
            #     return redirect(redirect_to)
            # else:
            #     return redirect('/')
        else:
            error = form.errors
            return api_response(0, "用户信息填写有误, 请修改后重新填写", error)

    else:
        return api_response(0, "用户信息填写有误, 请修改后重新填写", '')


@login_required
def account_change(request):
    username = request.user.username
    user_obj = get_object_or_404(User, username=username)
    if request.method == 'POST':
        user_data_dict = json.loads(request.body.decode('utf-8'))
        form = AccountChangeForm(user_data_dict)

        if form.is_valid():
            user_obj.alias = form.cleaned_data['alias']
            user_obj.email = form.cleaned_data['email']
            user_obj.phone = form.cleaned_data['phone']
            user_obj.job_number = form.cleaned_data['job_number']
            user_obj.dept_id = form.cleaned_data['dept_id']
            user_obj.save()

            form_dict = {'username': username,
                         'alias': user_obj.alias,
                         'email': user_obj.email,
                         'phone': user_obj.phone,
                         'job_number': user_obj.job_number,
                         'dept_id': user_obj.dept_id}

            return api_response(1, "", form_dict)

        else:
            error = form.errors
            return api_response(0, "用户信息填写有误, 请修改后重新填写", error)

    else:
        user_restful_detail, msg = AccountBaseService.get_user_detail(user_id=user_obj.id)
        return api_response(1, '', user_restful_detail)


def login(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        user_data_dict = json.loads(request.body.decode('utf-8'))
        username = user_data_dict.get('username', '')
        password = user_data_dict.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            _login(request, user)
            return api_response(1, "用户已经登陆", username)
        else:
            return api_response(0, "用户名与密码不匹配, 请修改后再尝试连接", '')
    else:
        return api_response(0, "请输入用户名与密码, 然后登陆", '')


@login_required
def logout(request):
    """

    :param request:
    :return:
    """
    _logout(request)
    return api_response(1, "用户已注销", '')


@login_required
def password_change(request):
    """
    :param request:
    :return:
    """
    if request.method == 'POST':
        user_data_dict = json.loads(request.body.decode('utf-8'))
        form = PasswordChangeForm(user=request.user, data=user_data_dict)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return api_response(1, "密码修改成功, 请重新登陆", '')
        else:
            error = form.errors
            return api_response(0, error, '')
    else:
        return redirect('/')


def get_token(request):
    """
    获取 csrf token
    :param request:
    :return:
    """
    token = csrf.get_token(request)
    return api_response(1, 'get_token', token)


@login_required
def user_list(request):
    """
    返回用户列表
    :param request:
    :return:
    """
    if request.method == "GET":
        user = request.user.username
        permission, msg = admin_permission_check(user)
        if not permission:
            return api_response(0, "非管理员用户", '')

        request_data = request.GET
        username = request_data.get('username', '')
        email = request_data.get('email', '')
        alias = request_data.get('alias', '')
        per_page = int(request_data.get('per_page', 10))
        page = int(request_data.get('page', 1))
        category = request_data.get('category', 'all')

        account_restful_list, msg = AccountBaseService.get_user_list(username=username,
                                                                     email=email,
                                                                     alias=alias,
                                                                     per_page=per_page,
                                                                     page=page,
                                                                     category=category)
        if account_restful_list is False:
            return api_response(0, msg, '')
        else:
            data = dict(value=account_restful_list,
                        per_page=msg['per_page'],
                        page=msg['page'],
                        total=msg['total'])
            return api_response(1, '', data)
    else:
        return redirect('/')


@login_required
def user_detail(request, pk):
    """
    管理员查看用户信息
    :param request:
    :param pk:
    :return:
    """
    if request.method == "GET":
        user = request.user.username
        permission, msg = admin_permission_check(user)
        if not permission:
            return api_response(0, "非管理员用户", '')

        user_restful_detail, msg = AccountBaseService.get_user_detail(user_id=pk)
        return api_response(1, '', user_restful_detail)
    elif request.method == "POST":
        user = request.user.username
        permission, msg = admin_permission_check(user)
        if not permission:
            return api_response(0, "非管理员用户", '')

        user_obj = get_object_or_404(User, username=user)
        user_data_dict = json.loads(request.body.decode('utf-8'))
        form = AccountChangeForm(user_data_dict)

        if form.is_valid():
            user_obj.alias = form.cleaned_data['alias']
            user_obj.email = form.cleaned_data['email']
            user_obj.phone = form.cleaned_data['phone']
            user_obj.job_number = form.cleaned_data['job_number']
            user_obj.dept_id = form.cleaned_data['dept_id']
            user_obj.is_active = form.cleaned_data['is_active']
            user_obj.is_admin = form.cleaned_data['is_admin']
            user_obj.is_viewer = form.cleaned_data['is_viewer']
            user_obj.save()

            form_dict = {'username': user,
                         'alias': user_obj.alias,
                         'email': user_obj.email,
                         'phone': user_obj.phone,
                         'job_number': user_obj.job_number,
                         'dept_id': user_obj.dept_id,
                         'is_active': user_obj.is_active,
                         'is_viewer': user_obj.is_viewer,
                         'is_admin': user_obj.is_admin}

            return api_response(1, "用户信息修改成功", form_dict)

        else:
            error = form.errors
            return api_response(0, "用户信息填写有误, 请修改后重新填写", error)

    else:
        return redirect('/')


@login_required
def user_delete(request):
    """
    删除用户
    :param request:
    :return:
    """
    if request.method == "POST":
        user = request.user.username
        request_data_dict = json.loads(request.body.decode('utf-8'))
        permission, msg = admin_permission_check(user)
        if not permission:
            return api_response(0, "非管理员用户", '')
        user_id = request_data_dict.get('user_id', '')
        if not user_id:
            return api_response(0, "请提供用户id", '')

        delete_result, msg = AccountBaseService.user_delete(user_id=user_id)
        if not delete_result:
            return api_response(0, msg, '')
        else:
            return api_response(1, msg, delete_result)
    else:
        return redirect('/')


@login_required
def role_list(request):
    """
    角色列表
    :param request:
    :return:
    """
    if request.method == "GET":
        username = request.user.username
        request_data = request.GET

        permission, msg = admin_permission_check(username)
        if not permission:
            return api_response(0, "非管理员用户", '')

        role_name = request_data.get('role', '')
        per_page = request_data.get('per_page', 10)
        page = request_data.get('page', 1)
        role_restful_list, msg = AccountBaseService.get_role_list(role_name, per_page, page)

        if role_restful_list is False:
            return api_response(0, msg, '')
        else:
            data = dict(value=role_restful_list,
                        per_page=msg['per_page'],
                        page=msg['page'],
                        total=msg['total'])
            return api_response(1, '', data)

    else:
        return redirect('/')


@login_required
def role_detail(request, pk):
    """
    角色列表细节
    :param pk:
    :param request:
    :return:
    """
    if request.method == "GET":
        username = request.user.username
        request_data = request.GET

        permission, msg = admin_permission_check(username)
        if not permission:
            return api_response(0, "非管理员用户", '')

        per_page = request_data.get('per_page', 10)
        page = request_data.get('page', 1)

        restful_result_role, msg = AccountBaseService.get_role_detail(role_id=pk, per_page=per_page, page=page)

        if not restful_result_role:
            return api_response(0, msg, '')
        else:
            return api_response(1, '', restful_result_role)

    else:
        return redirect('/')


@login_required
def role_members(request, pk):
    if request.method == "POST":
        username = request.user.username
        request_data_dict = json.loads(request.body.decode('utf-8'))
        permission, msg = admin_permission_check(username)
        if not permission:
            return api_response(0, "非管理员用户", '')

        user_info = request_data_dict.get('user', '')
        command = request_data_dict.get('command', '')

        deal_result, msg = AccountBaseService.deal_role_members(role_id=pk, user_info=user_info, command=command)
        if deal_result is False:
            return api_response(0, msg, '')
        else:
            return api_response(1, '', deal_result)

    else:
        return redirect('/')


@login_required
def role_delete(request):
    """
    删除角色
    :param request:
    :return:
    """
    if request.method == "POST":
        user = request.user.username
        request_data_dict = json.loads(request.body.decode('utf-8'))
        permission, msg = admin_permission_check(user)
        if not permission:
            return api_response(0, "非管理员用户", '')
        role_id = request_data_dict.get('role_id', '')
        if not role_id:
            return api_response(0, "请提供角色id", '')

        delete_result, msg = AccountBaseService.role_delete(role_id=role_id)
        if not delete_result:
            return api_response(0, msg, '')
        else:
            return api_response(1, msg, delete_result)
    else:
        return redirect('/')


@login_required
def dept_list(request):
    """
    部门列表
    :param request:
    :return:
    """
    if request.method == "GET":
        username = request.user.username
        request_data = request.GET

        permission, msg = admin_permission_check(username)
        if not permission:
            return api_response(0, "非管理员用户", '')

        dept_name = request_data.get('dept', '')
        per_page = request_data.get('per_page', 10)
        page = request_data.get('page', 1)
        dept_restful_list, msg = AccountBaseService.get_dept_list(dept_name, per_page, page)

        if dept_restful_list is False:
            return api_response(0, msg, '')
        else:
            data = dict(value=dept_restful_list,
                        per_page=msg['per_page'],
                        page=msg['page'],
                        total=msg['total'])
            return api_response(1, '', data)

    else:
        return redirect('/')


@login_required
def dept_detail(request, pk):
    """
    部门细节
    :param pk:
    :param request:
    :return:
    """
    if request.method == "GET":
        username = request.user.username
        request_data = request.GET

        permission, msg = admin_permission_check(username)
        if not permission:
            return api_response(0, "非管理员用户", '')

        restful_result_dept, msg = AccountBaseService.get_dept_detail(dept_id=pk)

        if not restful_result_dept:
            return api_response(0, msg, '')
        else:
            return api_response(1, '', restful_result_dept)

    else:
        return redirect('/')


@login_required
def dept_delete(request):
    """
    删除部门
    :param request:
    :return:
    """
    if request.method == "POST":
        user = request.user.username
        request_data_dict = json.loads(request.body.decode('utf-8'))
        permission, msg = admin_permission_check(user)
        if not permission:
            return api_response(0, "非管理员用户", '')

        dept_id = request_data_dict.get('dept_id', '')
        if not dept_id:
            return api_response(0, "请提供部门id", '')

        delete_result, msg = AccountBaseService.dept_delete(dept_id=dept_id)
        if not delete_result:
            return api_response(0, msg, '')
        else:
            return api_response(1, msg, delete_result)
    else:
        return redirect('/')