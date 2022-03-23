import telebot
import time
from multiprocessing.context import Process
import schedule
import datetime
import parcer
import json

bot = telebot.TeleBot('1868908140:AAFU1Xeh3EFz5BKTvdDy4a5rHUwMrZxcoY0')


# noinspection PyMethodParameters


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
    a = [False, False]
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
    return a


def check():
    print('checkes1')
    with open("database.json") as f:
        database = json.load(f)
        print('checkes2')
    for _id in database.keys():
        try:
            print('checkes2')
            nowtime = OurTime(int(database[_id]['timez']))
            print(nowtime.minute, nowtime.hour)
            dt = database[_id]['dtime']
            nowtime.minute += dt
            if nowtime.minute < 0:
                nowtime.hour -= 1
                nowtime.minute += 60
            if nowtime.minute >= 60:
                nowtime.hour += 1
                nowtime.minute -= 60
            print(nowtime.minute, nowtime.hour)
            time_form = f'{nowtime.hour if len(str(nowtime.hour)) == 2 else str(0) + str(nowtime.hour)}:' \
                        f'{nowtime.minute if len(str(nowtime.minute)) == 2 else str(0) + str(nowtime.minute)}'

            send_not(_id=_id,
                     lesson=database[_id][str(nowtime.weekday)][time_form],
                     t=time_form)
        except KeyError as e:
            print(e)

def start_sch():
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


start_sch()


@bot.message_handler(commands=['start'])
def start(message):
    gif = \
        'vgifbot.online/gif/BAACAgIAAxkBAAFHeqJiOjZILiGb0tPsqgoVy9cRv3dQvQACvxgAAnJb0UlZOyxguHTiIiME_1647982227.79.gif'
    bot.send_message(message.chat.id, f'Привет, <b>{message.from_user.first_name}</b>', parse_mode='html')
    bot.send_animation(message.chat.id, gif)
    bot.send_message(message.chat.id, "Скинь боту Execel файл с сайта эжд https://school.mos.ru/")
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = telebot.types.InlineKeyboardButton('Часовой пояc')
    b2 = telebot.types.InlineKeyboardButton('Я из Москвы')
    markup.add(b1, b2)
    bot.send_message(message.chat.id, 'Если ты не из Москвы\nНажмите на кнопку "Часовой пояс"', reply_markup=markup)


@bot.message_handler(commands=['dtime'])
def setdtime(message):
    a = message.text.replace('/dtime ', '')
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
            bot.send_message(message.chat.id, "Все сделано")
    except TypeError as e:
        print(e)
        bot.send_message(message.chat.id, str(e) + '')


@bot.message_handler()
def text(message):
    if message.text == 'Часовой пояc':
        bot.send_message(message.chat.id, 'отправь сообщение в формате "+- х"', reply_markup=telebot.types.ReplyKeyboardRemove())

    elif message.text[0] in "+-":
        timez = message.text.replace(" ", "").replace('+', '')
        parcer.change_tz(_id=message.chat.id,
                         newtz=timez)
        bot.send_message(message.chat.id, "За сколько до урока скидывать уведомление(число кратное 5)?"
                                          " Напишите команду /dtime x")
    elif message.text == "Я из Москвы":
        timez = "3"
        parcer.change_tz(_id=message.chat.id,
                         newtz=timez)
        bot.send_message(message.chat.id, "За сколько до урока скидывать уведомление(число кратное 5)?"
                                          " Напишите команду /dtime x", reply_markup=telebot.types.ReplyKeyboardRemove())



@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
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
            bot.send_message(message.chat.id, "Все сделано")
    except Exception as exc:
        bot.reply_to(message, (str(exc) + '  - ОШИБКА!'))


@bot.message_handler()
def send_not(_id, lesson, t):
    bot.send_message(_id, f'Скоро урок "{lesson}"!\nНюхай бебру сынуля, время {t}')


class ScheduleMessage:
    def try_send_schedule():
        while True:
            schedule.run_pending()
            time.sleep(1)

    def start_process():
        p1 = Process(target=ScheduleMessage.try_send_schedule, args=())
        p1.start()


if __name__ == '__main__':
    ScheduleMessage.start_process()
    try:
        bot.polling(none_stop=True)
    except Exception as exc:
        print(exc)
