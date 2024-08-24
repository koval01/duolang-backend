import sys
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from application.src.middleware import NodeMiddleware, ProcessTimeMiddleware

from fastapi_async_sqlalchemy import SQLAlchemyMiddleware

from aiogram_fastapi_server import SimpleRequestHandler, setup_application
from aiogram import Bot, Dispatcher
from aiogram.types import MenuButtonWebApp, WebAppInfo

from .config import settings
from .bot import bot, bot_routers
from .api.api import api_router


async def on_startup(bot: Bot, base_url: str):
    await bot.set_webhook(f"{settings.BACK_BASE_URL}/webhook")
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(text="Open Duolang", web_app=WebAppInfo(url=base_url))
    )


def create_app():
    """Application factory."""
    # logging configuration
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    # Configure dispatcher
    dispatcher = Dispatcher()
    dispatcher["base_url"] = settings.FRONT_BASE_URL
    dispatcher.startup.register(on_startup)

    # Register bot routers
    register_bot_router(dispatcher)

    # configure application
    app = FastAPI(
        title="Duolang API",
        docs_url="/docs",
    )

    # Register application routers
    register_app_routers(app)

    # Add app middleware
    app.add_middleware(
        SQLAlchemyMiddleware,
        db_url=settings.SQLALCHEMY_DATABASE_URI,
        engine_args={  # SQLAlchemy engine example setup
            "echo": True,
            "pool_pre_ping": True
        },
    )
    app.add_middleware(
        CORSMiddleware,  # type: ignore[no-untyped-call]
        allow_origins=[settings.FRONT_BASE_URL],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(NodeMiddleware)  # type: ignore[no-untyped-call]
    app.add_middleware(ProcessTimeMiddleware)  # type: ignore[no-untyped-call]

    # Add bot and dispatcher to application
    SimpleRequestHandler(
        dispatcher=dispatcher,
        bot=bot
    ).register(app, path="/webhook")
    setup_application(app, dispatcher, bot=bot)

    return app


def register_bot_router(dispatcher: Dispatcher):
    for router in bot_routers:
        dispatcher.include_router(router)


def register_app_routers(app: FastAPI):
    app.include_router(api_router)
