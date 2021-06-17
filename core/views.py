from django.db.models import expressions
from core.models import Owner
from django.shortcuts import render
from rest_framework import generics, status, views
from .serializers import EmailVerificationSerializer, RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Owner
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings

# Create your views here.

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, data):
        user = self.request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data

        user = Owner.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(self.request)
        relative_link = reverse('email-verify')
        absurl = 'http://' + str(current_site) + relative_link + '?token=' + str(token) 

        email_body = 'Hi ' + user.username + ' user below link to verify your email for shopease store \n' + absurl

        data = {'email_body': email_body, 'email_subject': 'Verify your email', 'to_email': user.email}
        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')
        print(token, settings.SECRET_KEY)
        payload = jwt.decode(token, settings.SECRET_KEY)
        print('payload', payload)
        user = Owner.objects.get(id=payload['owner_id'])
        print('user: ', user)
        if not user.is_verified:
            user.is_verified = True
            user.save()

        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = Owner.objects.all(id=payload['owner_id'])
            print('user: ', user)
            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({'email': 'Successfull activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'email': 'Activation link expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError as identifier:
            return Response({'email': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)