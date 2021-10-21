
import settings, time, json, random, information, simplemysql
import asyncio
from vkbottle.tools.dev_tools.keyboard.action import Payload
from vkbottle.bot import Bot, Message
from vkbottle.tools import Keyboard, KeyboardButtonColor, Text
from vkbottle import BaseStateGroup

####################################################

bot = Bot(token=settings.TOKEN) #### group_ids=settings.GROUP_ID

database = simplemysql.Pymysql(host = settings.DB_HOST, 
			user = settings.DB_USER, 
			db = settings.DATABASE, 
			password = settings.DB_PASSWORD, 
			port = settings.DB_PORT)

async def getUser(user_id):
	try: 
		return (await bot.api.users.get(user_ids=user_id))[0]
	except: 
		return None


async def getChat(chat_id):
	try:
		result = (await bot.api.messages.get_conversations_by_id(
			peer_ids = int(chat_id) + 2e9, 
			group_id=settings.GROUP_ID)).items
		if result != []: 
			return result[0]
		else: 
			return False
	except: 
		return None


async def getid(pattern):
	pattern = str(pattern)
	if pattern.isdigit(): 
		return pattern
	elif "vk.com/" in pattern:
		your_id = (await bot.api.users.get(user_ids=pattern.split("/")[-1]))[0]
		return your_id.id
	elif "[id" in pattern:
		your_id = pattern.split("|")[0]
		your_id = (await bot.api.users.get(user_ids = your_id.replace("[id", "")))[0]
		return your_id


async def add_gamer(member):
	database.request(f"INSERT INTO `gamers` (`gamer_id`) VALUES ('{member}')")

async def del_gamer(member):
	database.request(f"DELETE FROM `gamers` WHERE gamer_id = '{member}'")

async def win_plus(member):
	database.request(f"UPDATE `vk_users` SET `wins`=`wins` + 1 WHERE user_id = '{member}'")

async def defeat_plus(member):
	database.request(f"UPDATE `vk_users` SET `defeats`=`defeats` + 1 WHERE user_id = '{member}'")

async def win_bet(bet, member):
	database.request(f"UPDATE `vk_users` SET `balance`=`balance` + {bet} WHERE user_id = '{member}'")

async def defeat_bet(bet, member):
	database.request(f"UPDATE `vk_users` SET `balance`=`balance` - {bet} WHERE user_id = '{member}'")

	

####################################################



####################################################


Menu_key = (
	Keyboard(one_time=True, inline=False)
	.add(Text("Расскажи о себе"), color=KeyboardButtonColor.SECONDARY)
	.add(Text("/help"), color=KeyboardButtonColor.SECONDARY)
	.get_json()
)

@bot.on.private_message(text = "/reg")
async def registrate(event: Message):
	result = database.request(f"SELECT * FROM `vk_users` WHERE `user_id` = '{event.peer_id}'", "result")
	member = await getUser(event.from_id)

	if result == 0:
		database.request(f"INSERT INTO `vk_users`(`user_id`) VALUES ('{event.peer_id}')")
		await event.answer("Теперь вы зарегестрированы в боте", keyboard=Menu_key)
	else:
		await event.answer("Ты и так зареган")




@bot.on.private_message(text = "Расскажи о себе")
async def InfoSelf(event: Message):
	await event.answer(
		"Драсте, я свободный бот, плывущий по течению\n" +
		"Я - никто, и зовут меня - никак\n" +
		"Мой создатель - стесняшка и создал меня для проветки: сможет ли он укратить змею\n" +
		"Не отвликайте его, но я буду благодарен если дадите ему совет, спасибо\n" +
		"Крч, ближе к делу. Коль уж ты решил узнать мои команды напиши\n" +
		"{/help} - Без скобок)", 
		disable_mentions=1, random_id=0)


@bot.on.message(text = "/help")
async def Help(event: Message):
	await event.answer(
		"Не знаешь что делать, да?\n" +
		"Лады, держи основной перечень моих команд (которые не похожи на команды)\n" +
		"/help - список команд, прикинь\n" +
		"/reg - регистрация для бота\n\n" +
		"/tell (виртуальный ютубер или Hololive)\n\n" +
		"/repeat (текст) - просто повторяю\n" +
		"/calc (число) (+ , - , * , /) (число)\n" +
		"/game - есть несколько игр (нужно зарегистрироваться)\n\n" +
		"/for (ссылка на человека) (сообщание) - бот отправляет сообщение по ссылке в вк (только тем, у кого есть диалог с ботом)", 
		disable_mentions=1, random_id=0)


