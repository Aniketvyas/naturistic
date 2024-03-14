from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import *
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

class CustomAuthToken(ObtainAuthToken):
    def post(self,request,**kwargs):
        # print(request.POST,request.data,request)
        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user= Token.objects.get(key=token.key).user
        print(user.groups,user)
        group = GroupsSerializer(user.groups.all(),many=True,context={'request':None})
        print(group.data)
        sinfo = UserSerializer(user, context={'request': None})
        loda = {
            'token': token.key,

        }
        return Response(loda)