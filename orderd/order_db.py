#!/usr/bin/env python

import peewee
from peewee import *
import datetime


# All bitcoin values are in Satoshi i.e. divide by 100000000 to get the amount in BTC
# Each Litecoin is subdivided into 100,000,000 smaller units, defined by eight decimal places

#db = MySQLDatabase('btcltc_ML', host=DBHOST, user='jack', passwd='hammer')
db = MySQLDatabase('btcltc_ML', host='192.168.1.22', user='jack', passwd='hammer')
#db = MySQLDatabase('btcltc_ML', host='192.168.1.22', user='jack', passwd='hammer')
#deferred_db = MySQLDatabase(None)

class BTCModel(Model): 
	class Meta:
		database = db
		#database = deferred_db



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
	source = CharField(max_length=3, default='	 ')
	target = CharField(max_length=3, default='	 ')
	amount = BigIntegerField(default=0)
	amount_settled = BigIntegerField(default=0)
	amount_ask = BigIntegerField(default=0)
	price = DoubleField(default=0)
	amount_bought = BigIntegerField(default=0)
	amount_send = BigIntegerField(default=0)
	tid_send = CharField(max_length=40, default="") 
	valid_until = DateTimeField(default='0000-00-00 00:00:00')
	confirmations = IntegerField(default=0)
	
