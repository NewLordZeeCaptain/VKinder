import vk_api
from random import randrange
from vk_api.longpoll import VkLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
# from functions.vk_functions import search_users, get_photo, sort_likes, json_create
# from db.db import (
#     engine,
#     Session,
#     write_msg,
#     register_user,
#     add_user,
#     add_user_photos,
#     add_to_black_list,
#     check_db_user,
#     check_db_black,
#     check_db_favorites,
#     check_db_master,
#     delete_db_blacklist,
#     delete_db_favorites,
# )
from configs.config import GROUP_TOKEN, USER_TOKEN, CALLBACK_TYPES

from db.db import DB
# from functions.user_functions import User

kbsetting = dict()
    
class Bot(object):
    """Used to interact with Vk Bot API with longpoll"""
    def __init__(self, GROUP_TOKEN, USER_TOKEN, CONSTR):
        super(Bot, self).__init__()
        self.GROUP_TOKEN=GROUP_TOKEN
        self.USER_TOKEN=USER_TOKEN
        self.CONSTR=CONSTR
        self.kb = VkKeyboard()
        

    def bot_loop(self):
        self.vk = vk_api.VkApi(token=self.GROUP_TOKEN)
        
        longpoll = VkLongPoll(self.vk)
        
        for event in longpoll.listen():
            return event
        

    def start(self):
        self.db = DB(self.CONSTR, self.USER_TOKEN)
        
        
        while True:
            event = self.bot_loop()
            # print(event.text, event.user_id)
            self.bot_menu(event)
            
            

    def greating(self, user_id):
        
        self.write_msg(user_id=user_id,message=
              f"Приветствую!\nЭтот бот заменит вам ныне не работающий Tinder и поможет найти близких людей\nВы были автоматически зарегистрированы, но можете в любой момент удалить свой профиль\nДля работы с ботом используйте кнопки ниже\n"
              )
    
    def test(self, user_id, vk_id):
        
        self.db.add_to_blacklist(user_id, vk_id)
    
    
    
    def bot_menu(self, event):
        
        # #Bottons
        # self.kb.add_callback_button("test",payload={"type": "show_snackbar", "text": "test"})
        # self.kb.add_callback_button("Избранные")
        # self.kb.add_callback_button("Blacklist")
        # self.kb.add_line()
        # self.kb.add_callback_button("Поиск партнёра",payload={"type": "find_dating"})
        # self.kb.add_line()
        # self.kb.add_callback_button("Настройки",color=VkKeyboardColor.NEGATIVE) 

        match event.type:
            case VkBotEventType.MESSAGE_NEW:
                print(event.text)
                if event.text == "Начать":
                    self.greating(event.user_id)
                    self.db.register_user(event.user_id)
                elif event.text == "test":
                    
                    self.test(event.user_id, event.from_id)
                    
                    
                elif self.event.from_user:
                    vk.messages.send(
                        user_id=event.obj.message['from_id'],
                        random_id=get_random_id(),
                        peer_id=event.obj.message['from_id'],
                        keyboard=keyboard_1.get_keyboard(),
                        message=event.obj.message['text'])
            # case VkBotEventType.USER_CALL:
            #         if event.object.payload.get('type') in CALLBACK_TYPES:
            #             r = vk.messages.sendMessageEventAnswer(
            #             event_id=event.object.event_id,
            #             user_id=event.object.user_id,
            #             peer_id=event.object.peer_id,                                                   
            #             event_data=json.dumps(event.object.payload))
            #         elif event.object.payload.get('type') == "find_dating":
            #             pass
                    
            
    
    
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
        