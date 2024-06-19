import telebot
import time

try:
    with open('token_telegram.txt', 'r') as f:
        bot_token = f.read().strip()
        bot = telebot.TeleBot(bot_token)
except FileNotFoundError:
    bot_token = input("Введите ваш токен Telegram ")
    bot = telebot.TeleBot(bot_token)
    with open('token_telegram.txt', 'w') as f:
        f.write(bot_token)
        bot = telebot.TeleBot(bot_token)
moderators = [5025429154]

@bot.message_handler(commands=['ban'])
def kick_user(message):
    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id

    if user_id != bot.get_me().id:
        if message.from_user.id in moderators:
            try:
                ban_time = message.text.split()[1]
                reason = ' '.join(message.text.split()[2:])
            except (IndexError, ValueError):
                bot.reply_to(message, "Неправильный формат команды. Используйте /ban [количество минут]m [причина]")
                return

            if ban_time != 'Навсегда':
                ban_time = ban_time.replace('m', '')
                bot.kick_chat_member(chat_id, user_id, until_date=int(time.time()) + int(ban_time) * 60)
                bot.reply_to(message, f"Участник {message.reply_to_message.from_user.first_name} заблокирован на {ban_time} минут. Причина: {reason}")
            else:
                bot.kick_chat_member(chat_id, user_id, until_date=int(time.time()) + 2147483647)
                bot.reply_to(message, f'Участник {message.reply_to_message.from_user.first_name} заблокирован навсегда. Причина: {reason}')
        else:
            bot.reply_to(message, "У вас нет прав модератора для использования этой команды.")
    else:
        bot.reply_to(message, "Вы попытались заблокировать бота!")

@bot.message_handler(commands=['mute'])
def mute_user(message):
    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id

    if user_id != bot.get_me().id:
        if message.from_user.id in moderators:
            try:
                mute_time = message.text.split()[1]
                reason = ' '.join(message.text.split()[2:]) 
            except (IndexError, ValueError):
                bot.reply_to(message, "Неправильный формат команды. Используйте /mute [количество минут]m [причина]")
                return

            if mute_time != 'Навсегда':
                mute_time = mute_time.replace('m', '')
                bot.restrict_chat_member(chat_id, user_id, can_send_messages=False, until_date=int(time.time()) + int(mute_time) * 60) 
                bot.reply_to(message, f"Участник {message.reply_to_message.from_user.first_name} заглушён на {mute_time} минут. Причина: {reason}")
            else:
                bot.restrict_chat_member(chat_id, user_id, can_send_messages=False, until_date=int(time.time()) + 2147483647)
                bot.reply_to(message, f"Участник {message.reply_to_message.from_user.first_name} заглушён навсегда. Причина: {reason}")
        else:
            bot.reply_to(message, "У вас нет прав модератора для использования этой команды.")
    else:
        bot.reply_to(message, "Нельзя отключить бота.")

bot.polling()