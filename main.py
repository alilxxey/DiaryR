import telebot
import time
from multiprocessing.context import Process
import schedule
import datetime
import parcer
import json
import random

bot = telebot.TeleBot('1868908140:AAFU1Xeh3EFz5BKTvdDy4a5rHUwMrZxcoY0')

Efremov = ['CAACAgIAAxkBAAIF1WI7k-69I8AqNMUEAcCI2YUkkwXnAAIUKwAC4KOCB9LIZOk_oYwwIwQ',
           'CAACAgIAAxkBAAIF1mI7k-8k3LJxXlM9D_Fa6NfjdteLAAIVKwAC4KOCB5zLy1d58Hm7IwQ',
           'CAACAgIAAxkBAAIF12I7k_DOwtp3E6XKFtVKedwyti1aAAIWKwAC4KOCB6VK7oULYB7VIwQ',
           'CAACAgIAAxkBAAIF2GI7k_HaX_lKzwrI7iUrzEZ68Ty-AAIXKwAC4KOCB3A4tS5ZHSazIwQ',
           'CAACAgIAAxkBAAIF2WI7k_Ljw1NIqfhAYqZmMQSlwjgjAAIYKwAC4KOCB230ikNVTe9EIwQ',
           'CAACAgIAAxkBAAIF2mI7k_MnGi0ysLMQpi152STvDQuQAAIZKwAC4KOCB8PWNM1xrjJSIwQ',
           'CAACAgIAAxkBAAIF22I7k_WrgfY7Dv7Sf6vgkSHr8vsDAAIcKwAC4KOCB4x_OaEtX2qqIwQ',
           'CAACAgIAAxkBAAIF3GI7k_edCVCXxhf_Z7je-RhIsGXdAAIfKwAC4KOCBzOT8iv10acNIwQ',
           'CAACAgIAAxkBAAIF3WI7lEKgfYDZ_91Y5XN_AQ4v0qcfAAK-awAC4KOCB43ZT50M7DHqIwQ',
           'CAACAgIAAxkBAAIF3mI7lEOz-hh2C2zqCobII5tJ7VzuAAK_awAC4KOCB-pj81RwQk96IwQ',
           'CAACAgIAAxkBAAIF32I7lETqTo_WXFPhUPELmoBOTCCtAALAawAC4KOCBxJDRKez-cFAIwQ',
           'CAACAgIAAxkBAAIF4GI7lEVcYJ9-WiEr_d-v0uq8fKKuAALBawAC4KOCB36m8ggebDPBIwQ',
           'CAACAgIAAxkBAAIF4WI7lEZXcYKBOsCdDImgrpriORFgAALCawAC4KOCBwYcn2HfpRXsIwQ',
           'CAACAgIAAxkBAAIF4mI7lEZfELnrjwIoVixoWX1Iv9TsAALDawAC4KOCB698xgjx609XIwQ',
           'CAACAgIAAxkBAAIF42I7lEuh_pzt-ejoCkJCPdxjREsZAALSawAC4KOCB-Oc6nSwIUuTIwQ',
           'CAACAgIAAxkBAAIF5GI7lEvn4K8DZSQnYQxsN0XDH4TPAALRawAC4KOCBwMvb9X2NYZuIwQ',
           'CAACAgIAAxkBAAIF5WI7lEyPJ7qF3dOQPFAmfODQPxtMAALOawAC4KOCB9KPgR9jGdlPIwQ',
           'CAACAgIAAxkBAAIF5mI7lE105g14iPLEjZlkEKFg670iAALQawAC4KOCBxLIUnIdTiKwIwQ',
           'CAACAgIAAxkBAAIF52I7lE1_a3_ExNLvV5FglKRSLEq4AALLawAC4KOCB6vsjdaatEAJIwQ']


# noinspection PyMethodParameters
class ScheduleMessage:
    @staticmethod
    def try_send_schedule():
        while True:
            schedule.run_pending()
            time.sleep(1)

    @staticmethod
    def start_process():
        p1 = Process(target=ScheduleMessage.try_send_schedule,
                     args=())
        p1.start()


