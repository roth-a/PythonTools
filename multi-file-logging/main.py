import logging, sys


logger = logging.getLogger('decorator-log')
logger.setLevel(logging.DEBUG)
if len(logger.handlers)==0:
	# writing to stdout
	handler = logging.StreamHandler(sys.stdout)
	handler.setLevel(logging.DEBUG)
#	formatter = logging.Formatter('dddd ')
#	handler.setFormatter(formatter)
	logger.addHandler(handler)



# optional linux notify messages
# import subprocess as s
# class NotifyHandler(logging.Handler):
# 	def emit(self, record):
# 		log_entry = self.format(record)
# 		s.call(['notify-send','My app', str(log_entry)])

# nh = NotifyHandler()
# nh.setLevel(logging.DEBUG)
# logger.addHandler(nh)




import logger_decorator
log_decorator = logger_decorator.get_logger_decorator(logger, write_in_new_line=False)


#%%

class Myclass():
	## Start example
	@log_decorator.log_this
	def helperfunc3(self, *args):
# 		self.crash(4)
		return 5

	@log_decorator.log_this
	def helperfunc2(self, d):
		return self.helperfunc3(5,7, ['bla']*3)

	@log_decorator.log_this
	def helperfunc(self, a, b, d):
		return a + b + self.helperfunc2(d)

	@log_decorator.log_this
	def call_crash_function(self, i):
		return self.crash(i)

	@log_decorator.log_this
	def func(self, a, b, d, op=None):
		return a + b + self.helperfunc(a,b,d)

	@log_decorator.log_this
	def crash(self, i):
		raise ValueError(str(i))



d = {'useless_dict':[{'use_less_sub_structure':0}]}


print('\n=====================================\n'+
		  'Test deep function call logging:\n')

my = Myclass()
my.func(1,2, d, op='dd')



print('\n=====================================\n'+
		  'Now test cross-file logging:\n')

import sub
@log_decorator.log_this
def call_other_file(s):
	return sub.function_in_sub(s)

#
call_other_file(d)




print('\n=====================================\n'+
		  'Test exception 1 level down:\n')

try:
 	my.call_crash_function(d)
except:
 	pass


