#!/usr/bin/env python

from logger import log

#################################################
# Order matching class
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



class OrderBookDicts(list):
	def __init__(self, data=''):
		self.lod = []
		if data != '':
			self.lod = data[:]	#convert to list using shallow copy so list operations work
			log.debug('init with orderbook dicts')
		else:
			self.lod = ''
			log.debug('init with empty orderbook dicts')
	
	def show_order_dicts(self):
		for row in self.lod:
			print row

	def get_fok(self):
		for row in self.lod:
			if row['order_type'] == 2:
				print row
	def get_next_order(self):
		self.order = self.lod.pop(0)
		x = self.order['send_to_address'][0:8]
		print x
		#print x.iterkeys().next()
		#print x.itervalues().next()
		#print y
		
	def query_ob(self, filter=None, sort_keys=None):
		if filter is not None:
			self.lod = (r for r in self.lod if filter(r))
		if sort_keys is not None:
 			self.lod = sorted(self.lod, key=lambda r:[r[k] for k in sort_keys])
		else:
			self.lod = list(self.lod)
		return self.lod

	def lookup_ob(self,**kw):
		self.rows = []
		for row in self.lod:
			for k,v in kw.iteritems():
				if row[k] == str(v):
					self.rows.append(row)
		return self.rows
