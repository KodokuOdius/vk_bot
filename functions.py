from bot import BOT
from settings import GROUP_ID
from vkbottle.tools import DocMessagesUploader


async def getUser(user_id):
	try: 
		return (await BOT.api.users.get(user_ids=user_id))[0]
	except: 
		return None


async def getChat(chat_id):
	try:
		result = (await BOT.api.messages.get_conversations_by_id(
			peer_ids = int(chat_id) + 2e9, 
			group_id=GROUP_ID)).items
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
		your_id = (await BOT.api.users.get(user_ids=pattern.split("/")[-1]))[0]
		return your_id.id
	elif "[id" in pattern:
		your_id = pattern.split("|")[0]
		your_id = (await BOT.api.users.get(user_ids = your_id.replace("[id", "")))[0]
		return your_id



async def Photo_to_Ascii(event):
	import requests as req
	from PIL import Image
	from os import remove

	# Скачивание картинки по ссылке
	with open(f"photos/{event.attachments[0].photo.access_key}.png", "wb") as _out:
		file = req.get(event.attachments[0].photo.sizes[-1].url)
		_out.write(file.content)
	

	_asciiTable = ['.', ',', ':', '+', '*', '?', '%', 'S', '#', '@'][::-1]

	img = Image.open(f"photos/{event.attachments[0].photo.access_key}.png")

	WIDTH_OFFSET = 2.5
	MAX_WIDTH = 450
	MAX_HEIGHT = int(img.height / WIDTH_OFFSET * MAX_WIDTH / img.width)

	# Измнение масштаба картинки (Scale)
	if img.width > MAX_WIDTH or img.height > MAX_HEIGHT:
		img = img.resize((MAX_WIDTH, MAX_HEIGHT))

	x, y = img.size	

	# Перевод в Ascii изображение
	with open(f"photos/{event.attachments[0].photo.access_key}.txt", "w") as _out:
		for i in range(y):
			for j in range(x):
				pixels = img.getpixel((j, i))
				map_val = sum(pixels) / len(pixels)

				_out.write(_asciiTable[ int((map_val / 255) * 9) ])
				
			_out.write('\n')


	doc = await DocMessagesUploader(BOT.api).upload(
		title="Assci_photo.txt",
		file_source=f"photos/{event.attachments[0].photo.access_key}.txt",
		peer_id=event.peer_id
	)

	# Удаление временных файлов
	remove(f"photos/{event.attachments[0].photo.access_key}.png")
	remove(f"photos/{event.attachments[0].photo.access_key}.txt")

	return doc