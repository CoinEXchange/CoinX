#!/usr/bin/env python
import paydaemon
from paydaemon import PAYDaemon
from bitcoinrpc.connection import BitcoinConnection

DEBUG = 1

class BTCDaemon(PAYDaemon):

    def __init__(self,pidfile):
        PAYDaemon.__init__(self,pidfile,'BTC','LTC',BitcoinConnection)



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
