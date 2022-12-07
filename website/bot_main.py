from telegram_bot import LectorAssistantBot

import telebot
from telebot import types
import time

def init():
    TOKEN = '5732212828:AAFquGjvVgsemjSh2WcwYBGCpSd1jTfCAgQ'
    bot = telebot.TeleBot(TOKEN)
    global lector_assistant_bot
    lector_assistant_bot = LectorAssistantBot(bot)


    @bot.message_handler(commands=['start'])
    def start_command(message: types.Message) -> None:
        # bot introduction
        bot.send_message(message.chat.id, 'Hello!\n'
                                          'Ask your mentor to create room on <...> and share room code\n'
                                          'Type /help to get command list')


    @bot.message_handler(commands=['help'])
    def help_command(message: types.Message) -> None:
        # see command list
        bot.send_message(message.chat.id, 'Command list:\n'
                                          '/join room_code to join room, ask your mentor for the code\n'
                                          '/leave to leave current room\n'
                                          '/feedback your_feedback to send feedback to your mentor\n'
                                          '/help to get command list')


    @bot.message_handler(commands=['join'])
    def join_command(message: types.Message) -> bool:
        # join room
        if lector_assistant_bot.join(message):
            bot.send_message(message.chat.id, 'You are now a member of room')
            return True
        else:
            bot.send_message(message.chat.id, 'Seems like there is no room with the code sent')
            return False


    @bot.message_handler(commands=['leave'])
    def leave_command(message: types.Message) -> bool:
        # leave room
        if lector_assistant_bot.leave(message):
            bot.send_message(message.chat.id, 'Room left')
            return True
        else:
            bot.send_message(message.chat.id, 'Seems like you are not a member of any room')
            return False


    @bot.message_handler(commands=['feedback'])
    def feedback_command(message: types.Message) -> bool:
        # send feedback
        if lector_assistant_bot.feedback(message):
            bot.send_message(message.chat.id, 'Feedback sent')
            return True
        else:
            bot.send_message(message.chat.id, 'Seems like you are not a member of any room')
            return False
