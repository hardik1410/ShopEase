from django.urls import path
from django.conf.urls import url 
from store import views
from .views import getStore, addStore, updateStore, deleteStore

urlpatterns = [
    url(r'getStore/', views.getStore),
    url(r'addStore/', views.addStore),
    url(r'updateStore/', views.updateStore),
    url(r'deleteStore/', views.deleteStore),
    
]