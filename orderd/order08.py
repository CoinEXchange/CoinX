#!/usr/bin/env python

import sys, time, os, atexit
#import logging
#import logging.handlers
from daemon import Daemon
import peewee
from peewee import *
import datetime
import logger
from logger import log
# read configuration values from module
import conf
from conf import *
from order_db import *
#from order_db import Order


# All bitcoin values are in Satoshi i.e. divide by 100.000.000 to get the amount in BTC
# Each Litecoin is subdivided into 100,000,000 smaller units, defined by eight decimal places

#db = MySQLDatabase(DBDB,host=DBHOST, user=DBUSER,passwd=DBPWD)




class OrderDaemon(Daemon):
	def run(self):
		# set up db
		print "DBHOST ",DBHOST
		timestamp = '2013-10-16 00:00:00'
		src_cry = 'BTC'
		trg_cry = 'LTC'
		
		active_orders = (Order
			.select(Order.send_to_address,Order.order_type,Order.source,Order.target,Order.amount,Order.amount_settled,Order.amount_ask,Order.created,Order.price,Order.status)
			.where((Order.source == src_cry) | (Order.source == trg_cry) & (Order.status >= STATUS_ACTIVE) & (Order.status < STATUS_SETTLED) & (timestamp < Order.valid_until))
			.order_by(Order.price.asc(),Order.created.desc())
			.for_update(True))
		active_orders.execute()

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
		for row in active_orders:
			#print row
			print ('>> {0} {1} {2} {3} {4:4d} {5:13d} {6:13d} {7:13d} @ {8:4.5f}'.format(
				row.send_to_address[0:8],
				row.source,
				row.target,
				str(row.order_type).zfill(2),
				row.status,
				row.amount,
				row.amount_ask,
				row.amount_settled,
				row.price))
		
		
		
		
		while True:
			log.debug('running ...D')
			log.info('running ...I')
			time.sleep(2)



#####################################################
if __name__ == "__main__":

	logger.set_logging(DEBUG)	
	daemon = OrderDaemon('/home/markus/order_daemon.pid')
	
	if len(sys.argv) == 3 and 'debug' == sys.argv[2]:
		logger.set_logging(True)
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
