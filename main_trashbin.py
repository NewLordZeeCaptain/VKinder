        msg_text, user_id = loop_bot()
        print(msg_text,user_id)
        match msg_text:
            case "начать":
                register_user(user_id)
            
                
        if msg_text == "vkinder":
            menu_bot(user_id)
            msg_text, user_id = loop_bot()
            # Регистрируем пользователя в БД
            if msg_text.lower() == "да":
                reg_new_user(user_id)
            # Ищем партнера
            elif len(msg_text) > 1:
                sex = 0
                if msg_text[0:7].lower() == "девушка":
                    sex = 1
                elif msg_text[0:7].lower() == "мужчина":
                    sex = 2
                age_at = msg_text[8:10]
                if int(age_at) < 18:
                    write_msg(user_id, "Выставлен минимальный возраст - 18 лет.")
                    age_at = 18
                age_to = msg_text[11:14]
                if int(age_to) >= 100:
                    write_msg(user_id, "Выставлено максимальное значение 99 лет.")
                    age_to = 99
                city = msg_text[14 : len(msg_text)].lower()
                # Ищем анкеты
                result = search_users(sex, int(age_at), int(age_to), city)
                json_create(result)
                current_user_id = check_db_master(user_id)
                # Производим отбор анкет
                for i in range(len(result)):
                    dating_user, blocked_user = check_db_user(result[i][3])
                    # Получаем фото и сортируем по лайкам
                    user_photo = get_photo(result[i][3])
                    if (
                        user_photo == "нет доступа к фото"
                        or dating_user is not None
                        or blocked_user is not None
                    ):
                        continue
                    sorted_user_photo = sort_likes(user_photo)
                    # Выводим отсортированные данные по анкетам
                    write_msg(
                        user_id,
                        f"\n{result[i][0]}  {result[i][1]}  {result[i][2]}",
                    )
                    try:
                        write_msg(
                            user_id,
                            f"фото:",
                            attachment=",".join(
                                [
                                    sorted_user_photo[-1][1],
                                    sorted_user_photo[-2][1],
                                    sorted_user_photo[-3][1],
                                ]
                            ),
                        )
                    except IndexError:
                        for photo in range(len(sorted_user_photo)):
                            write_msg(
                                user_id,
                                f"фото:",
                                attachment=sorted_user_photo[photo][1],
                            )
                    # Ждем пользовательский ввод
                    write_msg(
                        user_id,
                        "1 - Добавить, 2 - Заблокировать, 0 - Далее, \nq - выход из поиска",
                    )
                    msg_text, user_id = loop_bot()
                    if msg_text == "0":
                        # Проверка на последнюю запись
                        if i >= len(result) - 1:
                            show_info()
                    # Добавляем пользователя в избранное
                    elif msg_text == "1":
                        # Проверка на последнюю запись
                        if i >= len(result) - 1:
                            show_info()
                            break
                        # Пробуем добавить анкету в БД
                        try:
                            add_user(
                                user_id,
                                result[i][3],
                                result[i][1],
                                result[i][0],
                                city,
                                result[i][2],
                                current_user_id.id,
                            )
                            # Пробуем добавить фото анкеты в БД
                            add_user_photos(
                                user_id,
                                sorted_user_photo[0][1],
                                sorted_user_photo[0][0],
                                current_user_id.id,
                            )
                        except AttributeError:
                            write_msg(
                                user_id,
                                "Вы не зарегистрировались!\n Введите Vkinder для перезагрузки бота",
                            )
                            break
                    # Добавляем пользователя в черный список
                    elif msg_text == "2":
                        # Проверка на последнюю запись
                        if i >= len(result) - 1:
                            show_info(user_id)
                        # Блокируем
                        add_to_black_list(
                            user_id,
                            result[i][3],
                            result[i][1],
                            result[i][0],
                            city,
                            result[i][2],
                            sorted_user_photo[0][1],
                            sorted_user_photo[0][0],
                            current_user_id.id,
                        )
                    elif msg_text.lower() == "q":
                        write_msg(user_id, "Введите Vkinder для активации бота")
                        break

            # Переходим в избранное
            elif msg_text == "2":
                go_to_favorites(user_id)

            # Переходим в черный список
            elif msg_text == "0":
                go_to_blacklist(user_id)


# User functions 



