from aiogram import Router
from aiogram import filters as flt
from aiogram.types import Message

from Bot import bot
import filters
import db

router = Router()


@router.message(flt.Command('curator'))
async def bot_start(message: Message):
    user_id = message.from_user.id
    chat_id =message.chat.id
    if str(user_id) in db.select_students(chat_id):
        db.update_user(user_id, 1, chat_id)
    else:
        db.insert_member(user_id, 1, chat_id)


@router.message(flt.Command('start'))
async def bot_start(message: Message):
    chat_id = message.chat.id
    db.create_db(chat_id)
    db.create_members_table(chat_id)
    db.create_messages_table(chat_id)
    db.create_replies_table(chat_id)
    db.insert_member(message.from_user.id, 1, chat_id)


@router.message(filters.non_students_filter, filters.start_message_filter)
async def message_write(message: Message):
    message_id = message.message_id
    user_id = message.from_user.id
    message_body = message.text
    message_date = message.date
    is_replied = 0
    chat_id = message.chat.id
    if str(user_id) not in db.select_students(chat_id):
        db.insert_member(message.from_user.id, 0, chat_id)
    db.insert_message(message_id, user_id, message_body, message_date, is_replied, chat_id)


@router.message(filters.reply_filter)
async def reply_write(message: Message):
    reply_id = message.message_id
    reply_user = message.from_user.id
    reply_body = message.text
    reply_date = message.date
    message_id = message.reply_to_message.message_id
    is_replied = 1
    interval = (message.date.timestamp() - message.reply_to_message.date.timestamp()) / 3600
    chat_id = message.chat.id
    if str(message_id) in db.select_messages_id(chat_id):
        db.update_message(message_id, is_replied, chat_id)
    db.insert_reply(reply_id, reply_user, reply_body, reply_date, interval, message_id, chat_id)


@router.message(flt.Command('reply_stats'))
async def get_message_stats(message: Message):
    chat_id = message.chat.id
    massage_status = db.select_messages(chat_id)
    messages = list(massage_status.keys())
    replied = sum(massage_status.values())
    stats_answer = f'Сообщения от учеников: {len(messages)}.\n' \
                   f'Число отвеченных сообщений: {replied}.\n' \
                   f'Число неотвеченных сообщений: {len(messages) - replied}.'
    await bot.send_message(chat_id=message.from_user.id, text=stats_answer)


@router.message(flt.Command('non_replied'))
async def get_nreplied_texts(message: Message):
    chat_id = message.chat.id
    non_replied = db.get_nreplied(chat_id)
    texts = ''
    for i in range(0, len(non_replied)):
        texts = texts + f'Сообщение {i+1}: {str(non_replied[i]).strip("(),")}.\n'
    await bot.send_message(chat_id=message.from_user.id, text=texts)


@router.message(flt.Command('time'))
async def get_interval(message: Message):
    chat_id = message.chat.id
    time = db.select_message_reply_interval(chat_id)
    time_avg = sum(time) / len(time)
    answer = f'Среднее время отклика кураторов: {str(round(time_avg, 4))} часа.'
    await bot.send_message(chat_id=message.from_user.id, text=answer)


@router.message(flt.Command('time_curator'))
async def get_curator_interval(message: Message):
    chat_id = message.chat.id
    curator_interval = list(db.select_curator_interval(chat_id).values())
    curator_interval_dict = {}
    curator_message_count = {}
    curator_interval_avg = {}
    for i in curator_interval:
        if i[0] not in curator_interval_dict.keys():
            curator_interval_dict[i[0]] = i[1]
            curator_message_count[i[0]] = 1
        else:
            curator_interval_dict[i[0]] += i[1]
            curator_message_count[i[0]] += 1
    for i in curator_interval_dict.keys():
        curator_interval_avg[i] = curator_interval_dict[str(i)] / curator_message_count[str(i)]
    text = ''
    for i, x in curator_interval_avg.items():
        text = text + f'Среднее время ответа куратора {i}: {round(x, 4)} часа.\n'
    await bot.send_message(chat_id=message.from_user.id, text=text)
