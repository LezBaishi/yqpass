#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, dep=0):
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email=self.normalize_email(email), username=username, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    用户
    """
    username = models.CharField("用户名", max_length=20, unique=True)
    alias = models.CharField("姓名", max_length=20, blank=True, default='')
    email = models.EmailField("电子邮箱", max_length=128)
    phone = models.CharField("手机号码", max_length=13, default='')
    dept_id = models.CharField("部门编号", max_length=20, default=0)
    job_number = models.CharField("员工编号", max_length=20, blank=True, default='')

    is_active = models.BooleanField("激活", default=True)
    is_admin = models.BooleanField("管理员权限", default=False)
    is_viewer = models.BooleanField("参观者", default=False)

    creator = models.CharField('创建人', max_length=50, default='admin')
    gmt_created = models.DateTimeField('创建时间', auto_now_add=True)
    modifier = models.CharField('修改人', max_length=50, default='admin')
    gmt_modified = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField("已删除", default=False)

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def get_short_name(self):
        return self.username

    def get_alis_name(self):
        return self.alias

    def get_full_name(self):
        return ','.join((self.username, self.alias))

    def has_active(self):
        return self.is_active

    @property
    def dept_name(self):
        dept_id = self.dept_id
        dept_object = Department.objects.filter(id=dept_id)
        if dept_object:
            return dept_object[0].name
        else:
            return 'Depatment does not exist.'

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"


class Role(models.Model):
    """
    角色
    """
    name = models.CharField("名称", max_length=50)
    description = models.CharField("描述", max_length=100, default='')
    label = models.CharField("标签", max_length=50, blank=True, default='')

    creator = models.CharField('创建人', max_length=50, default='admin')
    gmt_created = models.DateTimeField('创建时间', auto_now_add=True)
    modifier = models.CharField('修改人', max_length=50, default='admin')
    gmt_modified = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField("已删除", default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "角色"
        verbose_name_plural = "角色"


class Department(models.Model):
    """
    部门
    """
    name = models.CharField("部门名称", max_length=50)
    parent_dept_id = models.IntegerField("上级部门id", blank=True, default=0)
    leader = models.CharField("部门领导", max_length=50, blank=True, default='', help_text="部门leader, user表中的用户名")
    approver = models.CharField("审批人", max_length=50, blank=True, default='', help_text="user表中的用户名, 用逗号隔开多个user。")
    label = models.CharField("标签", max_length=50, blank=True, default='')

    creator = models.CharField('创建人', max_length=50, default='admin')
    gmt_created = models.DateTimeField('创建时间', auto_now_add=True)
    modifier = models.CharField('修改人', max_length=50, default='admin')
    gmt_modified = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField("已删除", default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "部门"
        verbose_name_plural = "部门"


class UserRole(models.Model):
    """
    用户角色
    """
    user_id = models.IntegerField("用户id")
    role_id = models.IntegerField("角色id")

    creator = models.CharField('创建人', max_length=50, default='admin')
    gmt_created = models.DateTimeField('创建时间', auto_now_add=True)
    modifier = models.CharField('修改人', max_length=50, default='admin')
    gmt_modified = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField("已删除", default=False)

    def __str__(self):
        return str(self.user_id) + '-' + str(self.role_id)

    class Meta:
        verbose_name = "用户角色"
        verbose_name_plural = "用户角色"
