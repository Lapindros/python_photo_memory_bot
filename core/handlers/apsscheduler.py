import logging

from aiogram import Bot
from aiogram.types import FSInputFile

import random
import os
import yadisk

from utils.caption_dict import dict_caption
from utils.get_quotes_today import get_quotes_today
from utils.reset_counter import reset_counter

async def send_message_time(bot: Bot):
    await bot.send_message(<your_telegram_id>, f'Это будет сообщение отправлено через несколько секунд после старта бота')


async def send_message_cron(bot: Bot):
    await bot.send_message(<your_telegram_id>, f'Это сообщение будет отправляться ежедневно в указанное время')


async def send_photo_interval(bot: Bot):
    client = yadisk.Client(token=<your_yandex_token>)

    all_photos = []

    file = open('photo_counter.txt', 'r')
    counter = file.readlines()
    int_counter = int(counter[0])

    if int_counter == len(all_photos) - 1:
        await reset_counter()

    # Проверяет, валиден ли токен
    # print(client.check_token())

    if client.check_token():
        for item in client.listdir('/old_friends_photos/'):
            all_photos.append(item['name'])
    else:
        logging.error("Неверный токен!")

    # Генератор случайных фраз для фото
    number_caption = random.randrange(1, len(dict_caption), 1)

    client.download(f'/old_friends_photos/{all_photos[int_counter]}', 'test.jpg')

    await bot.send_photo(
        <your_telegram_chat_id>,
        photo=FSInputFile('test.jpg'),
        caption=f"{dict_caption[number_caption]}"
    )

    logging.info(f"Фото {all_photos[int_counter]} отправлено")

    if int_counter == len(all_photos) - 1:
        await reset_counter()
    else:
        int_counter += 1
        text_file = open("photo_counter.txt", "w")
        text_file.write(str(int_counter))
        text_file.close()

    try:
        if os.path.exists('test.jpg'):
            os.remove('test.jpg')
    except Exception as e:
        logging.info(f'Ошибка при удалении файла {"test.jpg"}. {e}')


async def send_quotes_interval(bot: Bot):
    usd = get_quotes_today('USD')
    eur = get_quotes_today('EUR')
    cny = get_quotes_today('CNY')

    await bot.send_message(
        <your_telegram_chat_id>,
        text=f"\U0001F4B0 {usd}, {eur}, {cny} \U0001F4B0"
    )