@bot.on.private_message(text = ["/calc", "/calc <first> <math_act> <second>"])
async def Calculator(event: Message, first = None, second = None, math_act = None):
	if ( str(first).isdigit() ) and ( str(second).isdigit() ) and ( math_act in ["+", "-", "*", "/"] ):
		if math_act == "+":
			await event.answer(f"{ int(first) + int(second) }")
		elif math_act == "-":
			await event.answer(f"{ int(first) - int(second) }")
		elif math_act == "*":
			await event.answer(f"{ int(first) * int(second) }")
		elif math_act == "/":
			if second != "0":
				await event.answer(f"{ int(first) / int(second) }")
			else:
				await event.answer("На ноль делить нельзя", disable_mentions=1, random_id=0)	
	else: 
		await event.answer("Неверно указаны значения", disable_mentions=1, random_id=0)

	
@bot.on.private_message(text = ["Привет", "привет", "прив", "Прив"])
async def Hello(event: Message):
	await event.answer("Привет", disable_mentions=1, random_id=0)

@bot.on.private_message(text = ["Пока", "пока", "Покеда", "покеда", "До свидания", "до свидания"])
async def GoodBye(event: Message):
	await event.answer("Пока", disable_mentions=1, random_id=0)


@bot.on.private_message(text = ["/repeat", "/repeat <that_repeat>"])
async def Parrot(event: Message, that_repeat = None):
	if that_repeat:
		await event.answer(that_repeat, disable_mentions=1, random_id=0)
	else:
		await event.answer("ты ничё не ввёл, придурок...", disable_mentions=1, random_id=0)


@bot.on.private_message(text = ["Молодец", "Красава", "Лучший", "Повторил"])
async def Thank(event: Message):
	await event.answer("пасибо, чел", disable_mentions=1, random_id=0)


@bot.on.private_message(text = ["Плохо", "Плохой", "нет"])
async def NoThank(event: Message):
	await event.answer("Ну и ладно, ну и не надо", disable_mentions=1, random_id=0)


###################################################################

