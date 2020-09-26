#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import misc
from answers import answers
from yobit import get_btc
from time import sleep

# https://api.telegram.org/bot1360377031:AAGxjN-QbQd62_5M4z3kRclGuh1WZFy5oDw/getMe


class Bot:
	def __init__(self, token):
		self.last_updated_id = 0
		self.token = token
		self.URL = 'https://api.telegram.org/bot' + token + '/'

	def get_updates(self):
		url = self.URL + 'getupdates'
		r = requests.get(url)
		return r.json()

	def get_message(self):

		data = self.get_updates()
		try:
			last_object = data['result'][-1]
		except IndexError:
			return None
		current_update_id = last_object['update_id']

		if current_update_id != self.last_updated_id:
			chat_id = last_object['message']['chat']['id']
			message_text = last_object['message']['text']
			message = {'chat_id': chat_id,
						'text': message_text}
			self.last_updated_id = current_update_id
			return message

		return None

	def send_message(self, chat_id, text='Wait for a second...'):
		url = self.URL + f'sendmessage?chat_id={chat_id}&text={text}'
		requests.get(url)


def main():
	bot = Bot(misc.token)
	while True:
		answer = bot.get_message()

		if answer is not None:  # проверяет новое ли сообщение
			chat_id = answer['chat_id']
			text = answer['text']

			if text == '/btc':
				bot.send_message(chat_id, get_btc())
				continue
			elif text.lower() in answers:
				text_to_send = answers[text.lower()]
				bot.send_message(chat_id, text_to_send)
			else:
				bot.send_message(chat_id, 'мой твой не понимать')
				continue

		sleep(3)


if __name__ == "__main__":
	main()
