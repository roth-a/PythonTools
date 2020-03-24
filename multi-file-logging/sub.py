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


import logger_decorator
log_decorator = logger_decorator.get_logger_decorator(logger, write_in_new_line=False)



@log_decorator.log_this
def function_in_sub(s):
	return s