class OurTime:
    def __init__(self, t=3):
        nowtime = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=t)))
        self.weekday = datetime.datetime.today().isoweekday()
        self.minute = nowtime.minute
        self.hour = nowtime.hour


def check_person(_id):
    _id = str(_id)
    with open("database.json") as f:
        database = json.load(f)
    a = [False, False, False]
    try:
        if database[_id]["1"]:
            a[0] = True
    except KeyError:
        pass
    try:
        if database[_id]['timez']:
            a[1] = True
    except KeyError:
        pass
    try:
        if database[_id]["ditme"]:
            a[2] = True
    except KeyError:
        pass
    return a


def check():
    try:
        with open("database.json") as f:
            database = json.load(f)
        for _id in database.keys():
            try:
                nowtime = OurTime(int(database[_id]['timez']))
                dt = database[_id]['dtime']
                nowtime.minute += dt

                if nowtime.minute < 0:
                    nowtime.hour -= 1
                    nowtime.minute += 60

                if nowtime.minute >= 60:
                    nowtime.hour += 1
                    nowtime.minute -= 60
                time_form = f'{nowtime.hour if len(str(nowtime.hour)) == 2 else str(0) + str(nowtime.hour)}:' \
                            f'{nowtime.minute if len(str(nowtime.minute)) == 2 else str(0) + str(nowtime.minute)}'

                send_not(_id=_id,
                         lesson=database[_id][str(nowtime.weekday)][time_form],
                         dimet=dt)

            except KeyError as e:
                print(e)

    except Exception as e:
        print(e)


def start_sch():
    try:
        for hour in range(0, 24):
            for minute in range(0, 60, 5):
                if len(str(hour)) == 2:
                    h = hour

                else:
                    h = str(0) + str(hour)

                if len(str(minute)) == 2:
                    m = minute

                else:
                    m = str(0) + str(minute)
                schedule.every().day.at(f'{h}:{m}').do(check)

    except Exception as e:
        print(e)


start_sch()


@bot.message_handler(commands=['changeDtime'])
def changedtime(message):
    try:
        bot.send_message(message.chat.id,
                         f"За сколько минут до урока скидывать "
                         f"уведомление(число кратное 5)?\nНапишите команду /dtime <b>'x'</b>",
                         parse_mode="html")
    except Exception as e:
        print(e)


@bot.message_handler(commands=['changeTZ'])
def changetz(message):
    try:
        bot.send_message(message.chat.id, 'Напиши свой часовой пояс в формате ± <b>x</b>\n(Москва: +3)')

    except Exception as e:
        print(e)


@bot.message_handler(commands=['diary'])
def diary(message):
    try:
        _id = message.chat.id
        with open('database.json') as f:
            database = json.load(f)
        sat = " ".join(database[str(_id)]["1"]) if database[str(_id)]["6"] else "Вы не учитесь в субботу"
        bot.send_message(message.chat.id, f'Ваше расписание:\n'
                                          f'Понедельник: \n{" ".join(database[str(_id)]["1"])}\n\n'
                                          f'Вторник: \n{" ".join(database[str(_id)]["2"])}\n\n'
                                          f'Среда: \n{" ".join(database[str(_id)]["3"])}\n\n'
                                          f'Четверг: \n{" ".join(database[str(_id)]["4"])}\n\n'
                                          f'Пятница: \n{" ".join(database[str(_id)]["5"])}\n\n'
                                          f'Суббота: \n{sat}')

        bot.send_message(message.chat.id, f'Расписание устарело или загрузилось неправильно?\n'
                                          f'Просто отправь новый файл с расписанием')

    except Exception as e:
        print(e)


