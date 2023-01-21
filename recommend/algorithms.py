import random
# from user import models as um
# from user import serializers as us

from user.views import make_info

from store import models as sm
from store import serializers as ss

from recommend import models as rm
from recommend import serializers as rs

from bs4 import BeautifulSoup
import datetime
import requests, json

def insertTeamAndMenu(serializer_data, team_algo_num, menu_algo_num):
    teams = recommendTeam(serializer_data, team_algo_num)
    menus = recommendMenu(teams, menu_algo_num)
    for team, menu in zip(teams, menus):
        rm.Team(team=','.join(team), menu=','.join(menu),date=int(str(datetime.date.today()).replace('-',''))).save()
   
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

    i = 0
    while len(res[-1]) < 3:
        res[-1].append(res[i].pop(random.randint(0, 3)))
        i += 1

    print(res)
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
        res[-1].append(res[i].pop(random.randint(0, 3)))
        i += 1
    
    return res

def familiarTeam(data):
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
        res[-1].append(res[i].pop(random.randint(0, 3)))
        i += 1
    
    return res

def recommendMenu(teams, way):
    store_list = ss.InfoSerializer(sm.Info.objects.all(), many=True).data
    func_list = [[randomMenu, [store_list, teams]]]
    return func_list[way][0](func_list[way][1])

def randomMenu(data):
    store_list, length = data[0], len(data[1])
    store_id_list, res = [], []
    for store in store_list:
        store_id_list.append(str(store['id']))

    for _ in range(length):
        res.append(random.sample(store_id_list,4))
    
    print('menu_res: ', res)
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

def recommendTeamAndMenu(team, menu):
    team_way, team_number = team[0], team[1]
    pass