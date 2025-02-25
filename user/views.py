from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer, MustFoodSerializer, PreferenceSerializer
from django.db.models import Q

from . import emails
from .models import Preference, MustFood

from recommend import models as rm
from recommend import serializers as rs

from store import models as sm
from store import serializers as ss
from store.views import addAverStoreRating

import jwt, datetime
import bcrypt
import requests
import traceback

from osyulraeng import settings

@api_view(['POST'])
def login(request):
    # print('header token: ', request.headers['token'])
    # print("hi: " , settings.LOGIN_API_ADDRESS)
    try:
        result = Response(requests.post(settings.LOGIN_API_ADDRESS, data={'manager_id': request.data['user_id'], 'password': request.data['password']})).status_code
        if result == 200:
            for user in eval(requests.get(url=settings.OE_WORKERS_API_ADDRESS, headers={'key': settings.OE_WORKERS_API_KEY}).text)['list']: 
                # print('user=',user)
                if user['id'] == request.data['user_id']:
                    payload = {
                    'id': user['idn'],
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(weeks=60),
                    'iat': datetime.datetime.utcnow()
                    }

                    token = jwt.encode(payload, settings.JWT_KEY, algorithm='HS256')
                    response = Response()
                    response.set_cookie(key='jwt', value=token, httponly=True, samesite=None)
                    response.data = {
                        'id': user['idn'],
                        'name': user['name'],
                        'department': user['department'],
                        'jwt': token
                    }
                    return response
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        return JsonResponse({'error': str(traceback.format_exc())})

@api_view(['GET'])
def cookie(request):
    try:
        print('header token: ', request.headers['token'])
        payload = tokenCheck(request)
        print(make_info()[payload['id']])
        # return JsonResponse(make_info()[payload['id']])

        response = Response()
        response.data = make_info()[payload['id']]
        return response

    except Exception as e:
        return JsonResponse({'error': str(traceback.format_exc())})
# filter(string__contains='pattern')
# q = Q(user_id=payload['id']) & Q(user_id=payload['id'])
@api_view(['GET'])
def myTeamAndMenu(request):
    try:
        payload = tokenCheck(request)
        my_list = rm.Team.objects.filter(date=int(str(datetime.date.today()).replace('-','')))
        serializer = rs.TeamSerializer(my_list, many=True)
        for user in serializer.data:
            team_memebers_id = [int(x) for x in user['team'].split(',')]
            team_menus_id = [int(x) for x in user['menu'].split(',')]
            if payload['id'] in team_memebers_id:
                # team_members_info = User.objects.filter(id__in=team_memebers_id)
                team_menus_info = sm.Info.objects.filter(id__in=team_menus_id)
                break
        members = make_info()
        team_member_list, team_menu_list = [], []
        # team_members_info = UserSerializer(team_members_info, many=True).data
        team_menus_info = addAverStoreRating(ss.InfoSerializer(team_menus_info, many=True))
        # print(team_menus_info)
        for id in team_memebers_id:
            team_member_list.append({'id': members[id]['id'], 'name': members[id]['name'], 'department': members[id]['department']})
        
        for menu in team_menus_info:
            team_menu_list.append({
                'id': menu['id'],
                'name': menu['name'],
                'category': menu['category'],
                'aver_price': menu['aver_price'],
                'arrival_time': menu['arrival_time'],
                'call_number': menu['call_number'],
                'location': menu['location'],
                'aver_rating': menu['aver_rating']
            })
        return JsonResponse({'team': team_member_list, 'menu': team_menu_list})

    except Exception as e:
        return JsonResponse({'error': str(traceback.format_exc())})

@api_view(['GET'])
def myFoodPreferenceList(request):
    try:
        payload = tokenCheck(request)
        my_list = Preference.objects.filter(user_id=payload['id'])
        serializer = PreferenceSerializer(my_list, many=True)
        return Response(serializer.data)

    except Exception as e:
        return JsonResponse({'error': str(traceback.format_exc())})

@api_view(['POST'])
def insertFoodPreference(request):
    try:
        payload = tokenCheck(request)
        request.data['user_id'] = payload['id']
        print('request:', request.data)
        serializer = PreferenceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

        q = Q(user_id=payload['id']) & Q(preference=request.data['preference']) & Q(category=request.data['category'])
        temp = Preference.objects.filter(q)
        serializer = PreferenceSerializer(temp, many=True)
        # print(serializer.data)

        return Response(serializer.data[0])

    except Exception as e:
        return JsonResponse({'error': str(traceback.format_exc())})
    
    # return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteFoodPreference(request):
    try:
        payload = tokenCheck(request)
        Preference.objects.filter(id=request.data['id']).delete()
        return Response(status=status.HTTP_200_OK)

    except Exception as e:
        return JsonResponse({'error': str(traceback.format_exc())})

