import csv
import os
import re
from BTrees.OOBTree import OOBTree
from BTrees.IOBTree import IOBTree
import pickle

def count_rows(tablename):
	i = 0
	filename = tablename + ".csv"
	with open(filename, 'r') as readFile:
		reader = csv.reader(readFile)
		for row in reader:
			i += 1
	return i

def merge(list1, list2):
      
    merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))]
    return merged_list

def get_loc(colname, colname_list):
	i = -1
	for col in colname_list:
		i += 1
		if colname == col:
			return(i)

def condition_function(obj1, sign, obj2):
	if sign == '=':
		if obj1 == obj2:
			return True
	elif sign == '<':
		if int(obj1) < int(obj2):
			return True
	elif sign == '>':
		#print(obj1)
		#print(obj2)
		#print(int(obj1) > int(obj2))
		if int(obj1) > int(obj2):
			return True
	elif sign == '<=':
		if int(obj1) <= int(obj2):
			return True
	elif sign == '>=':
		if int(obj1) >= int(obj2):
			return True
	return False

def mmcas_function(lines, mmcas_list):
	col = 0
	answer = []
	for operation in mmcas_list:
		if operation == 'max':
			val = lines[0][col]
			for line in lines:
				if line[col] > val:
					val = line[col]
			answer.append(val)
			
		elif operation == 'min':
			val = lines[0][col]
			for line in lines:
				if line[col] < val:
					val = line[col]
			answer.append(val)
			
		elif operation == 'count':
			val = 0
			for line in lines:
				val += 1
			answer.append(val)
			
		elif operation == 'sum':
			val = 0
			for line in lines:
				val += int(line[col])
			answer.append(val)
			
		elif operation == 'avg':
			val = 0
			count = 0
			for line in lines:
				count += 1
				val += int(line[col])
			val = val/count
			answer.append(val)
		col += 1
	print(answer)
	return(answer)

def _init_storage():
	with open("table_data.csv", 'a', newline='') as file:
		writer = csv.writer(file, delimiter = ",")
		writer.writerow(["table_name", "nrows", "ncols", "datatype_list", "primary_key_list"])

def _init_index():
	with open("index_data.csv", 'a', newline='') as file:
		writer = csv.writer(file, delimiter = ",")
		writer.writerow(["index_name", "table_name", "col_name"])


def _create_table(table_name, nrows, ncols, datatype_list, colname_list, primary_key_list):
	with open('table_data.csv') as file:
		# check for duplicates
		csv_reader = csv.reader(file, delimiter=',')
		for row in csv_reader:
			# print(row)
			if row[0] == table_name:
				print("Duplicate entry, cannot create table")
				return
		
		# if no duplicates found write
	with open('table_data.csv', 'a') as file:
		writer = csv.writer(file, delimiter = ",")
		writer.writerow([table_name, nrows, ncols, datatype_list, primary_key_list])

	file_name = table_name + ".csv"
	with open(file_name, 'w') as file:
		writer = csv.writer(file, delimiter = ",")
		writer.writerows([colname_list])

def _create_index(index_name, table_name, col_name):
	with open('index_data.csv') as file:
		# check for duplicates
		csv_reader = csv.reader(file, delimiter=',')
		for row in csv_reader:
			# print(row)
			if row[0] == index_name and row[1] == table_name:
				print("Duplicate entry, cannot create index")
				return
		
		# if no duplicates found write
	with open('index_data.csv', 'a') as file:
		writer = csv.writer(file, delimiter = ",")
		writer.writerow([index_name, table_name, col_name])
###
	
	file_name = table_name + '.csv'
	with open(file_name, 'r') as readFile:
		reader = csv.reader(readFile)
		for row in reader:
			loc = get_loc(col_name, row)
			#print(loc)
			break

	with open('table_data.csv', 'r') as readFile:
		reader = csv.reader(readFile)
		for row in reader:
			if row[0] == table_name:
				datatype_list = re.findall("'([^']*)'", row[3])
				#print(datatype_list[loc])

	if datatype_list[loc] == 'int':
		int_flag = True
		t = IOBTree()
	else:
		int_flag = False
		t = OOBTree()

