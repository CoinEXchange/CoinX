#!/usr/bin/env python

import sys, time, os, atexit, logging
import logging.handlers
from daemon import Daemon
import peewee
from peewee import *
import datetime

DEBUG = True

# config
COIN_MIN_FREEPOOL = 10
SMULT = 100000000
MINAMNT = 0.01
FEEPERCT = 0.2
TRANSFEE = 10000
DBHOST = '192.168.1.22'
#DBHOST = 'dontoc.dlinkddns.com'
LAST_PRICE = 0.0133

# All bitcoin values are in Satoshi i.e. divide by 100000000 to get the amount in BTC
# Each Litecoin is subdivided into 100,000,000 smaller units, defined by eight decimal places

db = MySQLDatabase('btcltc_ML',host=DBHOST, user='jack',passwd='hammer')

class BTCModel(Model): 
    class Meta:
        database = db

	
class Order(BTCModel):
    class Meta:
        db_table = 'orders'

    send_to_address = CharField(primary_key=True,max_length=40)
    sender_address = CharField(max_length=40, default="")
    receiver_address = CharField(max_length=40, default="")
    created = DateTimeField(default='0000-00-00 00:00:00')
    active = DateTimeField(default='0000-00-00 00:00:00')
    last_update = DateTimeField(default='0000-00-00 00:00:00')
    order_type = IntegerField(default=0)
    status = IntegerField(default=0)
    source = CharField(max_length=3, default='   ')
    target = CharField(max_length=3, default='   ')
    amount = BigIntegerField(default=0)
    amount_settled = BigIntegerField(default=0)
    amount_ask = BigIntegerField(default=0)
    price = DoubleField(default=0)
    amount_bought = BigIntegerField(default=0)
    amount_send = BigIntegerField(default=0)
    tid_send = CharField(max_length=40, default="") 
    valid_until = DateTimeField(default='0000-00-00 00:00:00')
    confirmations = IntegerField(default=0)
    

    # status values
    #STATUS_POOL_FREE = 0
    #STATUS_PREORDER = 100
    STATUS_ACTIVE = 200
    STATUS_PART_SETTLED = 250
    STATUS_SETTLED = 300
    STATUS_TOPAY = 400
    #STATUS_PAYED = 500
    #STATUS_CONFIRMED = 550
    #STATUS_DELETE = 999


class OrderDaemon(Daemon):
	def init(self):
	########
	# Try to connect to btcltc db
	########
		try:
			db.connect()
		except: ### access denied
			log.error('db access denied')
			exit()
		else:
			log.info('Connect DB:')
			log.debug('Connect ...')
			
	def run(self):

		def get_orders(src_cry, trg_cry):
			# either here or in the data held i need to filter/sort by price wich is an expression of amount and amount_ask
			timestamp = '2013-10-16 00:00:00'
			#log.debug('mememe')
			#timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			db.set_autocommit(False)
			#log.debug('AUTOCOMMIT ' + str(db.get_autocommit()))
			active_orders = (Order
				.select(Order.send_to_address,Order.order_type,Order.source,Order.target,Order.amount,Order.amount_settled,Order.amount_ask,Order.created,Order.price,Order.status)
				.where((Order.source == src_cry) | (Order.source == trg_cry) & (Order.status >= Order.STATUS_ACTIVE) & (Order.status < Order.STATUS_SETTLED) & (timestamp < Order.valid_until))
				.order_by(Order.price.asc(),Order.created.desc())
				.for_update(True))
			return active_orders

		def settle_orders(orders):
			# get active orders orders
			orig_orders = orders
			# convert to list
			myCopy = orig_orders[:]
			first = myCopy.pop(0)
			print "First order: " + first.send_to_address
			for x in myCopy:
				print x.send_to_address
			time.sleep(30)
			
			loop_orders = orders[:]
			for left in orig_orders:
				log.debug('LEFT:  ' + left.send_to_address + ' ' + left.source + ' ' + left.target + ' ' + str(left.order_type) + ' ' + str(left.status))
				for right in loop_orders:
					if (left.source == right.source):
						continue
					log.debug('RIGHT: ' + right.send_to_address + ' ' + right.source + ' ' + right.target + ' ' + str(right.order_type) + ' ' + str(right.status))
					break
				break
			left.status = '203'
			right.status = '204'
			time.sleep(20)

		slh=logging.handlers.SysLogHandler(address='/dev/log')
		fm=logging.Formatter('ORDERD %(levelname)s:%(message)s')
		slh.setFormatter(fm)
		log = logging.getLogger()
		logging.basicConfig(format='%(asctime)s ORDERD %(levelname)s:%(message)s')
		if DEBUG:
			log.setLevel(logging.DEBUG)
		else:
			log.setLevel(logging.INFO)
		log.addHandler(slh)
		log.debug('Start Daemon')
	
		
		while True:
			log.debug('Start loop')
			active_orders = get_orders('BTC','LTC')
			#db.set_autocommit(False)
			#log.debug('AUTOCOMMIT ' + str(db.get_autocommit()))
			settle_orders(active_orders)
			log.debug('sleep ...')
			time.sleep(20)
			log.debug('continue ...')

			
			#for sell in copy_active_orders:
			#	print "RIGHT: ", sell.send_to_address

		#log.debug('before Order.update')
		#q = Order.update(status = '201').where(Order.send_to_address == 'f30dc365715569d58d0268d8c9d3f956e7')
		#time.sleep(20)
		#log.debug('before execute')
		#q.execute()
		#time.sleep(20)
		#log.debug('before commit')
		#db.commit()
		#log.debug('after commi')
		#time.sleep(100000)

if __name__ == "__main__":
    daemon = OrderDaemon('/var/run/order_daemon.pid')
    if DEBUG:
		daemon.init()
		daemon.run()
    else:
	if len(sys.argv) == 2:
	    if 'start' == sys.argv[1]:
	        daemon.start()
	    elif 'stop' == sys.argv[1]:
	        daemon.stop()
	    elif 'restart' == sys.argv[1]:
	        daemon.restart()
	    else:
	        print "Unknown command"
	        sys.exit(2)
	        sys.exit(0)
        else:
	    print "usage: %s start|stop|restart [debug]" % sys.argv[0]
	    sys.exit(2)
