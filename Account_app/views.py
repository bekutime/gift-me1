from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from Account_app.serializer import RegisterSerializer


class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.create(user=user)
        return (
            {'token': str(token.key)})

