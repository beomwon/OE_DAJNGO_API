import random
from user.views import make_info, addAverStoreRating
from store import models as sm
from store import serializers as ss
from osyulraeng import settings

from recommend import models as rm
from recommend import serializers as rs

from user import models as um
from user import serializers as us

from bs4 import BeautifulSoup
import datetime
import requests, json

from django.db.models import Q

def insertTeamAndMenu(serializer_data, team_algo_num, menu_algo_num):
    teams = recommendTeam(serializer_data, team_algo_num)
    print('팀이 선정되었습니다.')
    menus = recommendMenu(teams, menu_algo_num)
    print('팀별 메뉴가 선정되었습니다.')
    for team, menu in zip(teams, menus):
        rm.Team(team=','.join(team), menu=','.join(menu),date=int(str(datetime.date.today()).replace('-',''))).save()
    print('DB에 저장되었습니다.')
    # aligo(teams)
    print('알리고 문자가 전송되었습니다.')
   
def recommendTeam(serializer_data, way): #개인이 누구와 몇번씩 팀을 했는지 알려주는 dict, 팀의 갯수를 알려주는 number, 추천 알고리즘 번호 (0,1,2)
    dict = makeDict(serializer_data)
    # user_list = us.UserSerializer(um.User.objects.all(), many=True).data
    workers = {str(k): {'name': v['name'], 'department': v['department']} for k, v in make_info().items()}
    # res[user['idn']] = {'id': user['idn'], 'name': user['name'], 'department': user['department'], 'phone': user['phone']}
    # print(user_list)
    # workers = {}
    # for user in user_list:
    #     workers[str(user['id'])] = {'name': user['name'], 'department': user['department']}

    if len(workers.keys()) <= 5:
        res = []
        for key in workers.keys():
            res.append(key)
        return res

    func_list = [[randomTeam, [workers]], [departmentTeam, [workers]], [familiarTeam, [workers, dict]]]
    return func_list[way][0](func_list[way][1])

def randomTeam(data):
    workers = data[0]
    workers_random_list = []
    for w in random.sample(list(workers.keys()), len(workers)):
        workers_random_list.append(w)

    res = []
    count = int(len(workers_random_list)/4) - (0 if len(workers_random_list)%4 else 1)
    for _ in range(count):
        res.append(workers_random_list[:4])
        workers_random_list = workers_random_list[4:]
    res.append(workers_random_list)
    # print(res)
    i = 0
    while len(res[-1]) < 3:
        res[-1].append(res[i].pop(random.randint(0, 2)))
        i += 1

    print('팀 랜덤 선정 결과:', res)
    return res

def departmentTeam(data): # 수정 필요
    workers = data[0]
    develop_tag = ['디자인', '프론트엔드', '백엔드', 'AI'] # non_develop_tag = ['마케팅', '모임플래너', 'IR', '전략기획']
    
    workers_random_list = []
    for w in random.sample(list(workers.keys()), len(workers)):
        workers_random_list.append(w)

    develop, non_develop = [], []
    for worker in workers_random_list:
        if workers[worker]['department'] in develop_tag:
            develop.append(workers[worker]['name'])
        else:
            non_develop.append(workers[worker]['name'])
    
    workers_random_list = develop + non_develop

    res = []
    count = int(len(workers_random_list)/4) - (0 if len(workers_random_list)%4 else 1)
    for _ in range(count):
        res.append(workers_random_list[:4])
        workers_random_list = workers_random_list[4:]
    res.append(workers_random_list)

    i = 0
    while len(res[-1]) < 3:
        res[-1].append(res[i].pop(random.randint(0, len(res[i])-1)))
        i += 1
    
    print('팀 랜덤 선정 결과:', res)
    return res

