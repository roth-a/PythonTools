
import functools
from datetime import datetime
import pprint



DECORRATORS = {}


class LoggerDecorator():
	def __init__(self, logger, max_length = None, depth = 2, write_in_new_line=False):
		self.logger = logger
		self.log_depth = -1
		self.max_length = max_length
		self.write_in_new_line = write_in_new_line
		self.pp = pprint.PrettyPrinter(depth=depth)
		self.pp_full = pprint.PrettyPrinter(depth=None)


	def log_this(self, fn):
		@functools.wraps(fn)
		def decorated(*args, **kwargs):
			try:
				start = datetime.now()
				global log_depth
				self.log_depth += 1
				depth_string = '\n    '*int(self.write_in_new_line) + '|   '*max(0, self.log_depth)


				pargs = args
				method_string = ''
				# check if it is a method  (then the first agrument is self)
				if len(args)>=1 and str(fn.__name__) in dir(args[0]):
					pargs = pargs[1:]
					method_string += '{}.'.format(args[0].__class__.__name__)


				self.logger.debug(depth_string + method_string + '{} args: {} kwargs: {}'.format(
						fn.__name__,
					  self.pp.pformat(pargs) ,
					  self.pp.pformat(kwargs)))


				# call the function
				result = fn(*args, **kwargs)


				self.logger.debug(depth_string + method_string + '{} after {}ms  returns {}'.format(fn.__name__,
					(datetime.now() - start).total_seconds()*1000 ,
					self.pp.pformat(result)))
				self.log_depth -= 1
				return result
			except Exception as ex:
				self.logger.exception("-------------------------------------------\nException in {} in {} with args {}, kwargs {}".format(
						method_string + str(fn.__name__),
						ex,
						self.pp_full.pformat(args), self.pp_full.pformat(kwargs)) )
				self.log_depth -= 1
				raise ex
			return result
		return decorated


def get_logger_decorator(logger, name='root', *args, **kwargs):
	global DECORRATORS
	if not name in DECORRATORS:
		DECORRATORS[name] = LoggerDecorator(logger, *args, **kwargs)
	return DECORRATORS[name]


#%%






