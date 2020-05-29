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
import time



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







def rate_limited_threadtable(f, arglist, rate_limit=30):
	"""
	It guarantees that less than rate_limit processes run at the same time
	AND no more than rate_limit/second processes were started.


	You can test the function with this code:
		def f(x):
		 	print('Start {}'.format(x))
		 	time.sleep(2)

		start = time.time()
		arglist=range(30)
		res = rate_limited_threadtable(f, arglist, rate_limit=15)
		print(time.time()- start)
	"""
	min_duration = 1  # each process needs to take exactly 1 second
	def rate_limited_f(*args, **kwargs):
		start = time.time()
		ret = f(*args, **kwargs)

		duration = time.time() - start
		if duration < min_duration:
# 			print('Sleeping {}s'.format(min_duration - duration))
			time.sleep(min_duration - duration)
		return ret

	return threadtable(rate_limited_f, arglist, max_workers=rate_limit)








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
