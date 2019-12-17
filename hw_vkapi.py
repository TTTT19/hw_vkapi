import requests
from collections import Counter
import time


access_token = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'

def get_params_id_first500():
    params = {'access_token': access_token, 'v': 5.101, 'user_id': id_hero,'count': 500}
    return params

def get_params_id_next500():
    params = {'access_token': access_token, 'v': 5.101, 'user_id': id_hero,'count': 500, 'offset': 500}
    return params

def get_params_for_group_id():
    params = {'access_token': access_token, 'v': 5.101, 'user_id': id_hero}
    return params

def get_params_for_group_id_member(user_ids, group_id_for_param):
    params = {'access_token': access_token, 'v': 5.101, 'group_id': group_id_for_param, 'user_id': id_hero, 'user_ids': user_ids}
    return params

class users_vk:

    def get_followers_first_500():
        followers = requests.get('https://api.vk.com/method/friends.get', get_params_id_first500())
        return followers.json()['response']

    def get_followers_second_500():
        followers = requests.get('https://api.vk.com/method/friends.get', get_params_id_next500())
        return followers.json()['response']

    def get_groups():
        groups = requests.get('https://api.vk.com/method/groups.get', get_params_for_group_id())
        groups_list = (groups.json()['response']['items'])
        return groups_list



def friend_is_member(user_ids, group_id_for_param):
    groups = requests.get('https://api.vk.com/method/groups.isMember', get_params_for_group_id_member(user_ids, group_id_for_param))
    groups_list = (groups.json()['response'])
    return groups_list



#Ноль: Создаем пользователя, у которого будем искать друзей в группах

new_user = users_vk
# id_hero = input('Введите ID пользователя: ')
id_hero = 171691064



#Первое: узнаем количество друзей

print(f'У пользователя {new_user.get_followers_first_500()["count"]} друзей')
if new_user.get_followers_first_500()["count"] > 500:
    print(f'Создаем 2 списка пользователей, чтобы проверить есть ли они в группах, в которых состоит пользователь')
    lists = 2
else:
    print("Создаем 1 список пользователей, чтобы проверить есть ли они в группах, в которых состоит пользователь")
    lists = 1

#Второе: узнаем количество групп

group_list = new_user.get_groups()
print(f'Пользователь состоит в {len(group_list)} группе/группах')

#Третье: формируем один или два списка друзей по 500 человек и превращаем ее в строку, для запроса IS MEMBER

if lists == 1:
    list_500_friends_1 = new_user.get_followers_first_500()['items']
    string_500_friends_1 = ', '.join(str(key) for key in list_500_friends_1)
else:
    list_500_friends_1 = new_user.get_followers_first_500()['items']
    string_500_friends_1 = ', '.join(str(key) for key in list_500_friends_1)
    time.sleep(1)
    list_500_friends_2 = new_user.get_followers_second_500()['items']
    string_500_friends_2 = ', '.join(str(key) for key in list_500_friends_2)

#Четвертое: начинаем проходится в по каждой группе из списка групп (2 пункт) и смотрим есть ли там пользователи
for group in group_list:
    time.sleep(1)
    spisol = friend_is_member(user_ids = string_500_friends_1, group_id_for_param = group)
    c = Counter()
    for d in spisol:
        c.update(d)
    print(f'В группе c id{group} друзей: {c["member"]}')
