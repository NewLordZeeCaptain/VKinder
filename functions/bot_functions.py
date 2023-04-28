import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from functions.vk_functions import search_users, get_photo, sort_likes, json_create
from db.db import (
    engine,
    Session,
    write_msg,
    register_user,
    add_user,
    add_user_photos,
    add_to_black_list,
    check_db_user,
    check_db_black,
    check_db_favorites,
    check_db_master,
    delete_db_blacklist,
    delete_db_favorites,
)
from configs.config import GROUP_TOKEN, USER_TOKEN

kbsetting = dict()

# Для работы с вк_апи
vk = vk_api.VkApi(token=GROUP_TOKEN)
longpoll = VkLongPoll(vk)
# Для работы с БД
session = Session()
connection = engine.connect()

def loop_bot():
    """creates 

    Returns:
        _type_: _description_
    """
    for this_event in longpoll.listen():
        if this_event.type == VkEventType.MESSAGE_NEW:
            if this_event.to_me:
                message_text = this_event.text
                return message_text, this_event.user_id