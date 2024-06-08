from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# from django.shortcuts import get_object_or_404
# from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
# Create your views here.

@api_view(['GET'])
def home(request):
    # Check token in local storage of browser
    check_token = request.COOKIES.get('token')
    try :
        token = Token.objects.get(key=check_token)
        template = loader.get_template('home.html')
        return HttpResponse(template.render())
    except Token.DoesNotExist:
        template = loader.get_template('login.html')
        return HttpResponse(template.render())

@api_view(['GET'])
def node_status(request):
    # Check token in local storage of browser
    check_token = request.COOKIES.get('token')
    try :
        token = Token.objects.get(key=check_token)
        template = loader.get_template('node_status.html')
        return HttpResponse(template.render())
    except Token.DoesNotExist:
        template = loader.get_template('login.html')
        return HttpResponse(template.render())