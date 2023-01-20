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

from django.shortcuts import render
from django.http import JsonResponse

import jwt, datetime
import bcrypt

# Create your views here.
@api_view(['GET'])
def teamList(request):
    payload = tokenCheck(request)
    team_list = Team.objects.all()
    serializer = TeamSerializer(team_list, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def saveTeamAndMenu(request):
    payload = tokenCheck(request)
    team_list = Team.objects.all()
    serializer = TeamSerializer(team_list, many=True)
    insertTeamAndMenu(serializer.data, request.data['team'], request.data['menu'])
    # aligo()
    return Response(status=status.HTTP_200_OK)

"""
{
    'header': {
                'token': token,
                }
    'body': {
                'team': [1, 2] # [팀선정방식, 몇팀으로 나눌지]
                'menu': 1
            }
}

filter(string__contains='pattern')
"""

@api_view(['GET'])
def todayCafeteria(request): # 해결
    # print('호잇', request.META['HTTP_TOKEN']) # header: token
    # print('team=', request.data['team'], 'menu=', request.data['menu'])
    return JsonResponse({'today_cafetria': crawling().split(', ')}, json_dumps_params={'ensure_ascii': False}, status=200)


def tokenCheck(request):
    token = request.COOKIES.get('jwt')
    if not token: raise Response(status=status.HTTP_401_UNAUTHORIZED)
    try: return jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError: raise Response(status=status.HTTP_401_UNAUTHORIZED)


# def check(request):
#     token = request.COOKIES.get('jwt')

#     if not token:
#         raise AuthenticationFailed('Unauthenticated')

#     try:
#         return jwt.decode(token, 'secret', algorithms=['HS256'])

#     except jwt.ExpiredSignatureError:
#         raise AuthenticationFailed('Unauthenticated')

# ================================================================== 대량 문자 보낼 때 필수 key값
# API key, userid, sender, rec_1, msg_1, cnt, msg_type	
# API키, 알리고 사이트 아이디, 발신번호, 수신번호, 문자내용, 메세지 전송건수, [SMS(단문) , LMS(장문), MMS(그림문자) 구분]


"""
[랜덤] 그룹:
- 1
- 2
- 3
[랜덤] 그룹:
- 1
- 2
- 3
학식정보,

[웹사이트 바로가기]
"""
def aligo():
    ALIGO_APIKEY = 'h92swsbnn03venz0z5ubo8hnk0l6mn3q'
    ALIGO_USERID = 'koco4277'
    ALIGO_SENDERKEY = '4509ad36e2388e6e9cfbf5cc899bdf2b2cd1c894'
    ALIGO_TOKEN = 'fb0ad9141988474e0083d3af2c88bca954a61375e4985b1c1b32bf35ed95f2c9d21d0b919bb2c17b90ca698010456269786380e15761b25fb37ce23f1d6534c2Er3hs6Q4X8xt80NqsT4YT97P1+0wkkgUWBY45VLpkrmbh3LCs+jerYld2AGso9zfk6U3ivCBZ6hoNHJRpYA0AA=='
    ALIGO_SENDER = '1566-4515'
    template_code = 'TL_4008'
    basic_send_url = 'https://kakaoapi.aligo.in/akv10/alimtalk/send/'
    button_info = json.dumps({'button': [{'name':'name', # 버튼명
                            'linkType':'MD', # DS, WL, AL, BK, MD
                            'linkTypeName' : '메시지전달', # 배송조회, 웹링크, 앱링크, 봇키워드, 메시지전달 중에서 1개
                            #'linkM':'mobile link', # WL일 때 필수
                            #'linkP':'pc link', # WL일 때 필수
                            #'linkI': 'IOS app link', # AL일 때 필수
                            #'linkA': 'Android app link' # AL일 때 필수
                    }]})
    
    sms_data = {
                'apikey': ALIGO_APIKEY, #api key
                'token': ALIGO_TOKEN,
                'userid': ALIGO_USERID, # 알리고 사이트 아이디
                'sender': ALIGO_SENDER, # 발신번호
                'senderkey': ALIGO_SENDERKEY,
                'tpl_code': template_code,
                'subject_1': '당신의 테이블입니다.',
                # 'emtitle_1': '당신의 테이블입니다.',
                'button_1': button_info,
                'receiver_1': '01048703170',
                'message_1': 'test'
              }
    m = MultipartEncoder(fields=sms_data)
    headers = {"Content-Type" : 'multipart/form-data'}

    alimtalk_send_response = requests.post(basic_send_url, headers=headers, data=m)
    return alimtalk_send_response.json()