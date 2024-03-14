from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.contrib.sessions.models import Session
from ckeditor.fields import RichTextField

import uuid
# Create your models here.

class categories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100000)
    slug = models.SlugField(unique=True)
    image = models.ImageField()
    description = models.TextField()

    def __str__(self):
        return self.name

class products(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000000)
    image = models.ImageField()
    slug = models.SlugField(unique=True,blank=True)
    price = models.IntegerField()
    discounted_price = models.IntegerField(null=True,blank=True)
    category = models.ForeignKey('categories',on_delete=models.CASCADE)
    description = models.TextField()
    quantity = models.IntegerField()
    added_on = models.DateTimeField(auto_now_add=True)
    eligible_for_cod = models.BooleanField()
    enable_sample = models.BooleanField()
    specifications = RichTextField()
    warranty_info = RichTextField()
    shipping_info = RichTextField()


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(products, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class productImages(models.Model):
    image = models.FileField()
    product = models.ForeignKey(products,on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name


class cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.first_name

class cartItem(models.Model):
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey('cart',on_delete=models.CASCADE)
    product = models.ForeignKey('products',on_delete=models.CASCADE)
    quantity = models.IntegerField()
    added_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.cart.user.email+" "+self.product.name +" "+ str(self.quantity) +" " +str(self.added_on)


class guestCart(models.Model):
    id = models.AutoField(primary_key=True)
    session = models.ForeignKey(Session,on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.session.session_key
    
class guestCartItems(models.Model):
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey('guestCart',on_delete=models.CASCADE)
    product = models.ForeignKey('products',on_delete=models.CASCADE)
    quantity = models.IntegerField()
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.cart.session.session_key +" "+ self.product.name + " "+str(self.quantity)

class temporaryLoginData(models.Model):
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(guestCart,on_delete=models.CASCADE,related_name="Tempcart")
    session = models.ForeignKey(Session,on_delete=models.SET_NULL,null=True)

    def __str__(self) -> str:
        return self.session.session_key
    
# class orders(models.Model):
#     id = models.AutoField(primary_key=True)
#     product = models.ForeignKey('products',on_delete=models.CASCADE)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,)
#     created_on = models.DateTimeField()
#     invoice = models.FileField(blank=True,null=True)

#     def __str__(self):
#         return self.product.name + self.user.first_name

class blogs(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=10000)
    slug = models.SlugField(unique=True,max_length=10000,blank=True,null=True)
    content = RichTextField()
    image = models.ImageField(blank=True, null=True)
    publish_on = models.DateField()
    meta_description = models.TextField(max_length=10000, null=True, blank=True)
    meta_keywords = models.TextField(max_length=10000, null=True, blank=True)
    meta_author = models.TextField(max_length=10000, null=True, blank=True)
    show_on_homepage = models.BooleanField()
    is_page = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(blogs, self).save(*args, **kwargs)



    def __str__(self):
        return self.title




    
class reviews(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey('products',on_delete=models.CASCADE)
    review_description = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.CharField(max_length=1)
    created_on = models.DateTimeField()


    def __str__(self):
        return self.product.name + self.review_description


class highlights(models.Model):
    choices = (
        ( "btn btn-danger",'red'),
        ("btn btn-primary","blue"),
         ("btn btn-success","green"),
          ("btn btn-default","white"),
           ("btn btn-info","sky blue"),
           ("btn btn-secondary","Grey"),

    )
    
    id = models.AutoField(primary_key=True)
    link = models.TextField()
    highlight_heading = models.CharField(max_length=10000000)
    highlight_description = models.TextField()
    highlight_image = models.FileField()
    background_color = models.CharField(max_length=100000)
    text_color = models.CharField(max_length=10000)
    description_color = models.CharField(max_length=100)
    image_orientation_on_left = models.BooleanField()
    button_color = models.CharField(choices = choices,max_length=100000)


    def __str__(self):
        return self.highlight_heading







class vouchers(models.Model):
    id = models.AutoField(primary_key=True)
    voucher_code = models.CharField(max_length=100)
    discount_price = models.IntegerField()
    minimum_amount = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField()


    def __str__(self):
        return self.voucher_code

class applied_vouchers(models.Model):
    id = models.AutoField(primary_key=True)
    voucher = models.ForeignKey('vouchers',on_delete=models.CASCADE)
    applied_on = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    previous_price = models.IntegerField()
    after_price = models.IntegerField()
    payment_done = models.BooleanField()


    def __str__(self):
        return self.voucher.voucher_code +" used by ".upper()+ self.user.first_name.upper()



class pincodes(models.Model):
    id = models.AutoField(primary_key=True)
    pincode = models.IntegerField()
    state = models.CharField(max_length=1000)
    village  = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    sub_district = models.CharField(max_length=100)


    def __str__(self):
        return str(self.pincode ) + self.district + self.sub_district
    

class orders(models.Model):
    raw_id_field = ['user','postal']
    list_select_related = ['user','postal']
    status_codes = [
        ("CONFIRMED", "CONFIRMED"),
        ("NOT CONFIRMED","NOT CONFIRMED"),
        ("SHIPPED","SHIPPED"),
        ("DELIVERED","DELIVERED"),
        ("OUT FOR DELIVERY","OUT FOR DELIVERY"),
        ("CANCELED","CANCELED"),
        ("REFUND INITIATED","REFUND INITIATED"),
        ("REFUNDED", "REFUNDED"),
    ]
    payment_mode = (
        ("CASH ON DELIVERY","CASH ON DELIVERY"),
    )
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    order_id = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=1000)
    address = models.TextField()
    contact = models.CharField(max_length=100)
    email = models.EmailField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=1000)
    postal = models.ForeignKey('pincodes',on_delete=models.CASCADE)
    tax = models.IntegerField()
    status = models.CharField(choices=status_codes,max_length=10000)
    total_amount = models.IntegerField()
    discount = models.IntegerField()
    tracking_id = models.CharField(max_length=1000,null=True,blank=True)
    tracking_link = models.CharField(max_length=1000,null=True,blank=True)
    payment_status = models.BooleanField(default=False)
    order_string = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.order_id) +"    "+ str(self.user) + "    " + self.name + "    " + str(self.total_amount) +"   "+ str(self.created_at)



class payments(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4,blank=True, null=True)
    order = models.ForeignKey('orders',on_delete=models.CASCADE)
    payment_status = models.BooleanField(null=True,blank=True)  # signifies status in phonepe
    code = models.CharField(max_length=1000,null=True,blank=True)
    message = models.TextField(null=True,blank=True)
    merchantTransactionId = models.CharField(max_length=1000,null=True,blank=True)
    phonepeTransactionId = models.CharField(max_length=1000,null=True,blank=True)
    phonepeReferenceId = models.CharField(max_length=1000,null=True,blank=True)
    merchantId = models.CharField(max_length=1000,null=True,blank=True)
    redirectInfo = models.TextField(null=True,blank=True)
    amount = models.IntegerField(null=True,blank=True)
    paymentViaCOD = models.BooleanField(null=True,blank=True)

    def __str__(self):
        return str(self.order.id) + str(self.payment_status)
        
class invoices(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey('orders',on_delete=models.CASCADE)
    invoice_id = models.CharField(max_length=100000)
    date_of_generation = models.DateTimeField(auto_now_add=True)
    invoice_file = models.FileField(blank=True,null=True)

class order_items(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey('orders',on_delete=models.CASCADE)
    product = models.ForeignKey('products',on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_at_bought = models.IntegerField()
    original_price = models.IntegerField()
    voucher_applied = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order)+ self.product.name+ str(self.quantity)
    
class newsletter(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    subscribed = models.BooleanField()

    def __str__(self):
        return str(self.email) + str(self.subscribed)
    


class contact_query(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)
    email = models.EmailField(max_length=100)
    message = models.TextField()
    contact_no = models.CharField(max_length=1000)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name +" "+ self.message
    
    
    
class global_properties(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.CharField(max_length=1000)
    value = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.property+" "+ self.value
        
class highlighted_products(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey('products',on_delete=models.CASCADE)
    show_on_home_page = models.BooleanField() 
    
    def __str__(self):
        return self.product.name + str(self.show_on_home_page)



        
