#!/usr/bin/env python

import sys, time, os, atexit
from modules.daemon import Daemon
import peewee
from peewee import *
import datetime
import orderd.logger
from orderd.logger import log

from coindb.coindb import *
from orderd.order_book import OrderBook



# All bitcoin values are in Satoshi i.e. divide by 100.000.000 to get the amount in BTC
# Each Litecoin is subdivided into 100,000,000 smaller units, defined by eight decimal places

#db = MySQLDatabase(DBDB,host=DBHOST, user=DBUSER,passwd=DBPWD)

class OrderDaemon(Daemon):

	def run(self):
		# set up db
		dname = 'BTCLTC_ML'
		
		SRC_CRY = 'BTC'
		TRG_CRY = 'LTC'
		
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
			# get active orders from db
			#db.set_autocommit(False)
			db.set_autocommit(True)
			
			#TIMESTAMP = '2013-10-16 00:00:00'
			TIMESTAMP = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			log.debug('TIME ' + str(TIMESTAMP))
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
					# (Order.source == SRC_CRY) | (Order.source == TRG_CRY) &
					(Order.status >= Order.STATUS_ACTIVE)
					& (Order.status < Order.STATUS_FILLED)
					& (TIMESTAMP < Order.valid_until))
				.order_by(Order.price_ask.asc(),Order.created.desc())
			#	.for_update(True) ## maybe add nowait?
				) 
			
			
			######################
			# set canceled orders to topay
			pay_canceled_orders = (Order
				.update(
					status=Order.STATUS_TOPAY)
				.where(
					(Order.status == Order.STATUS_CANCELED) 
					)
				) 
			
			
			###############################################
			## set canceled order to TOPAY
			no_canceled = pay_canceled_orders.execute()
			log.debug('paying canceled order: ' + str(no_canceled))
			
			###############################################
			## get the order book and init class
			active_orders.execute()
			ob = OrderBook(active_orders)
			ob.show_order_book('screen')
			
			if ob.size == 0:
				log.debug('empty orderbook')
				time.sleep(10)
				continue
			else:
				log.debug('Orderbook size: '+str(ob.size))
			###############################################
			# discover price
			# if the orderbook matching has been down this will be an open price scenario			
			#ob.show_order_book('screen')
			market_price = ob.discover_price()
			
			if market_price == 0:
				log.debug('There are only market order.')
				time.sleep(10)
				continue
			elif market_price == None:
				log.debug('settle valid transactions first.')
			
			ob.settle_orderbook()
			
			#___________________________________
			# looping using a generator
			#ob.loop_orders()
			#c = ob.get_next()
			#print next(c).send_to_address
			#print next(c).send_to_address

			#sys.exit('stop')
			pass
			#____TODO____
			# before writing check if there is a new cancel status
			
			###############################################
			## DB LOCKING TESTS
			#log.debug('created query')
			#time.sleep(20)
			#log.debug('executing')
			#active_orders.execute()
			#time.sleep(20)
			#log.debug('committing')
			#db.commit()
			#log.debug('after commi')
			#time.sleep(100000)
			
			###############################################
			# testing updateing data in a tuple/row
			#x = ob.update_status('999')
			#print x
			#ob.show_order_book('raw')			
			
			log.debug('done settleing')
			time.sleep(10)

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
