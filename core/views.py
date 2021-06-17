from core.models import Owner
from django.shortcuts import render
from rest_framework import generics, status
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Owner
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

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


class VerifyEmail(generics.GenericAPIView):
    def get(self):
        pass
