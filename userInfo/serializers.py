
from models import MyUser
from rest_framework import serializers


class MyUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ('username', 'first_name', 'last_name', 'birth', 'gender', 'email')
