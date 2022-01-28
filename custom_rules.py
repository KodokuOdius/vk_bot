from vkbottle.dispatch.rules import ABCRule
from vkbottle.bot import Message


class Ban(ABCRule):

    async def check(self, event: Message) -> bool:
        if event.from_id == event.peer_id:
            await event.answer("Это личка")
        else:
            await event.answer("Это чат")
        return True
