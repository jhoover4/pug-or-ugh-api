from django.contrib.auth import get_user_model

from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = get_user_model()


class DogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dog
        fields = (
            'id',
            'name',
            'image_filename',
            'breed',
            'age',
            'gender',
            'size',
        )


class UserPrefSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserPref
        fields = (
            'id',
            'gender',
            'age',
            'size',
        )


class UserDogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserDog
        fields = (
            'id',
            'user',
            'status',
            'dog'
        )
        extra_kwargs = {'user': {'write_only': True}}
