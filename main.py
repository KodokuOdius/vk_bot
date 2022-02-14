from bot import BOT
from vkbottle.bot import Message, rules
from vkbottle import BaseStateGroup
import keys
from custom_rules import Ban
from asyncio import sleep
from vkbottle.tools import DocMessagesUploader

####################################################

# database = simplemysql.Pymysql(host = settings.DB_HOST, 
# 			user = settings.DB_USER, 
# 			db = settings.DATABASE, 
# 			password = settings.DB_PASSWORD, 
# 			port = settings.DB_PORT)



@BOT.on.private_message(text=["меню", "главная", "main", "menu", "key"])
async def special_word(event: Message):
	await main(event)




@BOT.on.private_message(payload={"main": "work"})
async def work_info(event: Message):
	await event.answer(
		"В этом разделе меню будут находиться служебные функции\n" +
		"Не знаю как это работает (づ￣ 3￣)づ",
		keyboard=keys.WorkKey
	)


class WorkStates(BaseStateGroup):
	GEN_PASSWORD = 1

@BOT.on.private_message(payload={"work": "gen_password"})
async def password_info(event: Message):
	await event.answer(
		"Просто введи длинну пароля от 8 до 36 символов\n" +
		"На что-то другое не буду реагировать (∪.∪ )...zzz"
	)
	await BOT.state_dispenser.set(event.from_id, WorkStates.GEN_PASSWORD)


@BOT.on.private_message(state=WorkStates.GEN_PASSWORD)
async def generate_password(event: Message):
	if event.text.isdigit() and 7 < int(event.text) < 37:
		import string
		from random import sample
		symbols = string.ascii_letters + string.digits + "_(){}[]\/?!@*#$^<>+"
		await event.answer(
			f"Вот твой пароль в {event.text} символов\n" +
			f"{''.join(sample(symbols, int(event.text)))}"
		)
		await BOT.state_dispenser.delete(event.from_id)
	else:
		await BOT.api.messages.delete(
			message_ids=event.id,
			delete_for_all=True
		)
	


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
	RockScissorsPaper = 2

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
	chosen = ["Камень", "Ножницы", "Бумага"]
	if event.text in chosen:
		from random import choice as ch

		bot_choice = ch(chosen)
		if bot_choice == event.text:
			await event.answer(
				f"У меня тоже {bot_choice}\n" +
				r"Видимо ничья ¯\_(ツ)_/¯"
			)
		elif bot_choice.count("а") > event.text.count("а") or (event.text == "Ножницы" and bot_choice == "Бумага"):
			await event.answer(
				f"У меня {bot_choice}\n" +
				r"Я победил ( ͡~ ͜ʖ ͡°)"
			)
		else:
			await event.answer(
				f"У меня  {bot_choice}\n" +
				r"Ладно, ты победил <(＿　＿)>"
			)
		sleep(1)

		await event.answer(
			"Держи главное меню",
			keyboard=keys.MainKey
		)
		

		await BOT.state_dispenser.delete(event.from_id)


@BOT.on.private_message(payload={"main": "interesting"})
async def interesting_info(event: Message):
	await event.answer(
		"В этом меню будут интересные функции\n" +
		"Что - то намечает O(∩_∩)O",
		keyboard=keys.InterestingKey
	)

class InterestingState(BaseStateGroup):
	IterestingDigits = 3

@BOT.on.private_message(payload={"interesting": "digits"})
async def interesting_digits(event: Message):
	await BOT.state_dispenser.set(event.from_id, InterestingState.IterestingDigits)
	await event.answer(
		"Введи любое число, а я найду интереснй факт об этом числе\n" +
		"Если такой есть (/≧▽≦)/"
	)

@BOT.on.private_message(state=InterestingState.IterestingDigits)
async def find_interesting_digits(event: Message):
	# Проблема с гугл переводчиком
	if event.text.isdigit():
		await event.answer("Давай поищем.....")

		import requests as req

		#from googletrans import Translator
		#translator = Translator()

		api_link = f"http://numbersapi.com/{event.text}/math"
		
		data = req.get(api_link, params={"json": True}).json()["text"]
		#result = translator.translate("Привет")

		await event.answer(data)
		
		await BOT.state_dispenser.delete(event.from_id)
	else:
		# [15] Access denied: message can not be deleted (peer message)
		await BOT.api.messages.delete(
			message_ids=event.id,
			delete_for_all=True
		)



@BOT.on.private_message(attachment='photo')
async def photo_trigger(event: Message):
	import requests as req
	from PIL import Image
	
	# with open(f"photos/{event.attachments[0].photo.access_key}.png", "wb") as _out:
	# 	file = req.get(event.attachments[0].photo.sizes[-1].url)
	# 	_out.write(file.content)
	
	await event.answer("Конвертирую.....")

	_asciiTable = ".,:+*?%S#@"[::-1]
	file = req.get(event.attachments[0].photo.sizes[-1].url)

	img = Image.open(file)

	WIDTH_OFFSET = 1.75
	MAX_WIDTH = 500
	MAX_HEIGHT = int(img.height / WIDTH_OFFSET * MAX_WIDTH / img.width)

	if img.width > MAX_WIDTH or img.height > MAX_HEIGHT:
		img = img.resize((MAX_WIDTH, MAX_HEIGHT))


	x, y = img.size

	await event.answer("Секунду....")

	with open("ascii.txt", "w") as _out:
		for i in range(y):
			for j in range(x):
				pixels = img.getpixel((j, i))
				map_val = sum(pixels) / len(pixels)

				_out.write(_asciiTable[ int((map_val / 255) * 9) ])
			
			_out.write('\n')
		
		# url = requests.get('https://vk.com/doc550522050_622166526?hash=db5d813ac61d66abd5&dl=8f84d53f948d3dbe3e')
		# doc = await DocMessagesUploader(bot.api).upload(
		# 	title='HomeWork.txt',
		# 	file_source=url.content,
		# 	peer_id=event.peer_id
		# )
		# await event.answer(attachment=doc)

	doc = await DocMessagesUploader(BOT.api).upload(
		title="Assci_photo.txt",
		file_source="ascii.txt",
		peer_id=event.peer_id
	)

	await event.answer(
		"Твоя ascii фотка, прошу!",
		attachment=doc
	)






@BOT.on.private_message()
async def main(event: Message):
	await event.answer(
		message="Держи клавиатуру...",
		keyboard=keys.MainKey
	)


BOT.run_forever()