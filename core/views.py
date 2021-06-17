from django.shortcuts import render
from rest_framework import generics, status
from .serializers import RegisterSerializer,OwnerSerializer,StoreSerializer
from rest_framework.response import Response
from .models import Owner,Store
from rest_framework.decorators import api_view
# Create your views here.

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, data):
        user = self.request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data

        return Response(user_data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def getUser(request):
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
 
 
# @api_view(['GET'])
# def getStore(request):
#     store = Store.objects.all()
#     storeList = StoreSerializer(store, many = True)
#     return Response(storeList.data)