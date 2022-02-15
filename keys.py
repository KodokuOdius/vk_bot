from vkbottle.tools import Keyboard, KeyboardButtonColor, Text, EMPTY_KEYBOARD
from vkbottle import Callback


MainKey = (
    Keyboard(one_time=False, inline=False)
    .add(Text("Служебное...", payload={"main": "work"}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text("Игры", payload={"main": "games"}), color=KeyboardButtonColor.POSITIVE)
    .row()
    .add(Text("Интересное", payload={"main": "interesting"}), color=KeyboardButtonColor.SECONDARY)

    .get_json()
)

# Возрат в предыдущее состояние
CancelKey = (
    Keyboard(one_time=False, inline=False)
    .add(Text("Главное меню", payload={"to_main": "main"}), color=KeyboardButtonColor.NEGATIVE)
    .get_json()
)

InterestingKey = (
    Keyboard(one_time=True, inline=False)
    .add(Text("Интересное числа", payload={"interesting": "digits"}), color=KeyboardButtonColor.POSITIVE)
    .add(Text("Ascii", payload={"interesting": "ascii_img"}), color=KeyboardButtonColor.PRIMARY)

    .row()
    .add(Text("Главное меню", payload={"to_main": "main"}), color=KeyboardButtonColor.NEGATIVE)
    .get_json()
)



WorkKey = (
    Keyboard(one_time=True, inline=False)
    .add(Text("Генерация пароля", payload={"work": "gen_password"}), color=KeyboardButtonColor.SECONDARY)

    .row()
    .add(Text("Главное меню", payload={"to_main": "main"}), color=KeyboardButtonColor.NEGATIVE)
    .get_json()
)



GameKey = (
    Keyboard(one_time=True, inline=False)
    .add(Text("Камень-Ножницы-Бумага", payload={"games": "rsp"}))

    .row()
    .add(Text("Главное меню", payload={"to_main": "main"}), color=KeyboardButtonColor.NEGATIVE)
    .get_json()
)

RSPKey = (
    Keyboard(one_time=False, inline=False)
    .add(Text("Камень"), color=KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("Ножницы"), color=KeyboardButtonColor.NEGATIVE)
    .row()
    .add(Text("Бумага"), color=KeyboardButtonColor.PRIMARY)

    .row()
    .add(Text("Главное меню", payload={"to_main": "main"}), color=KeyboardButtonColor.POSITIVE)
    .get_json()
)