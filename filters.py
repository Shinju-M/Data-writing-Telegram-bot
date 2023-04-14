from aiogram import Router
from aiogram.types import Message
import db

router = Router()


def not_bot(message: Message):
    if message.from_user.is_bot == False:
        return True


def student_filter(message: Message):
    if str(message.from_user.id) in db.select_students(message.chat.id):
        return True


def non_students_filter(message: Message):
    if str(message.from_user.id) not in db.select_curators(message.chat.id):
        return True


def curator_filter(message: Message):
    if str(message.from_user.id) in db.select_curators(message.chat.id):
        return True


def start_message_filter(message: Message):
    if not message.reply_to_message:
        return True


def reply_filter(message: Message):
    if message.reply_to_message:
        return True
