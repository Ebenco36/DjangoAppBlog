from rest_framework import serializers
from rest_framework.validators import UniqueValidator
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.contrib.auth.hashers import make_password
from django.core.validators import *
import hashlib
import secrets
import string
from datetime import datetime
from rest_framework.serializers import ModelSerializer
from accounts.models import Profile
from decimal import Decimal
import decimal
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core import serializers as serial



User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(required=True,min_length=6, max_length=100,write_only=True)
    first_name = serializers.CharField(required=True,min_length=1, max_length=100,write_only=True)
    last_name = serializers.CharField(required=True,min_length=1, max_length=100,write_only=True)
    phone = serializers.CharField(required=True,min_length=11, max_length=100,write_only=True)


    class Meta:
        model = User
        fields = ("email", "password", "first_name", "last_name", "phone")
        error_messages = {"email": {"unique": "Give yourself a username"}}

    def create(request, validator_data):
        # random_password = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        user = User.objects.create_user(
            email=validator_data['email'].lower(), 
            password=validator_data['password'], 
            auto_password=validator_data['password'], 
            remember_token=hashlib.sha1(str(datetime.now()).encode('utf-8')).hexdigest()
        )
        
        user.profile.first_name = validator_data['first_name']
        user.profile.last_name = validator_data['first_name']
        user.profile.phone = validator_data['phone']
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk','email','date_joined','last_login']



from django.contrib.auth.hashers import check_password
class ChangePasswordSerializer(serializers.Serializer):
    
    new_password = serializers.CharField(max_length=20, min_length=6, required=True)
    confirm_password = serializers.CharField(max_length=20, min_length=6, required=True)
    old_password = serializers.CharField(max_length=20, required=True)



    def create(self, validated_data):
        data = {
            "user": self.context['user'],
            "new_password": validated_data['new_password'],
            "confirm_password": validated_data['confirm_password'],
            "old_password": validated_data['old_password'],
        }
        return data


    
    def validate(self, data):
        person = self.context['user']
        if not check_password(data.get('old_password'), person.password):
            raise serializers.ValidationError('Password verification invalid')

        if data.get('new_password') != data.get('confirm_password'):
            raise serializers.ValidationError('Password does not match')
        
        return data

from django.db.models import Sum, Q
from django.urls import reverse
class LoginUserSerializer(TokenObtainPairSerializer):


    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['email'] = self.user.email
        data['first_name'] = self.user.profile.first_name
        data['last_name'] = self.user.profile.last_name
        data['phone'] = self.user.profile.phone
        data['id'] = self.user.id
        data['lifetime'] = int(refresh.access_token.lifetime.total_seconds())
        return data



class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)


