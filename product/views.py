from django.shortcuts import render
from core.models import Product, Category, Store, Order, OrderProduct
from .serializers import OrderPSerializer, ProductSerializer, CategorySerializer, StoreSerializer, OrderProductSerializer, OrderSerializer
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from datetime import date
from django.forms.models import model_to_dict

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


@api_view(['GET'])
def getOrders(request):
    try:
        order = Order.objects.get(customerId=81)
    except:
        order = None

    orders = OrderSerializer(order, many=False)

    products = OrderProduct.objects.filter(orderId=orders.data['orderId'])

    all_products = OrderProductSerializer(products, many=True)

    print(all_products.data)

    res = orders.data.copy()

    res['products'] = all_products.data
    print(res)
    if orders:
        return Response(res)

    return Response({"message": "No orders exist for this customer."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def getOrderByStoreId(request, storeId):
    z = storeId
    try:
        orders = OrderProduct.objects.filter(storeId=z)
    except:
        orders = None
    #orderList = [x for x in orders if x.thruDate > date.today()]
    order_data = OrderProductSerializer(orders, many=True)
    if orders:
        return Response(order_data.data)
    return Response({"message": "No orders exists."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def getAllOrdersByProduct(request):
    orders = OrderProduct.objects.all()
    order_product_data = OrderProductSerializer(orders, many=True)
    return Response(order_product_data.data)


@api_view(['POST'])
def addOrder(request):
    order_data = JSONParser().parse(request)
    order_data["thruDate"] = "2099-01-01"
    order_serializer = OrderSerializer(data=order_data)
    if order_serializer.is_valid():
        order_serializer.save()
        return JsonResponse(order_serializer.data)
    return JsonResponse(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def placeOrder(request):
    order_data = JSONParser().parse(request)
    print(order_data["customerId"])
    order = {}
    if(order_data['customerId']):
        try:
            order["orderId"] = order_data['orderId']
            order["customerId"] = order_data['customerId']
            order["orderDate"] = datetime.now()
            order["orderType"] = order_data['orderType']
            order["OrderAmount"] = order_data['OrderAmount']
            order["status"] = order_data['status']
            order["paid"] = order_data['paid']
            order["creator"] = order_data['creator']
            order["created"] = date.today()
            order["modifier"] = order_data['modifier']
            order["modified"] = order_data['modified']
            order["fromDate"] = date.today()
            order["thruDate"] = "2099-01-01"
        except:
            order = None
        print(order)
        if(order):
            order_serializer = OrderSerializer(data=order, many=False)
            if order_serializer.is_valid():
                order_serializer.save()
            else:
                return JsonResponse(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            current_order = Order.objects.get(
                customerId=order['customerId'], orderDate=order['orderDate'], OrderAmount=order['OrderAmount'])
            order_id = current_order.orderId
            print(order_id)
    # addOrderProducts(order_data['products'])
    order_total = 0
    for product in order_data['products']:
        product['orderId'] = order_id
        order_total += (product['amount']*product['quantity'])
        product_serializer = OrderProductSerializer(data=product)

        if product_serializer.is_valid():
            product_serializer.save()
            flag = 1
        else:
            flag = 0
            break

    if flag == 1:
        try:
            fetch_order = Order.objects.get(orderId=order_id)
            order_serializer2 = OrderSerializer(fetch_order, many=False)
        except:
            fetch_order = None
        if(fetch_order):
            updated_order = fetch_order
            updated_order.OrderAmount = order_total
            order_serializer1 = OrderSerializer(
                fetch_order, data=model_to_dict(updated_order))
            if order_serializer1.is_valid():
                order_serializer1.save()
                return JsonResponse({'message': "order is placed."})
            else:
                return JsonResponse(order_serializer1.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': "order is not placed."})


@api_view(['PUT'])
def updateOrder(request):
    order = Order.objects.get(orderId=request.data["orderId"])
    order_serializer = OrderSerializer(order, data=request.data)
    if order_serializer.is_valid():
        order_serializer.save()
        return JsonResponse(order_serializer.data)
    return JsonResponse(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def deleteOrder(request, orderId):
    try:
        order = Product.objects.get(orderId=orderId)
    except:
        order = None
    if(order):
        order.thruDate = date.today()
        order.save()
        return Response({"message": "Deleted Product Successfully !"})
    else:
        return Response({"message": "No such product exist"}, status=status.HTTP_400_BAD_REQUEST)
