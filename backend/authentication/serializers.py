# Imports
from rest_framework import serializers
from authentication.models import User
from django.contrib.auth.hashers import check_password
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from authentication.utils import Util

# imports

# User Registration


class UserRegistrationSerializer(serializers.ModelSerializer):
    # We are writing this because we need confirm password field in our Registration Request
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2', 'tc']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    # Validataing Password and Confirm Password while Registration

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password Doesn't Match")
        return attrs
    # Using this create method because we're using custom user model

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)

# user Login


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']

# user Profile access serializer


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name',]


class UserChangePasswordSerializer(serializers.Serializer):
    oldPassword = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)
    password3 = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['oldPassword', 'password2', 'password3']

    def validate(self, attrs):
        password2 = attrs.get('password2')
        password3 = attrs.get('password3')
        oldPassword = attrs.get('oldPassword')
        user = self.context.get('user')
        # Check if old_password matches the current user's password
        if not check_password(oldPassword, user.password):
            raise serializers.ValidationError("Current password is incorrect")

        # Check if password2 and password3 match
        if password2 != password3:
            raise serializers.ValidationError(
                "Password and Confirm Password does not match")

        # Set the new password for the user
        user.set_password(password2)
        user.save()
        return attrs


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = f'http://localhost:5173/api/user/reset/{uid}/{token}'
            # Send Email
            # Create a button with a link
            reset_button = f'<a href="{link}" style="display:inline-block; padding: 10px 20px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px;">Reset Your Password</a>'

            # Send Email
            email_subject = 'Reset Your Password'
            to_email = user.email

            # Combine the button with the rest of the email content
            body = f"""
                <html>
                <head>
                    <title>Reset Your Password</title>
                </head>
                <body>
                    <p>Hello,</p>
                    <p>Click the button below to reset your password:</p>
                    <table style="width:100%; text-align:center;">
                        <tr>
                            <td>
                                <a href="{link}" style="background-color: #4CAF50; color: white; text-decoration: none; padding: 10px 20px; border-radius: 5px; display: inline-block;">Reset Your Password</a>
                            </td>
                        </tr>
                    </table>
                    <p>If you didn't request this password reset, please ignore this email.</p>
                    <p>Thank you!</p>
                </body>
                </html>
                """
            data = {
                'email_subject': 'Reset Your Password',
                'body': body,
                'to_email': user.email,
                'is_html': True  # Specify that the email body contains HTML
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError("You are not a Registered User")


class UserPasswordResetSerializer(serializers.Serializer):
    password1 = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password1', 'password2']

    def validate(self, attrs):
        try:
            password1 = attrs.get('password1')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            # Check if password2 and password3 match
            token = self.context.get('token')
            if password1 != password2:
                raise serializers.ValidationError(
                    "Password and Confirm Password don't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationError('Token is not Valid or Expired')
            # Set the new password for the user
            user.set_password(password2)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise ValidationError('Token is not Valid or Expired')
