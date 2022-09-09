from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

class RegisterSerializer(serializers.Serializer):

    email = serializers.CharField()
    password = serializers.CharField()
    repeat_password = serializers.CharField()

    def validate_email(self,value):

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(f' {value}  - This login already exists ')
        return value

    def password_value(self, repeat_password, value):
        if not User.objects.filter(password=repeat_password).exists():
            raise serializers.ValidationError(f' {repeat_password} -  Вы не правельно ввели пароль')

        try: validate_password(value)

        except ValidationError as e:
            raise serializers.ValidationError(e)
        return value

    def create(self, validated_data):
        user = User.objects.create(username=validated_data.get('login'))
        user.set_password(validated_data.get('password'))
        user.save()

        return user


