import peewee
from peewee import *


DEBUG = True



db = MySQLDatabase(None)
class COINModel(Model): 
    class Meta:
        database = db

	
class Order(COINModel):
    class Meta:
        db_table = 'orders'

##    CREATE TABLE `order` (
##  `address` varchar(40) NOT NULL DEFAULT '',
##  `btc_address` varchar(40) DEFAULT NULL,
##  `ltc_address` varchar(40) DEFAULT NULL,
##  `order_created` timestamp NULL DEFAULT '0000-00-00 00:00:00',
##  `order_type` varchar(1) DEFAULT NULL,
##  `price` bigint(11) DEFAULT NULL,
##  `amount` bigint(20) DEFAULT NULL,
##  `amount_settled` bigint(20) DEFAULT NULL,
##  `valid_until` timestamp NULL DEFAULT '0000-00-00 00:00:00',
##  `confirmations` int(11) DEFAULT NULL,
##  PRIMARY KEY (`address`)
## ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
## CREATE INDEX created ON btcltc (order_created);
## CREATE VIEW orders AS SELECT * FROM btcltc WHERE confirmations > '5';

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
    price_ask = DecimalField(default=0)
    price_bought = DecimalField(default=0)
    amount_ask = BigIntegerField(default=0)
    amount_bought = BigIntegerField(default=0)
    amount_send = BigIntegerField(default=0)
    tid_send = CharField(max_length=40, default="") 
    valid_until = DateTimeField(default='0000-00-00 00:00:00')
    confirmations = IntegerField(default=0)
    

    # status values
    STATUS_POOL_FREE = 0
    STATUS_PREORDER = 100
    STATUS_ACTIVE = 200
    STATUS_FILLED = 300
    STATUS_CANCELED = 333
    STATUS_TOPAY = 400
    STATUS_PAYED = 500
    STATUS_CONFIRMED = 550
    STATUS_DELETE = 999
    