###
	file_name = table_name + '.csv'
	dictt = {}
	with open(file_name, 'r') as readFile:
		reader = csv.reader(readFile)
		first_row = True
		loc = 0
		row_number = -1
		for row in reader:
			row_number += 1
			if first_row:
				first_row = False
				loc = get_loc(col_name, row)
				continue
#			l = {}
#			l[row_number] = row_number
			if int_flag:
				if int(row[loc]) in dictt:
					dictt[int(row[loc])][row_number] = row_number
				else:
					dictt[int(row[loc])] = {}
					dictt[int(row[loc])][row_number] = row_number
			else:
				if row[loc] in dictt:
					dictt[row[loc]][row_number] = row_number
				else:
					dictt[row[loc]] = {}
					dictt[row[loc]][row_number] = row_number
			
		#print(dictt)
		t.update(dictt)
		print(list(t.values()))


	index_file = index_name + '.' + table_name
	with open(index_file, 'wb') as save_file:
		pickle.dump(t, save_file)

def _index_test(index_name, table_name):
	index_file = index_name + '.' + table_name
	with open(index_file, 'rb') as load_file:
		t = pickle.load(load_file)
#		t.update({1119: '9999'})
		l = list(t.values(max=1400, excludemax=False))
		for d in l:
			for key in d:
				print(key)

#	index_file = index_name + '.' + table_name
#	with open(index_file, 'wb') as save_file:
#		pickle.dump(t, save_file)

def _drop_index(table_name, index_name):
	
	file_name= table_name + ".csv"
	index_file = index_name + '.' + table_name
	# check if table exists 
	lines = list()
	flag = 0
	with open('index_data.csv', 'r') as readFile:
	    reader = csv.reader(readFile)
	    for row in reader:
	        if row[0] == index_name:
	        	flag = 1
	        else:
		        lines.append(row)
	with open('index_data.csv', 'w') as writeFile:
	    writer = csv.writer(writeFile)
	    writer.writerows(lines)

	if flag == 1:
		if os.path.exists(index_file):
		    os.remove(index_file)
		    print("The index: {} is deleted!".format(index_name))
		else:
		    print("The index: {} does not exist!".format(index_name))
	else:
		print("The index: {} does not exist!".format(index_name))


def _drop_table(table_name):
	
	file_name= table_name + ".csv"

	# check if table exists 
	lines = list()
	flag = 0
	with open('table_data.csv', 'r') as readFile:
	    reader = csv.reader(readFile)
	    for row in reader:
	        if row[0] == table_name:
	        	flag = 1
	        else:
		        lines.append(row)
	with open('table_data.csv', 'w') as writeFile:
	    writer = csv.writer(writeFile)
	    writer.writerows(lines)

	if flag == 1:
		if os.path.exists(file_name):
		    os.remove(file_name)
		    print("The table: {} is deleted!".format(table_name))
		else:
		    print("The table: {} does not exist!".format(table_name))
	else:
		print("The table: {} does not exist!".format(table_name))

	if flag == 1:
		del_list = []
		with open('index_data.csv', 'r') as readFile:
			reader = csv.reader(readFile)
			for row in reader:
				if row[1] == table_name:
					del_list.append([table_name, row[0]])

		for element in del_list:
			_drop_index(element[0], element[1])


