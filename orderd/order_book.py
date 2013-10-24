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
	def __init__(self, data=''):
		if data != '':
			self.orderbook = data
			log.debug('init with orderbook data')
		else:
			self.orderbook = ''
			log.debug('init with empty orderbook')
	
	def settle_order(self, address):
		self.address = address
		log.debug('Settling order  ' + address)
		pass
	
	def settle_orders(self):
		pass
		for left in self.orderbook:
			self.settle_order(left.send_to_address)

	
	def show_order_book(self):
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
