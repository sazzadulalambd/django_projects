from rest_framework import serializers
from django.contrib.auth.models import User  # import django admin user
from .models import *
from . import views


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        if attrs['username']:
            if User.objects.filter(username=attrs['username']).exists():
                raise serializers.ValidationError('This user name is taken!')

        if attrs['email']:
            if User.objects.filter(email=attrs['email']).exists():
                raise serializers.ValidationError('This email is taken!')
        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        
        return super().create(validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Team
        # fields = ['url', 'name', 'position']
        fields = '__all__'

    def validate(self, attrs):
        special_char = "~!@#$%^&*()_+=-<>/|\*{}[]"
        if any(sc in special_char for sc in attrs['name']):
            raise serializers.ValidationError(
                'Name cannot contain special characters')
        return super().validate(attrs)


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    # assign = UserSerializer()
    teams = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='TeamView')

    class Meta:
        model = Task
        fields = '__all__'
        # depth = 1   #this is fro seeing the Foreign key