@bot.on.message(text = ["/tell <something>", "/tell"])
async def InfoOfMember(event: Message, something = None):
	if something:
		if something == "Hololive" or something == "Хололайв" or something == "hololive" or something == "хололайв": 
			await event.answer(information.HOLOLIVE, disable_mentions=1, random_id=0)
			
		elif something == "Sora" or something == "Tokino" or something == "Сора" or something == "Токино":
			await event.answer(information.SORA_1, disable_mentions=1, random_id=0)
			time.sleep(4)
			await event.answer(information.SORA_2, disable_mentions=1, random_id=0)
			time.sleep(2)
			await event.answer(information.SORA_3, disable_mentions=1, random_id=0)
			time.sleep(5)
			await event.answer(information.SORA_4, disable_mentions=1, random_id=0)

		elif something == "Roboco" or something == "Робоко":
			await event.answer(information.ROBOCO_1, disable_mentions=1, random_id=0)
			time.sleep(4)
			await event.answer(information.ROBOCO_2, disable_mentions=1, random_id=0)
			time.sleep(2)
			await event.answer(information.ROBOCO_3, disable_mentions=1, random_id=0)
			time.sleep(5)
			await event.answer(information.ROBOCO_4, disable_mentions=1, random_id=0)

		elif something == "Miko" or something == "Sakura" or something == "Мико" or something == "Сакура":
			await event.answer(information.MIKO_1, disable_mentions=1, random_id=0)
			time.sleep(4)
			await event.answer(information.MIKO_2, disable_mentions=1, random_id=0)
			time.sleep(2)
			await event.answer(information.MIKO_3, disable_mentions=1, random_id=0)
			time.sleep(5)
			await event.answer(information.MIKO_4, disable_mentions=1, random_id=0)

		elif something == "Suisei" or something == "Hoshimachi" or something == "Суисей" or something == "Хошимачи":
			await event(information.SUISEI_1, disable_mentions=1, random_id=0)
			time.sleep(4)
			await event.answer(information.SUISEI_2, disable_mentions=1, random_id=0)
			time.sleep(2)
			await event.answer(information.SUISEI_3, disable_mentions=1, random_id=0)
			time.sleep(5)
			await event.answer(information.SUISEI_4, disable_mentions=1, random_id=0)

		elif something == "AZKi" or something == "Азки":
			await event.answer(information.AZKi_1, disable_mentions=1, random_id=0)
			time.sleep(4)
			await event.answer(information.AZKi_2, disable_mentions=1, random_id=0)
			time.sleep(2)
			await event.answer(information.AZKi_3, disable_mentions=1, random_id=0)
			time.sleep(5)
			await event.answer(information.AZKi_4, disable_mentions=1, random_id=0)

		elif something == "Mel" or something == "Yozora" or something == "Мэл" or something == "Ёзора":
			await event.answer(information.MEL_1, disable_mentions=1, random_id=0)
			time.sleep(4)
			await event.answer(information.MEL_2, disable_mentions=1, random_id=0)
			time.sleep(2)
			await event.answer(information.MEL_3, disable_mentions=1, random_id=0)
			time.sleep(5)
			await event.answer(information.MEL_4, disable_mentions=1, random_id=0)

		elif something == "Fubuki" or something == "Shirakami" or something == "Фубуки" or something == "Шираками":
			await event.answer(information.FUBUKI_1, disable_mentions=1, random_id=0)
			time.sleep(4)
			await event.answer(information.FUBUKI_2, disable_mentions=1, random_id=0)
			time.sleep(2)
			await event.answer(information.FUBUKI_3, disable_mentions=1, random_id=0)
			time.sleep(5)
			await event.answer(information.FUBUKI_4, disable_mentions=1, random_id=0)

		elif something == "Marsuri" or something == "Natsuiro" or something == "Мацури" or something == "Нацуиро":
			await event.answer(information.MATSURI_1, disable_mentions=1, random_id=0)
			time.sleep(4)
			await event.answer(information.MATSURI_2, disable_mentions=1, random_id=0)
			time.sleep(2)
			await event.answer(information.MATSURI_3, disable_mentions=1, random_id=0)
			time.sleep(5)
			await event.answer(information.MATSURI_4, disable_mentions=1, random_id=0)

		elif something == "Aki" or something == "Rosenthal" or something == "Аки" or something == "Розенталь":
			await event.answer(information.AKI_1, disable_mentions=1, random_id=0)
			time.sleep(4)
			await event.answer(information.AKI_2, disable_mentions=1, random_id=0)
			time.sleep(2)
			await event.answer(information.AKI_3, disable_mentions=1, random_id=0)
			time.sleep(5)
			await event.answer(information.AKI_4, disable_mentions=1, random_id=0)

		elif something == "Haato" or something == "Akai" or something == "Haachama" or something == "Хаачама" or something == "Хаато" or something == "Акаи":
			await event.answer(information.HAATO_1, disable_mentions=1, random_id=0)
			time.sleep(4)
			await event(information.HAATO_2, disable_mentions=1, random_id=0)
			time.sleep(2)
			await event.answer(information.HAATO_3, disable_mentions=1, random_id=0)
			time.sleep(5)
			await event.answer(information.HAATO_4, disable_mentions=1, random_id=0)
			time.sleep(4)	
			await event.answer(information.HAATO_5, disable_mentions=1, random_id=0)

		elif something == "Chris" or something == "Hitomi" or something == "Крис" or something == "Хитоми":
			await event.answer(information.CHRIS_1, disable_mentions=1, random_id=0)
			time.sleep(4)
			await event.answer(information.CHRIS_2, disable_mentions=1, random_id=0)
			time.sleep(2)
			await event.answer(information.CHRIS_3, disable_mentions=1, random_id=0)
			time.sleep(5)
			await event.answer(information.CHRIS_4, disable_mentions=1, random_id=0)

		elif something == "Aqua" or something == "Minato" or something == "Аква" or something == "Минато":
			await event.answer(information.AQUA_1, disable_mentions=1, random_id=0)
			time.sleep(4)
			await event.answer(information.AQUA_2, disable_mentions=1, random_id=0)
			time.sleep(2)
			await event.answer(information.AQUA_3, disable_mentions=1, random_id=0)
			time.sleep(5)
			await event.answer(information.AQUA_4, disable_mentions=1, random_id=0)			

		elif something == "Shion" or something == "Murasaki" or something == "Шион" or something == "Мурасаки":
			await event.answer(information.SHION_1, disable_mentions=1, random_id=0)
			time.sleep(4)
			await event.answer(information.SHION_2, disable_mentions=1, random_id=0)
			time.sleep(2)
			await event.answer(information.SHION_3, disable_mentions=1, random_id=0)
			time.sleep(5)
			await event.answer(information.SHION_4, disable_mentions=1, random_id=0)						

		elif something == "Ayame" or something == "Nakiri" or something == "Аямэ" or something == "Накири":
			await event.answer(information.AYAME_1, disable_mentions=1, random_id=0)
			time.sleep(4)
			await event.answer(information.AYAME_2, disable_mentions=1, random_id=0)
			time.sleep(2)
			await event.answer(information.AYAME_3, disable_mentions=1, random_id=0)
			time.sleep(5)
			await event.answer(information.AYAME_4, disable_mentions=1, random_id=0)

		elif something == "Choko" or something == "Yuzuki" or something == "Чоко" or something == "Юзуки": 
			await event.answer(information.CHOKO_1, disable_mentions=1, random_id=0)
			time.sleep(4)
			await event.answer(information.CHOKO_2, disable_mentions=1, random_id=0)
			time.sleep(2)
			await event.answer(information.CHOKO_3, disable_mentions=1, random_id=0)
			time.sleep(5)
			await event.answer(information.CHOKO_4, disable_mentions=1, random_id=0)

		elif something == "Subaru" or something == "Oozora" or something == "Субару" or something == "Одзора":
			await event.answer(information.SUBARU_1, disable_mentions=1, random_id=0)
			time.sleep(4)
			await event.answer(information.SUBARU_2, disable_mentions=1, random_id=0)
			time.sleep(2)
			await event.answer(information.SUBARU_3, disable_mentions=1, random_id=0)
			time.sleep(5)
			await event.answer(information.SUBARU_4, disable_mentions=1, random_id=0)			




		else:
			await event.answer("Не-a, не понял", disable_mentions=1, random_id=0)
	else:
		await event.answer("Ну, так о чём рассказать-то?", disable_mentions=1, random_id=0)

