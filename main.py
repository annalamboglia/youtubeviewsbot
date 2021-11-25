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
			return false

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
	url=str(link)

	chrome_options = webdriver.ChromeOptions()
	chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
	chrome_options.add_argument("--headless")
	chrome_options.add_argument("--disable-dev-shm-usage")
	chrome_options.add_argument("--no-sandbox")
	driver1 = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
	
	#driver1=webdriver.Chrome()

	for i in range(0,999):
		#bot.sendMessage(id,"Apro il browser")
		driver1.get(url)
		#bot.sendMessage(id,"Ho aperto il Browser")
		try:
			element=driver1.find_element_by_xpath("//*[text()='Accetto']").click()
			
		except:
			#bot.sendMessage(id,"Non Sono Riuscito ad aprire il driver!")
			print("Non ho cliccato")
			
		if i==0:
			bot.sendMessage(id,"ho aperto i browser ora aspetto")
		if i==100:
			bot.sendMessage(id,"sto a 100 views")
		time.sleep(3600)
	driver1.close()


def startMainLoop():
	MessageLoop(bot, handle).run_forever()

bot = telepot.Bot("1990524390:AAFEZYwose4jyVKokNUWfHGisQdSRI750_Q")

# Lista di utenti autorizzati
authorizedUsers= [] 
authorizedUsers.append("145318515")

t2 = Thread(target=startMainLoop)
t2.start()
