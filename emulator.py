import requests
import json

address = 'http://localhost:8000/bot/'

data = {
	"order": ["Corndog with \ud83e\uddc0 Big x11", "Corndog \ud83c\udf2e Medium x14"],
	"cname": "\ud83d\ude81",
	"phone": "+998983147766",
	"location": {"latitude": 41.317896, "longitude": 69.23791},
	"id": 710810997,
	"username": "@kaktu2"
}

try:
	print('Sent')
	response = requests.post(address, {'data': json.dumps(data)})
	print(response.text)
except Exception as e:
	print(e)