#################

@bot.on.message(text = "Список участниц Hololive")
async def ListOfHololive(event: Message):
	await event.answer(
		"На сегодняшний день виртуальные ютуберы есть в 4 странах:\n" +
		"Япония (JP)\n" +
		"Индонезия (ID)\n" +
		"Китай (CH)\n" +
		"Англия (EN)\n\n" +
		"Чтобы узнать подробнее о каждой группе напиши\n" +
		"{Список участниц Hololive (Индекс)}\n" + 
		"Без скобок)",
		disable_mentions=1, random_id=0)


@bot.on.message(text = ["Список участниц Hololive <index> <number>", "Список участниц Hololive <index>"])
async def ListOfMembers(event: Message, index = None, number = None):
	if number:
		if index == "JP" or index == "jp":
			if number == "0":
				await event.answer(information.LIST_OF_MEMBER_0, disable_mentions=1, random_id=0)
				time.sleep(2)
				await event.answer(
					"Если хочешь узнать подробнее о втубере напиши\n" +
					"/tell (Имя или Фамилия втубера) - без скобочек)))", 
					disable_mentions=1, random_id=0)

			elif number == "1":
				await event.answer(information.LIST_OF_MEMBER_1, disable_mentions=1, random_id=0)
				time.sleep(2)
				await event.answer(
					"Если хочешь узнать подробнее о втубере напиши\n" +
					"/tell (Имя или Фамилия втубера) - без скобочек)))", 
					disable_mentions=1, random_id=0)

			elif number == "2":
				await event.answer(information.LIST_OF_MEMBER_2, disable_mentions=1, random_id=0)
				time.sleep(2)
				await event.answer(
					"Если хочешь узнать подробнее о втубере напиши\n" +
					"/tell (Имя или Фамилия втубера) - без скобочек)))", 
					disable_mentions=1, random_id=0)

			elif number == "3":
				await event.answer(information.LIST_OF_MEMBER_3, disable_mentions=1, random_id=0)
				time.sleep(2)
				await event.answer(
					"Если хочешь узнать подробнее о втубере напиши\n" +
					"/tell (Имя или Фамилия втубера) - без скобочек)))", 
					disable_mentions=1, random_id=0)

			elif number == "4":
				await event.answer(information.LIST_OF_MEMBER_4, disable_mentions=1, random_id=0)
				time.sleep(2)
				await event.answer(
					"Если хочешь узнать подробнее о втубере напиши\n" +
					"/tell (Имя или Фамилия втубера) - без скобочек)))", 
					disable_mentions=1, random_id=0)

			elif number == "5":
				await event.answer(information.LIST_OF_MEMBER_5, disable_mentions=1, random_id=0)
				time.sleep(2)
				await event.answer(
					"Если хочешь узнать подробнее о втубере напиши\n" +
					"/tell (Имя или Фамилия втубера) - без скобочек)))", 
					disable_mentions=1, random_id=0)

			elif number == "G" or number == "g":
				await event(information.LIST_OF_MEMBER_GAMERS, disable_mentions=1, random_id=0)
				time.sleep(2)
				await event.answer(
					"Если хочешь узнать подробнее о втубере напиши\n" +
					"/tell (Имя или Фамилия втубера) - без скобочек)))", 
					disable_mentions=1, random_id=0)

			else:
				await event.answer("Этой инфы пока что нет)", disable_mentions=1, random_id=0)

		elif index == "EN" or index == "en":
			if int(number) == 1:
				await event.answer(information.LIST_OF_MEMBER_EN, disable_mentions=1, random_id=0)
				time.sleep(2)
				await event.answer(
					"Если хочешь узнать подробнее о втубере напиши\n" +
					"/tell (Имя или Фамилия втубера) - без скобочек)))", 
					disable_mentions=1, random_id=0)

		else:
			await event.answer("Этой инфы пока что нет)", disable_mentions=1, random_id=0)

	else:
		if index == "JP" or index == "jp":
			await event.answer(
				"В японском отделении Hololive\n6 поколений (0 - 5) и поколение Gamers (G)\n" +
				"Для подробной информации о каждом поколении используй\n" +
				"Список участниц Hololive JP (номер поколения или G)\n" +
				"Без скобок))",
				disable_mentions=1, random_id=0)
		elif index == "EN" or index == "en":
			await event.answer(
				"На западе на данный момент одно поколение втуберов (1)\n" +
				"Для подробной информации используй\n" +
				"Список участниц Hololive EN (номер поколения)\n" +
				"Без скобок))",
				disable_mentions=1, random_id=0)

		else:
			await event.answer(
				"СОРИ\n" +
				"Или пока что такого в боте нет, или такого в Hololive нет, или ты ввёл чушь",
				disable_mentions=1, random_id=0)

		




