
def object_walker(o, max_depth = 2):
	d = {}
	if max_depth<0: return d

	for name in dir(o):
		if name.startswith('__'): continue
		try:
			sub_o = getattr(o, name)
			if callable(sub_o) or isinstance(sub_o, (str, int, float, list, tuple, set)) :
				d[name] = type(sub_o)
			else:
				d[name] = object_walker(sub_o, max_depth=max_depth-1)
		except:
			continue
	return d