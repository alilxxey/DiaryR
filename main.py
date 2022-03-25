import telebot
import time
from multiprocessing.context import Process
import schedule
import datetime
import parcer
import json
import random

bot = telebot.TeleBot('1868908140:AAFU1Xeh3EFz5BKTvdDy4a5rHUwMrZxcoY0')


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
        if database[_id]["dtime"]:
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
                         dtime=dt)

            except KeyError as e:
                print(e)

    except Exception as e:
        print(e)


def start_sch():
    try:
        times = []
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
                if f'{h}:{m}' not in times:
                    times.append(f'{h}:{m}')
        for i in times:
            schedule.every().day.at(i).do(check)
    except Exception as e:
        print(e)


start_sch()


@bot.message_handler(commands=['changeDtime'])
def changedtime(message):
    try:
        bot.send_message(message.chat.id,
                         f"За сколько минут до урока скидывать уведомление(число кратное 5)?\n"
                         f"Напишите команду /dtime <b>{'x'}</b>",
                         parse_mode="html")
    except Exception as e:
        print(e)


@bot.message_handler(commands=['stickers'])
def stickers(message):
    bot.send_message(message.chat.id, "Скинь боту свои любимые стикеры\n"
                                      "/del_stickers - Если ты хочешь удалить уже ранее добавленные стикеры\n"
                                      "/ready - Обратно", reply_markup=telebot.types.ReplyKeyboardRemove())


@bot.message_handler(content_types=['sticker'])
def get_sticker(message):
    with open("database.json") as file:
        sfile = json.load(file)
        sfile1 = sfile[str(message.chat.id)]
        if "stickers" in sfile1:
            sfile1["stickers"].append(message.sticker.file_id)
        else:
            sfile1["stickers"] = [message.sticker.file_id]
        sfile[str(message.chat.id)] = sfile1
    with open("database.json", "w") as file:
        json.dump(sfile, file)


@bot.message_handler(commands=['del_stickers'])
def del_stickers(message):
    try:
        with open("database.json") as file:
            sfile = json.load(file)
            sfile1 = sfile[str(message.chat.id)]
            sfile1["stickers"] = []
            sfile[str(message.chat.id)] = sfile1
        with open("database.json", "w") as file:
            json.dump(sfile, file)
        bot.send_message(message.chat.id, "Скинь боту свои любимые стикеры\n/ready - Обратно")
    except Exception as e:
        print(e)


@bot.message_handler(commands=['changeTZ'])
def changetz(message):
    try:
        bot.send_message(message.chat.id, f'Напиши свой часовой пояс в формате ± <b>x</b>\n(Москва: +3)',
                         reply_markup=telebot.types.ReplyKeyboardRemove())

    except Exception as e:
        print(e)


@bot.message_handler(commands=['diary'])
def diary(message):
    with open("database.json") as file:
        sfile = json.load(file)
    if str(message.chat.id) in sfile and "stickers" in sfile[str(message.chat.id)]:
        bot.send_sticker(message.chat.id, random.choice(sfile[str(message.chat.id)]["stickers"]))
    try:
        _id = message.chat.id
        alldairy = ""
        for i in range(1, 8):
            day_d = parcer.day_dairy(_id, i)
            alldairy += f'{day_d}\n'
        bot.send_message(_id, alldairy)
        bot.send_message(message.chat.id, f'Расписание устарело или загрузилось неправильно?\n'
                                          f'Просто отправь новый файл с расписанием\n'
                                          f'/ready - Обратно')

    except Exception as e:
        print(e)


@bot.message_handler(commands=['ready'])
def ready(message):
    with open("database.json") as file:
        sfile = json.load(file)
    if str(message.chat.id) in sfile and "stickers" in sfile[str(message.chat.id)]:
        bot.send_sticker(message.chat.id, random.choice(sfile[str(message.chat.id)]["stickers"]))
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = telebot.types.InlineKeyboardButton("Расписание на сегодня")
    b2 = telebot.types.InlineKeyboardButton("Расписание на завтра")
    b3 = telebot.types.InlineKeyboardButton("Следующий урок")
    markup.add(b1, b2, b3)

    bot.send_message(message.chat.id, "Все сделано\n/settings - Проверить или изменить\n"
                                      "/stickers - Tы можешь разбавить дизайн своими стикерами", reply_markup=markup)


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
                                          f'/diary - проверить расписание\n'
                                          f'/ready - Обратно')

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
                                 "Все сделано\n/settings - Проверить или изменить\n"
                                 "/stickers - Tы можешь разбавить дизайн своими стикерами",
                                 reply_markup=markup)

        except TypeError as e:
            print(e)
            bot.send_message(message.chat.id, str(e) + '')

    except Exception as e:
        print(e)


