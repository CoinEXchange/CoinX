#!/usr/bin/env python

from logger import log

#################################################
# Order matching class
#################################################
## TODO
## - get orders
## - instanziate an Orders objects, which takes the db object
##   and has the methods
##   creates a shallow copy via [:]
##		show() ... 	returns the current order table in pretty format
##					may take an argument for various display formatting, i.e 'sql', 'screen'
##		match()		does a round of matching
##					may return a list of modified orders as a list of addresses
##					OR
##					iterative starting at top
##						checking for next order with status <300/200 = active or partially filled
##						try match && match
##


class OrderBook(list):
	__last_transactions = []
	__last_price = ''
	__recent_prices = []
	
	def __init__(self, data=''):
		if data != '':
			self.orderbook = data[:] # shallow copy required to have a proper lsit o dicts
			log.debug('init with sliced orderbook data')
		else:
			self.orderbook = ''
			log.debug('init with empty orderbook')

	def get_recent_transactions(self):
		pass
		
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
	def get_recent_prices():
		pass
		
	def get_last_price(self):
		print self.__last_price
		
	def settle_order(self, address):
		self.address = address
		log.debug('Settling order  ' + address)
		pass
	
	def settle_orders(self):
		pass
		for left in self.orderbook:
			self.settle_order(left.send_to_address)

	def print_order(self, order):
		self.order = order
		for v in self.order: 
			print v
			
	def show_order_book(self, type):
		self.type = type
		if type == 'screen':
			print '   ADDRESS  SRC TRG TYP STAT          AMT       AMT_ASK    AMT_FILLED   PRICE'
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
		
	def show_order_book2(self):
		print '   ADDRESS  SRC TRG TYP STAT          AMT       AMT_ASK    AMT_FILLED   PRICE'
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
