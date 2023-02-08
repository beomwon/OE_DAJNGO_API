from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from .serializers import InfoSerializer, RatingSerializer
from .models import Info, Rating
from osyulraeng import settings
from django.db.models import Q
import jwt, datetime
from io import StringIO
import json
import traceback

# Create your views here.
@api_view(['GET'])
def storeList(request):
    try:
        payload = tokenCheck(request)
        store_info = Info.objects.all()
        serializer = InfoSerializer(store_info, many=True)
        return Response(addAverStoreRating(serializer))

    except Exception as e:
        return JsonResponse({'error': str(traceback.format_exc())})

@api_view(['GET']) #POST로 아무것도 보내지 않고 전송하여 payload에서 id를 찾아와서 뽑아줌
def ratingList(request):
    try:
        payload = tokenCheck(request)
        my_lating_list = Rating.objects.filter(user_id=payload['id'])
        serializer = RatingSerializer(my_lating_list, many=True)

        result = []
        for data in serializer.data:
            if data['store_id'] == 0:
                continue
            temp = data['id']
            store_info = Info.objects.filter(id=data['store_id'])
            store_serializer = InfoSerializer(store_info, many=True)
            data.update(store_serializer.data[0])
            data['id'] = temp
            result.append(data)
        
        return Response(result)
        
    except Exception as e:
        print({'error': str(traceback.format_exc())})
        return JsonResponse({'error': str(traceback.format_exc())})

@api_view(['POST']) # body에 store_name, store_rating, comment 3개를 보내줘야함
def insertRating(request):
    try:
        payload = tokenCheck(request)
        request.data['user_id'] = payload['id']
        request.data['date'] = int(str(datetime.date.today()).replace('-',''))
        # print(request.data)
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return JsonResponse({'error': str(traceback.format_exc())})

@api_view(['PUT']) # ratingList에서 선택하면 변경가능하게 할것임,
def updateRating(request):
    try:
        payload = tokenCheck(request)
        rating = Rating.objects.get(id=request.data['id'])
        serializer = RatingSerializer(instance=rating, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return JsonResponse({'error': str(traceback.format_exc())})
@api_view(['GET'])
def checkTodayRating(request): #### 없으면 -> store.models.Rating.DoesNotExist: Rating matching query does not exist.
    payload = tokenCheck(request)
    # int(str(datetime.date.today()).replace('-',''))
    # q = Q(user_id=payload['id']) & Q(user_id=payload['id'])
    q = Q(user_id=payload['id']) & Q(date=int(str(datetime.date.today()).replace('-','')))
    print(payload['id'], int(str(datetime.date.today()).replace('-','')))
    check = Rating.objects.filter(q)
    return JsonResponse({'result': 1 if len(check) > 0 else 0})

@api_view(['DELETE'])
def deleteRating(request):
    try:
        payload = tokenCheck(request)
        rating = Rating.objects.get(id=request.data['id'])
        if rating:
            rating.delete()

        return Response(status=status.HTTP_200_OK)

    except Exception as e:
        return JsonResponse({'error': str(traceback.format_exc())})

def addAverStoreRating(serializer):
    # temp = json.load(StringIO(JSONRenderer().render(serializer.data).decode()))
    try:
        for i, data in enumerate(serializer.data):
            aver = 0
            store_ratings = Rating.objects.filter(store_id=data['id'])
            for s in store_ratings:
                aver += s.store_rating

            if aver == 0: serializer.data[i]['aver_rating'] = 0
            else: serializer.data[i]['aver_rating'] = round(aver/len(store_ratings), 1)

        return serializer.data

    except Exception as e:
        return JsonResponse({'error': str(traceback.format_exc())})

def tokenCheck(request):
    # token = request.COOKIES.get('jwt')
    token = request.headers['token']
    if not token: raise Response(status=status.HTTP_401_UNAUTHORIZED)
    try: return jwt.decode(token, settings.JWT_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError: raise Response(status=status.HTTP_401_UNAUTHORIZED)