@api_view(['GET'])
def myMustFoodList(request):
    try:
        payload = tokenCheck(request)
        q = Q(user_id=payload['id']) & Q(date=int(str(datetime.date.today()).replace('-','')))
        my_list = MustFood.objects.filter(q)
        serializer = MustFoodSerializer(my_list, many=True)
        return Response(serializer.data)

    except Exception as e:
        return JsonResponse({'error': str(traceback.format_exc())})

@api_view(['POST'])
def insertMustFood(request):
    try:
        payload = tokenCheck(request)
        request.data['user_id'] = payload['id']
        request.data['date'] = int(str(datetime.date.today()).replace('-',''))

        try: 
            q = Q(user_id=payload['id']) & Q(date=request.data['date']) & Q(preference=request.data['preference'])
            MustFood.objects.filter(q).delete()
        except: 
            pass

        serializer = MustFoodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            q = Q(user_id=payload['id']) & Q(preference=request.data['preference']) & Q(category=request.data['category'])
            temp = MustFood.objects.filter(q)
            serializer = MustFoodSerializer(temp, many=True)

            return Response(serializer.data[0])

        return Response(status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return JsonResponse({'error': str(traceback.format_exc())})

@api_view(['PUT'])
def updateMustFood(request):
    try:
        payload = tokenCheck(request)
        rating = MustFood.objects.get(id=request.data['id'])
        serializer = MustFoodSerializer(instance=rating, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return JsonResponse({'error': str(traceback.format_exc())})

@api_view(['DELETE'])
def deleteMustFood(request):
    try:
        payload = tokenCheck(request)
        MustFood.objects.filter(id=request.data['id']).delete()
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error': str(traceback.format_exc())})

def tokenCheck(request):
    try:
        print(request.COOKIES.get('token'))
        token = request.headers['token']
        if not token: raise Response(status=status.HTTP_401_UNAUTHORIZED)
        try: return jwt.decode(token, settings.JWT_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError: raise Response(status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        return JsonResponse({'error': str(traceback.format_exc())})


"""
사용 할지 안할지 모르는 코드 [수정이 필요하다]
"""
# @api_view(['GET'])
# def test(request):
#     payload = {'id': request.data['id']}
#     my_list = rm.Team.objects.filter(date=int(str(datetime.date.today()).replace('-','')))
#     serializer = rs.TeamSerializer(my_list, many=True)
#     for user in serializer.data:
#         team_memebers_id = [int(x) for x in user['team'].split(',')]
#         team_menus_id = [int(x) for x in user['menu'].split(',')]
#         if payload['id'] in team_memebers_id:
#             team_members_info = User.objects.filter(id__in=team_memebers_id)
#             team_menus_info = sm.Info.objects.filter(id__in=team_menus_id)
#             break

#     team_member_list, team_menu_list = [], []
#     team_members_info = UserSerializer(team_members_info, many=True).data
#     team_menus_info = addAverStoreRating(ss.InfoSerializer(team_menus_info, many=True))
#     # print(team_menus_info)
#     for member in team_members_info:
#         team_member_list.append({'id': member['id'], 'name': member['name'], 'department': member['department']})
    
#     for menu in team_menus_info:
#         team_menu_list.append({
#             'id': menu['id'],
#             'name': menu['name'],
#             'category': menu['category'],
#             'aver_price': menu['aver_price'],
#             'arrival_time': menu['arrival_time'],
#             'call_number': menu['call_number'],
#             'location': menu['location'],
#             'aver_rating': menu['aver_rating']
#         })
#     return JsonResponse({'team': team_member_list, 'menu': team_menu_list})



def make_info():
    res = {}
    
    for user in eval(requests.get(url=settings.OE_WORKERS_API_ADDRESS, headers={'key': settings.OE_WORKERS_API_KEY}).text)['list']:
        # if user['idn'] == 4:
        #     continue
        res[user['idn']] = {'id': user['idn'], 'name': user['name'], 'department': user['department'], 'phone': user['phone']}
    
    return res