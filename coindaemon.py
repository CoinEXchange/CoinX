import sys, datetime, time, os, atexit, logging
import logging.handlers
from daemon import Daemon
import bitcoinrpc
from bitcoinrpc.exceptions import InsufficientFunds
from bitcoinrpc.config import read_default_config
from bitcoinrpc.connection import BitcoinConnection
import litecoinrpc
from litecoinrpc.connection import LitecoinConnection
import peewee
from peewee import *
from fixedpoint import FixedPoint

DEBUG = True



db = MySQLDatabase(None)
class COINModel(Model): 
    class Meta:
        database = db

	
class Order(COINModel):
    class Meta:
        db_table = 'order'

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
    STATUS_SETTLED = 300
    STATUS_TOPAY = 400
    STATUS_PAYED = 500
    STATUS_CONFIRMED = 550
    STATUS_DELETE = 999
    

class COINDaemon(Daemon):
    # config
    COIN_MIN_FREEPOOL = 10
    SMULT = FixedPoint('100000000',8)
    MINAMNT = FixedPoint('0.01',8)
    FEEPERCT = FixedPoint('0.2',8)
    TRANSFEE = FixedPoint('10000',8)


    def __init__(self, pidfile='', scur='', tcur='',XYZcoinConnection=BitcoinConnection):
	self.scur = scur
	self.tcur = tcur
        self.XYZcoinConnection = XYZcoinConnection
        Daemon.__init__(self, pidfile)


    def run(self):

        def check_address_pool(db,coin):
	    log.debug('checking address pool')
	    pool_free = Order.select().where((Order.status == Order.STATUS_POOL_FREE) & (Order.source == self.scur)).count()
	    #pool_free = pool.count()
	    log.info('%s free addresses found' % pool_free)
	    if pool_free < COIN_MIN_FREEPOOL:
	        for n in range(10):### variable amount
		    newadr = coin.getnewaddress()
		    st = coin.setaccount(newadr,'work')### exception...no address left????
		    try:
		        Order.create(send_to_address=newadr,source='self.scur')
		    except: # Duplicate entry: # duplicate prim key - simply get another address
			newadr = coin.getnewaddress()
			st = coin.setaccount(newadr,'work')### exception...no address left????
		        Order.create(send_to_address=newadr,source='self.scur')
		    coin.keypoolrefill()
	    
        def init():
	    config = read_default_config()
	    log.debug('config: %s' % config)

	    ########
	    #
	    # Try to connect to scur Daemon if successful print version
	    #
	    ########
	    conn = self.XYZcoinConnection(config["rpcuser"],config["rpcpassword"],config["rpcconnect"],config["rpcport"],0)
	    try:
	        info = conn.getinfo()
	    except InsufficientFunds: ###
	        print "insu"
            except: ###
	        log.error("cant connect daemon!")
	        exit() ###
            else:
	        log.info('Found %s Daemon Version:%s', self.scur,info.version)

	    ########
	    #
	    # Try to connect to btcltc db
	    #
	    ########
            log.debug('self-scur %s',  self.scur) 
            if self.scur < self.tcur:
                dname = self.scur + self.tcur +'_TK' ########
            else:
                dname = self.tcur + self.scur +'_TK' ########                
	    db.init(dname,host='dontoc.dlinkddns.com', user='jack',passwd='hammer')
	    try:
	        db.connect()
            except: ### access denied
	        log.error('db %s access denied' % dname)
	        exit()
            else:
	        log.info('Connect DB: %s' % dname)
	    return conn

        def now():
            d=datetime.datetime.now()
	    fmt = '%Y-%m-%d %H:%M:%S'
	    d_string = d.strftime(fmt)
	    return d_string

        def check_transactions(db,coin):
	    log.debug('checking transactions')
	    preorders = Order.select().where((Order.status == Order.STATUS_PREORDER)  & (Order.source == self.scur))
	    translist = coin.listtransactions('work')### fehler wenn keine vorhanden
	    for preorder in preorders:
	        log.debug('key:>>%s<<' % preorder.send_to_address)
		padr=preorder.send_to_address
		for trans in translist:
		    if trans.category <> 'receive': continue
		    if trans.address <> preorder.send_to_address: continue
		    log.debug('       AMNT: %s  T: %s   PO:%s  ADR:%s', trans.amount, trans.confirmations, preorder.confirmations,trans.address)
		    if trans.confirmations <> preorder.confirmations:
		        preorder.confirmations = trans.confirmations
		        if preorder.confirmations >= 6:
		            preorder.amount = int(SMULT * trans.amount)
			    if trans.amount < MINAMNT:
			        preorder.status = Order.STATUS_TOPAY
				preorder.amount_bought = preorder.amount
				preorder.target = preorder.source
				preorder.receiver_address = preorder.sender_address
			    else:
			        preorder.status = Order.STATUS_ACTIVE
				preorder.active = now()
		        preorder.save()

	def send_payments(db,coin):
	    log.debug('send payments')
	    payments = Order.select().where((Order.status == Order.STATUS_TOPAY) & (Order.target == self.scur))
	    for payment in payments:
	        log.debug('PAYM: key: %s  amount: %s' , payment.receiver_address,payment.amount_bought)
		fees = int(payment.amount_bought * FEEPERCT)###########
		btc_fees = fees / SMULT
		btc_sendamnt = (payment.amount_bought - fees - TRANSFEE) / SMULT
		sendamnt = int(btc_sendamnt * SMULT)
		log.debug('     FEES: %s->%s  SENDAMNT: %s->%s',fees,btc_fees,sendamnt, btc_sendamnt)
		log.debug('  sendfrom(work,%s,%s,%s)',payment.receiver_address,sendamnt / SMULT,6)
		tid = coin.sendfrom('work',payment.receiver_address,float(btc_sendamnt),6)###
		payment.tid_send = tid
		payment.amount_send = sendamnt
		coin.move('work','fees',float(btc_fees),6)###
		payment.status = Order.STATUS_PAYED
		payment.confirmations = 0
		payment.save()

		
        ######################################
        #
        #   Begin of run()
        #
        slh=logging.handlers.SysLogHandler(address='/dev/log')
	fm=logging.Formatter('COIN %(levelname)s:%(message)s')
	slh.setFormatter(fm)
	log = logging.getLogger()
	logging.basicConfig(format='%(asctime)s COIN %(levelname)s:%(message)s')
	if DEBUG:
	   log.setLevel(logging.DEBUG)
	else:
	   log.setLevel(logging.INFO)		
	log.addHandler(slh)
	log.debug('Start Daemon')


	conn=init();     
	while True:
	    log.debug('Start loop')
	    check_address_pool(db=db,coin=conn)
	    check_transactions(db=db,coin=conn)
	    send_payments(db=db,coin=conn)
	    time.sleep(10)