def _insert(table_name, colname_list, value_list):

	file_name = table_name + ".csv"

	#  check if table_name exists
	flag = 0
	with open('table_data.csv') as readFile:
		reader = csv.reader(readFile, delimiter=',')
		for row in reader:
			if row[0] == table_name:
				primary_key_list = row[-1]
				# primary_key_list = re.findall('"([^"]*)"', primary_key_list)
				primary_key_list = re.findall("'([^']*)'", primary_key_list)
				# print(primary_key_list)
				flag = 1
				break
	if flag == 0 or not os.path.exists(file_name):
	    print("The table: {} does not exist!".format(table_name))
	    return

	# check for uniqueness of primary key
	with open(file_name, 'r') as readFile:
	    reader = csv.reader(readFile)
	    for row in reader:
	    	sorted_colname_list = row
	    	break

	primary_key_loc = []
	for pk in primary_key_list:
		i = -1
		for col in sorted_colname_list:
			i += 1
			if pk == col:
				primary_key_loc.append(i)

	tuple_list = merge(colname_list, value_list)
	sorted_tuple_list = [tuple for x in sorted_colname_list for tuple in tuple_list if tuple[0] == x]

	with open(file_name, 'r') as readFile:
		reader = csv.reader(readFile)
		for row in reader:
			count = 0
			for i in primary_key_loc:
				if str(sorted_tuple_list[i][1]) == row[i]:
					count += 1
					if count == len(primary_key_list):
						print("Entry with the same primary key exist")
						return

	# write
	with open(file_name, 'a') as file:
		writer = csv.writer(file, delimiter = ",")
		writer.writerow(list(map(list, zip(*sorted_tuple_list)))[1])

####
	index_flag = False
	with open('index_data.csv', 'r') as readFile:
		reader = csv.reader(readFile)
		for row in reader:
			if row[1] == table_name:
				index_file = row[0] + '.' + table_name
				index_col = row[2]
				index_flag = True
				with open(index_file, 'rb') as load_file:
							t = pickle.load(load_file)

	if index_flag:
		dictt = dict(t.items())
		print(dictt)
		print(type(dictt))
		loc = get_loc(index_col, sorted_colname_list)
		key_value = sorted_tuple_list[loc][1]
		print(key_value)
		row_id = count_rows(table_name) - 1
		if key_value in dictt:
			dictt[key_value].update({row_id : row_id})
		else:
			dictt.update({key_value: {}})
			dictt[key_value].update({row_id : row_id})
		
		print(dictt)
		t.update(dictt)

		with open(index_file, 'wb') as save_file:
			pickle.dump(t, save_file)



def _delete(table_name, colname_list, condition_list, value_list):
	
	file_name= table_name + ".csv"
	index_flag = False
	# check if table exists
	flag = 0
	with open('table_data.csv') as readFile:
		reader = csv.reader(readFile, delimiter=',')
		for row in reader:
			if row[0] == table_name:
				flag = 1
				break
	if flag == 0 or not os.path.exists(file_name):
		print("The table: {} does not exist!".format(table_name))
		return

	# get the sorted complete col names
	with open(file_name, 'r') as readFile:
		reader = csv.reader(readFile)
		for row in reader:
			sorted_colname_list = row
			break	

####
	with open('index_data.csv', 'r') as readFile:
		reader = csv.reader(readFile)
		for row in reader:
			if row[1] == table_name:
				index_file = row[0] + '.' + table_name
				index_col = row[2]
				index_flag = True
				with open(index_file, 'rb') as load_file:
							t = pickle.load(load_file)

####

	lines = list()
	with open(file_name, 'r') as readFile:
		reader = csv.reader(readFile)
		first_row = True
		row_id = -1
		row_ids = []
		for row in reader:
			row_id += 1
			true_flag = 0
			if(not first_row):
				for i in range(0, len(colname_list)):
					loc = get_loc(colname_list[i], sorted_colname_list)
					if not condition_function(row[loc], condition_list[i], str(value_list[i])):
						true_flag = 1
			else:
				first_row = False
				true_flag = 1
			if true_flag == 1:
				lines.append(row)
			else:
				if index_flag:
					row_ids.append(row_id)

	with open(file_name, 'w') as writeFile:
		writer = csv.writer(writeFile)
		writer.writerows(lines)


	if index_flag:
		dictt = dict(t.items())
		print(dictt)
		print(type(dictt))
		for row_id in row_ids:
			key_list = list(t.keys())
			for key in key_list:
				element_list = list(dictt[key])
				for element in element_list:
					if dictt[key][element] > row_id:
						del dictt[key][element]
						dictt[key].update({element-1 : element-1})
					elif dictt[key][element] == row_id:
						del dictt[key][element]
		print(dictt)
		t.update(dictt)

		with open(index_file, 'wb') as save_file:
			pickle.dump(t, save_file)