######################### T E S T ##############################

@bot.on.message(text = "Кто я")
async def WhoAmI(event: Message):
	member = await getUser(event.from_id)
	await event.answer(f"{member.last_name} {member.first_name} - это ты", disable_mentions=1, random_id=0)


#@bot.on.message(text = "Пост <textum>")
#async def post_pub(textum = None):
#	api = API(settings.TOKEN)
#   await api.wall.post( "#vkbottle прекрасен!" )


#@bot.on.message(text = "Фото")
#async def photo(event: Message):
#	image = "/home/kod/BotVK/photos/UruhaRushia.jpg"
#	attachments = []
#	upload_image = upload.photo_messages(photos = image)[0] 
#	attachments.append('photo{}_{}'.format(upload_image['owner_id'], upload_image['id']))
#
#	await bot.api.message.send(
#		"Сообщение",
#		attachment = ','.join(attachments) )


################################################################

@bot.on.private_message(text = "/for <id> <message>")
async def TheLetter(event: Message, id = None, message = None):
	member = await getUser(event.from_id)

	await bot.api.messages.send(
		peer_id = id,
		message = (
			f"Вам сообщение от пользователя: {member.last_name} {member.first_name}\n" +
			f"id = {event.from_id}\n\n" +
			f"Сообщение: {message}"),
			random_id=0)
	await event.answer("Сообщение отправлено")


# await bot.api.messages.send(chat_id=domain,
# message=f'Пришло сообщение из беседы <<{chat.chat_settings.title}>> 
# {event.chat_id}:\n\n{text}\n\nДля ответа используйте: /pm <<{event.chat_id}>> <<текст>>', 
# disable_mentions=1, random_id=0)

class Gamers(BaseStateGroup):
    BLACKJACK = 1

BlackJack_key = (
	Keyboard(one_time=True, inline=False)
	.add(Text("/bj more"), color=KeyboardButtonColor.SECONDARY)
	.add(Text("/bj check"), color=KeyboardButtonColor.SECONDARY)
	.get_json()
)


