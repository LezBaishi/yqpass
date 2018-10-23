#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth import login as _login
from django.contrib.auth import logout as _logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.middleware import csrf
from django.shortcuts import render, redirect, get_object_or_404
from backend.account.forms import RegisterForm, AccountChangeForm
from backend.account.models import User
from service.common.format_response import api_response, DateEncoder


def index(request):
    return render(request, 'index.html')


def register(request):
    # get 请求中，next 通过 url 传递，即 /?next=value
    # post 请求中，next 通过表单传递，即 <input type="hidden" name="next" value="{{ next }}"/>
    # redirect_to = request.POST.get('next', request.GET.get('next', ''))

    if request.method == 'POST':
        form = RegisterForm(request.POST)
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
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = AccountChangeForm(request.POST)

        if form.is_valid():
            user.alias = form.cleaned_data['alias']
            user.email = form.cleaned_data['email']
            user.phone = form.cleaned_data['phone']
            user.job_number = form.cleaned_data['job_number']
            user.dept_id = form.cleaned_data['dept_id']
            user.save()

            form_dict = {'alias': user.alias,
                         'email': user.email,
                         'phone': user.phone,
                         'job_number': user.job_number,
                         'dept_id': user.dept_id}

            return api_response(1, "用户信息修改成功", form_dict)

        else:
            error = form.errors
            return api_response(0, "用户信息填写有误, 请修改后重新填写", error)

    else:
        user_dict = user.__dict__
        user_dict.pop('_state')
        user_dict.pop('password')
        user_dict.pop('_password')
        user_form_dict = json.dumps(user_dict, cls=DateEncoder, ensure_ascii=False)
        return api_response(1, "用户信息", user_form_dict)


def login(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

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
        form = PasswordChangeForm(user=request.user, data=request.POST)
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
