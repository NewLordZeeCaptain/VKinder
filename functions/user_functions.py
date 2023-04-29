import vk_api
import json
import datetime
from vk_api.longpoll import VkLongPoll
from configs.config import VERSION
from vk_api.exceptions import ApiError
from random import randrange


# Для работы с ВК


""" 
ФУНКЦИИ ПОИСКА
"""


class User(object):
    """User class is used to interact with user api"""

    def __init__(self, USER_TOKEN):
        # super(User, self).__init__()
        self.vk = vk_api.VkApi(token=USER_TOKEN)

    def user_get(self, vk_id):
        response = self.vk.method(
            "users.get",
            {
                "user_ids": vk_id,
                "fields": "nickname,sex,city,interests,has_photo,photo_id",
            },
        )
        return response[0]

    def search_user(self, sex, age_at, age_to, city):
        all_ersons = []
        link_profile = "https://vk.com/id"
        response = self.vk.method(
            "users.search",
            {
                "sort": 1,
                "sex": sex,
                "status": 1,
                "age_from": age_at,
                "age_to": age_to,
                "has_photo": 1,
                "count": 25,
                "online": 1,
                "hometown": city,
            },
        )
        for element in response["items"]:
            person = [
                element["first_name"],
                element["last_name"],
                link_profile + str(element["id"]),
                element["id"],
            ]
            all_persons.append(person)
        return all_persons

    def get_photo(self, user_owner_id):
        try:
            response = self.vk.method(
                "photos.get",
                {
                    # "access_token": USER_TOKEN,
                    # "v": VERSION,
                    "owner_id": user_owner_id,
                    "album_id": "profile",
                    "count": 10,
                    "extended": 1,
                    "photo_sizes": 1,
                },
            )
        except ApiError:
            return "нет доступа к фото"
        users_photos = []
        for i in range(10):
            try:
                users_photos.append(
                    [
                        response["items"][i]["likes"]["count"],
                        "photo"
                        + str(response["items"][i]["owner_id"])
                        + "_"
                        + str(response["items"][i]["id"]),
                    ]
                )
            except IndexError:
                users_photos.append(["нет фото."])
        # return users_photos
        result = []
        for photo in users_photos:
            if photo != ["нет фото."] and users_photos != "нет доступа к фото":
                result.append(photo)
        return sorted(result)

        """
        Sorting, Responce & JSON
        """

    

    def json_create(self, lst):
        today = datetime.date.today()
        today_str = f"{today.day}.{today.month}.{today.year}"
        res = {}
        res_list = []
        for info in lst:
            res["data"] = today_str
            res["first_name"] = info[0]
            res["second_name"] = info[1]
            res["link"] = info[2]
            res["id"] = info[3]
            res_list.append(res.copy())

        with open("result.json", "a", encoding="UTF-8") as write_file:
            json.dump(res_list, write_file, ensure_ascii=False)

        print(f"Информация о загруженных файлах успешно записана в json файл.")

    def write_msg(self, user_id, message, attachment=None):
        self.vk.method(
            "messages.send",
            {
                "user_id": user_id,
                "message": message,
                "random_id": randrange(10**7),
                "attachment": attachment,
            },
        )


""" 
ФУНКЦИИ СОРТИРОВКИ, ОТВЕТА, JSON
"""


# Сортируем фото по лайкам, удаляем лишние элементы
