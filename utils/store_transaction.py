import os

from dotenv import load_dotenv
import mysql.connector 

load_dotenv()

REQ_FIELDS = ['user_name', 'uid', 'transaction_time', 'transaction_date', 'item', 'price']
DB_HOST = os.getenv('DB_HOST')
DB_UNAME = os.getenv('DB_UNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_TABLE_NAME = os.getenv('DB_TABLE_NAME')

def store_transaction(transaction: dict):
	mydb = mysql.connector.connect(
		host=DB_HOST,
		user=DB_UNAME,
		password=DB_PASSWORD,
		database=DB_NAME
		)

	if mydb:
		print("DB connection established!")
	else:
		print("could not connect to DB")

	# cannot store a malformed entry
	for key in REQ_FIELDS:
		if key not in transaction.keys():
			print(f"Field {key} missing.")
			return 0
	
	mycursor = mydb.cursor()
	sql = f"""INSERT INTO {DB_TABLE_NAME} 
		(uid, user_name, transaction_date, transaction_time, item, price) 
		VALUES 
		(%s, %s, %s, %s, %s, %s)"""
	val = (
		transaction['uid'],
		transaction['user_name'],
		transaction['transaction_date'], 
		transaction['transaction_time'], 
		transaction['item'], 
		transaction['price'])

	try:
		mycursor.execute(sql, val)
		mydb.commit()
		return 1

	
	except:
		return 0