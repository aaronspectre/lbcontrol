
price = document.getElementById('price')
amount = document.getElementById('amount')
order_list = document.getElementById('order_list')
product_list = document.getElementById('product_list')
order = document.getElementById('order')

action_button = document.getElementById('send-order')
action_button.disabled = true
console.log(action_button)


price_list = {
	'Corndog': 9000,
	'Corndog with Cheese': 12000,
}

function add_order(){
	if (amount.value < 0 || amount.value == 0){
		alert('Please Check Amount')
		return
	}
	let bill = product_list.value+' x'+amount.value
	let node = document.createElement('span')
	let node_text = document.createTextNode(bill)
	node.appendChild(node_text)
	node.classList.add('badge')

	order_list.appendChild(node)
	order.value += bill+'|'
	price.value = Number(price.value)+(Number(price_list[product_list.value]) * Number(amount.value))

	amount.value = '1'
	action_button.disabled = false
}