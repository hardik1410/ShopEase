from django.urls import path
from django.conf.urls import url
from product import views
from .views import getProduct, addProduct, updateProduct, deleteProduct

urlpatterns = [
    url(r'getProduct/', views.getProduct),
    url(r'addProduct/', views.addProduct),
    url(r'updateProduct/', views.updateProduct),
    url(r'deleteProduct/(?P<productId>[0-9]+)$', views.deleteProduct),
    url(r'getProductByStoreId/(?P<storeId>[0-9]+)$',
        views.getProductByStoreId),
    url(r'getProductByCategoryId/(?P<categoryId>[0-9]+)$',
        views.getProductByCategoryId),

]
