from django.core.mail import EmailMessage
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from utils.email import EmailThread
from utils.jwt_token import token_generator


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
    

class ResendEmailVerificationSerializer(serializers.Serializer):
    """This serializer resend email verification code"""

    email = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"error": "User does not exist!"})
        if user.is_verified:
            raise serializers.ValidationError({"error": "Email already verified"})
        # Adding the user field to attrs to be captured in the resend email confirmation view to prevent re-query
        attrs["user"] = user
        return super().validate(attrs)


class ChangePasswordSerializer(serializers.Serializer):
    """This serializer change user password"""

    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        new_password = attrs.get("new_password")
        confirm_new_password = attrs.get("confirm_new_password")
        # If new password & confirm new password are not match
        if new_password != confirm_new_password:
            raise serializers.ValidationError({"error": "The passwords do not match"})

        # validate password complexity
        try:
            validate_password(new_password)
        # password is not strong
        except serializers.ValidationError:
            raise serializers.ValidationError()

        return super().validate(attrs)


class ResetPasswordSerializer(serializers.Serializer):
    """Reset user password"""

    email = serializers.EmailField(required=True)


class SetPasswordSerializer(serializers.Serializer):
    """Set user password after reset password"""

    new_password = serializers.CharField(required=True, write_only=True)
    confirm_new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        new_password = attrs.get("new_password")
        confirm_new_password = attrs.get("confirm_new_password")
        # If new password & confirm new password are not match
        if new_password != confirm_new_password:
            raise serializers.ValidationError({"error": "The passwords do not match"})

        # validate password complexity
        try:
            validate_password(new_password)
        # password is not strong
        except serializers.ValidationError:
            raise serializers.ValidationError()

        return super().validate(attrs)
