class Customer:
	def __init__(self, email, phone):
		self.email = email
		self.phone = phone

	def place_order(self):
		# some code that provides order_id from the transaction
		print('Order placed')
		# return order_id
	
	def cancel_order(self, order_id):
		# some code that uses order_id to cancel the transaction
		print('Order cancelled')

cust1 = Customer('lara@company.com',  '614-555-0177')
cust2 = Customer('tess@company.com',  '602-555-0191')
cust3 = Customer('dave@company.com',  '317-555-0188')

# cust1 wants to place order
order_id_cust1 = cust1.place_order()

# cust2 places order for 3 meals
order_id_cust2 = cust2.place_order()

# cust1 notices and finds her favourite dish in cust2’s order and cancels her own order
cust1.cancel_order(order_id_cust1)
