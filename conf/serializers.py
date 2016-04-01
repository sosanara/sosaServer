# -*- coding: utf-8 -*-

from allauth.account.utils import user_field
from rest_auth.serializers import PasswordResetSerializer
from rest_framework import serializers, exceptions
from rest_auth.registration.serializers import RegisterSerializer
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate

import re

UserModel = get_user_model()

GENDER_CHOICE = ['Man', 'Women']


class RegisterDetailSerializer(RegisterSerializer):
    email = serializers.EmailField(required=True)
    birth = serializers.IntegerField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    gender = serializers.ChoiceField(required=True, choices=GENDER_CHOICE)

    cleanup_name = re.compile(r'''^[\d.@!#$%^&*`'"\|=?~,+_-]+$''')

    def validate_birth(self, birth):
        if 1900 > birth or birth > 2016:
            raise serializers.ValidationError(_("This birth is too much or less."))
        return birth

    def validate_first_name(self, first_name):
        if self.cleanup_name.match(first_name):
            raise serializers.ValidationError(_("invalid_first_name"))
        return first_name

    def validate_last_name(self, last_name):
        if self.cleanup_name.match(last_name):
            raise serializers.ValidationError(_("invalid_last_name"))
        return last_name

    def validate_gender(self, gender):
        if not (gender == "Man" or gender == "Women"):
            raise serializers.ValidationError(_("invalid_gender"))
        return gender

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


class UserDetailsSerializer(serializers.ModelSerializer):
    birth = serializers.IntegerField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    gender = serializers.ChoiceField(required=True, choices=GENDER_CHOICE)

    class Meta:
        model = UserModel
        fields = ('username', 'email', 'first_name', 'last_name', 'birth', 'gender')
        read_only_fields = ('username', )


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
            msg = _('Must include "username" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def _validate_username_email(self, username, email, password):
        user = None

        if username and password:
            user = authenticate(username=username, password=password)
        else:
            msg = _('Must include either "username" or "email" and "password".')
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
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs
