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

    week = ['월','화','수','목','금','토','일'][datetime.datetime.today().weekday()]
    
    if week in ['월','목']:
        print(f'오늘은 {week}요일이므로 부서별 인원으로 팀이 선택됩니다.')
        insertTeamAndMenu(serializer.data, 1, 1) # 부서별
    elif week in ['화','수','금']:
        print(f'오늘은 {week}요일이므로 랜덤 인원으로 팀이 선택됩니다.')
        insertTeamAndMenu(serializer.data, 0, 1) # 랜덤

@api_view(['GET'])
def teamList(request):
    payload = tokenCheck(request)
    team_list = Team.objects.all()
    serializer = TeamSerializer(team_list, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def todayCafeteria(request): # 해결
    response = Response()
    response.data = {
        'today_cafetria': crawling().split(', ')
    }
    return response


def tokenCheck(request):
    # token = request.COOKIES.get('jwt')
    token = request.headers['token']
    if not token: raise Response(status=status.HTTP_401_UNAUTHORIZED)
    try: return jwt.decode(token, settings.JWT_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError: raise Response(status=status.HTTP_401_UNAUTHORIZED)