def _update(table_name, update_colname_list, update_value_list, colname_list, condition_list, value_list, andor):
	
	file_name= table_name + ".csv"

	# check if table exists
	flag = 0
	with open('table_data.csv') as readFile:
		reader = csv.reader(readFile, delimiter=',')
		for row in reader:
			if row[0] == table_name:
				flag = 1
				break
	if flag == 0 or not os.path.exists(file_name):
		print("The table: {} does not exist!".format(table_name))
		return

	# get the sorted complete col names
	with open(file_name, 'r') as readFile:
		reader = csv.reader(readFile)
		for row in reader:
			sorted_colname_list = row
			break	

####
	with open('index_data.csv', 'r') as readFile:
		reader = csv.reader(readFile)
		for row in reader:
			if row[1] == table_name:
				index_file = row[0] + '.' + table_name
				index_col = row[2]
				index_flag = True
				with open(index_file, 'rb') as load_file:
							t = pickle.load(load_file)

####

	lines = list()
	with open(file_name, 'r') as readFile:
		reader = csv.reader(readFile)
		first_row = True
		key_values = []
		row_ids = []
		key_old_values = []
		row_id = -1
		for row in reader:
			row_id += 1
			true_flag = 0
			false_flag = 0
			if(not first_row):
				for i in range(0, len(colname_list)):
					loc = get_loc(colname_list[i], sorted_colname_list)
					if not condition_function(row[loc], condition_list[i], str(value_list[i])):
						true_flag = 1
					if condition_function(row[loc], condition_list[i], str(value_list[i])):
						false_flag = 1	
			else:
				lines.append(row)
				first_row = False
				continue
			if (true_flag == 1 and andor != 'or') or (false_flag == 0 and andor == 'or'):
				lines.append(row)
			else:
				for i in range(0, len(update_colname_list)):
					loc = get_loc(update_colname_list[i], sorted_colname_list)
					if index_flag and update_colname_list[i] == index_col:
						row_ids.append(row_id)
						key_old_values.append(row[loc])
						key_values.append(update_value_list[i])
					row[loc] = update_value_list[i]
					
				lines.append(row)

	with open(file_name, 'w') as writeFile:
		writer = csv.writer(writeFile)
		writer.writerows(lines)

	if index_flag:
		dictt = dict(t.items())
		print(dictt)
		print(type(dictt))
		i = -1
		for row_id in row_ids:
			i += 1
			del dictt[int(key_old_values[i])][row_id]
		
		i = -1
		for row_id in row_ids:
			i += 1
			if key_values[i] in dictt:
				dictt[key_values[i]].update({row_id : row_id})
			else:
				dictt.update({key_values[i]: {}})
				dictt[key_values[i]].update({row_id : row_id})
	
		print(dictt)
		t.update(dictt)

		with open(index_file, 'wb') as save_file:
			pickle.dump(t, save_file)

def _select(table_name, view_colname_list, mmcas_list, colname_list, condition_list, value_list, andor):
	
	file_name= table_name + ".csv"

	# check if table exists
	flag = 0
	with open('table_data.csv') as readFile:
		reader = csv.reader(readFile, delimiter=',')
		for row in reader:
			if row[0] == table_name:
				flag = 1
				break
	if flag == 0 or not os.path.exists(file_name):
		print("The table: {} does not exist!".format(table_name))
		return

	# get the sorted complete col names
	with open(file_name, 'r') as readFile:
		reader = csv.reader(readFile)
		for row in reader:
			sorted_colname_list = row
			break	

	view_colname_locs = []
	for i in range(0,len(view_colname_list)):
		view_colname_locs.append(get_loc(view_colname_list[i], sorted_colname_list))
	
	
