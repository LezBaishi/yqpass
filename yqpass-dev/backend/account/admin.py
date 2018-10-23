#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from backend.account.forms import UserChangeForm, UserCreationForm
from backend.account.models import User, Department, Role, UserRole
from service.common.base_services import ModelBaseAdmin


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'email', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {
            'fields': ('alias', 'phone', 'dept_id',
                       'job_number', 'creator',
                       )
        }),
        ('Permissions', {
            'fields': ('is_admin', 'is_active', 'is_deleted',)
        }),
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2',
                       'alias', 'email', 'phone', 'dept_id',
                       'job_number', 'is_admin',
                       'creator',)}
         ),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()


class DeptAdmin(ModelBaseAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name', 'parent_dept_id', 'leader', 'approver',) + ModelBaseAdmin.list_display


class RoleAdmin(ModelBaseAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name', 'description', 'label') + ModelBaseAdmin.list_display


class UserRoleAdmin(ModelBaseAdmin):
    search_fields = ('user_id',)
    list_display = ('id', 'user_id', 'role_id') + ModelBaseAdmin.list_display


admin.site.register(User, UserAdmin)
admin.site.register(Department, DeptAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(UserRole, UserRoleAdmin)
admin.site.unregister(Group)
