import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from httpx import AsyncClient, Limits

from config import car_brands, greeting_msg
from handler import Handler
from requester import ModelRequester
from settings import Settings

bot = Bot(token=Settings.TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(
    level="INFO",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    force=True,
)

httpx_client = AsyncClient(
    headers={"User-Agent": "tg-bot"},
    timeout=Settings.HTTP_TIMEOUT,
    limits=Limits(
        max_connections=Settings.MAX_CONNECTIONS,
        max_keepalive_connections=Settings.MAX_KEEPALIVE_CONNECTIONS,
        keepalive_expiry=Settings.KEEPALIVE_EXPIRY,
    ),
)
requester = ModelRequester(client=httpx_client, base_url=Settings.MODEL_URL)
handler = Handler(path_to_swear_words=Settings.PATH_TO_SWEAR_WORDS, car_brands=car_brands, requester=requester)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer(greeting_msg)


@dp.message_handler(content_types=['text'])
async def echo_message(message: types.Message):
    msg = await handler.handle(message.text)
    await message.answer(msg)


if __name__ == '__main__':
    from aiogram import executor
    loop = asyncio.get_event_loop()
    try:
        loop.create_task(executor.start_polling(dp, skip_updates=True))
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.stop()
        loop.close()
