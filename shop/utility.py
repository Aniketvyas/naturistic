import random
from shop.models import *;


def generateOrderId():
    count=0
    while(True):
        id = random.randint(111111,999999)
        if(orders.objects.filter(order_id = id).exists()):
            count+=1
        elif(count>=100):
            break
        else:
            return id