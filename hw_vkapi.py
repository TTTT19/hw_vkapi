import requests
from collections import Counter
import time
import json
from storage_for_acess_token import access_token

N = 1  # Этот параметр определяет - меньше какого значения пользователей в гурппе - группа отображается в ответе


class users_vk:
    def get_id(id_or_screen_name):
        params = {'access_token': access_token, 'user_ids': id_or_screen_name, 'v': 5.103}
        user_info = requests.get('https://api.vk.com/method/users.get', params)
        id_hero = (user_info.json()['response'][0]['id'])
        return id_hero

    def get_followers_first_list():
        followers = requests.get('https://api.vk.com/method/friends.get',
                                 {'access_token': access_token, 'v': 5.103, 'user_id': id_hero, 'count': 340})
        return followers.json()['response']

    def get_followers_second_list():
        followers = requests.get('https://api.vk.com/method/friends.get',
                                 {'access_token': access_token, 'v': 5.103, 'user_id': id_hero, 'count': 330,
                                  'offset': 340})
        return followers.json()['response']

    def get_followers_third_list():
        followers = requests.get('https://api.vk.com/method/friends.get',
                                 {'access_token': access_token, 'v': 5.103, 'user_id': id_hero, 'count': 330,
                                  'offset': 670})
        return followers.json()['response']

    def get_groups():
        groups = requests.get('https://api.vk.com/method/groups.get',
                              {'access_token': access_token, 'v': 5.103, 'user_id': id_hero})
        groups_list = (groups.json()['response']['items'])
        return groups_list

    def get_groups_ById(group_string):
        groups = requests.get('https://api.vk.com/method/groups.getById',
                              {'access_token': access_token, 'v': 5.103, 'group_ids': group_string,
                               'fields': 'members_count'})
        groups_list = (groups.json()['response'])
        return groups_list

    def friend_is_member(user_ids, group_id_for_param):
        groups = requests.get('https://api.vk.com/method/groups.isMember',
                              {'access_token': access_token, 'v': 5.103, 'group_id': group_id_for_param,
                               'user_ids': user_ids})
        try:
            groups_list = (groups.json()['response'])
        except:

            return 0
        else:
            return groups_list

    def find_out_how_many_list_for_group():
        try:
            print(f'У пользователя {users_vk.get_followers_first_list()["count"]} друзей')
        except:
            print("C пользователем что то не то")
        else:
            if users_vk.get_followers_first_list()["count"] < 340:
                print(
                    f'Создаем 1 список пользователей, чтобы проверить есть ли они в группах, в которых состоит пользователь')
                users_vk.lists = 1
            elif users_vk.get_followers_second_list()["count"] == 0:
                print(
                    f'Создаем 1 список пользователей, чтобы проверить есть ли они в группах, в которых состоит пользователь')
                users_vk.lists = 1
            elif users_vk.get_followers_second_list()["count"] < 330:
                print(
                    "Создаем 2 списка пользователей, чтобы проверить есть ли они в группах, в которых состоит пользователь")
                users_vk.lists = 2
            elif users_vk.get_followers_third_list()["count"] == 0:
                print(
                    "Создаем 2 списка пользователей, чтобы проверить есть ли они в группах, в которых состоит пользователь")
                users_vk.lists = 2
            else:
                print(
                    "Создаем 3 списка пользователей, чтобы проверить есть ли они в группах, в которых состоит пользователь")
                users_vk.lists = 3

    def find_out_how_many_groups():
        users_vk.group_list = users_vk.get_groups()
        print(f'Пользователь состоит в {len(users_vk.group_list)} группе/группах')
        users_vk.count_group = len(users_vk.group_list)

    def make_list_for_search():
        if users_vk.lists == 1:
            list_friends_1 = users_vk.get_followers_first_list()['items']
            users_vk.string_friends_1 = ', '.join(str(key) for key in list_friends_1)
        elif users_vk.lists == 2:
            list_friends_1 = users_vk.get_followers_first_list()['items']
            users_vk.string_friends_1 = ', '.join(str(key) for key in list_friends_1)
            time.sleep(1)
            list_friends_2 = users_vk.get_followers_second_list()['items']
            users_vk.string_friends_2 = ', '.join(str(key) for key in list_friends_2)
        else:
            list_friends_1 = users_vk.get_followers_first_list()['items']
            users_vk.string_friends_1 = ', '.join(str(key) for key in list_friends_1)
            time.sleep(1)
            list_friends_2 = users_vk.get_followers_second_list()['items']
            users_vk.string_friends_2 = ', '.join(str(key) for key in list_friends_2)
            time.sleep(1)
            list_friends_3 = users_vk.get_followers_third_list()['items']
            users_vk.string_friends_3 = ', '.join(str(key) for key in list_friends_3)

    def search_in_group_make_list():
        users_vk.group_string = ""
        for group in users_vk.group_list:
            users_vk.count_group -= 1
            time.sleep(1)
            spisok = users_vk.friend_is_member(user_ids=users_vk.string_friends_1, group_id_for_param=group)

            if spisok == 0:
                print(
                    f'Данные с пользователями группы {group} не загрузились. Осталось {users_vk.count_group} группа/групп')
            else:
                c = Counter()
                for s1 in spisok:
                    c.update(s1)
                if users_vk.lists == 2 or users_vk.lists == 3:
                    spisok2 = users_vk.friend_is_member(user_ids=users_vk.string_friends_2, group_id_for_param=group)
                    for s2 in spisok2:
                        c.update(s2)
                if users_vk.lists == 3:
                    spisok3 = users_vk.friend_is_member(user_ids=users_vk.string_friends_3, group_id_for_param=group)
                    for s3 in spisok3:
                        c.update(s3)
                print(f'В группе c id{group} друзей: {c["member"]}. Осталось {users_vk.count_group} группа/групп')
                if c["member"] < N:
                    users_vk.group_string = users_vk.group_string + str(group) + ", "

    def dump_group_info_json():
        print(f'Список групп где количество друзей меньше {N} друга/друзей: {users_vk.group_string}')
        if users_vk.group_string == "":
            print("Удовлетворяющих условие групп не найдено.")
        else:
            print('Загружаем данные в json файл')
            with open("groups.json", "w", encoding="utf-8") as file:
                json.dump(users_vk.get_groups_ById(users_vk.group_string), file)


# Ноль: Создаем пользователя, у которого будем искать друзей в группах
new_user = users_vk
id_hero = new_user.get_id(input('Введите ID или screen name пользователя: '))

# Первое: узнаем количество друзей/проверяем вообщем можем ли мы это сделать
new_user.find_out_how_many_list_for_group()

# Второе: узнаем количество групп
new_user.find_out_how_many_groups()

# Третье: формируем один или два списка друзей по 500 человек и превращаем ее в строку, для запроса IS MEMBER
new_user.make_list_for_search()

# Четвертое: начинаем проходится в по каждой группе из списка групп (2 пункт) и смотрим есть ли там пользователи, создаем список в котором друзей меньше N
new_user.search_in_group_make_list()

# Пятое: если в списке есть хоть одно значение - делаем запрос и возращаем информацию по группам в файл
new_user.dump_group_info_json()