@bot.message_handler()
def text(message):
    with open("database.json") as file:
        sfile = json.load(file)
    if str(message.chat.id) in sfile and "stickers" in sfile[str(message.chat.id)]:
        bot.send_sticker(message.chat.id, random.choice(sfile[str(message.chat.id)]["stickers"]))
    today = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].index(
        time.strftime("%A")) + 1
    timing = time.strftime("%H:%M")
    if message.text == 'Часовой пояc':
        bot.send_message(message.chat.id, 'отправь сообщение в формате "+- х"',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    elif message.text[0] in "+-":
        timez = message.text.replace(" ", "").replace('+', '')
        parcer.change_tz(_id=message.chat.id,
                         newtz=timez)
        if not check_person(message.chat.id)[2]:
            bot.send_message(message.chat.id,
                             f"За сколько минут до урока скидывать уведомление(число кратное 5)?\n"
                             f"Напишите команду /dtime <b>{'x'}</b>",
                             parse_mode="html")
        else:
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            b1 = telebot.types.InlineKeyboardButton("Расписание на сегодня")
            b2 = telebot.types.InlineKeyboardButton("Расписание на завтра")
            b3 = telebot.types.InlineKeyboardButton("Следующий урок")
            markup.add(b1, b2, b3)
            bot.send_message(message.chat.id, "Все сделано\n/settings - Проверить или изменить\n"
                                              "/stickers - Tы можешь разбавить дизайн своими стикерами",
                             reply_markup=markup)
    elif message.text == "Я из Москвы":
        timez = "3"
        parcer.change_tz(_id=message.chat.id,
                         newtz=timez)
        bot.send_message(message.chat.id, f"За сколько до урока скидывать уведомление(число кратное 5)?"
                                          f"\nНапишите команду /dtime <b>{'x'}</b>",
                         parse_mode='html',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    elif message.text == "Расписание на сегодня":
        n = 0
        info = f'{parcer.day_dairy(message.chat.id, (today + n) % 7 if today != 6 else 7)}\n'
        info = f'<b>{info[:info.index(":") + 1]}</b>{info[info.index(":") + 1:]}'
        while info[-12:-2] == "нет уроков":
            n += 1
            info += f'{parcer.day_dairy(message.chat.id, (today + n) % 7 if today + n != 7 else 7)}\n'
        bot.send_message(message.chat.id, info, parse_mode="html")
    elif message.text == "Расписание на завтра":
        n = 1
        info = f'{parcer.day_dairy(message.chat.id, (today + n) % 7 if today != 6 else 7)}\n'
        info = f'<b>{info[:info.index(":") + 1]}</b>{info[info.index(":") + 1:]}'
        while info[-12:-2] == "нет уроков":
            n += 1
            info += f'{parcer.day_dairy(message.chat.id, (today + n) % 7 if today + n != 7 else 7)}\n'
        bot.send_message(message.chat.id, info, parse_mode="html")
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
                    info = f'<b>Следующий урок</b> в' \
                           f' {["пн", "вт", "ср", "чт", "пт", "сб", "вс"][next_today - 1]} в {i}\n{lessons[i]}'
                    break
            next_today = (next_today + 1) % 7 if next_today != 6 else 7
        bot.send_message(message.chat.id, info, parse_mode="html")
    else:
        bot.send_message(message.chat.id, "Не понял о чем ты\n/ready - Обратно")


@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    try:
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
                bot.send_message(message.chat.id, "Остался часовой пояс")

            else:
                markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
                b1 = telebot.types.InlineKeyboardButton("Расписание на сегодня")
                b2 = telebot.types.InlineKeyboardButton("Расписание на завтра")
                b3 = telebot.types.InlineKeyboardButton("Следующий урок")
                markup.add(b1, b2, b3)
                bot.send_message(message.chat.id,
                                 "Все сделано\n/settings - Проверить или изменить\n"
                                 "/stickers - Tы можешь разбавить дизайн своими стикерами",
                                 reply_markup=markup)

        except Exception as e1:
            bot.reply_to(message, (str(e1) + ' - ОШИБКА!'))

    except Exception as e:
        print(e)


@bot.message_handler()
def send_not(_id, lesson, dtime):
    _id = str(_id)
    with open("message.json") as file:
        mfile = json.load(file)
    if mfile != {}:
        if [i for i in mfile[[i for i in mfile][0]]][0] != time.strftime("%H:%M"):
            with open("message.json", "w") as file:
                json.dump({}, file)
    with open("message.json") as file:
        mfile = json.load(file)
    if _id in mfile:
        mfile1 = mfile[_id]
        if lesson not in mfile1[time.strftime("%H:%M")]:
            with open("database.json") as file:
                sfile = json.load(file)
            if str(_id) in sfile and "stickers" in sfile[str(_id)]:
                bot.send_sticker(_id, random.choice(sfile[str(_id)]["stickers"]))
            bot.send_message(_id, f'Скоро урок "{lesson}"!\nчерез {dtime} минут')
            mfile1[time.strftime("%H:%M")].append(lesson)
        mfile[_id] = mfile1
    else:
        mfile1 = {time.strftime("%H:%M"): [lesson]}
        mfile[_id] = mfile1
        with open("database.json") as file:
            sfile = json.load(file)
        if str(_id) in sfile and "stickers" in sfile[str(_id)]:
            bot.send_sticker(_id, random.choice(sfile[str(_id)]["stickers"]))
        bot.send_message(_id, f'Скоро урок "{lesson}"!\nчерез {dtime} минут')
    with open("message.json", "w") as file:
        json.dump(mfile, file)


if __name__ == '__main__':
    ScheduleMessage.start_process()
    try:
        bot.polling(none_stop=True)
        
    except Exception as exc:
        print(exc)