def familiarTeam(data): # 아직 안만들어짐
    # {'1': {'2': 1, '3': 1, '4': 1, '5': 2, '7': 1}, '2': {'1': 1, '3': 1, '5': 1, '6': 1}, '3': {'1': 1, '2': 1}, '4': {'5': 2, '6': 1, '1': 1}, '5': {'4': 2, '6': 2, '1': 2, '2': 1, '7': 1}, '6': {'4': 1, '5': 2, '2': 1}, '7': {'1': 1, '5': 1}}
    workers, record = data[0], data[1]
    workers_list = list(workers.keys())
    
    workers_random_list = []
    while True:
        if len(workers_list) == 0:
            break
        main_worker = workers_list.pop(workers_list.index[random.choice(workers_list)])
        workers_random_list.append(main_worker)

        little_meet_list = [k for k, _ in sorted(list(record[main_worker].items()), key= lambda x: x[1])]

        for worker in little_meet_list:
            if worker in workers_list:
                workers_random_list.append(worker)
                workers_list.remove(worker)

    res = []
    count = int(len(workers_random_list)/4) - (0 if len(workers_random_list)%4 else 1)
    for _ in range(count):
        res.append(workers_random_list[:4])
        workers_random_list = workers_random_list[4:]
    res.append(workers_random_list)

    i = 0
    while len(res[-1]) < 3:
        res[-1].append(res[i].pop(random.randint(0, 2)))
        i += 1
    
    return res

def recommendMenu(teams, way):
    store_list = ss.InfoSerializer(sm.Info.objects.all(), many=True).data
    func_list = [[randomMenu, [store_list, teams]], [preferenceMenu, [store_list, teams]]]
    return func_list[way][0](func_list[way][1])

def randomMenu(data):
    store_list, length = data[0], len(data[1])
    store_id_list, res = [], []
    for store in store_list:
        store_id_list.append(str(store['id']))

    for _ in range(length):
        res.append(random.sample(store_id_list, 4))
    
    print('팀별 메뉴 선정결과: ', res)
    return res
    
def preferenceMenu(data):
    store_list, teams = data[0], data[1]
    store_category = ["고기구이", "면요리", "분식", "샐러드", "양식", "일식·초밥", "중식", "찜·탕·찌개", "치킨", "피자", "한식", "햄버거"]
    store_category_counts = [[0 for _ in range(len(store_category))] for _ in range(len(teams))]
    must_store_category_counts = [[0 for _ in range(len(store_category))] for _ in range(len(teams))]

    for team_i, team in enumerate(teams):
        for user in team:
            user_preference = um.Preference.objects.filter(user_id=int(user))
            user_preference_serializer = us.PreferenceSerializer(user_preference, many=True)

            for data in user_preference_serializer.data:
                store_category_counts[team_i][store_category.index(data['category'])] += data['preference']
            
            q = Q(user_id=int(user)) & Q(date=int(str(datetime.date.today()).replace('-','')))
            user_must = um.MustFood.objects.filter(q)
            user_must_serializer = us.MustFoodSerializer(user_must, many=True)

            for data in user_must_serializer.data:
                must_store_category_counts[team_i][store_category.index(data['category'])] += data['preference']

    res = [[] for _ in range(len(teams))]
    # res[team_i]

    for team_i in range(len(teams)):
        must_list = [[] for _ in range(len(store_category))]
        for store in store_list:
            if must_store_category_counts[team_i][store_category.index(store['category'])] > 0:
                must_list[store_category.index(store['category'])].append(str(store['id']))
        
        print(team_i,'팀 꼭 먹어야하는 카테고리:',must_list)
        for category in must_list:
            if len(category) > 0:
                res[team_i] += random.sample(category, 1)

        print(team_i,'팀 꼭 먹어야하는 음식점:',res[team_i])
        # 무조건 먹어야 하는 카테고리 빼놓고, 나머지에서 고른다.
        # 가중치를 주는 코드
        store_id_list = []
        for store in store_list:
            if must_store_category_counts[team_i][store_category.index(store['category'])] < 0: continue
            
            alpha = store_category_counts[team_i][store_category.index(store['category'])]
            if random.randint(1, 10) > 5+alpha:
                store_id_list.append(str(store['id']))

        res[team_i] += random.sample(store_id_list, 4 - len(res[team_i]))

    print('팀별 메뉴 선정결과: ', res)
    return res

def crawling():
    search_url = "https://www.honam.ac.kr/Cafeteria_Diet/1" 
    r = requests.get(search_url, verify=False)

    soup = BeautifulSoup(r.text, "html.parser")
    items = soup.select("tr")
    today = datetime.datetime.today().strftime('%m/%d')

    for i, item in enumerate(items):
        if today in str(item):
            today_food = str(list(items[i])[3])[4:-5]
            return today_food

    return '오늘의 학식정보가 없습니다.'

def makeDict(data):
    dict = {}
    for d in data:
        team_list = d['team'].split(',')
        for v in team_list:
            temp = team_list.copy()
            temp.pop(temp.index(v))
            if v in dict.keys():
                for item in temp:
                    if item in dict[v].keys():
                        dict[v][item] += 1
                    else:
                        dict[v][item] = 1
            else:
                dict[v] = {k: 1 for k in temp}

    return dict

