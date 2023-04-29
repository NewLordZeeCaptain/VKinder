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
