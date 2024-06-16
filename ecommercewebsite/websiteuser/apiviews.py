from django.shortcuts import render
from django.shortcuts import render,redirect

from django.views.decorators.cache import cache_control
from website.models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import get_user
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import (EmailMessage, EmailMultiAlternatives,
                              get_connection, send_mail)
import os
import json
import math
import random
from django.contrib.auth.hashers import make_password,PBKDF2PasswordHasher,pbkdf2
# for rest_framework 
from rest_framework.response import Response 
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status

### for token ###
from rest_framework.authtoken.views  import ObtainAuthToken
from  rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

#  for serializers
from .serializers import userserializer
@api_view(['POST'])
def adduser(request):
    name=request.data.get('name')
    email=request.data.get('email')
    phone=request.data.get('phone')
    password=request.data.get('password')
    if User.objects.filter(phone=phone).exists():
        return Response("Phone Number already exist")
    elif User.objects.filter(email=email).exists():
        return Response("email already exist")
    else:
        u=User.objects.create_user(username=name,email=email,phone=phone,password=password)
        ad=User.objects.filter(phone=phone).values()
        serializer=userserializer(ad,many=True)
        return Response(serializer.data)
    
@api_view(['POST'])
def apilogin(request):
   if request.method=="POST":
       em=request.data.get('email')
       ps=request.data.get('password')
       if not em or not ps:
           return Response("Phone Number and Password Required")
       user=authenticate(request,email=em,passwors=ps)
       if not user.is_superuser:
             login(request,user)
             serial_data=userserializer(user)
             return Response({'Message' :'Login successful.','user':serial_data.data})
       else:
             return Response({'erroe':'Invalid phone number or password.'},status=401)
          