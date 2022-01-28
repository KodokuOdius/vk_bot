from bot import BOT
from vkbottle.bot import Message, rules
from vkbottle import BaseStateGroup
from vkbottle.modules import json
import keys
from custom_rules import Ban
####################################################

# database = simplemysql.Pymysql(host = settings.DB_HOST, 
# 			user = settings.DB_USER, 
# 			db = settings.DATABASE, 
# 			password = settings.DB_PASSWORD, 
# 			port = settings.DB_PORT)


@BOT.on.private_message(payload={"main":"games"})
async def games_info(event: Message):
	await event.answer(
		message=(
			"Держи рабочие мини - игры:\n" +
			"При нажатии игра автоматически запускается q(≧▽≦q)"
		),
		keyboard=keys.GameKey
	)


class GameState(BaseStateGroup):
	RockScissorsPaper = 1

@BOT.on.private_message(payload={"games": "rsp"})
async def rock_scisors_paper(event: Message):
	await BOT.state_dispenser.set(event.from_id, GameState.RockScissorsPaper)
	await event.answer(
		message=(
			"Выбери Камень, Ножницы или Бумагу\n" +
			"И мы посмотрим кто выйграл)\n" +
			"Примечание: Если вы ввели что-то другое игра закроется"
		),
		keyboard=keys.RSPKey
	)

@BOT.on.private_message(state=GameState.RockScissorsPaper)
async def end_rock_scissors_paper(event: Message):
	
	await event.answer()


@BOT.on.message(Ban(), text=["1"])
async def eveve(event: Message):
	await event.answer(event)


@BOT.on.private_message()
async def main(event: Message):
	await event.answer(
		message="Держи клавиатуру",
		keyboard=keys.MainKey
	)


BOT.run_forever()