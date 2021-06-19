from django.shortcuts import render
from core.models import Store,Owner
from .serializers import StoreSerializer, OwnerSerializer
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from datetime import date
 
# Create your views here.

@api_view(['GET'])
def getStore(request):
    store = Store.objects.all()
    # stores = [x for x in store if x.thruDate < date.today()]
    storeList = StoreSerializer(store, many = True)
    return Response(storeList.data)


@api_view(['GET'])
def getOwner(ownerId):
    owner = Owner.objects.get(ownerId=ownerId)
    owner_serializer = OwnerSerializer(owner,many=False)
    

@api_view(['GET'])
def getStoreByOwnerId(request,ownerId):

    try:
        store = Store.objects.get(ownerId = ownerId)
        
    except: 
        store = None
    store_data = StoreSerializer(store, many = False)
    if store:
        return Response(store_data.data)
    return Response(store_data.data,status  = status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def addStore(request):
    store_data = JSONParser().parse(request)
    store_serializer = StoreSerializer(data = store_data)
    if store_serializer.is_valid():
        store_serializer.save()
        return JsonResponse(store_serializer.data) 
    return JsonResponse(store_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['PUT'])
def updateStore(request):
    # ownerId = JSONParser().parse(request)
    # print(request.data)
    store = Store.objects.get(storeId= request.data["storeId"])
    store_serializer = StoreSerializer(store,data = request.data)
    if store_serializer.is_valid():
        store_serializer.save()
        return JsonResponse(store_serializer.data)  
    return JsonResponse(store_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
@api_view(['DELETE'])
def deleteStore(request):
    store = Store.objects.get(storeId= request.data["storeId"])
    store.thruDate = date.today()
    store.save()
    store_serializer = StoreSerializer(store,many = False)
    # store_serializer.save()
    return Response(store_serializer.data)


