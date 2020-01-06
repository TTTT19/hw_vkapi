import requests
from collections import Counter
import time


access_token = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'
N = 1  #Этот параметр определяет - меньше какого значения пользователей в гурппе - группа отображается в ответе


def get_params_id_first_list_friends():
    params = {'access_token': access_token, 'v': 5.103, 'user_id': id_hero,'count':340}
    return params

def get_params_id_second_list_friends():
    params = {'access_token': access_token, 'v': 5.103, 'user_id': id_hero,'count': 330, 'offset': 340}
    return params

def get_params_id_third_list_friends():
    params = {'access_token': access_token, 'v': 5.103, 'user_id': id_hero,'count': 330, 'offset': 670}
    return params

def get_params_for_group_id():
    params = {'access_token': access_token, 'v': 5.103, 'user_id': id_hero}
    return params

def get_params_for_group_ById(group_string):
    params = {'access_token': access_token, 'v': 5.103, 'group_ids': group_string, 'fields': 'members_count'}
    return params

def get_params_for_group_id_member(user_ids, group_id_for_param):
    params = {'access_token': access_token, 'v': 5.103, 'group_id': group_id_for_param, 'user_ids': user_ids}
    return params

def get_id(id_or_screen_name):
    params = {'access_token': access_token, 'user_ids': id_or_screen_name, 'v': 5.103}
    user_info = requests.get('https://api.vk.com/method/users.get', params)
    id_hero = (user_info.json()['response'][0]['id'])
    return id_hero




class users_vk:

    def get_followers_first_list():
        followers = requests.get('https://api.vk.com/method/friends.get', get_params_id_first_list_friends())
        return followers.json()['response']

    def get_followers_second_list():
        followers = requests.get('https://api.vk.com/method/friends.get', get_params_id_second_list_friends())
        return followers.json()['response']

    def get_followers_third_list():
        followers = requests.get('https://api.vk.com/method/friends.get', get_params_id_third_list_friends())
        return followers.json()['response']

    def get_groups():
        groups = requests.get('https://api.vk.com/method/groups.get', get_params_for_group_id())
        groups_list = (groups.json()['response']['items'])
        return groups_list

    def get_groups_ById(group_string):
        groups = requests.get('https://api.vk.com/method/groups.getById', get_params_for_group_ById(group_string))
        groups_list = (groups.json()['response'])
        return groups_list




def friend_is_member(user_ids, group_id_for_param):
    groups = requests.get('https://api.vk.com/method/groups.isMember', get_params_for_group_id_member(user_ids, group_id_for_param))
    try:
        groups_list = (groups.json()['response'])
    except:

        return 0
    else:
        return groups_list




#Ноль: Создаем пользователя, у которого будем искать друзей в группах

new_user = users_vk
id_hero = get_id(input('Введите ID или screen name пользователя: '))


#Первое: узнаем количество друзей/проверяем вообщем можем ли мы это сделать

try:
    print(f'У пользователя {new_user.get_followers_first_list()["count"]} друзей')
except:
    print("C пользователем что то не то")
else:
    if new_user.get_followers_first_list()["count"] < 340:
        print(f'Создаем 1 список пользователей, чтобы проверить есть ли они в группах, в которых состоит пользователь')
        lists = 1
    elif new_user.get_followers_second_list()["count"] == 0:
        print(f'Создаем 1 список пользователей, чтобы проверить есть ли они в группах, в которых состоит пользователь')
        lists = 1
    elif new_user.get_followers_second_list()["count"] < 330:
        print("Создаем 2 списка пользователей, чтобы проверить есть ли они в группах, в которых состоит пользователь")
        lists = 2
    elif new_user.get_followers_third_list()["count"] == 0:
        print("Создаем 2 списка пользователей, чтобы проверить есть ли они в группах, в которых состоит пользователь")
        lists = 2
    else:
        print("Создаем 3 списка пользователей, чтобы проверить есть ли они в группах, в которых состоит пользователь")
        lists = 3

    #Второе: узнаем количество групп

    group_list = new_user.get_groups()
    print(f'Пользователь состоит в {len(group_list)} группе/группах')
    count_group = len(group_list)

    #Третье: формируем один или два списка друзей по 500 человек и превращаем ее в строку, для запроса IS MEMBER

    if lists == 1:
        list_friends_1 = new_user.get_followers_first_list()['items']
        string_friends_1 = ', '.join(str(key) for key in list_friends_1)
    elif lists == 2:
        list_friends_1 = new_user.get_followers_first_list()['items']
        string_friends_1 = ', '.join(str(key) for key in list_friends_1)
        time.sleep(1)
        list_friends_2 = new_user.get_followers_second_list()['items']
        string_friends_2 = ', '.join(str(key) for key in list_friends_2)
    else:
        list_friends_1 = new_user.get_followers_first_list()['items']
        string_friends_1 = ', '.join(str(key) for key in list_friends_1)
        time.sleep(1)
        list_friends_2 = new_user.get_followers_second_list()['items']
        string_friends_2 = ', '.join(str(key) for key in list_friends_2)
        time.sleep(1)
        list_friends_3 = new_user.get_followers_third_list()['items']
        string_friends_3 = ', '.join(str(key) for key in list_friends_3)


    #Четвертое: начинаем проходится в по каждой группе из списка групп (2 пункт) и смотрим есть ли там пользователи, создаем список в котором друзей меньше N

    group_string = ""
    for group in group_list:
        count_group -= 1
        time.sleep(1)
        spisok = friend_is_member(user_ids = string_friends_1, group_id_for_param = group)


        if spisok == 0:
            print(f'Данные с пользователями группы {group} не загрузились. Осталось {count_group} группа/групп')
        else:
            c = Counter()
            for s1 in spisok:
                c.update(s1)
            if lists == 2 or lists == 3:
                spisok2 = friend_is_member(user_ids=string_friends_2, group_id_for_param=group)
                for s2 in spisok2:
                    c.update(s2)
            if lists == 3:
                spisok3 = friend_is_member(user_ids=string_friends_3, group_id_for_param=group)
                for s3 in spisok3:
                 c.update(s3)
            print(f'В группе c id{group} друзей: {c["member"]}. Осталось {count_group} группа/групп')
            if c["member"] < N:
                group_string = group_string + str(group)+ ", "


  #Пятое: если в списке есть хоть одно значение - делаем запрос и возращаем информацию по группам
    print(f'Список групп где количество друзей меньше {N} друга/друзей: {group_string}')
    if group_string == "":
        print("Удовлетворяющих условие групп не найдено.")
    else:
        print('Выгрузка json:')
        print(new_user.get_groups_ById(group_string))