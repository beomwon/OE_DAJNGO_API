from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from .serializers import InfoSerializer, RatingSerializer
from .models import Info, Rating
import jwt, datetime
from io import StringIO
import json

# Create your views here.
@api_view(['GET'])
def storeList(request):
    payload = tokenCheck(request)
    store_info = Info.objects.all()
    serializer = InfoSerializer(store_info, many=True)
    return Response(addAverStoreRating(serializer))

@api_view(['GET']) #POST로 아무것도 보내지 않고 전송하여 payload에서 id를 찾아와서 뽑아줌
def ratingList(request):
    payload = tokenCheck(request)
    my_lating_list = Rating.objects.filter(user_id=payload['id'])
    serializer = RatingSerializer(my_lating_list, many=True)
    return Response(serializer.data)

@api_view(['POST']) # body에 store_name, store_rating, comment 3개를 보내줘야함
def insertRating(request):
    payload = tokenCheck(request)
    request.data['user_id'] = payload['id']
    print(request.data)
    serializer = RatingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT']) # ratingList에서 선택하면 변경가능하게 할것임,
def updateRating(request):
    payload = tokenCheck(request)
    rating = Rating.objects.get(id=request.data['id'])
    serializer = RatingSerializer(instance=rating, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

# store/updateRating/tableId로 json파일을 보내주면 변경됨 (변경가능한건 3개지만, 줄때는 다줘야함)
# {
#     "id": 1,
#     "user_id": 1,
#     "store_name": "몰라",
#     "store_rating": 1,
#     "comment": "zzz"
# }

@api_view(['DELETE'])
def deleteRating(request):
    payload = tokenCheck(request)
    rating = Rating.objects.get(id=request.data['id'])
    if rating:
        rating.delete()

    return Response(status=status.HTTP_200_OK)

def addAverStoreRating(serializer):
    # temp = json.load(StringIO(JSONRenderer().render(serializer.data).decode()))
    for i, data in enumerate(serializer.data):
        aver = 0
        store_ratings = Rating.objects.filter(store_id=data['id'])
        for s in store_ratings:
            aver += s.store_rating

        if aver == 0: serializer.data[i]['aver_rating'] = 0
        else: serializer.data[i]['aver_rating'] = round(aver/len(store_ratings), 1)

    return serializer.data

def tokenCheck(request):
    token = request.COOKIES.get('jwt')
    if not token: raise Response(status=status.HTTP_401_UNAUTHORIZED)
    try: return jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError: raise Response(status=status.HTTP_401_UNAUTHORIZED)