###
	new_m_list = []
	flag_index = False
	with open('index_data.csv', 'r') as readFile:
		reader = csv.reader(readFile)
		if andor != 'or':
			for row in reader:
				i = -1
				for col in colname_list:
					i += 1
					if col == row[2] and table_name == row[1]:
						index_file = row[0] + '.' + table_name
						with open(index_file, 'rb') as load_file:
							t = pickle.load(load_file)
							flag_index = True
							break
				if flag_index == True:
				
					sign = condition_list[i]
					value_list[i]
					if sign == '=':
						m_list = list(t.values(min=value_list[i], max=value_list[i], excludemin=False, excludemax=False))
					elif sign == '<':
						m_list = list(t.values(max=value_list[i], excludemax=True))
					elif sign == '>':
						m_list = list(t.values(min=value_list[i], excludemin=True))
					elif sign == '<=':
						m_list = list(t.values(max=value_list[i], excludemax=False))
					elif sign == '>=':
						m_list = list(t.values(min=value_list[i], excludemin=False))


					for d in m_list:
						for key in d:
							new_m_list.append(key)
					break

	if flag_index == False:
		new_m_list = list(range(1,count_rows(table_name)))
			
###
	print(new_m_list)
	lines = list()
	with open(file_name, 'r') as readFile:
		reader = csv.reader(readFile)
		rows = list(reader)
		first_row = False

		for m in new_m_list:
			row = rows[m]
			true_flag = 0
			false_flag = 0
			if(not first_row):
				for i in range(0, len(colname_list)):
					loc = get_loc(colname_list[i], sorted_colname_list)
					if andor == 'or':
						if condition_function(row[loc], condition_list[i], str(value_list[i])):
							false_flag = 1
					else:
						if not condition_function(row[loc], condition_list[i], str(value_list[i])):
							true_flag = 1	
			else:
				first_row = False
				true_flag = 1
				false_flag = 1
				continue
			if (false_flag == 1 and andor == 'or'): # handles or
				new_row = []
				for i in range(0, len(view_colname_list)):
					new_row.append(row[view_colname_locs[i]])
				lines.append(new_row)
			elif true_flag == 0 and andor != 'or': # handles single, and
				new_row = []
				for i in range(0, len(view_colname_list)):
					new_row.append(row[view_colname_locs[i]])
				lines.append(new_row)
				
#	print(lines)
	if mmcas_list:
		return mmcas_function(lines, mmcas_list)
	print(lines)
	return lines

