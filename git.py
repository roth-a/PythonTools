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


from git import Repo
this_dir = os.path.dirname( __file__)

def clone_checkout_pull(url, root_dir='.', branch='master'):
	name = url.split('/')[-1].split('.')[0]
	if not os.path.isdir(os.path.join(this_dir, name)):	
		repo = Repo.clone_from(url,  os.path.join( this_dir, name ))
		repo.git.checkout(branch)
	else:
		repo = Repo( os.path.join( this_dir, name ))
		repo.git.checkout(branch)
		repo.remotes[0].pull()
	return repo