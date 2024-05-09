
import numpy as np


def trim_list(l, f_is_empty, call_back_hook=None):
	"""
	Removed elements from a list, if f_is_empty(elemnt) == True

	Parameters
	----------
	l : TYPE
		DESCRIPTION.
	f_is_empty : TYPE
		DESCRIPTION.
	call_back_hook : TYPE, optional
		Before it removed the function it calls call_back_hook(index, value). The default is None.

	Returns
	-------
	l : TYPE
		DESCRIPTION.

	"""
	for i in reversed(range(len(l))):
		if f_is_empty(l[i]):
			if call_back_hook: call_back_hook(i, l[i])
			del l[i]
	return l


def empty_array():
	return  np.empty([0,0], dtype=object)

def merge_2d_arrays(a, b, b_pos, empty_cell='', transparent_in_b=None):
	"""
	Given a 2d array a. It playces the 2d array b at the position (b_pos[0],b_pos[1])

	Try it with:

		a = np.empty([3,4] ,dtype=object)
		a[a==None] = 1
		b = np.empty([7,7] ,dtype=object)
		b[b==None] = 5
		b[1,:] = "a"
		b[2,:] = None
		b_pos = [0,1]

		full = merge_2d_arrays(a, b, b_pos, transparent_in_b="a")
	"""
	a = np.array(a,dtype=object)
	b = np.array(b,dtype=object)
	a_v = np.empty( [ max(0,b_pos[0] - a.shape[0] + b.shape[0])  , 
				  a.shape[1] ]  ,dtype=object)
	a_right = np.empty( [ max(a.shape[0] + a_v.shape[0],   b_pos[0] + b.shape[0])  , 
						  max(0,b_pos[1] - a.shape[1] + b.shape[1]) ] ,dtype=object )

	a_v[a_v == None] = empty_cell
	a_right[a_right == None] = empty_cell

	a_left = np.vstack([a, a_v])
	if min(a_right.shape) != 0:
		full = np.hstack([a_left, a_right])
	else:
		full = a_left

	full[b_pos[0]:(b_pos[0]+b.shape[0]), b_pos[1]:(b_pos[1]+b.shape[1])][b!=transparent_in_b] = b[b!=transparent_in_b]
	return full


def append_right(a, b, empty_cell="", row_shift=0, col_shift=0):
	a = np.array(a)
	return merge_2d_arrays(a, b, [row_shift, col_shift + a.shape[1]], empty_cell=empty_cell)

def append_bottom(a, b, empty_cell="", row_shift=0, col_shift=0):
	a = np.array(a)
	return merge_2d_arrays(a, b, [row_shift + a.shape[0], col_shift], empty_cell=empty_cell)
