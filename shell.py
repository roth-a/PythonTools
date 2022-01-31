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



import subprocess, shlex

def run_subprocess_cmd(cmd, shell=False, print_stdout=True):
	"""
	Runs a subprocess and returns the result as a CompletedProcess type

	Parameters
	----------
	cmd : TYPE
		DESCRIPTION.

	Returns
	-------
	result : TYPE
		object with the following propeties:
			- args
			- check_returncode
			- returncode
			- stderr
			- stdout
	"""
	result = subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=shell)
	if print_stdout:
		print(result.stdout)
	return result
