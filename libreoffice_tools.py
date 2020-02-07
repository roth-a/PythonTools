# general imports
import os, sys, psutil, time, datetime
import pickle

import pprint
pp = pprint.PrettyPrinter()

import logging
logger = logging.getLogger(str(os.getpid()) +'."'+__file__+'"')
# check if there are parents handlers. If not then add console output
if len(logging.getLogger(str(os.getpid())).handlers) == 0:	
	logger.setLevel(logging.DEBUG)	
	fh = logging.StreamHandler(sys.stdout)
	fh.setLevel(logging.DEBUG)
	logger.addHandler(fh)
logger.info('Loaded '+ __file__)
	

__author__ = "Alexander Roth"


sys.path.insert(0, './pyoo/')
import pyoo



class LibreOfficeConnector(): 
	def __init__(self, filename):
		#####################
		# add the following at the top of 
		# file:///home/alexander/programs/anaconda3/lib/python3.6/site-packages/pyoo.py
		# import sys
		# sys.path.append('/usr/lib/libreoffice/program')

		# and the following into	 def open_spreadsheet(self, path, as_template=False):
		#		 extra = ()
		#		 pv = uno.createUnoStruct('com.sun.star.beans.PropertyValue')
		#		 pv.Name = 'MacroExecutionMode'
		#		 pv.Value = 4
		#		 extra += (pv,)
		######################

		sys.path.append('/usr/lib/libreoffice/program')
		if not self.Running_process_id() is None:
			logger.info('Was ' + filename + ' already open?')
			
		os.system('libreoffice  --invisible --accept="socket,host=localhost,port=2002;urp;" --norestore --nologo	&' ) # call subprocess		
		time.sleep(3)
		
		self.desktop = pyoo.Desktop('localhost', 2002)

	
	def executeDispatch(self, url, property_values):
		"""
		Possible thanks to these ressources
		https://sourceforge.net/p/bibus-biblio/patches/33/attachment/bibOOoBase.py
		https://thebiasplanet.blogspot.com/2020/01/howtoexecuteanyunodispatchcommandandgetthewholeavailableinformationfromtheexecutioninpython.html
		https://www.openoffice.org/api/docs/common/ref/com/sun/star/frame/XDispatch.html#dispatch

		Parameters
		----------
		url : TYPE
			See first column in https://wiki.documentfoundation.org/Development/DispatchCommands
		property_values : TYPE
			DESCRIPTION.

		Returns
		-------
		None.

		"""
		ctx = self.desktop.remote_context
		oTrans = ctx.ServiceManager.createInstanceWithContext("com.sun.star.util.URLTransformer", ctx ) # used in __freezeBib to format URL
	
		URL = pyoo.uno.getClass("com.sun.star.util.URL")
	
		oUrl = URL()
		oUrl.Complete = url	# https://wiki.documentfoundation.org/Development/DispatchCommands
		countOfUrls, parsedUrl = oTrans.parseSmart( oUrl, ".uno" )
		oDisp = self.doc._target.getCurrentController().queryDispatch(parsedUrl, "", 0 )
	
		if oDisp != None:
			oDisp.dispatch(parsedUrl, property_values)	
			
	
	def dispatch_GoToCell(self, cell_name, sheet=''):
		property_values = []
		pv = pyoo.uno.createUnoStruct('com.sun.star.beans.PropertyValue')
		pv.Name = 'ToPoint'
		pv.Value = cell_name
		property_values += [pv]
		self.executeDispatch('.uno:GoToCell', property_values)
		
		
	def dispatch_SetHyperlink(self, text, url, sheet='', row=0, column=0):
		property_values = []
		pv = pyoo.uno.createUnoStruct('com.sun.star.beans.PropertyValue')
		pv.Name = 'Hyperlink.Text'
		pv.Value = text
		property_values += [pv]
	
		pv = pyoo.uno.createUnoStruct('com.sun.star.beans.PropertyValue')
		pv.Name = 'Hyperlink.URL'
		pv.Value = url
		property_values += [pv]
	
		self.executeDispatch('.uno:SetHyperlink', property_values)
	
			
	# set_hyperlink('blssa', 'http://bing.com')		
	# disptach_GoToCell('A2556')
