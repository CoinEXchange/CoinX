#!/usr/bin/env python

import sys, time, os, atexit
#import logging
#import logging.handlers
from modules.daemon import Daemon
import peewee
from peewee import *
import datetime
import orderd.logger
from orderd.logger import log
# read configuration values from module
#import orderd.conf
#from orderd.conf import *
from coindb.coindb import *
from orderd.order_book import OrderBook, OrderBookDicts
#from orderd.order_db import *
#from order_db import Order


# All bitcoin values are in Satoshi i.e. divide by 100.000.000 to get the amount in BTC
# Each Litecoin is subdivided into 100,000,000 smaller units, defined by eight decimal places

#db = MySQLDatabase(DBDB,host=DBHOST, user=DBUSER,passwd=DBPWD)

class OrderDaemon(Daemon):

	def run(self):
		# set up db
		dname = 'btcltc_ML'
		TIMESTAMP = '2013-10-16 00:00:00'
		SRC_CRY = 'BTC'
		TRG_CRY = 'LTC'
		
		
		def discover_price():
			## ?? market orders are removed. shold other order types be removed for price discovery
			highest_buy = (Order
				.select(fn.max(Order.price_ask)) # highest bid
				.where(
					(Order.source == SRC_CRY) # left side
					& (Order.status >= Order.STATUS_ACTIVE) 
					& (Order.status < Order.STATUS_FILLED)
					& (TIMESTAMP < Order.valid_until)
					& (Order.price_ask > 0))
				.scalar()) 

			lowest_sell = (Order
				.select(fn.min(Order.price_ask)) # lowest offer
				.where(
					(Order.target == SRC_CRY) # right side
					& (Order.status >= Order.STATUS_ACTIVE) 
					& (Order.status < Order.STATUS_FILLED)
					& (TIMESTAMP < Order.valid_until)
					& (Order.price_ask > 0))
				.scalar()) 

			left = highest_buy
			right = lowest_sell

			log.debug ('HIGHEST BUY: ' + str(left))
			log.debug ('LOWEST SELL: ' + str(right))

			if left == right:
				market_price = left
				log.debug('there is a market price based on orders' + str(left))
			elif left < right:
				market_price = (left + right)/2
				log.debug('there is a averaged market price' + str(market_price))
			elif left > right:
				log.debug('there are valid transactions to be executed first')
				## TODO
				## calculate market price based on balanceing the order book
				market_price = None

			return market_price

		db.init(dname,host='192.168.1.22', user='jack',passwd='hammer')
		try:
			db.connect()
		except: ### access denied
			log.error('db %s access denied' % dname)
			exit()
		else:
			log.info('Connect DB: %s' % dname)
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

		
		while True:
			######################
			# insert db query to get last price
			# from the last filled or part filled - potentially use price_bought db field
			# if none found get .... see voodoopad
			x = discover_price()
			print "Price ", x

			
			
			######################
			# get active orders
			db.set_autocommit(False)
			
			active_orders = (Order
				.select(
					Order.send_to_address,
					Order.order_type,
					Order.source,
					Order.target,
					Order.amount,
					Order.amount_settled,
					Order.amount_ask,
					Order.created,
					Order.price_ask,
					Order.status)
				.where(
					(Order.source == SRC_CRY) | (Order.source == TRG_CRY) 
					& (Order.status >= Order.STATUS_ACTIVE) 
					& (Order.status < Order.STATUS_FILLED) 
					& (TIMESTAMP < Order.valid_until))
				.order_by(Order.price_ask.asc(),Order.created.desc())
				.for_update(True) ## maybe add nowait?
				) 
			active_orders.execute()
			
			active_orders_dicts = (Order
				.select(
					Order.send_to_address,
					Order.order_type,
					Order.source,
					Order.target,
					Order.amount,
					Order.amount_settled,
					Order.amount_ask,
					Order.created,
					Order.price_ask,
					Order.status)
				.where(
					(Order.source == SRC_CRY) | (Order.source == TRG_CRY) 
					& (Order.status >= Order.STATUS_ACTIVE) 
					& (Order.status < Order.STATUS_FILLED) 
					& (TIMESTAMP < Order.valid_until))
				.order_by(Order.price_ask.asc(),Order.created.desc())
				.for_update(True) ## maybe add nowait?
				.dicts()
				) 
			active_orders_dicts.execute()
			
			orderbook = OrderBookDicts(active_orders_dicts)
			#orderbook.show_order_dicts()
			
			#sys.exit('stop')
			
			#x = orderbook.get_fok()
			#print "row",x
			
			#orderbook = OrderBook(active_orders)
			#log.debug('showing the orderbook')
			y = orderbook.lookup_ob(status='200')
			print "BTC ", y
			#x = orderbook.settle_orders()
			#print x
			#orderbook.show_order_book()
			sys.exit('stop')
			
			#log.debug('created query')
			#time.sleep(20)
			#log.debug('executing')
			#active_orders.execute()
			#time.sleep(20)
			#log.debug('committing')
			#db.commit()
			#log.debug('after commi')
			#time.sleep(100000)
			
			
			
			log.debug('running ...D')

			time.sleep(10)
			log.info('running ...I')


#####################################################
if __name__ == "__main__":

	orderd.logger.set_logging(DEBUG)	
	daemon = OrderDaemon('/home/markus/order_daemon.pid')
	
	if len(sys.argv) == 3 and 'debug' == sys.argv[2]:
		orderd.logger.set_logging(True)
		log.debug('Running in debug mode ...')
		daemon.run()

	if 'start' == sys.argv[1]:
		log.info('Starting ...')
		daemon.start()
	elif 'stop' == sys.argv[1]:
		log.info('Stopping ...')
		daemon.stop()
	elif 'restart' == sys.argv[1]:
		daemon.restart()
	else:
		print "usage: %s start|stop|restart [debug]" % sys.argv[0]
		sys.exit(2)
		sys.exit(0)
