from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from bot.models import Order

import json
from . import report

def auth(request):
	if request.user.is_anonymous:
		return render(request, 'auth.html')
	else:
		return HttpResponseRedirect(reverse('dashboard', args = ('pending',)))


def signIn(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(request, username = username, password = password)

	if user is not None:
		login(request, user)
		return HttpResponseRedirect(reverse('dashboard', args = ('pending',)))

	else:
		return HttpResponseRedirect(reverse('auth'))



@login_required
def signout(request):
	logout(request)
	return HttpResponseRedirect(reverse('auth'))



@login_required
def dashboard(request, status):

	date = timezone.now().date()

	if request.user.username == 'watcher':
		orders = Order.objects.filter(
			status = status,
			date__year = date.year,
			date__month = date.month,
			date__day = date.day
		)
		return render(request, 'dashboard.html', {'orders': orders})

	if status == 'left':
		orders = Order.objects.filter(status = 'pending', executor = request.user).exclude(
			date__year = date.year, date__month = date.month,
			date__day = date.day
		)
		return render(request, 'dashboard.html', {'orders': orders})


	orders = Order.objects.filter(
		status = status,
		executor = request.user,
		date__year = date.year,
		date__month = date.month,
		date__day = date.day
	)
	return render(request, 'dashboard.html', {'orders': orders})



@login_required
def analysis(request):

	if request.user.is_superuser == False:
		return HttpResponseRedirect(reverse('dashboard', args = ('pending',)))


	date = timezone.now().date()
	orders = Order.objects.filter(date__year = date.year, date__month = date.month, date__day = date.day).order_by('-date')

	orderSet = Order.objects.filter(date__year = date.year,
		date__month = date.month,
		date__day__in = [date.day - v for v in range(6)]
	).order_by('-date')


	return render(request, 'analysis.html', {'orders': orders, 'orderAnalysis': makeDailyData(orders), 'graphData': makeGraphData(orderSet)})




@login_required
def getAnalysisReport(request):

	if request.user.is_superuser == False:
		return HttpResponseRedirect(reverse('dashboard', args = ('pending',)))

	date = timezone.now().date()
	orders = Order.objects.filter(date__year = date.year, date__month = date.month, date__day = date.day).order_by('-date')
	data = makeDailyData(orders)
	report.updateReport(data)

	return HttpResponseRedirect(reverse('analysis'))



@login_required
def orderValidation(request, id, action):
	order = get_object_or_404(Order, id = id)

	if action == 'reject':
		order.status = 'reject'
		order.save()
		return HttpResponseRedirect(reverse('dashboard', args = ('pending',)))



	if order.status == 'pending' and order.source == 'robot':
		order.status = 'delivery'
	elif order.status == 'pending' and order.source == 'cash-register':
		order.status = 'done'
	elif order.status == 'delivery':
		order.status = 'done'

	order.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def addOrder(request):
	return render(request, 'add-order.html')


@login_required
def addOrderHandle(request):
	order = Order()

	order.order = request.POST['order'].split('|')
	order.order.pop()
	order.order = json.dumps(order.order)

	order.price = request.POST['price']
	order.date = timezone.now()
	order.customer_name = request.POST['cname']
	order.customer_phone = request.POST['cphone']
	order.executor = request.user

	order.save()

	if len(order.customer_name) == 0:
		order.customer_name = f'Customer {order.id}'
		order.save()


	return HttpResponseRedirect(reverse('dashboard', args = ('pending',)))





def makeDailyData(orderSet):
	orderAnalysis = dict()
	orderAnalysis['orderAmount'] = orderSet.count()
	orderAnalysis['orderRejectedAmount'] = int()
	orderAnalysis['orderRejectedSum'] = int()
	orderAnalysis['orderTotalSum'] = int()
	orderAnalysis['orderSum'] = int()
	orderAnalysis['orderBotAmount'] = int()
	orderAnalysis['orderBotSum'] = int()
	orderAnalysis['orderCashboxAmount'] = int()
	orderAnalysis['orderCashboxSum'] = int()
	orderAnalysis['orderDone'] = int()

	for order in orderSet:
		orderAnalysis['orderTotalSum'] += order.price
		if order.status == 'done':
			orderAnalysis['orderSum'] += order.price
			orderAnalysis['orderDone'] += 1

			if order.source == 'robot':
				orderAnalysis['orderBotAmount'] += 1
				orderAnalysis['orderBotSum'] += order.price
			else:
				orderAnalysis['orderCashboxSum'] += order.price
				orderAnalysis['orderCashboxAmount'] += 1

		elif order.status == 'reject':
			orderAnalysis['orderRejectedAmount'] += 1
			orderAnalysis['orderRejectedSum'] += order.price


	orderAnalysis['orderProfit'] = orderAnalysis['orderSum'] / 2

	return orderAnalysis



def makeGraphData(orderSet):
	dataOrders = dict()
	dataPrice = dict()
	dataBotOrders = dict()
	dataBotPrice = dict()
	dataCashboxOrders = dict()
	dataCashboxPrice = dict()

	for order in orderSet:
		dataOrders[order.date.date().day] = 0
		dataPrice[order.date.date().day] = 0
		dataCashboxOrders[order.date.date().day] = 0
		dataCashboxPrice[order.date.date().day] = 0
		dataBotOrders[order.date.date().day] = 0
		dataBotPrice[order.date.date().day] = 0


	for order in orderSet:
		if order.status == 'done':
			dataOrders[order.date.date().day] += 1
			dataPrice[order.date.date().day] += order.price

			if order.source == 'robot':
				dataBotOrders[order.date.date().day] += 1
				dataBotPrice[order.date.date().day] += order.price
			else:
				dataCashboxOrders[order.date.date().day] += 1
				dataCashboxPrice[order.date.date().day] += order.price


	return {'days': list(dataOrders.keys()),
		'orders': list(dataOrders.values()),
		'price': list(dataPrice.values()),
		'botOrders': list(dataBotOrders.values()),
		'botPrice': list(dataBotPrice.values()),
		'cashboxOrders': list(dataCashboxOrders.values()),
		'cashboxPrice': list(dataCashboxPrice.values())
	}