import re
from datetime import datetime

from telegram import Update

# regexp to match item
ITEM_PAT = r'^[a-zA-Z ]+'

# regexp to match price
PRICE_PAT = r'[0-9,.]+k?K?$' 

def parse_transaction(update: Update):
	item = " ".join(re.findall(ITEM_PAT, update.message.text)).strip()
	price = " ".join(re.findall(PRICE_PAT, update.message.text)).strip()

	user_name = f"{update.message.chat.first_name}_{update.message.chat.last_name}"
	uid = update.message.chat.id
	transaction_time = str(update.message.date.time())
	transaction_date = str(update.message.date.date())
	
	transaction = {}
	transaction['user_name'] = user_name
	transaction['uid'] = uid
	transaction['transaction_time'] = transaction_time
	transaction['transaction_date'] = transaction_date
	transaction['item'] = item
	transaction['price'] = price
	
	return transaction
