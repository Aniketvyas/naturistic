from django.conf import settings
from rest_framework import serializers
from shop.models import *
from accounts.serializers import *
# from datamanager.serializers import departmentSerializer, facultySerializer, batchSerializer


class categoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = categories
        fields = '__all__'


class productsSerializer(serializers.ModelSerializer):
    category = categoriesSerializer()
    class Meta:
        model = products
        fields = '__all__'

class productImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=productImages
        fields = '__all__'
    
class cartSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = cart
        fields = '__all__'

class cartItemSerializer(serializers.ModelSerializer):
    product = productsSerializer()
    cart = cartSerializer
    class Meta:
        model = cartItem
        fields = '__all__'

    
class guestCartSerializer(serializers.ModelSerializer):
    product = productsSerializer()
    cart = cartSerializer
    class Meta:
        model = guestCart
        fields = '__all__'
        


class blogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = blogs
        fields = '__all__'

class highlightsSerializer(serializers.ModelSerializer):
    # product = productsSerializer()
    class Meta:
        model = highlights
        fields = '__all__'


        

class vouchersSerializer(serializers.ModelSerializer):
    product = productsSerializer()
    class Meta:
        model = vouchers
        fields = '__all__'
        

class applied_vouchersSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    voucher = vouchersSerializer()
    class Meta:
        model = applied_vouchers
        fields = '__all__'

        

class pincodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = pincodes
        fields = '__all__'

        

class ordersSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    postal = pincodesSerializer()
    class Meta:
        model = orders
        fields = '__all__'

        


class paymentsSerializer(serializers.ModelSerializer):
    order = ordersSerializer()
    postal = pincodesSerializer()
    class Meta:
        model = payments
        fields = '__all__'
        

class invoicesSerializer(serializers.ModelSerializer):
    order = ordersSerializer()
    class Meta:
        model = invoices
        fields = '__all__'

        

class order_itemserializer(serializers.ModelSerializer):
    order = ordersSerializer()
    product = productsSerializer()
    class Meta:
        model = order_items
        fields = '__all__'



class highlighted_productsserializer(serializers.ModelSerializer):
    product = productsSerializer()
    class Meta:
        model = highlighted_products
        fields = '__all__'