#!/usr/bin/env python
import paydaemon.paydaemon
from paydaemon.paydaemon import PAYDaemon
from bitcoinrpc.connection import BitcoinConnection
from modules.fixedpoint import FixedPoint

DEBUG = 1

class BTCDaemon(PAYDaemon):

    def __init__(self,pidfile):
        PAYDaemon.__init__(self,pidfile,'BTC','LTC',BitcoinConnection)
        # config
        PAYDaemon.COIN_MIN_FREEPOOL = 10
        PAYDaemon.SMULT = FixedPoint('100000000',8)
        PAYDaemon.MINAMNT = FixedPoint('0.01',8)
        PAYDaemon.FEEPERCT = FixedPoint('0.2',8)
        PAYDaemon.TRANSFEE = FixedPoint('10000',8)



if __name__ == "__main__":
    daemon = BTCDaemon('/tmp/daemon-btc.pid')
    if DEBUG:
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
