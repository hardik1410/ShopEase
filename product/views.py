from django.shortcuts import render
from core.models import Product, Category, Store
from .serializers import ProductSerializer, CategorySerializer, StoreSerializer
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from datetime import date

# Create your views here.


@api_view(['GET'])
def getProduct(request):
    product = Product.objects.all()
    products = [x for x in product if x.thruDate > date.today()]
    productList = ProductSerializer(products, many=True)
    return Response(productList.data)


@api_view(['GET'])
def getStore(storeId):
    store = Store.objects.get(storeId=storeId)
    store_serializer = StoreSerializer(store, many=False)
    return Response(store_serializer.data)


@api_view(['GET'])
def getCategory(categoryId):
    category = Category.objects.get(categoryId=categoryId)
    category_serializer = CategorySerializer(category, many=False)
    return Response(category_serializer.data)


@api_view(['GET'])
def getProductByStoreId(request, storeId):
    z = storeId
    try:
        product = Product.objects.filter(storeId=z)
    except:
        product = None
    productList = [x for x in product if x.thruDate > date.today()]
    product_data = ProductSerializer(productList, many=True)
    if product:
        return Response(product_data.data)
    return Response({"message": "No products exist."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def getProductByCategoryId(request, categoryId):
    try:
        product = Product.objects.get(categoryId=categoryId)
    except:
        product = None
    product_data = ProductSerializer(product, many=False)
    if product:
        return Response(product_data.data)
    return Response(product_data.data, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def addProduct(request):
    product_data = JSONParser().parse(request)
    product_data["thruDate"] = "2099-01-01"
    product_serializer = ProductSerializer(data=product_data)
    if product_serializer.is_valid():
        product_serializer.save()
        return JsonResponse(product_serializer.data)
    return JsonResponse(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def updateProduct(request):
    product = Product.objects.get(productId=request.data["productId"])
    product_serializer = ProductSerializer(product, data=request.data)
    if product_serializer.is_valid():
        product_serializer.save()
        return JsonResponse(product_serializer.data)
    return JsonResponse(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def deleteProduct(request, productId):
    try:
        product = Product.objects.get(productId=productId)
    except:
        product = None
    if(product):
        product.thruDate = date.today()
        product.save()
        return Response({"message": "Deleted Product Successfully !"})
    else:
        return Response({"message": "No such product exist"}, status=status.HTTP_400_BAD_REQUEST)