# Находит фото людей
def get_photo(user_owner_id):
    vk_ = vk_api.VkApi(token=USER_TOKEN)
    try:
        response = vk_.method(
            "photos.get",
            {
                "access_token": USER_TOKEN,
                "v": VERSION,
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
    return users_photos

# Ищет людей по критериям
def search_users(sex, age_at, age_to, city):
    all_persons = []
    link_profile = "https://vk.com/id"
    vk_ = vk_api.VkApi(token=USER_TOKEN)
    response = vk_.method(
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

# Удаляет пользователя из черного списка
# def delete_db_blacklist(ids):
#     current_user = session.query(BlackList).filter_by(vk_id=ids).first()
#     session.delete(current_user)
#     session.commit()


# # Удаляет пользователя из избранного
# def delete_db_favorites(ids):
#     current_user = session.query(DatingUser).filter_by(vk_id=ids).first()
#     session.delete(current_user)
#     session.commit()


# # проверят зареган ли пользователь бота в БД
# def check_db_master(ids):
#     current_user_id = session.query(User).filter_by(vk_id=ids).first()
#     return current_user_id

# # Проверят есть ли юзер в черном списке
# def check_db_black(ids):
#     current_users_id = session.query(User).filter_by(vk_id=ids).first()
#     # Находим все анкеты из избранного которые добавил данный юзер
#     all_users = session.query(BlackList).filter_by(id_user=current_users_id.id).all()
#     return all_users


# # Проверяет есть ли юзер в избранном
# def check_db_favorites(ids):
#     current_users_id = session.query(User).filter_by(vk_id=ids).first()
#     # Находим все анкеты из избранного которые добавил данный юзер
#     alls_users = session.query(DatingUser).filter_by(id_user=current_users_id.id).all()
#     return alls_users

# # Сохранение выбранного пользователя в БД
# def add_user(event_id, vk_id, first_name, second_name, city, link, id_user):
#     try:
#         new_user = DatingUser(
#             vk_id=vk_id,
#             first_name=first_name,
#             second_name=second_name,
#             city=city,
#             link=link,
#             id_user=id_user,
#         )
#         session.add(new_user)
#         session.commit()
#         write_msg(event_id, "ПОЛЬЗОВАТЕЛЬ УСПЕШНО ДОБАВЛЕН В ИЗБРАННОЕ")
#         return True
#     except (IntegrityError, InvalidRequestError):
#         write_msg(event_id, "Пользователь уже в избранном.")
#         return False

# # Добавление пользователя в черный список
# def add_to_black_list(
#     event_id,
#     vk_id,
#     first_name,
#     second_name,
#     city,
#     link,
#     link_photo,
#     count_likes,
#     id_user,
# ):
#     try:
#         new_user = BlackList(
#             vk_id=vk_id,
#             first_name=first_name,
#             second_name=second_name,
#             city=city,
#             link=link,
#             link_photo=link_photo,
#             count_likes=count_likes,
#             id_user=id_user,
#         )
#         session.add(new_user)
#         session.commit()
#         write_msg(event_id, "Пользователь успешно заблокирован.")
#         return True
#     except (IntegrityError, InvalidRequestError):
#         write_msg(event_id, "Пользователь уже в черном списке.")
#         return False

# # Сохранение в БД фото добавленного пользователя
# def add_user_photos(event_id, link_photo, count_likes, id_dating_user):
#     try:
#         new_user = Photos(
#             link_photo=link_photo,
#             count_likes=count_likes,
#             id_dating_user=id_dating_user,
#         )
#         session.add(new_user)
#         session.commit()
#         write_msg(event_id, "Фото пользователя сохранено в избранном")
#         return True
#     except (IntegrityError, InvalidRequestError):
#         write_msg(
#             event_id, "Невозможно добавить фото этого пользователя(Уже сохранено)"
#         )
#         return False


                    # if event.text.lower() == "да":
                    #     # TODO отправка фото
                    #     self.write_msg(event.user_id, "Пожалуйста укажите номер: ")
                    #     event = self.get_event()
                    #     person_id = result[int(event.text) - 1][3]

                    #     # self.write_msg(event.user_id, self.db.user.get_photo(person_id))
                    #     for i in range(3):
                    #         print(f"{self.db.user.get_photo(person_id)[i][1]}")
                    #         self.write_msg(
                    #             event.user_id,
                    #             f"№{i}",
                    #             attachment=f"{self.db.user.get_photo(person_id)[i][1]}",
                    #         )

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
                