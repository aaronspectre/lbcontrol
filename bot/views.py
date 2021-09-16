from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.models import User
from bot.models import Order

import json
from math import sin, cos, sqrt, atan2, radians

@csrf_exempt
def index(request):
	try:
		data = json.loads(request.POST['data'])
		order = Order()

		order.order = json.dumps(data['order'])
		order.date = timezone.now()
		order.customer_name = data['cname']
		order.customer_phone = data['phone']
		order.customer_location = json.dumps(data['location'])
		order.customer_username = data['username']
		order.customer_id = int(data['id'])
		order.price = len(order.order) * 12000
		order.source = 'robot'
		order.executor = findNearest(data['location'])
		order.save()

		return HttpResponse('Got')
	except Exception as e:
		print(e)
		return HttpResponse(e)



def calculateDistance(client_location, locations):
	R = 6373.0

	distance_lat = radians(client_location['latitude']) - radians(locations[0])
	distance_lon = radians(client_location['longitude']) - radians(locations[1])

	a = sin(distance_lat/2)**2+cos(radians(locations[0]))*cos(radians(client_location['latitude']))*sin(distance_lon/2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	distance = R * c

	return distance



def findNearest(client_location):

	locations = {
		'oybek': {
			'user': User.objects.get(id = 1),
			'location': [41.294536, 69.2757165],
			'distance': int()
		},
		'chilonzor': {
			'user': User.objects.get(username = 'chilonzor'),
			'location': [41.2699296, 69.1693613],
			'distance': int()
		},
		'mega': {
			'user': User.objects.get(id = 1),
			'location': [41.367264, 69.2888269],
			'distance': int()
		},
	}

	locations['oybek']['distance'] = calculateDistance(client_location, locations['oybek']['location'])
	locations['chilonzor']['distance'] = calculateDistance(client_location, locations['chilonzor']['location'])
	locations['mega']['distance'] = calculateDistance(client_location, locations['mega']['location'])

	best_location = min(locations['oybek']['distance'], locations['chilonzor']['distance'], locations['mega']['distance'])

	if best_location == locations['oybek']['distance']:
		return locations['oybek']['user']
	elif best_location == locations['chilonzor']['distance']:
		return locations['chilonzor']['user']
	else:
		return locations['mega']['user']