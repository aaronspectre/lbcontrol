html_cards = document.getElementsByClassName('cashbox-card')
cards = Array()

for (var i = 1; i < html_cards.length; i++) {
	cards[i] = html_cards[i]
}



function filter_analyse(){
	current_filter = document.getElementById('analysisfilter').value
	if (current_filter == 'All'){
		for (var i = 1; i < cards.length; i++) {
			cards[i].style.display = 'block'
		}
		return
	}


	current_filter = 'cashbox-card-'+current_filter.toLowerCase()

	for (var i = 1; i < cards.length; i++) {
		if (cards[i].classList.contains(current_filter)) {
			cards[i].style.display = 'block'
			continue
		}
		cards[i].style.display = 'none'
	}
}



function filter_source(){
	current_filter = document.getElementById('analysisfiltersource').value
	if (current_filter == 'All'){
		for (var i = 1; i < cards.length; i++) {
			cards[i].style.display = 'block'
		}
		return
	}

	current_filter = 'cashbox-card-'+current_filter.toLowerCase()

	for (var i = 1; i < cards.length; i++) {
		if (cards[i].classList.contains(current_filter)) {
			cards[i].style.display = 'block'
			continue
		}
		cards[i].style.display = 'none'
	}
}



function drawGraph(daysSet, dailyOrders, dailyPrice, dailyBotOrders, dailyBotPrice, dailyCashboxOrders, dailyCashboxPrice){
	daysSet = JSON.parse(daysSet)
	dailyOrders = JSON.parse(dailyOrders)
	dailyPrice = JSON.parse(dailyPrice)
	dailyBotOrders = JSON.parse(dailyBotOrders)
	dailyBotPrice = JSON.parse(dailyBotPrice)
	dailyCashboxOrders = JSON.parse(dailyCashboxOrders)
	dailyCashboxPrice = JSON.parse(dailyCashboxPrice)
	dailyPrice.reverse()
	daysSet.reverse()
	dailyOrders.reverse()
	dailyBotOrders.reverse()
	dailyCashboxOrders.reverse()
	dailyCashboxPrice.reverse()
	dailyBotPrice.reverse()



	var dailyOrdersOptions = {
		chart: {
			type: 'line',
			zoom: {
				enabled: false
			}
		},
		grid: {
			row: {
				colors: ['#f3f3f3', 'transparent'],
				opacity: 0.5
			}
		},
		markers: {
			size: 5
		},
		title: {
			text: 'Daily Orders Report',
			align: 'left'
		},
		series: [{
			name: 'Orders',
			data: dailyOrders
		}],
		xaxis: {
			categories: daysSet
		}
	}

	var dailyPriceOptions = {
		chart: {
			type: 'line',
			zoom: {
				enabled: false
			}
		},
		grid: {
			row: {
				colors: ['#f3f3f3', 'transparent'],
				opacity: 0.5
			}
		},
		markers: {
			size: 5
		},
		title: {
			text: 'Daily Income Report',
			align: 'left'
		},
		series: [{
			name: 'Income',
			data: dailyPrice
		}],
		xaxis: {
			categories: daysSet
		}
	}

	var dailyBotCashboxOrdersChart = {
		chart: {
			type: 'line',
			zoom: {
				enabled: false
			}
		},
		grid: {
			row: {
				colors: ['#f3f3f3', 'transparent'],
				opacity: 0.5
			}
		},
		markers: {
			size: 5
		},
		title: {
			text: 'Daily Cashbox|Bot Orders Report',
			align: 'left'
		},
		series: [
		{
			name: 'Bot',
			data: dailyBotOrders
		},
		{
			name: 'Cashbox',
			data: dailyCashboxOrders
		}],
		xaxis: {
			categories: daysSet
		}
	}

	var dailyBotCashboxPriceChart = {
		chart: {
			type: 'line',
			zoom: {
				enabled: false
			}
		},
		grid: {
			row: {
				colors: ['#f3f3f3', 'transparent'],
				opacity: 0.5
			}
		},
		markers: {
			size: 5
		},
		title: {
			text: 'Daily Cashbox|Bot Income Report',
			align: 'left'
		},
		series: [{
			name: 'Bot',
			data: dailyBotPrice
		},
		{
			name: 'Cashbox',
			data: dailyCashboxPrice
		}
		],
		xaxis: {
			categories: daysSet
		}
	}

	var dailyOrdersChart = new ApexCharts(document.querySelector("#dailyOrdersChart"), dailyOrdersOptions);
	var dailyPriceChart = new ApexCharts(document.querySelector("#dailyPriceChart"), dailyPriceOptions);
	var dailyBotCashboxOrders = new ApexCharts(document.querySelector("#dailyBotCashboxOrders"), dailyBotCashboxOrdersChart);
	var dailyBotCashboxPrice = new ApexCharts(document.querySelector("#dailyBotCashboxPrice"), dailyBotCashboxPriceChart);

	dailyOrdersChart.render();
	dailyPriceChart.render();
	dailyBotCashboxOrders.render();
	dailyBotCashboxPrice.render();
}