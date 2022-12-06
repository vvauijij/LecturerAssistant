from collections import defaultdict
from typing import Union
import uuid
import re

import telebot
from telebot import types

from lecture_template import Poll


def get_message_text(message: types.Message) -> str:
    # get message text code from /command message_text
    text = message.json['text']
    return text[text.rfind(' ') + 1:]


class LectorAssistantBot:
    __slots__ = ['_bot',
                 '_rooms',
                 '_users',
                 '_polls',
                 '_feedback']

    def __init__(self, bot: telebot.TeleBot) -> None:
        # initializing bot
        self._bot = bot
        self._rooms = defaultdict(set)  # room_code - (chat_id1 ... chat_id2)
        self._users = defaultdict(str)  # chat_id - room_code

        self._polls = defaultdict(list)  # poll_id - (chat_id, poll_message_id)
        self._feedback = defaultdict(list)  # room_code - [feedback1 ... feedback2]

    def launch(self) -> None:
        # launch bot
        self._bot.polling(none_stop=True, interval=0)

    def stop(self) -> None:
        # stop bot
        self._bot.stop_polling()

    def create_room(self, room_code: str) -> bool:
        # create room
        if room_code not in self._rooms.keys():
            self._rooms[room_code] = set()
            self._feedback[room_code] = list()
            return True
        else:
            return False

    def delete_room(self, room_code: str) -> bool:
        # delete room
        if room_code in self._rooms.keys():
            for [chat_id, user_room_code] in self._users:
                if user_room_code == room_code:
                    self._users.pop(chat_id)
            self._rooms.pop(room_code)
            self._feedback.pop(room_code)
            return True
        else:
            return False

    def join(self, message: types.Message) -> bool:
        # join room
        room_code = get_message_text(message)
        if room_code in self._rooms.keys():
            self._rooms[room_code].add(message.chat.id)
            self._users[message.chat.id] = room_code
            return True
        else:
            return False

    def leave(self, message: types.Message) -> bool:
        # leave room
        chat_id = message.chat.id
        if chat_id in self._users.keys():
            self._rooms[self._users[chat_id]].remove(chat_id)
            self._users.pop(chat_id)
            return True
        else:
            return False

    def feedback(self, message: types.Message) -> bool:
        # send feedback
        chat_id = message.chat.id
        if chat_id in self._users.keys():
            self._feedback[self._users[chat_id]].append(get_message_text(message))
            return True
        else:
            return False

    def send_poll(self, room_code: str, poll: Poll) -> Union[str, None]:
        # send poll to room, return poll_id
        if room_code in self._rooms.keys():
            poll_id = uuid.uuid1().hex
            for chat_id in self._rooms[room_code]:
                self._polls[poll_id].append((chat_id, self._bot.send_poll(chat_id,
                                                                          question=poll.question,
                                                                          options=poll.options,
                                                                          type=poll.poll_type,
                                                                          correct_option_id=poll.correct_option_id,
                                                                          explanation=poll.explanation,
                                                                          is_closed=poll.is_closed,
                                                                          is_anonymous=poll.is_anonymous).id))
            return poll_id
        else:
            return None

    def get_poll_result(self, room_code: str, poll_id: str) -> Union[dict, None]:
        # bot close poll, return poll result
        poll_results = defaultdict(int)
        if room_code in self._rooms.keys() and poll_id in self._polls.keys():
            for [chat_id, poll_message_id] in self._polls[poll_id]:
                options = self._bot.stop_poll(chat_id, poll_message_id).options
                for option in options:
                    poll_results[option.text] += option.voter_count
            self._polls.pop(poll_id)
            return poll_results
        else:
            return None

    def get_feedback(self, room_code: str) -> Union[list[str], None]:
        # bot return feedback
        if room_code in self._feedback.keys():
            return self._feedback[room_code]
        else:
            return None
