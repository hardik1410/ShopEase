from django.shortcuts import render
from core.models import Category, Owner
from .serializers import StoreSerializer, CategorySerializer
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from datetime import date
# Create your views here.


@api_view(['GET'])
def getCategory(request):
    category = Category.objects.all()
    categoryList = CategorySerializer(category, many=True)
    return Response(categoryList.data)


@api_view(['GET'])
def getStore(storeId):
    store = Store.objects.get(storeId=storeId)
    owner_serializer = StoreSerializer(store, many=False)


@api_view(['GET'])
def getCategoryByStoreId(request, storeId):
    z = storeId
    try:
        category = Category.objects.filter(storeId=z)
    except:
        category = None
    categoryList = [x for x in category if x.thruDate > date.today()]
    category_serializer = CategorySerializer(categoryList, many=True)
    if category:
        return Response(category_serializer.data)
    return Response(category_serializer.data, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def addCategory(request):
    category_data = JSONParser().parse(request)
    category_data["thruDate"] = '2099-01-01'
    category_serializer = CategorySerializer(data=category_data)
    if category_serializer.is_valid():
        category_serializer.save()
        return JsonResponse(category_serializer.data)
    return JsonResponse(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def updateCategory(request):
    category = Category.objects.get(categoryId=request.data["categoryId"])
    category_serializer = CategorySerializer(category, data=request.data)
    if category_serializer.is_valid():
        category_serializer.save()
        return JsonResponse(category_serializer.data)
    return JsonResponse(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def deleteCategory(request, categoryId):
    try:
        category = Category.objects.get(categoryId=int(categoryId))
    except:
        category = None
    if(category):
        category.thruDate = date.today()
        category.save()
        #category_serializer = CategorySerializer(category, many=False)
        # product_serializer.save()
        return Response({"message": "Deleted Category Successfully !"})
    else:
        return Response({"message": "No such category exist"}, status=status.HTTP_400_BAD_REQUEST)