def _join(table_name_list, table1_col_list, table2_col_list, matchcol_table1, matchcol_table2, join_type, optimization):

	file1_name= table_name_list[0] + ".csv"
	file2_name= table_name_list[1] + ".csv"

	# check if tables exist
	for i in range(2):
		table_name = table_name_list[i]
		flag = 0
		with open('table_data.csv') as readFile:
			reader = csv.reader(readFile, delimiter=',')
			for row in reader:
				if row[0] == table_name:
					flag = 1
					break
		if flag == 0 or not os.path.exists(table_name_list[i] + ".csv"):
			print("The table: {} does not exist!".format(table_name_list[i]))
			return

	# get the sorted complete col names
	with open(file1_name, 'r') as readFile:
		reader = csv.reader(readFile)
		for row in reader:
			sorted_colname_list1 = row
			break
	# get the sorted complete col names
	with open(file2_name, 'r') as readFile:
		reader = csv.reader(readFile)
		for row in reader:
			sorted_colname_list2 = row
			break	

	view_colname_locs1 = []
	for i in range(0,len(table1_col_list)):
		view_colname_locs1.append(get_loc(table1_col_list[i], sorted_colname_list1))
	view_colname_locs2 = []
	for i in range(0,len(table2_col_list)):
		view_colname_locs2.append(get_loc(table2_col_list[i], sorted_colname_list2))

	matchcol_table1_loc = get_loc(matchcol_table1, sorted_colname_list1)
	matchcol_table2_loc = get_loc(matchcol_table2, sorted_colname_list2)

	outer_file = file1_name
	inner_file = file2_name
	outer_match_loc = matchcol_table1_loc
	inner_match_loc = matchcol_table2_loc
	outer_view_colname_locs = view_colname_locs1
	inner_view_colname_locs = view_colname_locs2
	if join_type == 'inner' or join_type == 'full':
		if optimization == 'off' and count_rows(table_name_list[0]) > count_rows(table_name_list[1]):
			outer_file = file2_name
			inner_file = file1_name
			outer_match_loc = matchcol_table2_loc
			inner_match_loc = matchcol_table1_loc
			outer_view_colname_locs = view_colname_locs2
			inner_view_colname_locs = view_colname_locs1
		elif optimization == 'on' and count_rows(table_name_list[0]) < count_rows(table_name_list[1]):
			outer_file = file2_name
			inner_file = file1_name
			outer_match_loc = matchcol_table2_loc
			inner_match_loc = matchcol_table1_loc
			outer_view_colname_locs = view_colname_locs2
			inner_view_colname_locs = view_colname_locs1

	lines = list()
	with open(outer_file, 'r') as outer_readFile:
		outer_reader = csv.reader(outer_readFile)
		ofirst_row = True
		inner_mark = [0] * count_rows(inner_file[:-4])
		for outer_row in outer_reader:
			if ofirst_row:
				ofirst_row = False
				continue
			flag2 = False
			with open(inner_file, 'r') as inner_readFile:
				inner_reader = csv.reader(inner_readFile)
				first_row = True
				k = -1
				ifirst_row = True
				for inner_row in inner_reader:
					if ifirst_row == True:
						ifirst_row = False
						continue
					k += 1
					line = []
					if (outer_row[outer_match_loc] == inner_row[inner_match_loc]):
						inner_mark[k] = 1
						flag2 = True
						for k in range(len(outer_view_colname_locs)):
							line.append(outer_row[outer_view_colname_locs[k]])
						for k in range(len(inner_view_colname_locs)):
							line.append(inner_row[inner_view_colname_locs[k]])
						lines.append(line)
			if flag2 == False and (join_type == 'full' or join_type == 'left'):
				line = []
				for k in range(len(outer_view_colname_locs)):
					line.append(outer_row[outer_view_colname_locs[k]])
				for k in range(len(inner_view_colname_locs)):
					line.append('NULL')
				lines.append(line)

		if join_type == 'full' or join_type == 'right':
			with open(inner_file, 'r') as inner_readFile:
				first_row = True
				inner_reader = csv.reader(inner_readFile)
				k = -1
				for inner_row in inner_reader:
					if first_row:
						first_row = False
						continue
					k += 1
					if inner_mark[k] == 0:
						line = []
						for k in range(len(outer_view_colname_locs)):
							line.append('NULL')
						for k in range(len(inner_view_colname_locs)):
							line.append(inner_row[inner_view_colname_locs[k]])
						lines.append(line)	

	print(lines)
	return lines					



#_init_storage()
#_drop_table('table_name_test')
#_create_table('table_name_test', 0, 2, ['int', 'varchar 20'], ['idd', 'namee'], ['idd', 'namee'])
#_insert('table_name_test', ['idd', 'namee'], [18, 'kujt'])
#_delete('table_name_test', ['idd', 'namee'], ['=', '='], [11, 'asdf'])
#_update('table_name_test', ['namee', 'idd'], ['=', '='], ['jkl', 13], ['zxcv', 22])
#_select('table_name_test', ['namee'], ['namee', 'idd'], ['=', '='], ['zxcv', 22])
#_select('table_name_test', ['idd'], ['namee'], ['='], ['asdf'])

#_select('table_name_test', ['idd', 'namee'], ['avg', 'max'], ['idd'], ['<'], [22], '')

#_select('table_name_test', ['idd', 'namee'], ['avg', 'max'], ['idd', 'namee'], ['<', '='], [19, 'kujt'], 'or')

