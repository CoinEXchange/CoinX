#!/usr/bin/env python
import logging
import logging.handlers

slh=logging.handlers.SysLogHandler(address='/dev/log')
fm=logging.Formatter('ORDERD %(levelname)s:%(message)s')
slh.setFormatter(fm)
log = logging.getLogger()
logging.basicConfig(format='%(asctime)s ORDERD %(levelname)s:%(message)s')

def set_logging(DEBUG=False):
	if DEBUG:
		log.setLevel(logging.DEBUG)
	else:
		log.setLevel(logging.INFO)

log.addHandler(slh)
log.debug('Start Daemon')