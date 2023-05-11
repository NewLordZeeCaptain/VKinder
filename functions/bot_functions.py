import vk_api
from random import randrange
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from configs.config import CALLBACK_TYPES  # GROUP_TOKEN, USER_TOKEN,
from keyboard.keyboard import *
from db.db import DB

# from functions.user_functions import User

kbsetting = dict()


class Bot(object):
    """Used to interact with Vk Bot API with longpoll"""

    def __init__(self, GROUP_TOKEN, USER_TOKEN, CONSTR):
        super(Bot, self).__init__()
        # self.GROUP_TOKEN = GROUP_TOKEN
        self.USER_TOKEN = USER_TOKEN
        self.CONSTR = CONSTR
        self.kb = VkKeyboard()
        self.vk = vk_api.VkApi(token=GROUP_TOKEN)

        self.longpoll = VkLongPoll(self.vk)

    def get_event(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                return event

    def start(self):
        self.db = DB(self.CONSTR, self.USER_TOKEN)

        while True:
            event = self.get_event()

            self.bot_menu(event)

    def greating(self, user_id):
        self.write_msg(
            user_id=user_id,
            message=f"Приветствую!\nЭтот бот заменит вам ныне не работающий Tinder и поможет найти близких людей\nВы были автоматически зарегистрированы, но можете в любой момент удалить свой профиль\nДля работы с ботом используйте кнопки ниже\n",
        )

    def test(self, user_id, vk_id):
        self.db.add_to_blacklist(user_id, vk_id)

    def sender(self, user_id, text, keyboard):
        self.vk.method(
            "messages.send",
            {"user_id": user_id, "message": text, "random_id": 0, "keyboard": keyboard},
        )

    def bot_menu(self, event):
        self.sender(str(event.user_id), event.text.lower(), keyboard)
        match event.text.lower():
            case "начать":
                self.greating(event.user_id)
                self.db.register_user(event.user_id)

            case "избранное":
                fav = self.db.check_db_favorites(event.user_id)
                self.write_msg(event.user_id, "Выполняем поиск\n")
                self.write_msg(event.user_id, fav)
                if type(fav) == type(" "):
                    self.write_msg(event.user_id, fav)
                else:
                    for k, v in fav.items():
                        self.write_msg(event.user_id, f"{k} - {v}")

            case "blacklist":
                black = self.db.check_db_blacklist(event.user_id)
                self.write_msg(event.user_id, "Выполняем поиск\n")
                if type(black) == type(" "):
                    self.write_msg(event.user_id, black)
                else:
                    for k, v in black.items():
                        self.write_msg(event.user_id, f"{k} - {v}")

            case "начать поиск":
                sex = 0
                age_at = 18
                age_to = 100
                try:
                    city = self.db.user.user_get(event.user_id)["city"]
                except:
                    self.write_msg(event.user_id, "Укажите свой город: ")
                    event = self.get_event()
                    # print(event.text)
                    city = self.db.user.get_city(event.text)["id"]

                self.write_msg(
                    event.user_id,
                    "Желаете добавить поиск по полу?",
                )
                self.sender(
                    event.user_id, "Желаете добавить поиск по полу?", keyboard_search
                )
                event = self.get_event()
                if event.text.lower() == "да":
                    self.write_msg(event.user_id, "Укажите пол: ")
                    self.sender(event.user_id, "Укажите пол", keyboard_sex)
                    event = self.get_event()
                    match event.text.lower():
                        case "муж":
                            sex = 1
                        case "жен":
                            sex = 2
                        case "любой":
                            sex = 0
                        case other:
                            self.write_msg(
                                event.user_id,
                                'Было установлено значение по умолчанию( "Любой")',
                            )

                self.sender(
                    event.user_id,
                    "Желаете добавить поиск по возрасту?",
                    keyboard_search,
                )
                event = self.get_event()
                if event.text.lower() == "да":
                    self.write_msg(event.user_id, "Укажите максимальный возраст: ")
                    event = self.get_event()
                    try:
                        age_to = int(event.text)
                    except:
                        self.write_msg(
                            event.user_id,
                            "Значение должно быть числом, было установлено значение по умолчанию(100)",
                        )
                    self.write_msg(event.user_id, "Укажите минимальный возраст: ")
                    event = self.get_event()
                    try:
                        age_from = int(event.text)
                    except:
                        self.write_msg(
                            event.user_id,
                            "Значение должно быть числом, было установлено значение по умолчанию(18)",
                        )

                    if age_from > age_to:
                        self.write_msg(
                            event.user_id,
                            "Так как значение минимального больше максимального, их поменяют местами",
                        )
                        age_from, age_to = age_to, age_from
                result = self.db.user.search_user(
                    city, sex=sex, age_at=age_at, age_to=age_to
                )
                if result == dict():
                    self.write_msg(
                        event.user_id,
                        "К сожалению мы ничего не нашли. Удачи в вечном одиночестве",
                    )
                else:
                    # TODO переписать так, чтобы выдавал только по одному
                    self.write_msg(
                        event.user_id,
                        "Вот несколько вариантов, что удовлетворяют вашим требованиям",
                    )

                    newline = "\n"
                    self.write_msg(
                        event.user_id,
                        f"{newline.join(f'{k+1}: {v[0],v[2]}' for k, v in result.items())}",
                    )
                    self.sender(
                        event.user_id,
                        "Хотите взглянуть на чьё-нибудь фото?",
                        keyboard_search,
                    )
                    event = self.get_event()
                    if event.text.lower() == "да":
                        # TODO отправка фото
                        self.write_msg(event.user_id, "Пожалуйста укажите номер: ")
                        event = self.get_event()
                        person_id = result[int(event.text) - 1][3]

                        # self.write_msg(event.user_id, self.db.user.get_photo(person_id))
                        for i in range(3):
                            print(
                                f"{self.db.user.get_photo(person_id)[i][1]}"
                            )
                            self.write_msg(
                                event.user_id,
                                f'№{i}',
                                attachment=f"{self.db.user.get_photo(person_id)[i][1]}",
                            )

                #                     if event.text == "1":
                #                         self.write_msg(event.user_id, "Укажите номер ")
                #                         event = self.get_event()
                #                         self.db.add_user(
                #                             event.user_id,
                #                             vk_id=result[int(event.text)][3],
                #                             city=city,
                #                             first_name=result[int(event.text)][0],
                #                             last_name=result[int(event.text)][1],
                #                         )
                #                         self.write_msg(event.user_id, "Пользователь успешно добавлен")
                # #
                # for k, v in result.items():
                #     self.write_msg(event.user_id, f"{k} - {v}")
                return
            case other:
                self.write_msg(
                    event.user_id,
                    f"Такой команды нет\n",
                )
                return
        # match event.type:
        #     case VkEventType.MESSAGE_NEW:
        #         print(event.text)
        #         if event.text == "Начать":
        #             self.greating(event.user_id)
        #             self.db.register_user(event.user_id)
        #         elif event.text == "test":
        #             self.test(event.user_id, event.from_id)

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
