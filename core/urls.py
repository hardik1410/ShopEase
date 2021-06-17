from django.urls import path
from django.conf.urls import url 
from core import views
from .views import RegisterView, getUser, getStore , getOwnerByEmail

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    url(r'getUser/', views.getUser),
    url(r'getStore/', views.getStore),
    url(r'getOwnerByEmail/', views.getOwnerByEmail),
    
]