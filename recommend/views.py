# -*- coding: utf-8 -*-
import requests
from requests_toolbelt import MultipartEncoder
import json

from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status

from .serializers import TeamSerializer
from .models import Team
from .algorithms import crawling, insertTeamAndMenu
from osyulraeng import settings
from django.shortcuts import render
from django.http import JsonResponse

import jwt, datetime
import bcrypt
import traceback
def saveTeamAndMenu():
    team_list = Team.objects.all()
    serializer = TeamSerializer(team_list, many=True)
    insertTeamAndMenu(serializer.data, 0, 0)
    # print('efjoiewjfoi')
    # aligo()

@api_view(['GET'])
def teamList(request):
    payload = tokenCheck(request)
    team_list = Team.objects.all()
    serializer = TeamSerializer(team_list, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def todayCafeteria(request): # 해결
    return JsonResponse({'today_cafetria': crawling().split(', ')}, json_dumps_params={'ensure_ascii': False}, status=200)


def tokenCheck(request):
    # token = request.COOKIES.get('jwt')
    token = request.headers['token']
    if not token: raise Response(status=status.HTTP_401_UNAUTHORIZED)
    try: return jwt.decode(token, settings.JWT_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError: raise Response(status=status.HTTP_401_UNAUTHORIZED)