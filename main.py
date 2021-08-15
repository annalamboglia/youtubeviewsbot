import os
import time
import logging
import configparser
import telepot
import createpost
import urllib
import random
import requests
import utils
import pprint
from bs4 import BeautifulSoup
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
from datetime import timedelta
from tornado import ioloop
from threading import Thread
from selenium import webdriver
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


def handle(msg):
	print(msg)
	if 'from' in msg and 'username' in msg['from']:
		logging.info('>request from user: ' + msg['from']['username'])
		print('>request from user: ' + msg['from']['username'])
		username = msg['from']['username']
		

	if 'from' in msg and 'id' in msg['from']:
		currId = str(msg['from']['id'])
		print('>id: ' + currId)
		logging.info('>id: ' + currId)

		# Check if user is authorized
		if not isAuthorized(currId):
			logging.error('>user ' + currId + ' not authorized!')
			return

		text = msg['text']
		print(text)
		logging.info('>text: ' + text)

		if text=="/start":
			bot.sendMessage(currId, 'Ciao! Benvenuto! Per iniziare scrivi /settings')
	
		if text=="/settings":
			bot.sendMessage(currId, "Invia un messaggio della chat del tuo canale")


		if utils.isValidCommand(text):
			tipoPost = text.replace('/', '')
			print(tipoPost)
			logging.debug('>tipoPost: ' + tipoPost)
			logging.info('>command - currId: ' + currId)
			bot.sendMessage(currId, 'Invia il link')
			return

		if utils.isLink(text):
			link = text
			print('>link - currId: ' + currId)
			logging.info('>link - currId: ' + currId)
			rand = os.urandom(10)
			idPost = int.from_bytes(rand, 'big')
			res = ''
			try:
				logging.debug('>begin download page')
				pageObj = requests.get(link)
				logging.debug('>end download page')
				#logging.debug(pageObj)
				page = pageObj.text
				logging.debug('>page: ' + page)
				res = utils.parsePage(page) # TODO: Parsa la pagina per ottenere i dati
			except Exception as e:
				logging.error('>Error in parsing page: ' + link + ' - currId: ' + currId)
				logging.error(e)
				bot.sendMessage(currId, 'Errore, invia un link valido')
				return

			logging.info('>res: ' + res)
	
			affiliate_tag="annalambogl0d-21"
			url=amazonify(text, affiliate_tag)
			print(url)
			nomeProdotto,prezzoPieno,prezzoAttuale,immagine = prediDati(url)
			
			postText=createPost(url, nomeProdotto , prezzoPieno, prezzoAttuale)
			print(postText)
			keyboard = utils.getResponseKeyboard(url)
			print(immagine)
			ID=-1001210576231
			try:
				bot.sendPhoto(chat_id=ID, photo=immagine, caption=postText, reply_markup=keyboard, parse_mode='Markdown')
				bot.sendMessage(currId, 'Messaggio Inviato!')
			except:
				bot.sendMessage(ID, postText, reply_markup=keyboard, parse_mode='Markdown')
				bot.sendMessage(currId, 'Messaggio Inviato!')
			
			
	else:
		logging.error('>unable to get id from request')


def isAuthorized(userId):
	# Check if user is authorized
	isAuthorized = False
	for x in range(0, len(authorizedUsers)):
		if authorizedUsers[x] == userId:
			isAuthorized = True
			print(isAuthorized)
	return isAuthorized


def amazonify(url, affiliate_tag):
    """Generate an Amazon affiliate link given any Amazon link and affiliate
    tag.
    :param str url: The Amazon URL.
    :param str affiliate_tag: Your unique Amazon affiliate tag.
    :rtype: str or None
    :returns: An equivalent Amazon URL with the desired affiliate tag included,
        or None if the URL is invalid.
    Usage::
        >>> from amazonify import amazonify
        >>> url = 'someamazonurl'
        >>> tag = 'youraffiliatetag'
        >>> print amazonify(url, tag)
        ...
    """
    # Ensure the URL we're getting is valid:
    url = url.replace(" ", "")
    if not url.startswith("http"):
        url = "https://" + url

    # resolve amzn.to links
    url = requests.head(url, allow_redirects=True).url

    new_url = urlparse(url)
    if not new_url.netloc:
        return None

    # Add or replace the original affiliate tag with our affiliate tag in the
    # querystring. Leave everything else unchanged.
    query_dict = parse_qs(new_url[4])
    query_dict['tag'] = affiliate_tag
    new_url = new_url[:4] + (urlencode(query_dict, True), ) + new_url[5:]
	
    return urlunparse(new_url)


