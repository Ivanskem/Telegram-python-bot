import telebot
import time
import requests
import datetime
import os

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
moderators = 123456789#Добавьте айди модераторов
Forbidden_words = ['даун', 'пидор', 'шлюха', 'гей', 'еблан', 'пидорас', 'хуйня', 'хуйни', 'шлюхи', 'пидрила', 'пидорасина', 'блять', 'блядь', 'блядина', 'ебланище', 'сука', 'негр', 'уёбище', 'шмара', 'хуесос', 'пиздализ', 'пизда', 'жопа', 'член', 'ссанина', 'лох', 'Пидор', 'ебанат', 'Ебанат']

print(f'Telegram bot with token {bot_token} started')

# @bot.message_handler(func=lambda message: True)
# def Check_message(message):
#     text = message.text.lower()
#     chat_id = message.chat.id
#     for word in Forbidden_words:
#         if word in text:
#             try:
#                 bot.reply_to(message, f"{message.from_user.first_name}, пожалуйста, избегайте использования запрещенных слов.")
#                 print(text)
#                 bot.delete_message(message.chat.id, message.message_id)
#             except Exception as e:
#                 if "A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: message to be replied not found" in str(e):
#                     bot.send_message(chat_id, "Сообщение не найдено, попробуйте снова.")
@bot.message_handler(commands=['chatinfo'])
def chat_info(message):
    if message.from_user.id in moderators:
        chat_id = message.chat.id
        chat_name = message.chat.title
        user_id = message.from_user.id
        user_username = message.from_user.username
        member_count = bot.get_chat_member_count(chat_id)
        try:
            admin_count = len(bot.get_chat_administrators(chat_id))
        except Exception as e:
            if "A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: there are no administrators in the private chat" in str(e):
                admin_count = 0
        if message.chat.type in ['group', 'supergroup', 'channel']:
            try:
                bot.send_message(chat_id, f'Наименование: {chat_name} \nId чата: {chat_id} \nТип: {message.chat.type} \nКоличество участников: {member_count} \nКоличество администраторов: {admin_count} \nВызвал: {user_username} ({user_id})')
            except Exception as e:
                if "A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: TOPIC_CLOSED" in str(e):
                    bot.reply_to(message, "Недостаточно прав для сбора информации!")
        elif message.chat.type == 'private':
            try:
                chat_name = f"@{message.from_user.username}"
                bot.send_message(chat_id, f'Наименование: {chat_name} \nId чата: {chat_id} \nТип: {message.chat.type} \nКоличество участников: {member_count} \nКоличество администраторов: {admin_count} \nВызвал: {user_username} ({user_id})')
            except Exception as e:
                if "A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: TOPIC_CLOSED" in str(e):
                    bot.reply_to(message, "Недостаточно прав для сбора информации!")
        else:
            bot.send_message(chat_id, f"Can't get chat type.")
    else:
        bot.reply_to(message, 'У вас недостаточно прав для использования этой команды.')

@bot.message_handler(commands=['info'])
def info(message):
    if message.from_user.id in moderators:
        if message.reply_to_message is None:
            bot.reply_to(message, "Пожалуйста, ответьте на сообщение пользователя, чтобы получить о нем информацию.")
            return

        try:
            user = message.reply_to_message.from_user
            user_id = user.id
            user_nickname = user.username

            chat_id = message.chat.id
            chat_member = bot.get_chat_member(chat_id, user_id)

            admin = 'да' if chat_member.status in ['administrator', 'creator'] else 'нет'

            bot.reply_to(message, f'Информация о {user_nickname}:\n\nID: {user_id}\nАдминистратор: {admin}')

        except Exception as e:
            print(f"Ошибка: {e}")
            bot.reply_to(message, "Произошла ошибка при получении информации о пользователе.")
    else:
        bot.reply_to(message, 'У вас не достаточно прав для использования.')