@bot.on.private_message(text = ["/game", "/game <game_name>", "/game <game_name> <bet>"])
async def GameSet(event: Message, game_name = None, bet = None):
	result = database.request(f"SELECT * FROM `vk_users` WHERE user_id = '{event.from_id}'", "result")
	if result != 0:
		if game_name:
			balance = database.request(f"SELECT `balance` FROM `vk_users` WHERE user_id = '{event.from_id}'", "fetchone")
			money = balance["balance"]
			try:
				if bet == None or (int(bet) > 0 and int(bet) <= money*0.5):
					if bet:
						bet = int(bet)
					database.request(f"UPDATE `gamers` SET `bet`='{bet}' WHERE user_id = '{event.from_id}'")

					if game_name in ["Решка", "Орёл", "Орел", "Решка"]:
						await add_gamer(event.peer_id)
						num = random.randint(0,11)
						if num == 0:
							await event.answer("Ребро")
							if game_name == "Ребро":
								await event.answer("Ты победил")
												
								if bet:
									await event.answer(f"Твой выигрыш = {bet * 2}")				
									await win_plus(event.peer_id)
									await win_bet(bet*2, event.peer_id)
								await del_gamer(event.peer_id)
							else:
								await event.answer("Ты проиграл")
								if bet:
									await defeat_plus(event.peer_id)
									await defeat_bet(bet*2, event.peer_id)
								await del_gamer(event.peer_id)

						elif num % 2 == 0:
							await event.answer("Решка")
							if game_name == "Решка":
								await event.answer("Ты победил")
												
								if bet:
									await event.answer(f"Твой выигрыш = {bet * 1.1}")
									await win_plus(event.peer_id)
									await win_bet(bet*1.1, event.peer_id)
								await del_gamer(event.peer_id)

							else:
								await event.answer("Ты проиграл")
								if bet:
									await defeat_plus(event.peer_id)
									await defeat_bet(bet*1.1, event.peer_id)
								await del_gamer(event.peer_id)

						else:
							await event.answer("Орёл")
							if game_name in ["Орёл", "Орел"]:
								await event.answer("Ты победил")
												
								if bet:
									await event.answer(f"Твой выигрыш = {bet * 1.1}")
									await win_plus(event.peer_id)
									await win_bet(bet*1.1, event.peer_id)
								await del_gamer(event.peer_id)

							else:
								await event.answer("Ты проиграл")
								if bet:
									await defeat_plus(event.peer_id)
									await defeat_bet(bet*1.1, event.peer_id)
								await del_gamer(event.peer_id)

					elif game_name in ["BlackJack", "БлекДжек", "blackjack", "блекджек"]:
						await event.answer("Играем в BlackJack!")
						await add_gamer(event.peer_id)
						await bot.state_dispenser.set(event.peer_id, Gamers.BLACKJACK)
						await asyncio.sleep(1.5)

						database.request(f"UPDATE `gamers` SET `score`='{random.randint(2,21)}' WHERE gamer_id = ('{event.peer_id}')")
						score = database.request(f"SELECT `score` FROM `gamers` WHERE gamer_id = '{event.peer_id}'", "fetchone")
						UserCards = score["score"]

						if UserCards == 21:
							await event.answer(f"Твои очки - {UserCards}")
							await event.answer("BlackJack! Ты победил")
							if bet:
								await event.answer(f"Твой выигрыш = {bet * 1.5}")
								await win_bet(bet*1.5, event.peer_id)
							await del_gamer(event.peer_id)
							await bot.state_dispenser.delete(event.peer_id)
						else:
							await event.answer(f"Твои очки - {UserCards}\n" + 
												"Действия:\n/bj more - добавить карту\n" + 
												"/bj check - вскрыть карты",
												keyboard=BlackJack_key)

				else:
					if int(bet) <= 0:
						await event.answer("Введите положительную ставку")
					else:
						await event.answer("Ставка должна быть меньше половины от вашего баланса\n" +
									"/balance - узнать свой баланс")
			except ValueError:
				await event.answer("Некорректная ставка")
		else:
			await event.answer("Есть несколько игр на данный момент\n" +
							"/game Орёл или Решка <ставка> - тут всё понятно\n" +
							"(в случае победы x1.1)\n" +
							"/game BlackJack <ставка> - игра в 21 (Если на русском)\n" +
							"(в случае победы x1.5)\n" +
							"Можно и без ставки")
	else:		
		await event.answer("Вы не прошли регистрацию!\n" + "Пиши /reg")

