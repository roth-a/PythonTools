
import numpy as np

def merge_2d_arrays(a, b, b_pos, empty_cell=""):
	"""
	Given a 2d array a. It playces the 2d array b at the position (b_pos[0],b_pos[1])

	Try it with:
		a = np.ones([3,4])
		b = np.ones([20,20])
		b[b==1] = 5
		b_pos = [5,5]
	"""
	a_v = np.empty( [ max(0,b_pos[0] - a.shape[0] + b.shape[0])  , a.shape[1] ]  ,dtype=object)
	a_right = np.empty( [ b_pos[0] + b.shape[0]  , max(0,b_pos[1] - a.shape[1] + b.shape[1]) ] ,dtype=object )

	a_v[a_v == None] = empty_cell
	a_right[a_right == None] = empty_cell

	a_left = np.vstack([a, a_v])
	if min(a_right.shape) != 0:
		full = np.hstack([a_left, a_right])
	else:
		full = a_left
	full[b_pos[0]:(b_pos[0]+b.shape[0]), b_pos[1]:(b_pos[1]+b.shape[1])] = b
	return full
