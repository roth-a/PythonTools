import os, sys

import logging
logger = logging.getLogger(str(os.getpid()) +'."'+__file__+'"')
# check if there are parents handlers. If not then add console output
if len(logging.getLogger(str(os.getpid())).handlers) == 0:
	logger.setLevel(logging.DEBUG)
	fh = logging.StreamHandler(sys.stdout)
	fh.setLevel(logging.DEBUG)
	logger.addHandler(fh)
logger.debug('Loaded '+ __file__)



from multiprocessing import Pool
from multiprocessing import cpu_count
from concurrent.futures.thread import ThreadPoolExecutor

import threading
import time
from functools import wraps



def ptable(f, arglist, max_workers=cpu_count()):
	logger.debug('Starting {} processes {}({})'.format(max_workers, str(f), str(arglist)))
	try:
		print ('starting the pool map')
		pool = Pool(processes=max_workers)
		result = pool.map(f, arglist)
		return result
		print ('pool map complete')
	finally:
		print ('joining pool max_workers')
		pool.close()
		pool.join()
		print ('join complete')







def threadtable(f, arglist, max_workers=8):
	with ThreadPoolExecutor(max_workers=max_workers) as executor:
		logger.debug('Starting {} threads {}({})'.format(max_workers, str(f), str(arglist)))
		res =  []
		for arg in arglist:
			res.append(executor.submit(f, arg))
	return [r.result() for r in res]






def rate_limited(max_per_second):
	"""
		This is a rate limiter from https://gist.github.com/gregburek/1441055
	"""
	lock = threading.Lock()
	min_interval = 1.0 / max_per_second

	def decorate(func):
		last_time_called = time.perf_counter()

		@wraps(func)
		def rate_limited_function(*args, **kwargs):
			lock.acquire()
			nonlocal last_time_called
			elapsed = time.perf_counter() - last_time_called
			left_to_wait = min_interval - elapsed

			if left_to_wait > 0:
				time.sleep(left_to_wait)

			ret = func(*args, **kwargs)
			last_time_called = time.perf_counter()
			lock.release()
			return ret

		return rate_limited_function

	return decorate


#
#def call_script(ordinal, arg):
#	print('Thread', ordinal, 'argument:', arg)
#	time.sleep(2)
#	print('Thread', ordinal, 'Finished')
#	return arg

# tests

#def  f(x):
#	res= 1
#	for i in range(1000000):
#		res=res* x/(x+1)
#	return res
#
#
#print(ptable(f, range(30), processes=10))
