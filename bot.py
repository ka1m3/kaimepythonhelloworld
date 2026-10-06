import telebot
from telebot import types
import random

# Вставьте сюда токен от @BotFather в Telegram
BOT_TOKEN = 'YOUR_TOKEN_HERE'
bot = telebot.TeleBot(BOT_TOKEN)

# Хранилище активных игр: {chat_id: загаданное_число}
games = {}


@bot.message_handler(commands=['start'])
def start(message):
    """Приветствие и меню кнопок."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton('Привет'),
        types.KeyboardButton('Играть в угадай число'),
        types.KeyboardButton('Пока'),
    )
    bot.send_message(
        message.chat.id,
        f'Привет, {message.from_user.first_name}! Я простой бот.',
        reply_markup=markup,
    )


@bot.message_handler(commands=['help'])
def help_command(message):
    """Справка по командам."""
    bot.send_message(
        message.chat.id,
        'Доступные команды:\n'
        '/start — начать\n'
        '/help — помощь\n'
        '/game — игра «Угадай число»',
    )


@bot.message_handler(commands=['game'])
def game_start(message):
    """Запуск игры «Угадай число»."""
    number = random.randint(1, 200)
    games[message.chat.id] = number
    bot.send_message(message.chat.id, 'Я загадал число от 1 до 200. Попробуй угадать!')


@bot.message_handler(content_types=['text'])
def handle_text(message):
    """Обработчик текстовых сообщений и кнопок."""
    text = message.text.lower()

    # Если пользователь в игре — обрабатываем догадку
    if message.chat.id in games:
        try:
            guess = int(message.text)
        except ValueError:
            bot.send_message(message.chat.id, 'Пожалуйста, введи число.')
            return

        secret = games[message.chat.id]
        if guess == secret:
            bot.send_message(message.chat.id, f'Поздравляю! Ты угадал число {secret}!')
            del games[message.chat.id]
        elif guess < secret:
            bot.send_message(message.chat.id, 'Моё число больше.')
        else:
            bot.send_message(message.chat.id, 'Моё число меньше.')
        return

    # Обработка кнопок
    if text == 'привет':
        bot.send_message(message.chat.id, f'И тебе привет, {message.from_user.first_name}!')
    elif text == 'играть в угадай число':
        game_start(message)
    elif text == 'пока':
        bot.send_message(message.chat.id, 'Пока! Возвращайся ещё!')
    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю. Попробуй /help')


if __name__ == '__main__':
    print('Бот запущен...')
    bot.polling(none_stop=True)
