# -*- coding: utf-8 -*-
import requests

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .serializers import TeamSerializer
from .models import Team
from .algorithms import crawling, insertTeamAndMenu, aligo
from osyulraeng import settings
import jwt, datetime
from bs4 import BeautifulSoup as bs
import re

def saveTeamAndMenu():
    if isHoliday():
        team_list = Team.objects.all()
        serializer = TeamSerializer(team_list, many=True)
        insertTeamAndMenu(serializer.data, 0, 1) # 랜덤
    
    # if week in ['월','목']:
    #     print(f'오늘은 {week}요일이므로 부서별 인원으로 팀이 선택됩니다.')
    #     insertTeamAndMenu(serializer.data, 1, 1) # 부서별
    # elif week in ['화','수','금']:
    #     print(f'오늘은 {week}요일이므로 랜덤 인원으로 팀이 선택됩니다.')
    #     insertTeamAndMenu(serializer.data, 0, 1) # 랜덤

@api_view(['GET'])
def teamList(request):
    payload = tokenCheck(request)
    team_list = Team.objects.all()
    serializer = TeamSerializer(team_list, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def todayCafeteria(request): # 해결
    response = Response()
    response.data = crawling()
    return response


@api_view(['GET'])
def test(request): # 해결
    aligo([[7]])
    # response = Response()
    # response.data = crawling()
    return {1}

def tokenCheck(request):
    # token = request.COOKIES.get('jwt')
    token = request.headers['token']
    if not token: raise Response(status=status.HTTP_401_UNAUTHORIZED)
    try: return jwt.decode(token, settings.JWT_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError: raise Response(status=status.HTTP_401_UNAUTHORIZED)

def isHoliday():
    today = datetime.datetime.today()
    url = settings.HOLIDAY_URL
    params ={
            'serviceKey' : settings.HOLIDAY_KEY, 
            'solYear' : str(today.year), 
            'solMonth' : str(f'{today.month:02d}') 
            }

    response = requests.get(url, params=params)
    if str(today).split()[0].replace('-','') in re.findall('\<locdate\>(\d+)\<\/locdate\>', str(bs(response.content, 'html.parser'))):
        return True
    if ['월','화','수','목','금','토','일'][today.weekday()] in ['토','일']:
        return True
    
    return False
