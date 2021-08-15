import os
import time
import telepot

from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
from datetime import timedelta
from tornado import ioloop
from threading import Thread
from selenium import webdriver

def handle(msg):
	print(msg)
	if 'from' in msg and 'username' in msg['from']:
		print('>request from user: ' + msg['from']['username'])
		username = msg['from']['username']
		

	if 'from' in msg and 'id' in msg['from']:
		currId = str(msg['from']['id'])
		print('>id: ' + currId)

		# Check if user is authorized
		if not isAuthorized(currId):
			bot.sendMessage(currId, 'Utente Non autorizzato')
			return

		text = msg['text']
		print(text)
		

		if text=="/start":
			bot.sendMessage(currId, 'Ciao! Benvenuto! Per iniziare scrivi il link del video')
	
		if text=="/settings":
			bot.sendMessage(currId, "Invia un messaggio della chat del tuo canale")

       
		if isLink(text):
			link = str(text)
			bot.sendMessage(currId, 'Sto iniziando con le views!')
			doViews(link,currId)
			bot.sendMessage(currId, "Ho finito di fare le views")
			
	else:
		pass

def isAuthorized(userId):
	# Check if user is authorized
	isAuthorized = False
	for x in range(0, len(authorizedUsers)):
		if authorizedUsers[x] == userId:
			isAuthorized = True
			print(isAuthorized)
	return isAuthorized


def isLink(text):
	if "https://" in text:
		return True
	else:
		return False 

def doViews(link,id):
	op=webdriver.ChromeOptions()
	op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
	op.add_argument("--headless")
	op.add_argument("--no-sandbox")
	op.add_argument("--disable-dev-sh-usage")

	url=link
	driver=[]
	
	for i in range(0,1000):
	  driver[i]=webdriver.Chrome(executable_path= os.environ.get("CHROMEDRIVER_PATH"), chrome_options=op)
	  driver[i].get(url)
	  bot.sendMessage(id,"ho aperto i browser ora aspetto")
	  time.sleep(60)
	  for i in range(0,1000):
	    driver[i].close()
	  return True 



def startMainLoop():
	MessageLoop(bot, handle).run_forever()

bot = telepot.Bot("1990436864:AAHBTxhv9a6guc7HdChoLbg4O4vGB-xFeTo")

# Lista di utenti autorizzati
authorizedUsers= [] 
authorizedUsers.append("145318515")

t2 = Thread(target=startMainLoop)
t2.start()
