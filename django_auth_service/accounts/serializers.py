from .models import User
from rest_framework import serializers
from django.core.validators import RegexValidator
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



phone_number_validator = RegexValidator(
    regex=r'^09\d{9}$',
    message="phone number start with 09 and 9 other id digits only"
)

# .......................................................................................
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

# .......................................................................................
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """یه کلاس واسه سفارشی سازی کردن اطلاعات jwt payload"""
    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)

        token['role'] = user.role
        token['username'] = user.username

        return token
#.....................................................................................
class UserIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']

#.....................................................................................
class TokenIntrospectionSerializer(serializers.Serializer):
    token = serializers.CharField()

# ....................................................................................
class UserRegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=100)
    phone_number = serializers.CharField(validators=[phone_number_validator,UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(max_length=100, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)


    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords must match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


# .......................................................................................
class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=False, allow_blank=True,validators=[phone_number_validator])
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        username = data.get("username")
        phone_number = data.get("phone_number")
        password = data.get("password")

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        elif phone_number and password:
            user = authenticate(request=self.context.get('request'), phone_number=phone_number, password=password)
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "username" or "phone_number" and "password".'
            raise serializers.ValidationError(msg, code='authorization')
        data['user'] = user
        return data





