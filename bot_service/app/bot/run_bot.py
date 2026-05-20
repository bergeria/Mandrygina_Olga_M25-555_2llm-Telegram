"""
Модуль запуска Telegram-бота.

Запускает polling aiogram
и основной цикл обработки сообщений.
"""

import asyncio

from app.bot.dispatcher import bot, dp


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