#_select('table_name_test', ['idd', 'namee', 'namee'], [], [], [], [], '')

#_update('table_name_test', ['idd'], ['24'], ['namee', 'idd'], ['=', '>='], ['zxcvb', 22], 'or')

#######################################

# select id, name, role, salary from employee;

# _select('employee', ['id', 'name', 'role', 'salary'], [], [], [], [], '')

# select id, role, name from employee where salary \> 900 and role = 'engineer';

# _select('employee', ['id', 'role', 'name'], [], ['salary', 'role'], ['>', '='], [900, 'engineer'], 'and')

# select max \( salary \), count \( id \), avg \( salary \), min \( salary \), sum \( id \) from employee where role = 'manager' or id \< 19;

#_select('employee', ['salary', 'id', 'salary', 'salary', 'id'], ['max', 'count', 'avg', 'min', 'sum'], ['role', 'id'], ['=', '<'], ['manager', 19], 'or')

# update employee set role = 'engineer2' where salary \> 1300 and role = 'engineer';

# _update('employee', ['role'], ['engineer2'], ['salary', 'role'], ['>', '='], [1300, 'engineer'], 'and')

# insert into employee \( 'name', 'role', 'salary', 'id' \) values \( 'qqqq', 'manager', '1900', 31 \);

# _insert('employee', ['name', 'role', 'salary', 'id'], ['qqqq', 'manager', 1900, 31])

# delete from employee where id \< 5 and role = 'engineer' and salary \< 1300;

# _delete('employee', ['id', 'role', 'salary'], ['>', '=', '>'], [5, 'engineer2', 1300])

# create table employee \( 'id' int, 'name' varchar\(30\), 'role' varchar\(30\), 'salary' int, primary key \( 'id', 'role' \) \);

#_create_table('employeee', 0, 4, ['int', 'varchar(20)', 'varchar(20)', 'int'], ['id', 'name', 'role', 'salary'], ['id', 'role'])

# select employee.id, employee.name, project.name, project.sector from employee full join project on employee.id = project.empid;

#_join(['employee', 'project'], ['id', 'name'], ['name', 'sector'], 'id', 'empid', 'right', 'off');

# project,0,4,"['int', 'varchar(30)', 'varchar(30)', 'int']","['id']"

#_create_table('sample1', 0, 4, ['int', 'varchar(20)', 'varchar(20)', 'int'], ['id', 'name', 'sector', 'empid'], ['id'])

#create table sample1 \( 'id' int, 'name' varchar\(30\), 'role' varchar\(30\), 'salary' int, primary key \( 'id' \) \);

#_create_table('sample2', 0, 4, ['int', 'varchar(20)', 'varchar(20)', 'int'], ['id', 'name', 'sector', 'empid'], ['id', 'empid'])

#create table sample2 \( 'id' int, 'name' varchar\(30\), 'role' varchar\(30\), 'salary' int, primary key \( 'id', 'salary' \) \);

#_init_index();
#_create_index('salary_index2', 'employeee', 'salary');
#_index_test('salary_index', 'employee');

#_select('employee', ['id', 'role', 'name'], [], ['salary', 'role'], ['>', '='], [1100, 'engineer'], 'and')

#_select('employee', ['id', 'role', 'name'], [], ['salary'], ['<'], [1100], '')
#_select('employee', ['id', 'role', 'name', 'salary'], [], ['name', 'salary'], ['=', '<='], ['bbbb', 1400], 'and')
	
#_delete('employee', ['id', 'role', 'salary'], ['>', '=', '>'], [30, 'manager', 1800])

#_update('employee', ['salary'], [2100], ['salary', 'role', 'name'], ['>', '=', '='], [1888, 'manager', 'qqqq'], 'and')

#_insert('employee', ['name', 'role', 'salary', 'id'], ['jjkk', 'manager', 1000, 35])

#_drop_index('employee', 'salary_index')

#_drop_table('employeee');
