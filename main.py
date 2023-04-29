import vk_api
from functions.bot_functions import Bot
from configs.config import GROUP_TOKEN, USER_TOKEN, CONSTR

# Для работы с вк_апи




# def loop_bot():
#     for this_event in longpoll.listen():
#         if this_event.type == VkBotEventType.MESSAGE_NEW:
#             if this_event.to_me:
#                 message_text = this_event.text
#                 return message_text, this_event.user_id





def show_info(user_id):
    write_msg(
        user_id,
        f"It was last profile."
        f"Go to favorite - 2"
        f"Go to blacklist - 0"
        f"Object: female"
        f"Menu",
    )


def reg_new_user(id_num):
    write_msg(id_num, "Reg. Finished.")
    write_msg(id_num, f"Vkinder activated\n")
    register_user(id_num)


def go_to_favorites(ids):
    alls_users = check_db_favorites(ids)
    write_msg(ids, f"Favorites:")
    for nums, users in enumerate(alls_users):
        write_msg(ids, f"{users.first_name}, {users.second_name}, {users.link}")
        write_msg(ids, "1 - Delete from favorite, 0 - Next \nq - Quit")
        msg_texts, user_ids = loop_bot()
        if msg_texts == "0":
            if nums >= len(alls_users) - 1:
                write_msg(user_ids, f"It was last profile.\n" f"Menu\n")
        # Удаляем запись из бд - избранное
        elif msg_texts == "1":
            delete_db_favorites(users.vk_id)
            write_msg(user_ids, f"Profile deleted.")
            if nums >= len(alls_users) - 1:
                write_msg(user_ids, f"It was last profile\n" f"Menu\n")
        elif msg_texts.lower() == "q":
            write_msg(ids, "Vkinder activated.")
            break


def go_to_blacklist(ids):
    all_users = check_db_black(ids)
    write_msg(ids, f"Анкеты в черном списке:")
    for num, user in enumerate(all_users):
        write_msg(ids, f"{user.first_name}, {user.second_name}, {user.link}")
        write_msg(ids, "1 - delete from blacklist, 0 - Next\nq - Quit")
        msg_texts, user_ids = loop_bot()
        if msg_texts == "0":
            if num >= len(all_users) - 1:
                write_msg(user_ids, f"It was last profile.\n" f"Menu\n")
        # Удаляем запись из бд - черный список
        elif msg_texts == "1":
            print(user.id)
            delete_db_blacklist(user.vk_id)
            write_msg(user_ids, f"Profile deleted")
            if num >= len(all_users) - 1:
                write_msg(user_ids, f"It was last profile.\n" f"Menu\n")
        elif msg_texts.lower() == "q":
            write_msg(ids, "Vkinder activated.")
            break


def main():
    bot = Bot(GROUP_TOKEN=GROUP_TOKEN, USER_TOKEN=USER_TOKEN, CONSTR=CONSTR)
    bot.start()
    
        


if __name__ == "__main__":
    main()
