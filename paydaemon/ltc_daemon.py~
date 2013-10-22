#!/usr/bin/env python
import coindaemon
from coindaemon import COINDaemon
from litecoinrpc.connection import LitecoinConnection

DEBUG = 1

class LTCDaemon(COINDaemon):

    def __init__(self,pidfile):
        COINDaemon.__init__(self,pidfile,'LTC','BTC',LitecoinConnection)



if __name__ == "__main__":
    daemon = LTCDaemon('/tmp/daemon-ltc.pid')
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
