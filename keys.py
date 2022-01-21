from vkbottle.tools import Keyboard, KeyboardButtonColor, EMPTY_KEYBOARD, Text
from vkbottle import Callback

MainKey = (
    Keyboard(one_time=False, inline=False)
    .add(Text("Игры", payload={"main": "games"}), color=KeyboardButtonColor.POSITIVE)
    .get_json()
)


GameKey = (
    Keyboard(one_time=True, inline=False)
    .add(Callback("Камень-Ножницы-Бумага", payload={"games": "rsp"}))
    .get_json()
)
RSPKey = (
    Keyboard(one_time=True, inline=False)
    .add(Text("Камень"), color=KeyboardButtonColor.SECONDARY)
    .add(Text("Ножницы"), color=KeyboardButtonColor.NEGATIVE)
    .add(Text("Бумага"), color=KeyboardButtonColor.PRIMARY)
    .get_json()
)