@bot.message_handler(commands=['ready'])
def ready(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = telebot.types.InlineKeyboardButton("Расписание на сегодня")
    b2 = telebot.types.InlineKeyboardButton("Расписание на завтра")
    b3 = telebot.types.InlineKeyboardButton("Следующий урок")
    markup.add(b1, b2, b3)
    bot.send_message(message.chat.id, random.choice(Efremov), reply_markup=markup)


@bot.message_handler(commands=['settings'])
def settings(message):
    try:
        _id = message.chat.id
        with open('database.json') as f:
            database = json.load(f)

        bot.send_message(message.chat.id, f'Время, за которое приходит уведомление: {database[str(_id)]["dtime"]}\n'
                                          f'Ваш часовой пояс: UTC{database[str(_id)]["timez"]}\n'
                                          f'Сообщить о неисправности: @alilxxey @bez_griga',
                         reply_markup=telebot.types.ReplyKeyboardRemove())

        bot.send_message(message.chat.id, f'Если один из параметров установлен неправильно '
                                          f'или ты хочешь его изменить:\n'
                                          f'/changeDtime - изменить время уведомления до урока\n'
                                          f'/changeTZ - изменить часовой пояс\n'
                                          f'/ready - все корректно')

    except Exception as e:
        print(e)


@bot.message_handler(commands=['start'])
def start(message):
    gif = \
        'vgifbot.online/gif/BAACAgIAAxkBAAFHeqJiOjZILiGb0tPsqgoVy9cRv3dQvQACvxgAAnJb0UlZOyxguHTiIiME_1647982227.79.gif'
    try:
        bot.send_message(message.chat.id,
                         f'Привет, <b>{message.from_user.first_name}</b>',
                         parse_mode='html')

        if message.chat.id == 512770440:
            bot.send_sticker(message.from_user.id, random.choice(Efremov))

        bot.send_animation(message.chat.id, gif)
        bot.send_message(message.chat.id, "Скинь боту Execel файл с сайта эжд https://school.mos.ru/")
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        b1 = telebot.types.InlineKeyboardButton('Часовой пояc')
        b2 = telebot.types.InlineKeyboardButton('Я из Москвы')
        markup.add(b1, b2)
        bot.send_message(message.chat.id,
                         'Если ты не из Москвы\nНажмите на кнопку "Часовой пояс"',
                         reply_markup=markup)

    except Exception as e:
        print(e)


@bot.message_handler(commands=['dtime'])
def setdtime(message):
    try:
        a = message.text.replace('/dtime ', '')
        if not a:
            bot.send_message(message.chat.id, f'Ты не отправил число:( \nПосле команды /dtime укажи число\n'
                                              f'Пример: (/dtime 5)')
            return

        if message.chat.id == 512770440:
            bot.send_sticker(message.from_user.id, random.choice(Efremov))

        try:
            dtime = int(a) - int(a) % 5

            if dtime <= 0 and int(a) != 0:
                dtime = 5

            parcer.add_dtime(_id=message.chat.id,
                             dtime=dtime)
            b = check_person(str(message.chat.id))

            if not b[0]:
                bot.send_message(message.chat.id, "Остался файл")

            else:
                markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
                b1 = telebot.types.InlineKeyboardButton("Расписание на сегодня")
                b2 = telebot.types.InlineKeyboardButton("Расписание на завтра")
                b3 = telebot.types.InlineKeyboardButton("Следующий урок")
                markup.add(b1, b2, b3)
                bot.send_message(message.chat.id,
                                 "Все сделано",
                                 reply_markup=markup)

        except TypeError as e:
            print(e)
            bot.send_message(message.chat.id, str(e) + '')

    except Exception as e:
        print(e)


@bot.message_handler()
def text(message):
    if message.chat.id == 512770440:
        bot.send_sticker(message.from_user.id, random.choice(Efremov))
    today = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].index(
        time.strftime("%A")) + 1
    timing = time.strftime("%H:%M")
    if message.text == 'Часовой пояc':
        bot.send_message(message.chat.id, 'отправь сообщение в формате "+- х"',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        if not check_person(message.chat.id)[2]:
            bot.send_message(message.chat.id,
                             f"За сколько минут до урока скидывать уведомление(число кратное 5)?\n"
                             f"Напишите команду /dtime <b>'x'</b>",
                             parse_mode="html")
    elif message.text[0] in "+-":
        timez = message.text.replace(" ", "").replace('+', '')
        parcer.change_tz(_id=message.chat.id,
                         newtz=timez)
        if check_person(str(message.chat.id))[2]:
            bot.send_message(message.chat.id,
                             f"За сколько минут до урока скидывать уведомление(число кратное 5)?\n"
                             f"Напишите команду /dtime <b>'x'</b>",
                             parse_mode="html")
        else:
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            b1 = telebot.types.InlineKeyboardButton("Расписание на сегодня")
            b2 = telebot.types.InlineKeyboardButton("Расписание на завтра")
            b3 = telebot.types.InlineKeyboardButton("Следующий урок")
            markup.add(b1, b2, b3)
            bot.send_message(message.chat.id, "Все сделано", reply_markup=markup)
    elif message.text == "Я из Москвы":
        timez = "3"
        parcer.change_tz(_id=message.chat.id,
                         newtz=timez)
        bot.send_message(message.chat.id, f"За сколько до урока скидывать уведомление(число кратное 5)?"
                                          f"\nНапишите команду /dtime <b>{'x'}</b>",
                         parse_mode='html',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    elif message.text == "Расписание на сегодня":
        info = parcer.day_dairy(message.chat.id, today)
        bot.send_message(message.chat.id, f'Сегодня{info}' if info == " нет уроков" else info)
    elif message.text == "Расписание на завтра":
        info = parcer.day_dairy(message.chat.id, (today + 1) % 7 if today != 6 else 7)
        bot.send_message(message.chat.id, f'Завтра{info}' if info == " нет уроков" else info)
    elif message.text == "Следующий урок":
        with open("database.json") as file:
            sfile = json.load(file)
        next_today = 0 + today
        info = ""
        while info == "":
            lessons = sfile[str(message.chat.id)][str(next_today)]
            for i in lessons.keys():
                if next_today != today or int(i.split(":")[0])\
                        > int(timing.split(":")[0]) or (int(i.split(":")[0]) == int(timing.split(":")[0])
                                                        and int(i.split(":")[1]) > int(timing.split(":")[1])):
                    info = f'Следующий урок в' \
                           f' {["пн", "вт", "ср", "чт", "пт", "сб", "вс"][next_today - 1]} в {i}\n{lessons[i]}'
                    break
            next_today = (next_today + 1) % 7 if today != 6 else 7
        bot.send_message(message.chat.id, info)


@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    try:
        if message.chat.id == 512770440:
            bot.send_sticker(message.from_user.id, random.choice(Efremov))

        try:
            chat_id = message.chat.id
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = f'savedFiles/{chat_id}diary.xlsx'

            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)

            bot.reply_to(message, "Я получил ваш файл")
            parcer.parce(chat_id)
            b = check_person(str(message.chat.id))

            if not b[1]:
                bot.send_message(message.chat.id, "Остался часовой пояс и /dtime")

            else:
                markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
                b1 = telebot.types.InlineKeyboardButton("Расписание на сегодня")
                b2 = telebot.types.InlineKeyboardButton("Расписание на завтра")
                b3 = telebot.types.InlineKeyboardButton("Следующий урок")
                markup.add(b1, b2, b3)
                bot.send_message(message.chat.id,
                                 "Все сделано, проверить: /settings",
                                 reply_markup=markup)

        except Exception as exc:
            bot.reply_to(message, (str(exc) + '  - ОШИБКА!'))

    except Exception as e:
        print(e)


@bot.message_handler()
def send_not(_id, lesson, dtime):
    try:
        bot.send_message(_id, f'Скоро урок "{lesson}"!\nУрок через {dtime} минут')

    except Exception as e:
        print(e)


if __name__ == '__main__':
    ScheduleMessage.start_process()
    try:
        bot.polling(none_stop=True)
        
    except Exception as exc:
        print(exc)
