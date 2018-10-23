#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date: 2018/7/26 15:05
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from backend.account.models import User
from yuanqu2 import settings

__author__ = 'x-zj'


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='密码确认', widget=forms.PasswordInput)

    error_messages = {
        'duplicate_email': "邮箱已被注册, 请更换后重试",
        'password_mismatch': "密码输入不一致, 请重试",
        'duplicate_username': "用户名已被注册, 请更换后重试"
    }

    class Meta:
        model = User
        fields = ('username', 'alias', 'email', 'phone', 'dept_id',)

    def clean_email(self):

        # Since User.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
        )

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = not settings.USERS_VERIFY_EMAIL
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    # """
    password = ReadOnlyPasswordHashField(label="密码")

    class Meta:
        model = User
        fields = ('username', 'alias', 'email', 'phone', 'dept_id',
                  'job_number', 'is_active', 'is_admin',
                  'creator', 'is_deleted')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'alias', 'email', 'phone', 'dept_id',)


class AccountChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('alias', 'email', 'phone', 'job_number', 'dept_id', 'is_active', 'is_admin')