@bot.message_handler(commands=['weather'])
def weather(message):
    try:
        with open('weather_api.txt', 'r') as f:
            global API_Weather
            API_Weather = f.read().strip()
    except FileNotFoundError:
        API_Weather = input("Введите ваш API ключ для метеорологического сервиса: ")
        with open('weather_api.txt', 'w') as f:
            f.write(API_Weather)

    chat_id = message.chat.id
    city = message.text.split()[1]
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_Weather}&units=metric'
    response = requests.get(url)
    weather_data = response.json()
    time = datetime.datetime.now().replace(microsecond=0)
    try:
        filtered_data = {
            "Temp_min": weather_data['main']['temp_min'],
            "Temp_max": weather_data['main']['temp_max'],
            "Temp": weather_data['main']['temp'],
            "Feels_like": weather_data['main']['feels_like'],
            "Country": weather_data['sys']['country'],
            "Wind_speed": weather_data['wind']['speed'],
            "Humidity": weather_data['main']['humidity'],
            "City_id": weather_data['id']
        }
    except KeyError:
        bot.reply_to(message, '*Произошла ошибка!*')
    if response.status_code == 200:
        try:
            url_png = f"https://tile.openweathermap.org/map/temp_new/0/0/0.png?appid={API_Weather}"
            message_text = f"**Погода в {city}**\n\nГород: {city}, Страна: {filtered_data['Country']}\nСредняя температура: {filtered_data['Temp']}°C \nМинимальная температура: {filtered_data['Temp_min']}°C \nМаксимальная температура: {filtered_data['Temp_max']}°C \nТемпература по ощущениям: {filtered_data['Feels_like']}°C \nСкорость ветра: {filtered_data['Wind_speed']}М/С \nВлажность: {filtered_data['Humidity']}% \nЗапрос выполнен: {time} \nЗапросил: {message.from_user.username} ({message.from_user.id}) \nИсточник: https://openweathermap.org/city/{filtered_data['City_id']}"
            bot.send_photo(chat_id, photo=url_png)
            bot.reply_to(message, message_text)
        except requests.exceptions.HTTPError:
            bot.reply_to(message, '*Ошибка получения данных*')

        except requests.exceptions.RequestException:
            bot.reply_to(message, '*Ошибка получения данных*')

@bot.message_handler(commands=['ban'])
def ban_user(message):
    chat_id = message.chat.id
    try:
        user_id = message.reply_to_message.from_user.id
    except AttributeError:
        bot.reply_to(message,'Команду нужно вводить только в ответ на сообщения пользователя с которым нужно взаимодействовать!')
        return

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
                try:
                    bot.kick_chat_member(chat_id, user_id, until_date=int(time.time()) + int(ban_time) * 60)
                    bot.reply_to(message, f"Участник {message.reply_to_message.from_user.first_name} заблокирован на {ban_time} минут. Причина: {reason}")
                except Exception as e:
                    if "A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: can't ban members in private chats" in str(e):
                        bot.reply_to(message, 'Невозможно заблокировать пользователя в приватном чате.')
                    elif "A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: method is available for supergroup and channel chats only" in str(e):
                        bot.reply_to(message, 'Данный метод может использоваться только каналах и супергруппах!')
                    elif f"invalid literal for int() with base 10: '{ban_time}'" in str(e):
                        bot.reply_to(message, 'Не правильное использование команды. Используйте: /mute [время] [причина]')
                    elif "A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: not enough rights to restrict/unrestrict chat member" in str(e):
                        bot.reply_to(message, 'Ошибка. Для корректной работы бота выдайте ему права администратора.')
                    else:
                        bot.reply_to(message, f'Произошла ошибка. Ошибка: {e}')
            else:
                try:
                    bot.ban_chat_member(chat_id, user_id)
                    bot.reply_to(message, f'Участник {message.reply_to_message.from_user.first_name} заблокирован навсегда. Причина: {reason}')
                except Exception as e:
                    if "A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: can't ban members in private chats" in str(
                            e):
                        bot.reply_to(message, 'Невозможно заблокировать пользователя в приватном чате.')
                    elif "A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: method is available for supergroup and channel chats only" in str(
                            e):
                        bot.reply_to(message, 'Данный метод может использоваться только каналах и супергруппах!')
                    elif f"invalid literal for int() with base 10: '{ban_time}'" in str(e):
                        bot.reply_to(message, 'Не правильное использование команды. Используйте: /ban [время] [причина]')
                    elif "A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: not enough rights to restrict/unrestrict chat member" in str(e):
                        bot.reply_to(message, 'Ошибка. Для корректной работы бота выдайте ему права администратора.')
                    else:
                        bot.reply_to(message, f'Произошла ошибка. Ошибка: {e}')
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
                bot.unban_chat_member(chat_id, user_id)
                bot.reply_to(message, f'Участник {message.reply_to_message.from_user.first_name} был разблокирован. Причина: {reason}')
            except Exception as e:
                if 'User is not banned' in str(e):
                    bot.reply_to(message, 'Пользватель не заблокирован')
                elif "A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: method is available for supergroup and channel chats only" in str(e):
                    bot.reply_to(message, 'Данный метод может использоваться только каналах и супергруппах!')
                elif "A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: not enough rights to restrict/unrestrict chat member" in str(
                        e):
                    bot.reply_to(message, 'Ошибка. Для корректной работы бота выдайте ему права администратора.')
                else:
                    bot.reply_to(message, f'Произошла ошибка. Ошибка: {e}')
        else:
            bot.reply_to('У вас нет необходимых прав!')
    else:
        bot.reply_to('Невозможно разблокировать бота')