@bot.on.private_message(state=Gamers.BLACKJACK, text = "/bj <act>")
async def ActForBlackJack(event: Message, act = None):
	result_vk = database.request(f"SELECT * FROM `vk_users` WHERE user_id = '{event.from_id}'", "result")
	result_gamers = database.request(f"SELECT * FROM `gamers` WHERE gamer_id = '{event.from_id}'", "result")
	
	if result_vk != 0 and result_gamers != 0:

		score = database.request(f"SELECT `score` FROM `gamers` WHERE gamer_id = '{event.peer_id}'", "fetchone")
		UserCards = score["score"]

		bet = database.request(f"SELECT `bet` FROM `gamers` WHERE gamer_id = '{event.peer_id}'", "fetchone")
		bet = int(bet["bet"])

		balance = database.request(f"SELECT `balance` FROM `vk_users` WHERE user_id = '{event.from_id}'", "fetchone")
		balance = balance["balance"]

		if UserCards == 0:
			await event.answer("Начни игру\n/game BlakJack")
		
		elif act == "check":
			DilerCards = random.randint(2,21)

			await event.answer(f"Твои очки - {UserCards}\n" +
								f"Очки Дилера - {DilerCards}")
			
			if DilerCards > UserCards or DilerCards == 21:
				await event.answer("Победил Дилер")
				if bet:
					await defeat_plus(event.peer_id)
					await defeat_bet(bet*1.5, event.peer_id)
				await defeat_bet(event.peer_id)
				await bot.state_dispenser.delete(event.peer_id)

			elif DilerCards < UserCards:
				await event.answer("Ты победил")
				if bet:
					await event.answer(f"Ты выиграл {bet * 1.5}")
					await win_plus(event.peer_id)
					await win_bet(bet*1.5, event.peer_id)
				await del_gamer(event.peer_id)
				await bot.state_dispenser.delete(event.peer_id)

			else:
				await event.answer("Ничья")
				if bet:
					await event.answer(f"Твоя ставка вернулась")
				await del_gamer(event.peer_id)
				await bot.state_dispenser.delete(event.peer_id)

		elif act == "more":
			UserCards += random.randint(1,11)
			database.request(f"UPDATE `gamers` SET `score`='{UserCards}' WHERE gamer_id = ('{event.peer_id}')")

			await event.answer(f"Теперь твои очки - {UserCards}")

			if UserCards > 21:
				await event.answer("Ты проиграл")
				if bet:
					await defeat_plus(event.peer_id)
					await defeat_bet(bet*1.5, event.peer_id)
				await del_gamer(event.peer_id)
				await bot.state_dispenser.delete(event.peer_id)
			else:
				await event.answer("/bj more - добавить карту\n" + 
								"/bj check - вскрыть карты",
								keyboard=BlackJack_key)
	else:
		if result_vk == 0:
			await event.answer("Ты не зарегистрирован\n" + "Пиши /reg")
		elif result_gamers == 0:
			await event.answer("Начни игру\n/game BlackJack")



	# if str(msg).isdigit():
	# 	if int(msg) == 4:
	# 		await event.answer("Молодец")
	# 		await event.answer("загрузка.....")
	# 		time.sleep(2)
	# 		await bot.state_dispenser.delete(event.peer_id)
	# 		await event.answer("Теперь ты свободен")
	# 	else:
	# 		await event.answer("не правильно, тупой")
	# else:
	# 	await event.answer("Вообще не то")



ShopKey = (
	Keyboard(one_time=False, inline=False)
	.add(Text("Товар 1", payload={"shop":"mat1"}), color=KeyboardButtonColor.SECONDARY)
	.add(Text("Товар 2", payload={"shop":"mat2"}), color=KeyboardButtonColor.SECONDARY)
	.row()
	.add(Text("Товар 3", payload={"shop":"mat3"}), color=KeyboardButtonColor.SECONDARY)
	.add(Text("Товар 4", payload={"shop":"mat4"}), color=KeyboardButtonColor.SECONDARY)
	.row()
	.add(Text("Следующая страница", payload={"shop":"next"}), color=KeyboardButtonColor.SECONDARY)
	.get_json()
)

ShopKey2 = (
	Keyboard(one_time=False, inline=False)
	.add(Text("Товар 5", payload={"shop":"mat5"}), color=KeyboardButtonColor.SECONDARY)
	.add(Text("Товар 6", payload={"shop":"mat6"}), color=KeyboardButtonColor.SECONDARY)
	.row()
	.add(Text("Пред. страница", payload={"shop":"back"}), color=KeyboardButtonColor.SECONDARY)
	.get_json()
)

