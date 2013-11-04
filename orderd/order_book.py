#!/usr/bin/env python

from logger import log

#################################################
# Order matching class
#################################################
## TODO
## - get orders
## - instanziate an Orders objects, which takes the db object
##	 and has the methods
##	 creates a shallow copy via [:]
##		show() ...	returns the current order table in pretty format
##					may take an argument for various display formatting, i.e 'sql', 'screen'
##		match()		does a round of matching
##					may return a list of modified orders as a list of addresses
##					OR
##					iterative starting at top
##						checking for next order with status <300/200 = active or partially filled
##						try match && match
##


class OrderBook(list):
	__last_transactions = []	# list of last transactions
	__last_price = ''			# price of last transaction
	__last_limit = ''			# last discovered limit price -- see VoodooPad
	__last_prices = []		# list of last prices for last transactions
	
	def __init__(self, data=''):
		if data != '':
			self.orderbook = data[:] # shallow copy required to have a proper lsit o dicts
			log.debug('init with sliced orderbook data')
		else:
			self.orderbook = ''
			log.debug('init with empty orderbook')
		self.size = len(self.orderbook)	
#________________________________________________________________________
	def discover_price(self):
		def highest_buy():
			pass
			self.high = 0
			for order in self.orderbook:
				if order.source == 'BTC' and order.price_ask > self.high:
					self.high = order.price_ask
			if self.high == 0:
				return None
			else:
				return self.high
			
		def lowest_sell(): 
			pass # due to the way the list is pre sorted it would be sufficient to use the first 
			pass # right side price > 0 as it will be the lowest
			self.low = 0
			self.sell = []
			for order in self.orderbook:
				if order.source == 'LTC' and order.price_ask > 0:
					# print order.source, order.price_ask
					self.sell.append(order.price_ask)
			if self.sell != []:
				return min(self.sell)
			else: return None
		#_____TODO_____
		# take into account that either or both could be yero as there are no limit orders
		# rules
		# if either side has no highest buy or lowest bid then the other side is the market price
		# if on both side values are zero ... then we have to wait for a limit order to start filling
		
		log.debug('Discover price ...')
		self.left_price = highest_buy()
		self.right_price = lowest_sell()
		log.debug('HIGHEST BUY: ' + str(self.left_price))
		log.debug('LOWEST SELL: ' + str(self.right_price))
		
		if self.left_price == None and self.right_price == None:
			# we only have market orders. stop processing the orderbook. wait for next limit order
			self.market_price = 0
		
		elif self.left_price == None:
			# left side has only market orders
			self.market_price = self.right_price
			
		elif self.right_price == None:
			# right side has only market orders
			self.market_price = self.left_price
				
		elif self.left_price == self.right_price:
			self.market_price = self.left_price
			log.debug('there is a market price based on orders' + str(left))
			
		elif self.left_price < self.right_price:
			self.market_price = (self.left_price + self.right_price)/2
			log.debug('there is a averaged market price: ' + str(self.market_price))
			
		elif self.left_price > self.right_price:
			log.debug('there are valid transactions to be executed first')
			## TODO
			## calculate market price based on balanceing the order book
			pass
			log.debug('build func to establish market price')
			self.market_price = None
			
		log.debug('MARKET PRICE: ' + str(self.market_price))	
		return self.market_price

#________________________________________________________________________
	def get_recent_transactions(self):
		"Return the transactions of this round of settling"
		pass

	def get_recent_prices():
		"Return the prices from the last round of settling"
		pass
		
	def get_last_price(self):
		print self.__last_price
		pass

	def clean_up(self):
		#_____TODO_____
		# when an interrupt is captured this function is to be called
		# revert orderbook to last state .. ie do not write back changes
		# close db
		# probably better located in daemon
		pass
		
#________________________________________________________________________
	def settle_orderbook(self):
		self.left = self.orderbook[:]
		# shallow copy of the orderbook so we can use pop
		while self.left != []:
			self.next_order = self.left.pop(0)
			log.debug('trying to settle next LEFT order:  ' + self.next_order.send_to_address[0:8] + ' ' + self.next_order.source + ' ' + str(self.next_order.status) + '-'*28)
			if self.next_order.status >= '300':
				continue
			else:
				for right in self.left:
					#_____TODO_____
					# replace hard coded values with STATUS_... ie Order.STATUS_TOPAY ...
					if (self.next_order.source == right.source):
						# opposite currency pairs only
						continue
					if self.next_order.status >= 300 or self.next_order.status < 200:
						# ignore the ones settled already
						continue
					if right.status >= 300 or right.status < 200:
						continue
					self.settle_order(self.next_order,right)


#________________________________________________________________________
	def settle_order(self, left_order, right_order):
		self.left_order = left_order
		self.right_order = right_order
		self.left_mo = '   '
		self.right_mo = '   '
		
		if left_order.amount_ask == 0:
			self.left_mo = ' MO'
			
		if right_order.amount_ask == 0:
			self.right_mo = ' MO'
			
		log.debug('trying to settle next RIGHT order: ' 
			+ self.left_order.send_to_address[0:8] + ' '
			+ self.left_order.source + ' '
			+ str(self.left_order.status) + ' '
			+ self.left_mo
			+ ' :: ' 
			+ self.right_order.send_to_address[0:8] + ' '
			+ self.right_order.source + ' '
			+ str(self.right_order.status)
			+ self.right_mo)
		
		
		
#________________________________________________________________________
	def show_order_book(self, type):
		self.type = type
		if type == 'screen':
			print '   ADDRESS  SRC TRG TYP STAT    AMT             AMT_ASK    AMT_FILLED   PRICE'
			for order in self.orderbook:
				print ('>> {0} {1} {2} {3} {4:4d} {5:13d} {6:13d} {7:13d} @ {8:4.5f}'.format(
					order.send_to_address[0:8],
					order.source,
					order.target,
					str(order.order_type).zfill(2),
					order.status,
					order.amount,
					order.amount_ask,
					order.amount_settled,
					order.price_ask))
		elif type == 'raw':
			for order in self.orderbook:
				print (
					order.send_to_address,
					order.source,
					order.target,
					order.order_type,
					order.status,
					order.amount,
					order.amount_ask,
					order.amount_settled,
					order.price_ask)
	
################################################
# Test functions ... remove when no longer required as a reference
	def update_status(self, status):
		pass
		self.new_status = status
		print "NEW STATUS: ", self.new_status
		# get first order
		self.addr = self.orderbook[0].send_to_address
		self.status = self.orderbook[0].status
		#print __print_order(self.order)
		print "Address: ", self.addr[0:6]," Status: ",self.status
		self.orderbook[0].status = self.new_status
		self.status = self.orderbook[0].status
		print "Address: ", self.addr[0:6]," Status: ",self.status

#________________________________________________________________________
	def get_next_order(self):
		# generator to loop over the orderbook, one by one
		for next in self.orderbook:
			yield next
			
#________________________________________________________________________
	def loop_orders(self):
		# using an generator to loop over the orders
		self.c = self.get_next_order()
		while True:
			try:
				print next(self.c).send_to_address[0:8]
			except StopIteration:
				break