@bot.message_handler(commands=['mute'])
def mute_user(message):
    chat_id = message.chat.id
    try:
        user_id = message.reply_to_message.from_user.id
    except AttributeError:
        bot.reply_to(message, 'Команду нужно вводить только в ответ на сообщения пользователя с которым нужно взаимодействовать!')
        return
    if user_id != bot.get_me().id:
        if message.from_user.id in moderators:
            try:
                mute_time = message.text.split()[1]
                reason = ' '.join(message.text.split()[2:])
            except (IndexError, ValueError):
                bot.reply_to(message, "Неправильный формат команды. Используйте /mute [количество минут]m [причина]")
                return

            if mute_time != 'Навсегда':
                try:
                    mute_time = mute_time.replace('m', '')
                    bot.restrict_chat_member(chat_id, user_id, can_send_messages=False, until_date=int(time.time()) + int(mute_time) * 60)
                    bot.reply_to(message, f"Участник {message.reply_to_message.from_user.first_name} заглушён на {mute_time} минут. Причина: {reason}")
                except Exception as e:
                    if "A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: can't ban members in private chats" in str(e):
                        bot.reply_to(message, 'Невозможно заглушить пользователя в приватном чате.')
                    elif "A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: method is available only for supergroups" in str(e):
                        bot.reply_to(message, 'Данный метод может использоваться только в супергруппах!')
                    elif f"invalid literal for int() with base 10: '{mute_time}'" in str(e):
                        bot.reply_to(message, 'Не правильное использование команды. Используйте: /mute [время] [причина]')
                    elif "A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: not enough rights to restrict/unrestrict chat member" in str(e):
                        bot.reply_to(message, 'Ошибка. Для корректной работы бота выдайте ему права администратора.')
                    else:
                        bot.reply_to(message, f'Произошла ошибка. Ошибка: {e}')
            else:
                try:
                    bot.restrict_chat_member(chat_id, user_id, can_send_messages=False, until_date=int(time.time()) + 2147483647)
                    bot.reply_to(message, f"Участник {message.reply_to_message.from_user.first_name} заглушён навсегда. Причина: {reason}")
                except Exception as e:
                    if "A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: can't ban members in private chats" in str(
                            e):
                        bot.reply_to(message, 'Невозможно заглушить пользователя в приватном чате.')
                    elif "A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: method is available only for supergroups" in str(
                            e):
                        bot.reply_to(message, 'Данный метод может использоваться только в супергруппах!')
                    elif "A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: not enough rights to restrict/unrestrict chat member" in str(e):
                        bot.reply_to(message, 'Ошибка. Для корректной работы бота выдайте ему права администратора.')
                    else:
                        bot.reply_to(message, f'Произошла ошибка. Ошибка: {e}')
        else:
            bot.reply_to(message, "У вас нет прав модератора для использования этой команды.")
    else:
        bot.reply_to(message, "Нельзя отключить бота.")

@bot.message_handler(commands=['unmute'])
def unmute_user(message):
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
                bot.reply_to(message, "Неправильный формат команды. Используйте /unmute [причина]")
                return
            try:
                bot.restrict_chat_member(chat_id, user_id, can_send_messages=True)
                bot.reply_to(message, f"Участник {message.reply_to_message.from_user.first_name} разглушён. Причина: {reason}")
            except Exception as e:
                if 'User is not banned' in str(e):
                    bot.reply_to(message, 'Пользватель не заглушён')
                elif "A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: method is available for supergroup and channel chats only" in str(e):
                    bot.reply_to(message, 'Данный метод может использоваться только каналах и супергруппах!')
                elif "A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: not enough rights to restrict/unrestrict chat member" in str(
                        e):
                    bot.reply_to(message, 'Ошибка. Для корректной работы бота выдайте ему права администратора.')
                else:
                    bot.reply_to(message, f'Произошла ошибка. Ошибка: {e}')
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
                if "A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: can't ban members in private chats" in str(
                        e):
                    bot.reply_to(message, 'Невозможно исключить пользователя в приватном чате.')
                elif "A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: method is available for supergroup and channel chats only" in str(
                        e):
                    bot.reply_to(message, 'Данный метод может использоваться только каналах и супергруппах!')
                elif "A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: not enough rights to restrict/unrestrict chat member" in str(
                        e):
                    bot.reply_to(message, 'Ошибка. Для корректной работы бота выдайте ему права администратора.')
                else:
                    bot.reply_to(message, f'Произошла ошибка. Ошибка: {e}')
        else:
            bot.reply_to(message, "У вас нет прав модератора для использования этой команды.")
    else:
        bot.reply_to(message, "Невозможно исключить бота.")
bot.polling()
