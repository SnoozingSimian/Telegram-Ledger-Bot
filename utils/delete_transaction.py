import os

from dotenv import load_dotenv
import mysql.connector 

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_UNAME = os.getenv('DB_UNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_TABLE_NAME = os.getenv('DB_TABLE_NAME')

def remove_last(transaction: dict):
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

	mycursor = mydb.cursor()

	sql = f"""DELETE FROM {DB_TABLE_NAME} 
		WHERE user_name = '{transaction['user_name']}'  
		ORDER BY tid DESC LIMIT 1 
		"""

	try:
		mycursor.execute(sql)
		mydb.commit()
		return 1
	
	except Exception as e:
		print(e)
		return 0
	
