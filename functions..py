from bot import BOT
from settings import GROUP_ID


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
