from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(
        label=("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        max_length=128,
        write_only=True,
    )

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )
            if not user:
                msg = ("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = ('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")
        data["user"] = user
        return data


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password1 = serializers.CharField(
        label=("Password1"),
        style={"input_type": "password"},
        trim_whitespace=False,
        max_length=128,
        write_only=True,
    )
    password2 = serializers.CharField(
        label=("Password2"),
        style={"input_type": "password2"},
        trim_whitespace=False,
        max_length=128,
        write_only=True,
    )

    def validate(self, data):
        username = data.get("username")
        password1 = data.get("password1")
        password2 = data.get("password2")

        if not password1 == password2:
            msg = ("Passwords must be equal")
            raise serializers.ValidationError(msg, code="authorization")
        if User.objects.filter(username=username).exists():
            msg = ("User already exists pick another username")
            raise serializers.ValidationError(msg, code="authorization")

        return data
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']

    # hide password
        extra_kwargs = {
            'password': {'write_only':True}
        }


    # hash passwords in the database, override default create function
    def create(self, validated_data):
        #extract password
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data) #doesnt include password

        if password is not None:
            instance.set_password(password) #hashes password
        instance.save()
        return instance