from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    MenuButtonWebApp,
    Message,
    WebAppInfo,
)

router = Router()


@router.message(Command("start"))
async def command_start(message: Message, bot: Bot, base_url: str):
    await bot.set_chat_menu_button(
        chat_id=message.chat.id,
        menu_button=MenuButtonWebApp(text="Open Duolang", web_app=WebAppInfo(url=base_url)),
    )
    await message.answer(
        "Hi!",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Open Duolang", web_app=WebAppInfo(url=base_url)
                    )
                ]
            ]
        ),
    )
