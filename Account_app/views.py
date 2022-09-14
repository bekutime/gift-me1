from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from rest_framework import response, status, generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from Account_app.utils import Util
from django.contrib.sites.shortcuts import  get_current_site
from Account_app.models import MyUser
from Account_app.serializer import RegisterSerializer
from django.urls import reverse


class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        userr = request.data
        serializer = RegisterSerializer(data=userr)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():

            user = serializer.save()
            user_data = serializer.data
            print(serializer.data)
            token = Token.objects.create(user=user)
            return Response({'token': str(token.key)}) #response.Response(user_data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            #
            # user = MyUser.objects.get(email=user_data['email'])
            #
            # token = RefreshToken.for_user(user).access_token
            #
            # current_site = get_current_site(request).domain
            # relativeLink = reverse('verify-email')
            #
            # absurl = 'http://' + current_site + relativeLink +"?token=" + str(token)
            # email_body = 'Hi'+ user.email + 'Use link below to verify your email \n' + absurl
            # data = {'email_body': email_body, 'to_email': user.email,
            #         'email_subject': 'Verify your email'}
            # Util.send_email(data)



# class VerifyEmail(generics.GenericAPIView):
#     def get(self):
#         pass


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        login = request.data.get('email')
        if not MyUser.objects.filter(email=login).exists():
            return Response('This email or password is not correct')
        user = MyUser.objects.get(email=login)
        password = request.data.get('password')
        password_check = check_password(password, user.password)
        if not password_check:
            return Response('This email or password is not correct')
        token = Token.objects.get(user=user)
        return Response({'token': str(token.key)})
