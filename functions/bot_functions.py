import vk_api
from random import randrange
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from configs.config import USER_TOKEN, GROUP_TOKEN
from keyboard.keyboard import *
from db.db import *
from functions.user_functions import *

# from functions.user_functions import User


class Bot(object):
    """Used to interact with Vk Bot API with longpoll"""

    def __init__(self, GROUP_TOKEN):
        super(Bot, self).__init__()
        # self.GROUP_TOKEN = GROUP_TOKEN
        # self.USER_TOKEN = USER_TOKEN
        self.vk = vk_api.VkApi(token=GROUP_TOKEN)
        self.longpoll = VkLongPoll(self.vk)
        self.offset = 0
        self.config = {"age_from": 18, "age_to": 100, "sex": 0}

    def get_event(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                return event

    def start(self):
        while True:
            event = self.get_event()
            self.bot_menu(event)

    def sender(self, user_id, text, keyboard, attachment=None):
        self.vk.method(
            "messages.send",
            {
                "user_id": user_id,
                "message": text,
                "random_id": 0,
                "keyboard": keyboard,
                "attachment": attachment,
            },
        )

    def create_config(self):
        self.sender(event.user_id, "Желаете добавить поиск по полу?", keyboard_search)
        event = self.get_event()
        if event.text.lower() == "да":
            self.sender(event.user_id, "Укажите пол: ", keyboard_sex)
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
            event.user_id, "Желаете добавить поиск по возрасту?", keyboard_search
        )
        event = self.get_event()
        if event.text.lower() == "да":
            self.write_msg(event.user_id, "Укажите минимальный возраст")
            try:
                event = self.get_event()
                self.config["age_from"] = int(event.text)
            except:
                self.write_msg(event.user_id, "Было установлено значение по умолчанию")
            self.write_msg(event.user_id, "Укажите максимальный возраст")
            try:
                event = self.get_event()
                self.config["age_to"] = int(event.text)
            except:
                self.write_msg(event.user_id, "Было установлено значение по умолчанию")
        if self.config["age_from"] > self.config["age_to"]:
            self.write_msg(
                event.user_id,
                "Так как значение минимального больше максимального, их поменяют местами",
            )
            self.config["age_form"], self.config["age_to"] = (
                self.config["age_to"],
                self.config["age_from"],
            )
        self.sender(
            event.user_id,
            "Желаете указать конкретный город для поиска? (По умолчанию берётся ваш город из профиля)",
            keyboard_search,
        )
        if event.text.lower() == "да":
            self.write_msg(event.user_id, "Укажите город")
            event = self.get_event()
            city = get_city(event.text)
            self.config["city"] = city

    def search_menu(self, event):
        pass

    def bot_menu(self, event):
        match event.text.lower():
            case "начать":
                isreg = register_user(event.user_id)
                print(isreg)
                if not isreg:
                    self.sender(
                        str(event.user_id),
                        "Приветствую!\nЭтот бот заменит вам ныне не работающий Tinder и поможет найти близких людей\nДля работы воспользуйтесь кнопками ниже\n",
                        keyboard,
                    )
                else:
                    self.sender(str(event.user_id), "С возвращением", keyboard)

            case "избранное":
                fav = check_db_favorites(event.user_id)
                self.write_msg(event.user_id, "Выполняем поиск\n")
                self.write_msg(event.user_id, fav)
                if type(fav) == type(" "):
                    self.write_msg(event.user_id, fav)
                else:
                    for k, v in fav.items():
                        self.write_msg(event.user_id, f"{k} - {v}")

            case "blacklist":
                black = check_db_blacklist(event.user_id)
                self.write_msg(event.user_id, "Выполняем поиск\n")
                if type(black) == type(" "):
                    self.write_msg(event.user_id, black)
                else:
                    for k, v in black.items():
                        self.write_msg(event.user_id, f"{k} - {v}")

            case "настройки":
                self.create_config()
                self.sender(
                    event.user_id, "Теперь можно браться за поиски, удачи!", keyboard
                )

            case "поиск":
                self.find_match(event)

                while True:
                    event = self.get_event()
                    match event.text.lower():
                        case "дальше":
                            self.find_match(event)
                        case "назад":
                            self.sender(
                                event.user_id, "Возвращаем в главное меню", keyboard
                            )
                            break

                    # newline = "\n"
                    # self.write_msg(
                    #     event.user_id,
                    #     f"{newline.join(f'{k+1}: {v[0],v[2]}' for k, v in result.items())}",
                    # )
                    # self.sender(
                    #     event.user_id,
                    #     "Хотите взглянуть на чьё-нибудь фото?",
                    #     keyboard_search,
                    # )
                    # event = self.get_event()

            case other:
                self.write_msg(
                    event.user_id,
                    f"Такой команды нет\n",
                )
                self.sender(event.user_id, "Такой команды нет", keyboard)

        # match event.type:
        #     case VkEventType.MESSAGE_NEW:
        #         print(event.text)
        #         if event.text == "Начать":
        #             self.greating(event.user_id)
        #             self.db.register_user(event.user_id)
        #         elif event.text == "test":
        #             self.test(event.user_id, event.from_id)

    def find_match(self, event):
        link_profile = "https://vk.com/id"
        try:
            self.config['city'] != None
        except:
            
            try:
                self.config["city"] = user_get(event.user_id)["city"]
            except:
                self.write_msg(event.user_id, "Укажите свой город: ")
                event = self.get_event()
                # print(event.text)
                city = get_city(event.text)
                self.config["city"] = cit
        result = search_user(
            city,
            sex=self.config["sex"],
            age_from=self.config["age_from"],
            age_to=self.config["age_to"],
            offset=self.offset,
        )
        if result == dict():
            # self.write_msg(
            #     event.user_id,
            #     "К сожалению мы ничего не нашли. Удачи в вечном одиночестве, ну а можете поменять настройки",
            # )
            self.sender(
                event.user_id,
                "К сожалению мы ничего не нашли, можете жить в вечном одиночестве, или же чуть подправить настройки",
                keyboard,
            )
        else:
            # TODO переписать так, чтобы выдавал только по одному

            self.sender(
                event.user_id,
                f"{result['first_name']} {result['last_name']} - {link_profile+result['id']}",
                keyboard_match,
            )
            self.offset += 1

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
