import os
import logging

# util imports
from utils.parse_transaction import parse_transaction
from utils.delete_transaction import remove_last
from utils.store_transaction import store_transaction

from dotenv import load_dotenv

# telegram imports
from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters


# version
VERSION = "0.0.1"

# securely get the API_KEY
load_dotenv()
API_KEY = os.getenv("API_KEY")

# set logging on
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# connect bot
#bot = telegram.Bot(token=API_KEY)

# create updater
updater = Updater(token=API_KEY, use_context=True)
dispatcher = updater.dispatcher

# define commands here

# start message
def start(update: Update, context: CallbackContext):
	context.bot.send_message(chat_id=update.effective_chat.id, 
				 text=f"This is leger_bot version {VERSION}\nI hope I can be of use")


# add support for deleting last entry
def delete_last(update: Update, context: CallbackContext):
	transaction = parse_transaction(update)
	remove = remove_last(transaction)
	
	if remove == 1:
		context.bot.send_message(chat_id=update.effective_chat.id,
				 text="Removed last entry.")
	
	elif remove == 0:
		context.bot.send_message(chat_id=update.effective_chat.id,
				 text="Could not remove last entry.")

def summary():
	#stub
    return 


# define message handling here
# our bot needs to simply parse input text into items and costs
# for now, the input format should be <item> <cost>
def transaction(update: Update, context: CallbackContext):
	transaction = parse_transaction(update)
	store = store_transaction(transaction)
	
	if store == 1:
		context.bot.send_message(chat_id=update.effective_chat.id,
				 	 text="Thanks for telling me!")

	elif store == 0:
		context.bot.send_message(chat_id=update.effective_chat.id,
				 	 text="I could not understand that, the format is <item> <price>")


# handlers handle different types of actions by user
start_handler = CommandHandler('start', start)
delete_last_handler = CommandHandler('rml', delete_last)
transaction_handler = MessageHandler(Filters.text & (~Filters.command), transaction)

# the above handlers need to be addded to the dispatcher
dispatcher.add_handler(start_handler)
dispatcher.add_handler(transaction_handler)
dispatcher.add_handler(delete_last_handler)
updater.start_polling()
