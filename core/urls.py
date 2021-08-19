from django.urls import path
from django.conf.urls import url 
from core import views 
from .views import  PasswordTokenCheckAPI, RegisterView, RequestPasswordResetEmail, VerifyEmail, LoginAPIView, \
                    SetNewPasswordAPIView, LogoutAPIView, getUser, getOwnerByEmail, ImageUpload, ImageDownload
from django.conf.urls import url
from core import views
from django.conf.urls import url
from core import views
from django.conf.urls import include
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(), name='request-reset-email'),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'),
    url(r'getUser/', views.getUser),
    url('getOwnerByEmail/', views.getOwnerByEmail),
    path('store/', include('store.urls')),
    path('product/', include('product.urls')),
    path('category/', include('category.urls')),
    url(r'^upload/$', ImageUpload.as_view(), name='file-upload'),
    url(r'download/(?P<productId>[0-9]+)$', ImageDownload.as_view(), name='file-download'),
]