@bot.on.private_message(text = "Магазин")
async def shop(event: Message):
	await event.answer("Наш магаз", keyboard = ShopKey)

@bot.on.private_message(payload = {"shop":"mat1"})
async def mat1(event: Message):
	await event.answer("Купил материал 1")
	await event.answer("Записал в кредит")

@bot.on.private_message(payload = {"shop":"mat2"})
async def mat2(event: Message):
	await event.answer("Купил материал 2")
	await event.answer("Записал в кредит")

@bot.on.private_message(payload = {"shop":"mat3"})
async def mat3(event: Message):
	await event.answer("Купил материал 3")
	await event.answer("Записал в кредит")

@bot.on.private_message(payload = {"shop":"mat4"})
async def mat4(event: Message):
	await event.answer("Купил материал 4")
	await event.answer("Записал в кредит")

@bot.on.private_message(payload = {"shop":"next"})
async def next(event: Message):
	await event.answer("Следующая страница", keyboard = ShopKey2)

@bot.on.private_message(payload = {"shop":"mat5"})
async def mat5(event: Message):
	await event.answer("Купил материал 5")
	await event.answer("Записал в кредит")

@bot.on.private_message(payload = {"shop":"mat6"})
async def mat6(event: Message):
	await event.answer("Купил материал 6")
	await event.answer("Записал в кредит")

@bot.on.private_message(payload = {"shop":"back"})
async def back(event: Message):
	await event.answer("Назад", keyboard = ShopKey)






@bot.on.message(text = "/balance")
async def UserBalance(event: Message):	
	result = database.request(f"SELECT * FROM `vk_users` WHERE user_id = '{event.from_id}'", "result")
	if result == 0:
		await event.answer(f"Вы не прошли регистрацию!")
	else:
		balance = database.request(f"SELECT `balance` FROM `vk_users` WHERE user_id = '{event.from_id}'", "fetchone")
		money = balance["balance"]
		await event.answer(f"Ваш баланс: {money} рублей")



@bot.on.message(text = ["/sql", "/sql <request> | <act>", "/sql <request>"])
async def SQLrequest(event: Message, request = None, act = None):

	result = database.request(f"SELECT * FROM `vk_users` WHERE user_id = '{event.from_id}'", "result")
	if result == 0:
		await event.answer(f'Вы не прошли регистрацию!')
	else:
		UserLvl = database.request(f"SELECT `user_lvl` FROM `vk_users` WHERE user_id = '{event.peer_id}'", "fetchone")
		UserLvl = UserLvl["user_lvl"]

		if UserLvl == 0 or UserLvl == 4:
			if request:
				try:
					await event.answer("Обрабатываю запрос")
					if act:	
						answer = database.request(f"{ str(request) }", f"{ str(act) }")
					else:
						answer = database.request(f"{ str(request) }")

					if answer and act:
						await event.answer("Ответ")
						await event.answer(f"{act} =\n {answer}")
					elif answer:
						await event.answer("Ответ")
						await event.answer(answer)
					else:
						await event.answer("Запрос выполнился")

				except:
					await event.answer("Неверный запрос")
			else:
				await event.answer("Нет запроса")
		else:
			await event.answer("У тебя нет прав")


@bot.on.message(text = "/all <msg>")
async def MessageAll(event: Message, msg = None):
	UserLvl = database.request(f"SELECT `user_lvl` FROM `vk_users` WHERE user_id = '{event.peer_id}'", "fetchone")
	UserLvl = UserLvl["user_lvl"]
	if UserLvl == 0:
		await event.answer("Отправляю")
		users = database.request(f"SELECT `user_id` FROM `vk_users`", "fetchall")
		
		for user in users:
			await bot.api.messages.send(
			peer_id = user["user_id"],
			message = (
				f"Вам сообщение от Aдмина:\n" +
				f"Сообщение: {msg}"),
				random_id=0)

		await event.answer("Сообщение отправлено всем")

	else:
		await event.answer("Не получится")


@bot.on.message(text = ["c# pidor", "C# pidor"])
async def lox(event: Message):
	await event.answer("Иди в жопу, Дима")


bot.run_forever()
#  bot.run_polling(skip_updates=False)