def createPost(link, nomeProdotto, prezzoPieno, prezzoAttuale):
	number=random.randint(0,2)
	
	Topbar=["🔥 MINIMO STORICO ", "❌ ERRORE DI PREZZO", " ❗❗ SUPER OFFERTA"]
	nomeProdotto=str(nomeProdotto).strip()
	emojiPrezzo	= "💶 Prezzo Pieno "
	emojiPrezzoAttuale = "📉 PREZZO OFFERTA "
	nomeProdotto=str(nomeProdotto)
	nomeProdotto.strip()
	emojiLink="➡️  LINK OFFERTA "
	descrizione= Topbar[number] + "\n" + nomeProdotto + "\n" + "\n" + emojiPrezzoAttuale + prezzoAttuale + "\n\n" + emojiLink + link
	return descrizione 

def prediDati(link):
	op=webdriver.ChromeOptions()
	op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
	op.add_argument("--headless")
	op.add_argument("--no-sandbox")
	op.add_argument("--disable-dev-sh-usage")
	
	driver=webdriver.Chrome(executable_path= os.environ.get("CHROMEDRIVER_PATH"), chrome_options=op)
	url=link
	#template="https://www.amazon.it/s?k={}"
	#search_tearm='computer'
	#search_tearm= search_tearm.replace(' ', '+')
	#linkTotale=template.format(search_tearm)
	#print(linkTotale)
	driver.get(url)
	try:
		element=driver.find_element_by_id("sp-cc-accept")
		element.click()
		element=driver.find_elements_by_class_name("a-button-input celwidget")
		element.click()
	except:
		print("Non ho cliccato")

	soup =BeautifulSoup(driver.page_source,'html.parser')
	results= soup.find('class', "a-section a-spacing-none")
	
	Nome = driver.find_elements_by_xpath('//*[@id="productTitle"]')

	titolo = Nome[0].get_attribute("innerHTML")

	try:
		prezzo = driver.find_elements_by_class_name("priceBlockStrikePriceString a-text-strike")
		prezzoPieno = str(prezzo[0].get_attribute("innerHTML")).replace("&nbsp;", " ")
	except:
		prezzoPieno= ""

	try:
		price=driver.find_elements_by_xpath('//*[@id="priceblock_dealprice"]')
		prezzoAttuale = str(price[0].get_attribute("innerHTML")).replace("&nbsp;", " ")
	except:	
		price = driver.find_elements_by_id("priceblock_ourprice")
		prezzoAttuale = str(price[0].get_attribute("innerHTML")).replace("&nbsp;", " ")

	try:
		#images=driver.find_element_by_tag_name('img')
		images=driver.find_element_by_xpath('//img[@class="a-dynamic-image a-stretch-vertical"]')
		print("SONO SOPRA")
	except:
		#images = driver.find_element_by_xpath("landingImage")
		#images = driver.find_elements_by_class_name("fullscreen")
		#img = images[0].get_attribute("innerHTML")
		#print("Sotto")
		images=""
	
	try:
		#src=images.src
		src=images[0].get_attribute('src')
	except: 
		src=""
	#immagine=urllib.request.urlretrieve(src, "filename.png")

	driver.close()

	return titolo,prezzoPieno,prezzoAttuale,src

""" 	item=results
	atag=item.h2.a
	description= atag.text
	url = "https://www.amazon.it/" + atag.get('href')
	price_parent = item.find('span', 'a-price')
	#price_parent.find('span', 'a-offscreen')
	print(price_parent.text)
	price=price.text
	rating=item.i.text """



def startMainLoop():
	MessageLoop(bot, handle).run_forever()

def startScheduleLoop():
	telegram_channel = config['telegram_api']['telegram_channel']
	while True:
		now = datetime.now()
		for x in range(0, len(postList)):
			if isinstance(postList[x].orario, datetime) and now.date() == postList[x].orario.date() and now.hour == postList[x].orario.hour and now.minute == postList[x].orario.minute:
				logging.info('>sending post idPost ' + str(postList[x].idPost))
				sendPost(postList[x], telegram_channel)
				bot.sendMessage(telegram_channel, str(postList[x].idPost))
				del postList[x]
				break
		time.sleep(2)


config = configparser.ConfigParser()
config.read('config.ini')

log_file = config['environment']['log_file']
logging.basicConfig(filename=log_file, level=logging.DEBUG)

telegram_token = config['telegram_api']['telegram_token']
bot = telepot.Bot("1941329366:AAFVJ1acWa6mPixyN9W2etxt2aQ91703Hc4")
print(bot.getMe())

# Lista delle sessioni
sessionList = []

# Lista dei post
postList = []

# Lista di utenti autorizzati
authorizedUsers = []
#user1 = config['authorized_users']['user_1']
authorizedUsers.append("145318515")

logging.info('START')

t1 = Thread(target=startMainLoop)
t2 = Thread(target=startScheduleLoop)

t1.start()
t2.start()