def aligo(teams):
    school_food = crawling()
    print(school_food)
    if school_food != '오늘의 학식정보가 없습니다.':
        school_food = school_food.replace(' ', '')
    template_code = 'TL_5606'
    basic_send_url = 'https://kakaoapi.aligo.in/akv10/alimtalk/send/'
    button_info = json.dumps({'button': [{'name': '오슐랭 바로가기', # 버튼명
                            'linkType':'WL', # DS, WL, AL, BK, MD
                            'linkTypeName' : '웹링크', # 배송조회, 웹링크, 앱링크, 봇키워드, 메시지전달 중에서 1개
                            'linkM':'https://oe-chelin.vercel.app/', # WL일 때 필수
                            'linkP':'https://oe-chelin.vercel.app/', # WL일 때 필수
                            #'linkI': 'IOS app link', # AL일 때 필수
                            #'linkA': 'Android app link' # AL일 때 필수
                    }]})
    
    try:
        for team in teams:
            for user_id in team:

                mi = messageInfo(user_id)
                # print('mi["menu"]:', mi['menu'])
                sms_data = {
                            'apikey': settings.ALIGO_APIKEY,
                            'token': settings.ALIGO_TOKEN,
                            'userid': settings.ALIGO_USERID,
                            'sender': settings.ALIGO_SENDER,
                            'senderkey': settings.ALIGO_SENDERKEY,
                            'tpl_code': template_code,
                            # 'subject_1': '당신의 테이블입니다.',
                            # 'emtitle_1': '당신의 테이블입니다.',
                            'button_1': button_info,
                            'receiver_1': mi['receiver_1'],
                            'message_1': f"""● 오늘의 오슐랭 팀원
(하하) {mi['teams']}

● 오늘의 오슐랭 추천메뉴
(꺄아) {mi['menu'][0]['name']} ({str(mi['menu'][0]['aver_rating'])}점)
(꺄아) {mi['menu'][1]['name']} ({str(mi['menu'][1]['aver_rating'])}점)
(꺄아) {mi['menu'][2]['name']} ({str(mi['menu'][2]['aver_rating'])}점)
(꺄아) {mi['menu'][3]['name']} ({str(mi['menu'][3]['aver_rating'])}점)

● 오늘의 학식정보
(굿) {school_food}"""
                            }
                
                alimtalk_send_response = requests.post(basic_send_url, data=sms_data)
    except:
        pass

def messageInfo(user_id):
    my_list = rm.Team.objects.filter(date=int(str(datetime.date.today()).replace('-','')))
    serializer = rs.TeamSerializer(my_list, many=True)
    team_menus_info = ''
    for user in serializer.data:
        team_memebers_id = [int(x) for x in user['team'].split(',')]
        team_menus_id = [int(x) for x in user['menu'].split(',')]
        if int(user_id) in team_memebers_id:
            # team_members_info = User.objects.filter(id__in=team_memebers_id)
            team_menus_info = sm.Info.objects.filter(id__in=team_menus_id)
            break
    members = make_info()
    team_member_list, team_menu_list = [], []
    # team_members_info = UserSerializer(team_members_info, many=True).data
    team_menus_info = addAverStoreRating(ss.InfoSerializer(team_menus_info, many=True))
    # print(team_menus_info)
    teams, receiver_phone = "", ""
    for id in team_memebers_id:
        teams =  teams + members[id]['name'] + "님,"
        # team_member_list.append({'id': members[id]['id'], 'name': members[id]['name'], 'department': members[id]['department']})
        # print(id, type(id), user_id, type(user_id))
        if str(id) == user_id:
            receiver_phone = members[id]['phone']

    for menu in team_menus_info:
        team_menu_list.append({
            # 'id': menu['id'],
            'name': menu['name'],
            'category': menu['category'],
            # 'aver_price': menu['aver_price'],
            # 'arrival_time': menu['arrival_time'],
            # 'call_number': menu['call_number'],
            # 'location': menu['location'],
            'aver_rating': menu['aver_rating']
        })
    
    # print('phone: ', receiver_phone, 'teams: ', teams, 'team_menu_list: ', team_menu_list)
    return {'receiver_1': receiver_phone, 'teams': teams, 'menu': team_menu_list}