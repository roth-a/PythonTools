#%%
import numpy as np

class JsonTable():
	def __init__(self):
		self.table = [[]]
		self.data = {}

	def write_table(self, row, column, value):
		delta_row = len(self.table) - row
		if delta_row <= 0:
			self.table += [[] for i in range(-delta_row+1)]

		delta_column = len(self.table[row]) - column
		if delta_column <= 0:
			self.table[row] += [None for i in range(-delta_column+1)]

		self.table[row][column] = value



	def json2table(self, data, emtpy_fields=None):
		self.table = [[]]
		def rec_json2table(data, row =0, column = 0):
			if isinstance(data, dict):
				for k, v in data.items():
					self.write_table(row, column, k)
					row = rec_json2table(v, row, column+1)
			elif isinstance(data, list):
				for i, v in enumerate(data):
					self.write_table(row, column, i)
					row = rec_json2table(v, row, column+1)
			else:
				self.write_table(row, column, data)
				row += 1

			return row

		def rectanglify():
			max_len = max([len(row) for row in self.table])
			for i in range(len(self.table)):
				self.write_table(i, max_len, None)

		rec_json2table(data)
		rectanglify()
		self.table = np.array(self.table)
		self.table[self.table == None] = emtpy_fields

		return self.table




	def table2json(self, table):
		self.data = {}
		table = np.array(table)
		def rec_table2json(table):
			start_row = 0

			key = table[start_row,0]
			if len(table)==1:
				return table[0,0]
			else:
				#check if it should be a list
				keys = np.array([key for key in table[:,0] if (key != None and key!='')])
				is_list = np.array([k==i for i,k in enumerate(keys)]).all()
				if is_list:
					data = []
				else:
					data = {}

				def my_append(key, value):
					if is_list:
						data.append(value)
					else:
						data[key] = value

				for i in range(start_row+1, len(table)):
					if not (table[i,0] is None or table[i,0] is ''):
						my_append(key, rec_table2json(table[start_row:i,1:]))
						key = table[i,0]
						start_row = i
					if i == len(table)-1:
						my_append(key, rec_table2json(table[start_row:,1:]))

				return data
		return rec_table2json(table)


	def json2mixedtable(self, data):
		"""
		Not correctly implemented yet
		"""
		self.table = [[]]
		def rec_json2table(data, row =0, column = 0, vertical = True):
			if isinstance(data, dict):
				initial_row = row
				for k, v in data.items():
					self.write_table(row, column, k)
					addrow, column = rec_json2table(v, initial_row+1, column, vertical=False)
				row += addrow
			elif isinstance(data, list):
				for i, v in enumerate(data):
					self.write_table(row, column, i)
					row, ___ = rec_json2table(v, row, column+1, vertical=True)
			else:
				self.write_table(row, column, data)
				if vertical:
					row += 1
				else:
					column += 1

			return row, column

		def rectanglify():
			max_len = max([len(row) for row in self.table])
			for i in range(len(self.table)):
				self.write_table(i, max_len, None)

		rec_json2table(data)
		rectanglify()

		return self.table




#%%
# import pprint
# pp = pprint.PrettyPrinter()
# from prettytable import PrettyTable
# import os
# def test_JsonTable():
#	 j = JsonTable()
#	 w = {'a':0, 'b':0, 'c':[{'a1':0, 'b1':0,},{'a2':0, 'b2':0,}], 'n':[2,3], 'l'}
#	 pp.pprint(w)

#	 t = PrettyTable()
#	 for row in j.json2mixedtable(w):
#		 t.add_row(row)
#	 print(t)
#	 #
#	 # with open('output.log', "w") as file:
#	 #	 file.write(str(t))
#	 # pp.pprint(j.table2json(j.table))

# # test_JsonTable()




	# %%
