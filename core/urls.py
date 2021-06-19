from django.urls import path
from django.conf.urls import url
from core import views
from .views import RegisterView, VerifyEmail, LoginAPIView, getUser, getOwnerByEmail
from django.conf.urls import include

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
    url(r'getUser/', views.getUser),
    url(r'getOwnerByEmail/', views.getOwnerByEmail),
    path('store/', include('store.urls')),
    path('category/', include('category.urls')),
]
