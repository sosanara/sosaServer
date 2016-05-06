# -*- coding: utf-8 -*-
from rest_auth.serializers import PasswordResetSerializer
from rest_framework import serializers, exceptions

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate

from allauth.account.adapter import get_adapter
from allauth.account.utils import user_field, setup_user_email
from allauth.account import app_settings as allauth_settings
from allauth.utils import get_username_max_length, email_address_exists

import re

UserModel = get_user_model()

GENDER_CHOICE = ['Man', 'Women']


class RegisterDetailSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=get_username_max_length(),
        min_length=allauth_settings.USERNAME_MIN_LENGTH,
        required=allauth_settings.USERNAME_REQUIRED
    )
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    birth = serializers.IntegerField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    gender = serializers.ChoiceField(required=True, choices=GENDER_CHOICE)

    cleanup_name = re.compile(r'''^[\d.@!#$%^&*`'"\|=?~,+_-]+$''')

    error_messages = {
        'invalid_username':
            _('아이디는 영어, 숫자와 특수문자 @/./+/-/_ 를 사용할 수 있습니다.'),
        'username_blacklisted':
            _('사용할 수 없는 아이디 입니다.'),
        'username_taken':
            _('이미 있는 사용자 아이디 입니다.'),
        'too_many_login_attempts':
            _('나중에 다시 시도해 주시기 바랍니다.')
    }

    def clean_username(self, username, shallow=False):
        """
        Validates the username. You can hook into this if you want to
        (dynamically) restrict what usernames can be chosen.
        """
        if not self.username_regex.match(username):
            raise forms.ValidationError(
                self.error_messages['invalid_username'])

        # TODO: Add regexp support to USERNAME_BLACKLIST
        username_blacklist_lower = [ub.lower()
                                    for ub in allauth_settings.USERNAME_BLACKLIST]
        if username.lower() in username_blacklist_lower:
            raise forms.ValidationError(
                self.error_messages['username_blacklisted'])
        # Skipping database lookups when shallow is True, needed for unique
        # username generation.
        if not shallow:
            username_field = allauth_settings.USER_MODEL_USERNAME_FIELD
            assert username_field
            user_model = get_user_model()
            try:
                query = {username_field + '__iexact': username}
                user_model.objects.get(**query)
            except user_model.DoesNotExist:
                return username
            raise forms.ValidationError(
                self.error_messages['username_taken'])
        return username

    def validate_username(self, username):
        return get_adapter().clean_username(username)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("이미 가입되어 있는 이메일 입니다."))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate_birth(self, birth):
        if 1900 > birth or birth > 2016:
            raise serializers.ValidationError(_("생일 기간을 확인해주세요."))
        return birth

    def validate_first_name(self, first_name):
        if self.cleanup_name.match(first_name):
            raise serializers.ValidationError(_("올바르지 않은 이름입니다."))
        return first_name

    def validate_last_name(self, last_name):
        if self.cleanup_name.match(last_name):
            raise serializers.ValidationError(_("올바르지 않은 성입니다."))
        return last_name

    def validate_gender(self, gender):
        if not (gender == "Man" or gender == "Women"):
            raise serializers.ValidationError(_("성별이 틀립니다."))
        return gender

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("패스워드가 일치하지 않습니다."))
        return data

    def custom_signup(self, request, user, commit=True):
        data = self.cleaned_data
        birth = data.get('birth')
        gender = data.get('gender')
        if birth:
            setattr(user, 'birth', birth)
        if gender:
            user_field(user, 'gender', gender)
        if commit:
            user.save()
        return user

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            'birth': self.validated_data.get('birth', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'gender': self.validated_data.get('gender', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


class UserDetailsSerializer(serializers.ModelSerializer):
    birth = serializers.IntegerField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    gender = serializers.ChoiceField(required=True, choices=GENDER_CHOICE)

    class Meta:
        model = UserModel
        fields = ('username', 'email', 'first_name', 'last_name', 'birth', 'gender')
        read_only_fields = ('username', 'email')


class PasswordDetailResetSerializer(PasswordResetSerializer):
    def get_email_options(self):
        return {
            'email_template_name': 'password_reset_email.html',
        }


class LoginDetailSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def _validate_username(self, username, password):
        user = None

        if username and password:
            user = authenticate(username=username, password=password)
        else:
            msg = _('아이디와 패스워드를 입력해주세요.')
            raise exceptions.ValidationError(msg)

        return user

    def _validate_username_email(self, username, email, password):
        user = None

        if username and password:
            user = authenticate(username=username, password=password)
        else:
            msg = _('아이디와 패스워드가 포함되어야 합니다.')
            raise exceptions.ValidationError(msg)

        return user

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = None

        if 'allauth' in settings.INSTALLED_APPS:
            from allauth.account import app_settings

            if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.USERNAME:
                user = self._validate_username(username, password)

            # Authentication through either username or email
            else:
                user = self._validate_username_email(username, '', password)

        else:
            user = self._validate_username_email(username, '', password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('사용할 수 없는 사용자 계정입니다.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('로그인할 수 없습니다.')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs
