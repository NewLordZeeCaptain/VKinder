import json


def get_button(text, color):
    return {
        "action": {
            "type": "text",
            "payload": '{"button": "' + "1" + '"}',
            "label": f"{text}",
        },
        "color": f"{color}",
    }


keyboard = {
    "one_time": True,
    "buttons": [
        [get_button("Начать поиск", "primary")],
        # [get_button("Вперёд", "secondary")],
        [get_button("Избранное", "secondary")],
        [get_button("Blacklist", "secondary")],
    ],
}

keyboard_search = {
    "one_time": True,
    "buttons": [[get_button("Да", "secondary")], [get_button("Нет", "secondary")]],
}

keyboard_sex = {
    "one_time": True,
    "buttons": [
        [get_button("Муж", "secondary")],
        [get_button("Жен", "secondary")],
        [get_button("Любой", "secondary")],
    ],
}
keyboard = json.dumps(keyboard, ensure_ascii=False).encode("utf-8")
keyboard = str(keyboard.decode("utf-8"))

keyboard_search = json.dumps(keyboard_search, ensure_ascii=False).encode("utf-8")
keyboard_search = str(keyboard_search.decode("utf-8"))

keyboard_sex = json.dumps(keyboard_sex, ensure_ascii=False).encode("utf-8")
keyboard_sex = str(keyboard_sex.decode("utf-8"))
