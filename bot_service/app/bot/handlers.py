"""
Telegram handlers Bot Service.

Реализует:
- команду /start
- команду /token
- проверку JWT
- отправку задач в очередь Celery
"""

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from app.core.jwt import decode_and_validate
from app.infra.redis import get_redis
from app.tasks.llm_tasks import llm_request


router = Router()


#def token_key(user_id: int) -> str:
#    return f"telegram:user:{user_id}:jwt"

def token_key(user_id: int) -> str:
    return f"token:{user_id}"

@router.message(Command("start"))
async def start(message: Message) -> None:
    await message.answer(
        "Привет! Сначала отправь JWT-токен командой:\n\n"
        "/token <твой_jwt>\n\n"
        "Токен нужно получить в Auth Service через /auth/login."
    )


@router.message(Command("token"))
async def save_token(message: Message, command: CommandObject) -> None:
    token = command.args

    if not token:
        await message.answer("Использование: /token <твой_jwt>")
        return

    try:
        decode_and_validate(token)
    except ValueError:
        await message.answer("Токен неверный или истёк. Получи новый в Auth Service.")
        return

    redis = get_redis()
    await redis.set(token_key(message.from_user.id), token)

    await message.answer("Токен принят и сохранён ✅")


@router.message()
async def handle_text(message: Message) -> None:
    redis = get_redis()
    token = await redis.get(token_key(message.from_user.id))

    if not token:
        await message.answer(
            "Доступ запрещён. Сначала отправь JWT:\n\n/token <твой_jwt>"
        )
        return

    try:
        decode_and_validate(token)
    except ValueError:
        await redis.delete(token_key(message.from_user.id))
        await message.answer(
            "Токен неверный или истёк. Получи новый в Auth Service и отправь /token заново."
        )
        return

    task = llm_request.delay(
        message.chat.id,
        message.text,
    )
    await message.answer(
        "Запрос принят в очередь ✅\n"
        f"Task ID: {task.id}\n\n"
        "Ответ придёт после обработки."
    )
    