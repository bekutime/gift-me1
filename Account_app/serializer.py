from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from Account_app.models import MyUser

'''required делает поле обязательным'''
class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True, min_length=8, write_only=True)

    class Meta:
        model = MyUser
        fields = ['id', 'email', 'password', 'confirm_password']

    def validate(self, attrs):
        attrs = super().validate(attrs)
        password = attrs['password']
        confirm_password = attrs['confirm_password']
        if password != confirm_password:
            raise serializers.ValidationError(detail='password does not match', code='password_match')

        return attrs


    def validate_email(self, value):

        if MyUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(f' {value}  - This login already exists ')
        return value

    def validate_password(self, password):
        try:
            validate_password(password)

        except ValidationError as e:
            raise serializers.ValidationError(e)
        return password




    # def create(self, validated_data):
    #     user = MyUser.objects.create(username=validated_data.get('email'))
    #     user.set_password(validated_data.get('password'))
    #     user.save()
    #     token = Token.objects.create(user=user)
    #
    #     return user, token.key

    def create(self, validated_data):
        user = MyUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"]
        )
        # Token.objects.create(user=user)
        user.save()
        return user

class LoginView(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'password', 'email']


