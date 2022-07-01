from asyncio import run, gather, Queue
from telebot.async_telebot import AsyncTeleBot
from os import environ as env, path
from random import choice


running = True
bot = AsyncTeleBot(env['TELEGRAM_BOT_TOKEN'], parse_mode='html')
queue = Queue(maxsize=512)
encouragements = []
enc_file_path = path.join(path.dirname(__file__), 'encouragements.txt')
with open(enc_file_path, 'r') as enc_file:
    for line in enc_file:
        encouragements.append(line)


async def flush_queue():
    file = open('botlog.txt', 'a')
    while (running):
        file.write(await queue.get() + '\n')
        file.flush()
    file.close()


@bot.message_handler(commands=['start'])
async def start(message):
    await bot.send_message(message.from_user.id, 'Напишите сюда все ваши пожелания по направлениям курсачей\n'
                                                 'Я буду молчать и слушать очень внимательно')


@bot.message_handler(func=lambda _: True)
async def any_message(message):
    await gather(queue.put(message.from_user.username + ': ' + message.text),
                 bot.send_message(message.from_user.id, choice(encouragements)))


async def main():
    await gather(flush_queue(),
                 bot.infinity_polling())

if __name__ == '__main__':
    run(main())
