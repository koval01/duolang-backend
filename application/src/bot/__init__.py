from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

from ..bot import start
from ..config import settings


# Bot initialization
bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))

bot_routers = [start.router]
