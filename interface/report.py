import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime


def updateReport(data):
	scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

	config = ServiceAccountCredentials.from_json_keyfile_name('interface/google_config.json', scope)

	client = gspread.authorize(config)


	sheets = client.open('Daily Report')
	order_sheet = sheets.worksheet('Orders')
	income_sheet = sheets.worksheet('Income')

	order_sheet_data = [
		str(datetime.now().date()),
		data['orderDone'],
		data['orderBotAmount'],
		data['orderRejectedAmount'],
		data['orderAmount']
	]

	income_sheet_data = [
		str(datetime.now().date()),
		data['orderSum'],
		data['orderBotSum'],
		data['orderRejectedSum'],
		data['orderTotalSum']
	]

	order_sheet.insert_row(order_sheet_data, len(order_sheet.get_all_records())+2)
	income_sheet.insert_row(income_sheet_data, len(income_sheet.get_all_records())+2)