import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from functions.vk_functions import search_users, get_photo, sort_likes, json_create
from db.db import engine, Session, write_msg, register_user, add_user, add_user_photos, add_to_black_list, \
    check_db_user, check_db_black, check_db_favorites, check_db_master, delete_db_blacklist, delete_db_favorites
from configs.config import GROUP_TOKEN

# Для работы с вк_апи
vk = vk_api.VkApi(token=GROUP_TOKEN)
longpoll = VkLongPoll(vk)
# Для работы с БД
session = Session()
connection = engine.connect()


def loop_bot():
    for this_event in longpoll.listen():
        if this_event.type == VkEventType.MESSAGE_NEW:
            if this_event.to_me:
                message_text = this_event.text
                return message_text, this_event.user_id


def menu_bot(id_num):
    write_msg(id_num,
              f"Vkinder\n"
              f"\nIf you're using it in first time you should registrate.\n"
              f"To registrate say Да\n"
              f"If you're allready in app start search\n"
              f"\nObject for searc: female \n"
              f"Press 2 to go to favorite\n"
              f"Press 0 to go to blacklist\n")


def show_info():
    write_msg(user_id, f'It was last profile.'
                       f'Go to favorite - 2'
                       f'Go to blacklist - 0'
                       f'Object: female'
                       f'Menu')


def reg_new_user(id_num):
    write_msg(id_num, 'Reg. Finished.')
    write_msg(id_num,
              f"Vkinder activated\n")
    register_user(id_num)


def go_to_favorites(ids):
    alls_users = check_db_favorites(ids)
    write_msg(ids, f'Favorites:')
    for nums, users in enumerate(alls_users):
        write_msg(ids, f'{users.first_name}, {users.second_name}, {users.link}')
        write_msg(ids, '1 - Delete from favorite, 0 - Next \nq - Quit')
        msg_texts, user_ids = loop_bot()
        if msg_texts == '0':
            if nums >= len(alls_users) - 1:
                write_msg(user_ids, f'It was last profile.\n'
                                    f'Menu\n')
        # Удаляем запись из бд - избранное
        elif msg_texts == '1':
            delete_db_favorites(users.vk_id)
            write_msg(user_ids, f'Profile deleted.')
            if nums >= len(alls_users) - 1:
                write_msg(user_ids, f'It was last profile\n'
                                    f'Menu\n')
        elif msg_texts.lower() == 'q':
            write_msg(ids, 'Vkinder activated.')
            break


def go_to_blacklist(ids):
    all_users = check_db_black(ids)
    write_msg(ids, f'Анкеты в черном списке:')
    for num, user in enumerate(all_users):
        write_msg(ids, f'{user.first_name}, {user.second_name}, {user.link}')
        write_msg(ids, '1 - delete from blacklist, 0 - Next\nq - Quit')
        msg_texts, user_ids = loop_bot()
        if msg_texts == '0':
            if num >= len(all_users) - 1:
                write_msg(user_ids, f'It was last profile.\n'
                                    f'Menu\n')
        # Удаляем запись из бд - черный список
        elif msg_texts == '1':
            print(user.id)
            delete_db_blacklist(user.vk_id)
            write_msg(user_ids, f'Profile deleted')
            if num >= len(all_users) - 1:
                write_msg(user_ids, f'It was last profile.\n'
                                    f'Menu\n')
        elif msg_texts.lower() == 'q':
            write_msg(ids, 'Vkinder activated.')
            break


if __name__ == '__main__':
    while True:
        msg_text, user_id = loop_bot()
        if msg_text == "vkinder":
            menu_bot(user_id)
            msg_text, user_id = loop_bot()
            # Регистрируем пользователя в БД
            if msg_text.lower() == 'да':
                reg_new_user(user_id)
            # Ищем партнера
            elif len(msg_text) > 1:
                sex = 0
                if msg_text[0:7].lower() == 'девушка':
                    sex = 1
                elif msg_text[0:7].lower() == 'мужчина':
                    sex = 2
                age_at = msg_text[8:10]
                if int(age_at) < 18:
                    write_msg(user_id, 'Выставлен минимальный возраст - 18 лет.')
                    age_at = 18
                age_to = msg_text[11:14]
                if int(age_to) >= 100:
                    write_msg(user_id, 'Выставлено максимальное значение 99 лет.')
                    age_to = 99
                city = msg_text[14:len(msg_text)].lower()
                # Ищем анкеты
                result = search_users(sex, int(age_at), int(age_to), city)
                json_create(result)
                current_user_id = check_db_master(user_id)
                # Производим отбор анкет
                for i in range(len(result)):
                    dating_user, blocked_user = check_db_user(result[i][3])
                    # Получаем фото и сортируем по лайкам
                    user_photo = get_photo(result[i][3])
                    if user_photo == 'нет доступа к фото' or dating_user is not None or blocked_user is not None:
                        continue
                    sorted_user_photo = sort_likes(user_photo)
                    # Выводим отсортированные данные по анкетам
                    write_msg(user_id, f'\n{result[i][0]}  {result[i][1]}  {result[i][2]}', )
                    try:
                        write_msg(user_id, f'фото:',
                                  attachment=','.join
                                  ([sorted_user_photo[-1][1], sorted_user_photo[-2][1],
                                    sorted_user_photo[-3][1]]))
                    except IndexError:
                        for photo in range(len(sorted_user_photo)):
                            write_msg(user_id, f'фото:',
                                      attachment=sorted_user_photo[photo][1])
                    # Ждем пользовательский ввод
                    write_msg(user_id, '1 - Добавить, 2 - Заблокировать, 0 - Далее, \nq - выход из поиска')
                    msg_text, user_id = loop_bot()
                    if msg_text == '0':
                        # Проверка на последнюю запись
                        if i >= len(result) - 1:
                            show_info()
                    # Добавляем пользователя в избранное
                    elif msg_text == '1':
                        # Проверка на последнюю запись
                        if i >= len(result) - 1:
                            show_info()
                            break
                        # Пробуем добавить анкету в БД
                        try:
                            add_user(user_id, result[i][3], result[i][1],
                                     result[i][0], city, result[i][2], current_user_id.id)
                            # Пробуем добавить фото анкеты в БД
                            add_user_photos(user_id, sorted_user_photo[0][1],
                                            sorted_user_photo[0][0], current_user_id.id)
                        except AttributeError:
                            write_msg(user_id, 'Вы не зарегистрировались!\n Введите Vkinder для перезагрузки бота')
                            break
                    # Добавляем пользователя в черный список
                    elif msg_text == '2':
                        # Проверка на последнюю запись
                        if i >= len(result) - 1:
                            show_info()
                        # Блокируем
                        add_to_black_list(user_id, result[i][3], result[i][1],
                                          result[i][0], city, result[i][2],
                                          sorted_user_photo[0][1],
                                          sorted_user_photo[0][0], current_user_id.id)
                    elif msg_text.lower() == 'q':
                        write_msg(user_id, 'Введите Vkinder для активации бота')
                        break

            # Переходим в избранное
            elif msg_text == '2':
                go_to_favorites(user_id)

            # Переходим в черный список
            elif msg_text == '0':
                go_to_blacklist(user_id)
