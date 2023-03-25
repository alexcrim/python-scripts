from subprocess import check_output
import telebot
import time

chats = <message.chat.id> 				# Параметр ID чата из API Telegram

msg_for_welcome = ("<текст>")		    # Произвольный текст приветствия пользователя
msg_for_customs = ("<текст>") 		    # Произвольный текст для ввода команды
msg_for_protect = ("<текст>") 	        # Произвольный текст запрета использования бота
msg_for_help = ("<текст>") 			    # Произвольный текст интрукций к боту

cmd_for_pods = ("<текст команды>")	    # Произвольная команда 

cmd_list = {						    # Список команд бота и названия функций
  '/start@<название_бота>':'welcome',
  '/pods@<название_бота>':'pods',
  '/custom@<название_бота>':'customs',
  '/help@<название_бота>':'help'
  }

bot = telebot.TeleBot("<токен>")		# Токен Telegram бота
@bot.message_handler(content_types=["text"])

def protection(message):
  if message.chat.id == chats:
    parse_command(message)
  else:
    bot.send_message(message.chat.id, f"{msg_for_protect}")

def parse_command(message):
  if message.text in cmd_list.keys():
    for key, value in cmd_list.items():
      if message.text == key:
        function_name = value + "(message)"
        eval(function_name)
        break

def welcome(message):

  msg_welcome = bot.send_message(message.chat.id, f"{msg_for_welcome}")
  bot.register_next_step_handler(msg_welcome, protection)

def pods(message):

  msg_pod = bot.send_message(message.chat.id, check_output([f"{cmd_for_pods}"], shell=True))
  bot.register_next_step_handler(msg_pod, protection)

def customs(message):

  msg_custom = bot.send_message(message.chat.id, f"{msg_for_customs}")
  bot.register_next_step_handler(msg_custom, custom_command)

def custom_command(message):

  comand = message.text
  if message.text in cmd_list.keys():
    protection(message)
  else:
    msg_custom_command = bot.send_message(message.chat.id, check_output(comand, shell = True))

def help(message):

  msg_help = bot.send_message(message.chat.id, f"{msg_for_help}")
  bot.register_next_step_handler(msg_help, protection)

if __name__ == '__main__':
  while True:
    try:
      bot.polling(none_stop=True)
    except:
      time.sleep(10)