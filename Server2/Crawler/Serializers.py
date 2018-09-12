from django.contrib.auth import authenticate
from rest_framework import exceptions
from Crawler.models import MyUser
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'pw', 'push_token')
