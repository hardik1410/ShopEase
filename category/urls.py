from django.urls import path
from django.conf.urls import url
from category import views
from .views import getCategory, addCategory, updateCategory, deleteCategory

urlpatterns = [
    url(r'getCategory/', views.getCategory),
    url(r'addCategory/', views.addCategory),
    url(r'updateCategory/', views.updateCategory),
    url(r'deleteCategory/', views.deleteCategory),
    url(r'getCategoryByStoreId/(?P<storeId>[0-9]+)$',
        views.getCategoryByStoreId),

]
