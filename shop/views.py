from django.shortcuts import render
import stripe
from rest_framework import status

from shop.utility import generateOrderId
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from django.http import JsonResponse
# Create your views here.



stripe.api_key = settings.STRIPE_SECRET_KEY




@api_view(['GET'])
@permission_classes([AllowAny])
def getProducts(request):
    obj = products.objects.all()
    serializer = productsSerializer(obj,many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def getCategories(request):
    obj = categories.objects.all()
    serializer = categoriesSerializer(obj,many=True)
    return Response(serializer.data)

@api_view(['GET',])
@permission_classes([AllowAny])
def getHighlights(request):
    obj = highlights.objects.all()
    serializer = highlightsSerializer(obj,many=True)
    print(obj)
    return Response(serializer.data)

@api_view(['GET',])
@permission_classes([AllowAny])
def getProductImageBySlug(request,slug):
    obj = productImages.objects.filter(product = products.objects.get(slug=slug))
    serializer = productImageSerializer(obj,many=True)
    return Response(serializer.data)

@api_view(['GET',])
@permission_classes([AllowAny])
def getBlogs(request):
    obj = blogs.objects.all()
    serializer = blogsSerializer(obj,many=True)
    print(serializer.data)
    return Response(serializer.data)

@api_view(['GET',])
@permission_classes([AllowAny])
def getHighlightedProducts(request):
    obj = highlighted_products.objects.all()
    serializer = highlighted_productsserializer(obj,many=True)
    print(serializer.data)
    return Response(serializer.data)


@api_view(['GET',])
@permission_classes([AllowAny])
def getProductBySlug(request,slug):
    obj = products.objects.get(slug=slug)
    serializer = productsSerializer(obj,many=False)
    return Response(serializer.data)




@api_view(['GET'])
@permission_classes([AllowAny])
def checkProductAvailability(request,slug):
    obj = products.objects.get(slug=slug)
    if(obj.quantity>=1):
        return JsonResponse({"message":True,"code":200})
    else:
        return JsonResponse({"message":False,"code":"200"})
    

@api_view(['POST'])
@permission_classes([AllowAny])
def giveCartData(request):
    if(request.method == 'POST'):
        print(request.data)
        dataDict = request.data
        mainResponseObject = {}
        responseObject = []
        for i in dataDict.keys():
            print(i)
            productObj = products.objects.get(slug=i)
            serializer = productsSerializer(productObj,many=False)
            responseObject.append({
                "product_details": serializer.data,
                "requested_quantity" : request.data[i]
            })
        mainResponseObject['TAX'] = 100;
        mainResponseObject['data'] = responseObject
        return Response(mainResponseObject)

    # return Response([{"message":"all good"}])

@api_view(['POST'])
@permission_classes([AllowAny])
def placeOrder(request):
    if(request.method == 'POST'):
        # print(request.data)
        shipping_info = request.data['shipping_info']
        cart_data = request.data['cart_data']
        total_payable = request.data['total_payable']
        discount = request.data['discount']
        overall = request.data['overall']
        tax = request.data['tax']
        voucher = request.data['voucher']

        obj = orders(
            order_id = generateOrderId(),
            name = shipping_info['full_name'],
            address = shipping_info['address'],
            contact = shipping_info['contact'],
            email = shipping_info['email'],
            country = shipping_info['country'],
            city = shipping_info['city'],
            state = shipping_info['state'],
            postal = pincodes.objects.get(pincode=shipping_info['postal']),
            tax = tax,
            status = "CONFIRMED",
            total_amount = total_payable,
            discount = discount,
            payment_status=False,
        )
        obj.save()

        print("keys", cart_data)
        
        for i in cart_data:
            print("\n\n\cart \n\n\n",i)
            if(i['details']['discounted_price'] !=0):
                price_at_bought_value = i['details']['discounted_price']
            else:
                price_at_bought_value = i['details']['price']
            
            if(voucher!=None):
                voucher_flag = True
            else:
                voucher_flag = False
            order_items(
                order=obj,
                product = products.objects.get(id = i['details']['id']),
                quantity = i['quantity'],
                price_at_bought = price_at_bought_value,
                original_price = i['details']['price'],
                voucher_applied = voucher_flag
            ).save()
        # try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': total_payable,
                        'quantity': 1,
                    },
                ],
                payment_method_types=['card',],
                mode='payment',
                success_url=settings.SITE_URL + '/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.SITE_URL + '/?canceled=true',
            )

            return Response(checkout_session.url)
        # except:
        #         print("error")
        #         return Response(
        #             {'error': 'Something went wrong when creating stripe checkout session'},
        #             status=status.HTTP_500_INTERNAL_SERVER_ERROR
        #         )
        return Response({'msg':"success"})
    

@api_view(['POST'])
@permission_classes([AllowAny])
def contact(request):
    if request.method == 'POST':
        email = request.data['email']
        contact = request.data['contact_number']
        message = request.data['message']
        name = request.data['name']
        country = request.data['country']
        contact_query(
            name=name,
            email=email,
            message=message,
            country=country,
            contact_no = contact
        ).save()
        return Response({'msg':"success"})
    

@api_view(['GET'])
@permission_classes([AllowAny])
def getProductsByCategory(request,slug):
    obj= products.objects.filter(category = categories.objects.get(slug=slug))
    serializer = productsSerializer(obj,many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def getBlogsBySlug(request,slug):
    obj = blogs.objects.get(slug=slug)
    serializer = blogsSerializer(obj,many=False)
    return Response(serializer.data)