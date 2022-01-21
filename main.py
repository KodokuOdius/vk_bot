from bot import BOT
from vkbottle.bot import Message

####################################################

# database = simplemysql.Pymysql(host = settings.DB_HOST, 
# 			user = settings.DB_USER, 
# 			db = settings.DATABASE, 
# 			password = settings.DB_PASSWORD, 
# 			port = settings.DB_PORT)


@BOT.on.message()
async def repeat(event: Message):
	await event.answer(event.text)







BOT.run_forever()