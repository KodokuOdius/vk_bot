from vkbottle.tools import Keyboard, KeyboardButtonColor, EMPTY_KEYBOARD, Text
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

InterestingKey = (
    Keyboard(one_time=True, inline=False)
    .add(Text("Интересное числа", payload={"interesting": "digits"}), color=KeyboardButtonColor.POSITIVE)
    .get_json()
)



WorkKey = (
    Keyboard(one_time=True, inline=False)
    .add(Text("Генерация пароля", payload={"work": "gen_password"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)



GameKey = (
    Keyboard(one_time=True, inline=False)
    .add(Text("Камень-Ножницы-Бумага", payload={"games": "rsp"}))
    .get_json()
)
RSPKey = (
    Keyboard(one_time=True, inline=False)
    .add(Text("Камень"), color=KeyboardButtonColor.SECONDARY)
    .add(Text("Ножницы"), color=KeyboardButtonColor.NEGATIVE)
    .add(Text("Бумага"), color=KeyboardButtonColor.PRIMARY)
    .get_json()
)