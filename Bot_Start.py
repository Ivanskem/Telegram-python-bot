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
def ban_user(message):
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

@bot.message_handler(commands=['unban'])
def unban_user(message):
    chat_id = message.chat.id
    try:
        user_id = message.reply_to_message.from_user.id
    except AttributeError:
        bot.reply_to(message, 'Команду нужно вводить только в ответ на сообщения пользователя с которым нужно взаимодействовать!')
        return
    if user_id != bot.get_me().id:
        if message.from_user.id in moderators:

            try:
                reason = ' '.join(message.text.split()[1:])
            except (IndexError, ValueError):
                bot.reply_to(message, "Неправильный формат команды. Используйте /unban [причина]")
                return

            try:
                bot.unban_chat_member(chat_id, user_id,)
                bot.reply_to(f'Участник {message.reply_to_message.from_user.first_name} был разблокирован. Причина: {reason}')
            except Exception as e:
                if 'User is not banned' in str(e):
                    bot.reply_to(message, 'Пользватель не заблокирован')
                elif "A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: can't ban members in private chats" in str(e):
                    bot.reply_to(message, 'Невозможно заблокировать пользователя в приватном чате.')
                elif "A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: method is available for supergroup and channel chats only" in str(e):
                    bot.reply_to(message, 'Данный метод может использоваться только каналах и супергруппах!')
                else:
                    bot.reply_to(message, f'Произошла ошибка. Ошибка: {e}')
        else:
            bot.reply_to('У вас нет необходимых прав!')
    else:
        bot.reply_to('Невозможно разблокировать бота')

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

@bot.message_handler(commands=['unmute'])
def unmute_user(message):
    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id

    if user_id != bot.get_me().id:
        if message.from_user.id in moderators:
            try:
                reason = ' '.join(message.text.split()[1:])
            except (IndexError, ValueError):
                bot.reply_to(message, "Неправильный формат команды. Используйте /mute [количество минут]m [причина]")
                return

            bot.restrict_chat_member(chat_id, user_id, can_send_messages=True)
            bot.reply_to(message, f"Участник {message.reply_to_message.from_user.first_name} разглушён. Причина: {reason}")
        else:
            bot.reply_to(message, "У вас нет прав модератора для использования этой команды.")
    else:
        bot.reply_to(message, "Нельзя отключить бота.")


@bot.message_handler(commands=['kick'])
def kick_user(message):
    chat_id = message.chat.id
    try:
        user_id = message.reply_to_message.from_user.id
    except AttributeError:
        bot.reply_to(message, 'Команду нужно вводить только в ответ на сообщения пользователя с которым нужно взаимодействовать!')
        return

    if user_id != bot.get_me().id:
        if message.from_user.id in moderators:
            try:
                reason = ' '.join(message.text.split()[1:])
            except (IndexError, ValueError):
                bot.reply_to(message, "Неправильный формат команды. Используйте /kick [причина]")
                return

            try:
                bot.kick_chat_member(chat_id, user_id)
                bot.reply_to(message, f'Участник {message.reply_to_message.from_user.first_name} был исключён. Причина: {reason}')
            except Exception as e:
                bot.reply_to(message, f'Ошибка при удалении участника. Ошибка: {e}')
        else:
            bot.reply_to(message, "У вас нет прав модератора для использования этой команды.")
    else:
        bot.reply_to(message, "Невозможно удалить бота.")
bot.polling()
