from os import stat
from django.db.models import expressions
from .models import Owner,Store
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import generics, status, views, permissions
from .serializers import EmailVerificationSerializer, RegisterSerializer, LoginSerializer, RequestPasswordResetEmailSerializer, \
                        SetNewPasswordSerializer, LogoutSerializer
from store.serializers import OwnerSerializer,StoreSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util


from core import serializers

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
        current_site = get_current_site(self.request).domain
        relative_link = reverse('email-verify')
        
        # absurl = 'http://' + str(current_site) + relative_link + '?token=' + str(token)
        print(str(current_site))
        print(relative_link)
        absurl = 'http://localhost:3000/' + str(token)

        email_body = 'Hi ' + user.username + ', use below link to verify your email for shopease store \n' + str(absurl)

        data = {'email_body': email_body, 'email_subject': 'Verify your email', 'to_email': user.email}
        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def getUser():
    owner = Owner.objects.all()
    ownerList = OwnerSerializer(owner, many = True)
    return Response(ownerList.data)

 
@api_view(['GET'])
def getOwnerByEmail(request, email):
    
    try: 
        owner = Owner.objects.get(email=email) 
        owner_by_email = OwnerSerializer(owner, many = False)
    except Owner.DoesNotExist: 
        return JsonResponse({'message': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    return Response(owner_by_email.data, status=status.HTTP_200_OK)
 

class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, None)

            user = Owner.objects.get(id=payload['user_id'])
            
            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({'email': 'Successfully verified email and activated account'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'email': 'Activation link expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError as identifier:
            print(identifier)
            return Response({'email': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        user = Owner.objects.get(email=serializer.data['email'])
        
        data = dict(serializer.data)
        data['id'] = user.id
        
        try:
            store_flag = Store.objects.get(ownerId=user.id)
        except:
            store_flag = None
            
        if store_flag:
            data['store_flag'] = True
        else:
            data['store_flag'] = False

        return Response(data, status=status.HTTP_200_OK)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = RequestPasswordResetEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        # data = {'request': request, 'data': request.data}
        email = request.data.get('email', '')

        if Owner.objects.filter(email=email).exists():
            user = Owner.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relative_link = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            
            # absurl = 'http://' + str(current_site) + relative_link

            absurl = 'http://localhost:3000/' + relative_link

            email_body = 'Hello, \n use below link to reset your password \n' + str(absurl)

            data = {'email_body': email_body, 'email_subject': 'Reset your password', 'to_email': user.email}
            Util.send_email(data)

            return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        
        return Response({'failure': 'This email does not exist.'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):

    def get(self, request, uidb64, token):
        
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = Owner.objects.get(id=id)


            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one.'}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({'success': True, 'message': 'Credentials', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator.check_token(user):
                return Response({'error': 'Token is not valid, please request a new one.'}, status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
