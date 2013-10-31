import bitcoinrpc
from bitcoinrpc.exceptions import InsufficientFunds
from bitcoinrpc.config import read_default_config
from bitcoinrpc.connection import BitcoinConnection
import peewee
from peewee import *
import sys, time
#from armoryengine import *
from modules.fixedpoint import FixedPoint
from coindb.coindb import db,COINModel, Order

db.init('BTCLTC_TK',host='dontoc.dlinkddns.com', user='jack',passwd='hammer')   

#Order.create_table()
#exit()
db.connect()
#Order.create(sender_address='mkfK3iZX5Yb6XfbbTXQv61CkHLbVdbqFc4',send_to_address='mkfK3iZX5Yb6XfbbTXQv61CkHLbVdbqFc4',receiver_address='mkfK3iZX5Yb6XfbbTXQv61CkHLbVdbqFc4')
#Order.get(Order.address =='mkfK3iZX5Yb6XfbbTXQv61CkHLbVdbqFc4')
#Order.address.print()
#print Order.price



#newadr = 'mgGEgPX6yU8Bco1XBAgJ5bNQ8zpmMEgnWp'
#try:
#    Order.create(send_to_address=newadr,source='BTC')
#except Order.DoesNotExist:
#    print 'not found'
#except Order.DuplicateEntry:
#    print 'dup'
#else:
#    print 'fine'
    
#FEEPERCT = FixedPoint('0.2',8)
#SMULT = FixedPoint('100000000',8)
#TRANSFEE = FixedPoint('0.0001',8)
#fees = FixedPoint(90000 * FEEPERCT,8)###########
#btc_fees = fees / SMULT
#btc_sendamnt = 90000 / SMULT - btc_fees - TRANSFEE
#sendamnt = btc_sendamnt * SMULT
#testzahl=FixedPoint('1',8) / SMULT
#print fees
#print btc_fees
#print btc_sendamnt
#print sendamnt
#print testzahl

#import datetime
#d=datetime.datetime.now()
#fmt = '%Y-%m-%d %H:%M:%S'
#d_string = d.strftime(fmt)
#print d_string
#exit()
#for order in Order.select():
#    print order.sender_address
    





#time.sleep(1000)

config = read_default_config()
print config
host="localhost"
print config["rpcuser"]
conn = BitcoinConnection(config["rpcuser"],config["rpcpassword"],config["rpcconnect"],config["rpcport"],0)

#try:
#    conn.move("testaccount", "testaccount2", 1.0)
#except InsufficientFunds,e:
#    print "Account does not have enough funds available!"


#balance = conn.getbalance()

#print "Balance: %f" % balance

#newadr = conn.getnewaddress();
#print "Newaddress: %s" % newadr



try:
    info = conn.getinfo()
except InsufficientFunds:
    print "insu"
except:
    print "cant connect daemon!"
    exit()
else:
    print info.version
    
print "Blocks: %i" % info.blocks
print "Connections: %i" % info.connections
print "Difficulty: %f" % info.difficulty

translist = conn.listtransactions()
for trans in translist:
    if trans.category == 'move': continue
    print trans.category
    print trans.account
    print trans.address
    print trans.category
    print trans.amount
    print trans.confirmations
    print trans.txid
# aa089b486e131fe3aa342a0c9df1671fada7c495e3cce79e2bca848f6bb7f52a
# 1234567890123456789012345678901234567890123456789012345678901234
# 0000000001111111111222222222233333333334444444444555555555566666
    t=conn.gettransaction(trans.txid)
    print t
    txHex1=conn.getrawtransaction(trans.txid,verbose=True)
    print prettyHex(txHex1)
    tx1 = PyTx().unserialize( hex_to_binary( txHex1 ))
    tx1.pprint()
    print 'Printing all inputs:'
    for txin in tx1.inputs:
        txin.pprint()
        print binary_to_hex(txin.outpoint.txHash, BIGENDIAN)
        try:
            txHex2=conn.getrawtransaction(binary_to_hex(txin.outpoint.txHash), verbose=False)
        except:
            print "not found"
        else:
            print prettyHex(txHex2)
            tx2 = PyTx().unserialize( hex_to_binary( txHex2 ))
            tx2.pprint()
            print 'Printing all inputs:'
            for txin in tx2.inputs:
                txin.pprint()
        
#conn.setaccount('mntueYMah5BitCbcKLz568Wui4N5bd5r3X', 'fees')

#acclist = conn.listaccounts()
#for acc in acclist:
#    print 'ACCOUNT: %s' % acc
#    adrlist = conn.getaddressesbyaccount(acc)
#    for adr in adrlist:
#        print '       ADR: %s' % adr

##print 'TRANSACTIONS FOR ADDRESS %s' % sadr
#translist = conn.listtransactions(account='work',address=sadr)
#for trans in translist:
#    print '    %s' % trans


#    print trans.address
#    try:
#        print trans.address
#        print trans
#    else:
#        print "internal"




